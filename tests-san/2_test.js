const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
// const fs = require('fs');
const path = require('path');
const csvWriter = require('csv-write-stream');
const fs = require('fs');
const csv = require('csv-parser');

var promiseLimit = require('promise-limit')
var limit = promiseLimit(2)

const DIRECTORY_PATH = './input_csv';  // Directory containing CSV files
const BATCH_SIZE = 10;

// // Generate a timestamp
// const timestamp = new Date().toISOString().replace(/[-:.]/g, '');

// // Create a filename with the timestamp
// const filename = `apartment_data_${timestamp}.csv`;


// Generate a human-readable timestamp
const now = new Date();
const timestamp = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}-${String(now.getMinutes()).padStart(2, '0')}-${String(now.getSeconds()).padStart(2, '0')}`;

// Create a filename with the human-readable timestamp
const filename = `apartment_data_${timestamp}.csv`;

console.debug("Saved data into :",filename)

// Use the dynamically generated filename
// const writer = fs.createWriteStream(path.join(__dirname, filename));


// Initialize the CSV writer
// const writer = csvWriter({ headers: ["Property Name", "Address", "Type", "Price", "Size (sf)","Floor Plan", "Description"] });
const writer = csvWriter({ headers: [
    "real_estate_property_identity"	,
    "Title",	
    "Province / State",	
    "City / Town",	
    "real_estate_property_price_short",	
    "real_estate_second-price",	
    "real_estate_property_size"	,
    "real_estate_second-size",	
    "real_estate_property_bedrooms",	
    "real_estate_second-bedroom",	
    "real_estate_property_bathrooms",	
    "real_estate_second-bathroom",	
    "real_estate_property_address",	
    "real_estate_property_zip"	,
    // "real_estate_property_location"	,
    "Floor Plans_floor_name"	,
    "Floor Plans_floor_price",	
    "Floor Plans_floor_size",	
    "Floor Plans_bedroom",	
    "Floor Plans_bathroom",
    "Extra Address Field",
    "Extra Latitude Field"
] });
writer.pipe(fs.createWriteStream(filename));

async function scrapeWebsiteWithCookies(page, targetUrl) {

    try {
        
        // Wait until the main frame is available before setting cookies
        await page.waitForSelector('html', { timeout: 10000 });  // Wait for the main document to load

        // Load the cookies from the file
        const cookiesString = fs.readFileSync('cookies.json', 'utf8');
        const cookies = JSON.parse(cookiesString);
        await page.setCookie(...cookies);

        // Navigate to the protected page
        await page.goto(targetUrl, { waitUntil: 'networkidle2',timeout: 0 });

        // Get the page content and load it into Cheerio
        const content = await page.content();

        // Save a full-page screenshot with timestamp
        const screenshotsDir = './screenshot';
        if (!fs.existsSync(screenshotsDir)) {
            fs.mkdirSync(screenshotsDir);
        }

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const screenshotPath = path.join(screenshotsDir, `screenshot_${timestamp}.png`);
        await page.screenshot({ path: screenshotPath, fullPage: true });
        console.log(`Full-page screenshot saved at ${screenshotPath}`);


        const $ = cheerio.load(content);
        const isErrorBoucher = $('b:contains("Error-Unable to load eBrochure")')
        // console.debug(isErrorBoucher?.nodeValue?.trim())

        if(isErrorBoucher?.nodeValue?.trim() != undefined){
            console.debug(targetUrl, " : ", "error boucher")
            return 
        }
        const fontWithID = $('div.AptFontMargin font:contains("ID:") font:first');
const id_apartments = $(fontWithID[0]);
const apartmentID = id_apartments[0]?.nextSibling?.nodeValue.trim();

    
    // console.log("Apartment ID:", apartmentID);

    const apartmentTitle = $('div.AptFont2Margin font font:first');
const title_apartments =$(apartmentTitle[0]);
// console.debug($(title_apartments).text().trim())
const apartments_title = $(title_apartments).text().trim();

    
    // console.log("Apartment Title:", apartments_title);


    // apartment-address

    const apartmentAddress = $('div.AptFont2Margin font br:first');
const apartmentAddress_elem =$(apartmentAddress[0]);
// console.debug($(title_apartments).text().trim())
const apartmentAddress_value = apartmentAddress_elem[0]?.nextSibling?.nodeValue?.trim();

    
    // console.log("apartmentAddress_value:", apartmentAddress_value);
// Split the address by commas first to separate street, city, and state/zip
const addressParts = apartmentAddress_value?.split(',') || "";

// Trim the whitespace from each part
const street = addressParts[0]?.trim() || "";
const city = addressParts[1]?.trim() || "";

// Split the state and zip code (separated by space)
const stateAndZip = addressParts[2]?.trim()?.split(' ') || "";

// console.debug(stateAndZip)

// The state will be the first part and zip code the second
const state = stateAndZip[0]?.trim();
const zip = stateAndZip[2]?.trim();

// console.log("Street:", street);
// console.log("City:", city);
// console.log("State:", state);
// console.log("Zip:", zip);

// total number of floors:
const total_number_of_floors_font = $('div.AptFontMargin font:contains("#Flrs:") font:nth-of-type(3)');
const total_number_of_floors_element = $(total_number_of_floors_font[0]);
const total_number_of_floors = total_number_of_floors_element[0]?.nextSibling?.nodeValue.trim();
// console.debug("Total Number of floors : ", total_number_of_floors)


// total number of floors:
const total_number_of_units_font = $('div.AptFontMargin font:contains("Units:") font:nth-of-type(2)');
const total_number_of_units_element = $(total_number_of_units_font[0]);
const total_number_of_units = total_number_of_units_element[0]?.nextSibling?.nodeValue.trim();
// console.debug("Total Number of units : ", total_number_of_units)


// map-number
const map_number_font = $('div.AptFontMargin font:contains("Map#:") font:nth-of-type(4)');
const map_number_element = $(map_number_font[0]);
const map_number = map_number_element[0]?.nextSibling?.nodeValue.trim();
// console.debug("Map Number : ", map_number)




const cr_number_font = $('div.AptFontMargin font:contains("CR:") font:nth-of-type(5) font:first');
const cr_number_element = $(cr_number_font[0]);
const cr_number = cr_number_element[0]?.nextSibling?.nodeValue.trim();
// console.debug("CR Number : ", cr_number)



let bedroomPlans = [];

let floorPrice = [];
let floorSizes = [];

let seenBedrooms = new Set();
const Plans_bedroom = []
const Plans_bathroom = []
// Select all <b> elements and filter by text containing "Bedroom" with a number
const floor_plans_elements = $("a[name='EBROCHURE_FLOORPLANS'] div.AptFont2 b table.Apt2 tbody tr b:contains('Bedroom')").filter((index, element) => {
    const text = $(element).text().trim();
    
    // console.debug(text)
    
    // Match text like "1 Bedroom", "2 Bedrooms", etc.
    if (/\d+ Bedroom/.test(text)) {
        // If the bedroom type has not been seen, add it to the set and allow it
        if (!seenBedrooms.has(text)) {
            seenBedrooms.add(text);
            bedroomPlans.push(`${text} Plan`); // Add "Plan" to the bedroom type
            // ;
            
            // 
            // console.debug()
            let requiredElements = $($(element)?.parent()?.parent()?.parent()?.[0])
            const cr_number = $(requiredElements[0]?.nextSibling).find("td:nth-of-type(2)")?.text();
            floorPrice.push(
                cr_number
                )

                const cr_number_2 = $(requiredElements[0]?.nextSibling).find("td:nth-of-type(3)")?.text();
                floorSizes.push(
                    cr_number_2
                )
                Plans_bedroom.push(
                    index+1
                )
                Plans_bathroom.push(
                    index+1
                )
         
        }
    }

    

    return false;
});

// console.debug(floor_plans_elements.length)
const bedroomPlanString = bedroomPlans.join('|');
const bedroomPriceString = floorPrice.join('|');
const bedroomSizeString = floorSizes.join('|');
const Plans_bedroomString = Plans_bedroom.join('|');
const Plans_bathroomString = Plans_bathroom.join('|');
// console.log(bedroomPlanString, bedroomPriceString, bedroomSizeString, Plans_bedroomString, Plans_bathroomString);

      
// console.debug("real_estate_property_price_short : ", floorPrice[0].split("-")[0])
// console.debug("real_estate_second-price : ", floorPrice[bedroomPlans?.length-1].split("-")[1])
// console.debug("real_estate_property_size : ", floorSizes[0].split("-")[0])
// console.debug("real_estate_second-size : ", floorSizes[bedroomPlans?.length-1].split("-")[1] || floorSizes[bedroomPlans?.length-1])
// console.debug("real_estate_property_bedrooms : ", Plans_bedroom[0])
// console.debug("real_estate_second-bedroom : ", Plans_bedroom[bedroomPlans?.length-1])
// console.debug("real_estate_property_bathrooms : ", Plans_bathroom[0])
// console.debug("real_estate_second-bathroom : ", Plans_bathroom[bedroomPlans?.length-1])

    // Extract the content of the script that contains `ShowMap_EBrochure`
    const scriptContent = await page.evaluate(() => {
        const scripts = Array.from(document.querySelectorAll('script'));
        let targetScript = '';

        scripts.forEach(script => {
            if (script.innerHTML.includes('ShowMap_EBrochure')) {
                targetScript = script.innerHTML;
            }
        });

        return targetScript;
    });

// Now, if the scriptContent has been found, proceed to extract parameters (from previous example)
if (scriptContent) {
    const url = scriptContent.match(/'([^']+)'/)[1]; // Extract the string inside the single quotes

    const queryString = url.split('?')[1]; // Get the part after '?'
    const params = new URLSearchParams(queryString);

    const mode = params.get('MODE');
    const mapWidth = params.get('MAP_WIDTH');
    const mapHeight = params.get('MAP_HEIGHT');
    const mapCenterLat = params.get('MAP_CENTER_LAT');
    const mapCenterLng = params.get('MAP_CENTER_LNG');
    const mapPointLat = params.get('MAP_POINT_LAT');
    const mapPointLng = params.get('MAP_POINT_LNG');
    const mapZoomLevel = params.get('MAP_ZOOMLEVEL');
    const mapUsePointInfo = params.get('MAP_USEPOINTINFO');
    const mapUseMapClick = params.get('MAP_USEMAPCLICK_LAT_LNG');
    const mapUseAddress = params.get('MAP_USEADDRESS');

    // console.log("Mode:", mode);
    // console.log("Map Width:", mapWidth);
    // console.log("Map Height:", mapHeight);
    // console.log("Center Latitude:", mapCenterLat);
    // console.log("Center Longitude:", mapCenterLng);
    // console.log("Point Latitude:", mapPointLat);
    // console.log("Point Longitude:", mapPointLng);
    // console.log("Zoom Level:", mapZoomLevel);
    // console.log("Use Point Info:", mapUsePointInfo);
    // console.log("Use Map Click:", mapUseMapClick);
    // console.log("Use Address:", mapUseAddress);

// console.debug(
//     {
//     "real_estate_property_identity"	:apartmentID ,
//     "Title": apartments_title,	
//     "Province / State":state ,	
//     "City / Town": city,	
//     "real_estate_property_price_short": floorPrice[0].split("-")[0] ,	
//     "real_estate_second-price": floorPrice[bedroomPlans?.length-1].split("-")[1],	
//     "real_estate_property_size"	:  floorSizes[0].split("-")[0],
//     "real_estate_second-size": floorSizes[bedroomPlans?.length-1].split("-")[1] || floorSizes[bedroomPlans?.length-1],	
//     "real_estate_property_bedrooms": Plans_bedroom[0],	
//     "real_estate_second-bedroom": Plans_bedroom[bedroomPlans?.length-1],	
//     "real_estate_property_bathrooms":Plans_bathroom[0] ,	
//     "real_estate_second-bathroom": Plans_bathroom[bedroomPlans?.length-1],	
//     "real_estate_property_address": apartmentAddress_value,	
//     "real_estate_property_zip"	: zip,
//     // "real_estate_property_location"	: `${mapPointLat},${mapPointLng}`,
//     "real_estate_property_location"	: `a:2:{s:8:"location";s:29:"${mapPointLat},${mapPointLng}";s:7:"address";s:38:"${apartmentAddress_value}";}`,
//     // "real_estate_property_location"	: `a:2:{s:8:"location";s:29:"40.7315899,-73.98948380000002";s:7:"address";s:38:"112 E 11th St, New York, NY 10003, USA";}`,
//     "Floor Plans_floor_name"	: bedroomPlanString,
//     "Floor Plans_floor_price":  floorPrice.map(price => {
//         // Check if there's a hyphen before splitting
//         const firstValue = price.includes('-') ? price.split('-')[0] : price;
//         return firstValue.replace('$', '');  // Remove the $ sign
//     }),	
//     "Floor Plans_floor_size": floorSizes.map(price => {
//         // Check if there's a hyphen before splitting
//         const firstValue = price.includes('-') ? price.split('-')[0] : price;
//         return firstValue.replace('$', '');  // Remove the $ sign
//     }),	
//     "Floor Plans_bedroom": Plans_bedroomString,	
//     "Floor Plans_bathroom" : Plans_bathroomString
// })
    console.table({
        "real_estate_property_identity"	:apartmentID ,
        "Title": apartments_title,	
        "Province / State":state ,	
        "City / Town": city,	
        "real_estate_property_price_short": floorPrice?.[0]?.split("-")?.[0]?.replace(/[$,]/g, '')  ,	
        "real_estate_second-price": floorPrice?.[bedroomPlans?.length-1]?.split("-")[1]?.replace(/[$,]/g, '') || floorPrice[bedroomPlans?.length-1]?.replace(/[$,]/g, ''),	
        "real_estate_property_size"	:  floorSizes?.[0]?.split("-")[0]?.replace(/[$,]/g, ''),
        "real_estate_second-size": floorSizes?.[bedroomPlans?.length-1]?.split("-")[1]?.replace(/[$,]/g, '') || floorSizes[bedroomPlans?.length-1]?.replace(/[$,]/g, ''),	
        "real_estate_property_bedrooms": Plans_bedroom[0],	
        "real_estate_second-bedroom": Plans_bedroom[bedroomPlans?.length-1],	
        "real_estate_property_bathrooms":Plans_bathroom[0] ,	
        "real_estate_second-bathroom": Plans_bathroom[bedroomPlans?.length-1],	
        "real_estate_property_address": apartmentAddress_value,	
        "real_estate_property_zip"	: zip,
        // "real_estate_property_location"	: `${mapPointLat},${mapPointLng}`,
        // "real_estate_property_location"	: `a:2:{s:8:"location";s:29:"${mapPointLat},${mapPointLng}";s:7:"address";s:38:"${apartmentAddress_value}";}`,
        // "real_estate_property_location"	: `a:2:{s:8:"location";s:29:"40.7315899,-73.98948380000002";s:7:"address";s:38:"112 E 11th St, New York, NY 10003, USA";}`,
        "Floor Plans_floor_name"	: bedroomPlanString,
        "Floor Plans_floor_price":  floorPrice.map(price => {
            // Check if there's a hyphen before splitting
            const firstValue = price.includes('-') ? price.split('-')[0] : price;
            return firstValue.replace(/[$,]/g, '');  // Remove the $ sign
        }).join('|'),	
        "Floor Plans_floor_size": floorSizes.map(price => {
            // Check if there's a hyphen before splitting
            const firstValue = price.includes('-') ? price.split('-')[0] : price;
            return firstValue.replace(/[$,]/g, '');  // Remove the $ sign
        }).join('|'),	
        "Floor Plans_bedroom": Plans_bedroomString,	
        "Floor Plans_bathroom" : Plans_bathroomString,
        "Extra Address Field" : apartmentAddress_value,
        "Extra Latitude Field" : `${mapPointLat},${mapPointLng}`
    })
    writer.write({
        "real_estate_property_identity"	:apartmentID ,
        "Title": apartments_title,	
        "Province / State":state ,	
        "City / Town": city,	
        "real_estate_property_price_short": floorPrice?.[0]?.split("-")?.[0]?.replace(/[$,]/g, '')  ,	
        "real_estate_second-price": floorPrice?.[bedroomPlans?.length-1]?.split("-")[1]?.replace(/[$,]/g, '') || floorPrice[bedroomPlans?.length-1]?.replace(/[$,]/g, ''),	
        "real_estate_property_size"	:  floorSizes?.[0]?.split("-")[0]?.replace(/[$,]/g, ''),
        "real_estate_second-size": floorSizes?.[bedroomPlans?.length-1]?.split("-")[1]?.replace(/[$,]/g, '') || floorSizes[bedroomPlans?.length-1]?.replace(/[$,]/g, ''),	
        "real_estate_property_bedrooms": Plans_bedroom[0],	
        "real_estate_second-bedroom": Plans_bedroom[bedroomPlans?.length-1],	
        "real_estate_property_bathrooms":Plans_bathroom[0] ,	
        "real_estate_second-bathroom": Plans_bathroom[bedroomPlans?.length-1],	
        "real_estate_property_address": apartmentAddress_value,	
        "real_estate_property_zip"	: zip,
        // "real_estate_property_location"	: `${mapPointLat},${mapPointLng}`,
        // "real_estate_property_location"	: `a:2:{s:8:"location";s:29:"${mapPointLat},${mapPointLng}";s:7:"address";s:38:"${apartmentAddress_value}";}`,
        // "real_estate_property_location"	: `a:2:{s:8:"location";s:29:"40.7315899,-73.98948380000002";s:7:"address";s:38:"112 E 11th St, New York, NY 10003, USA";}`,
        "Floor Plans_floor_name"	: bedroomPlanString,
        "Floor Plans_floor_price":  floorPrice.map(price => {
            // Check if there's a hyphen before splitting
            const firstValue = price.includes('-') ? price.split('-')[0] : price;
            return firstValue.replace(/[$,]/g, '');  // Remove the $ sign
        }).join('|'),	
        "Floor Plans_floor_size": floorSizes.map(price => {
            // Check if there's a hyphen before splitting
            const firstValue = price.includes('-') ? price.split('-')[0] : price;
            return firstValue.replace(/[$,]/g, '');  // Remove the $ sign
        }).join('|'),	
        "Floor Plans_bedroom": Plans_bedroomString,	
        "Floor Plans_bathroom" : Plans_bathroomString,
        "Extra Address Field" : apartmentAddress_value,
        "Extra Latitude Field" : `${mapPointLat},${mapPointLng}`
    });    
}

        

    } catch (error) {
        console.error('Error during scraping:' , error);
    } finally {
        // Ensure that the page is always closed to avoid memory leaks
        if (page && !page.isClosed()) {
            await page.close();
        }
    }
}


// Process a batch of rows
async function processBatch(browser, batch) {
    const scrapePromises = batch.map(async (row) => {
        // console.debug(row)
        const targetUrl = `https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=${row.id}&MODE2=StartFromTop_Directory&VIP=010`;

        console.debug(targetUrl)

        try {
            const page = await browser.newPage();
            await scrapeWebsiteWithCookies(page, targetUrl);
            // await page.close();
        } catch (error) {
            console.error(`Error scraping URL: ${targetUrl}`, error);
        }
    });

    await Promise.all(scrapePromises);  // Wait for all scraping tasks to finish
}

// Process a single CSV file
async function processCSVFile(browser, csvFilePath) {
    let batch = [];

    return new Promise((resolve, reject) => {
        fs.createReadStream(csvFilePath)
            .pipe(csv())
            .on('data', (row) => {
                batch.push(row);

                // Process the batch when it's full
                if (batch.length === BATCH_SIZE) {
                    processBatch(browser, batch).catch(console.error);
                    batch = [];  // Reset batch
                }
            })
            .on('end', async () => {
                // Process any remaining rows in the last batch
                if (batch.length > 0) {
                    await processBatch(browser, batch);
                }

                console.log(`Finished processing file: ${csvFilePath}`);
                resolve();
            })
            .on('error', (error) => {
                console.error(`Error processing file: ${csvFilePath}`, error);
                reject(error);
            });
    });
}

// Main function to read files from a directory and process each one
async function main() {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    // Read all CSV files from the directory
    fs.readdir(DIRECTORY_PATH, async (err, files) => {
        if (err) {
            console.error('Error reading directory:', err);
            return;
        }

        // Filter CSV files
        const csvFiles = files.filter((file) => path.extname(file) === '.csv');

        // Process each CSV file one by one
        for (const file of csvFiles) {
            const filePath = path.join(DIRECTORY_PATH, file);
            console.log(`Processing file: ${filePath}`);

            await processCSVFile(browser, filePath)
        }

        // Close the browser after all files are processed
        // await browser.close();
        console.log('All files successfully processed');
    });
    
}

main().catch((error) => {
    console.error('Error in main execution:', error);
});