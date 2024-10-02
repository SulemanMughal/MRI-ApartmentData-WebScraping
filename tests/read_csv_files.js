const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const cheerio = require('cheerio');
const csvWriter = require('csv-write-stream');

const csvDirectory = './input_csv'; // Modify this to your directory

const now = new Date();
const timestamp = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}-${String(now.getMinutes()).padStart(2, '0')}-${String(now.getSeconds()).padStart(2, '0')}`;
const filename = `apartment_data_${timestamp}.csv`;
console.debug("Saved data into :",filename)

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

// Function to process each row using Puppeteer (open, scrape, close)
async function processRowWithPuppeteer(row) {
    return new Promise(async (resolve) => {
        // console.log('Processing row with Puppeteer:', row);
        // const targetUrl = `https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=${row.id}&MODE2=StartFromTop_Directory&VIP=010`;
        // console.debug(targetUrl)

        // Start Puppeteer and scrape the data
        const browser = await puppeteer.launch({ headless: true }); // Launch the browser
        const page = await browser.newPage(); // Open a new page

        const cookiesString = fs.readFileSync('cookies.json', 'utf8');
        const cookies = JSON.parse(cookiesString);
        await page.setCookie(...cookies);

        try {
            const targetUrl = `https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=${row.id}&MODE2=StartFromTop_Directory&VIP=010`;
        console.debug(targetUrl)
            const url = targetUrl; // Assuming 'url' is a column in the CSV file
            await page.goto(url, {waitUntil: 'networkidle2',timeout: 0 }); // Go to the URL
const content = await page.content();
// const screenshotsDir = './screenshot';
// if (!fs.existsSync(screenshotsDir)) {
//     fs.mkdirSync(screenshotsDir);
// }

// const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
// const screenshotPath = path.join(screenshotsDir, `screenshot_${timestamp}.png`);
// await page.screenshot({ path: screenshotPath, fullPage: true });
// console.log(`Full-page screenshot saved at ${screenshotPath}`);


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
            console.error('Error during scraping:', error);
        }

        // Close the browser after processing the row
        await browser.close();

        // Indicate that the processing for this row is done
        resolve();
    });
}


// Function to read a CSV file row by row

// Function to read a CSV file row by row, ensuring each row is processed sequentially
async function readCSVFileRowByRow(filePath) {
    return new Promise((resolve, reject) => {
        const rows = []; // To store rows temporarily
        const stream = fs.createReadStream(filePath);
        const parser = csv();

        parser.on('data', (row) => {
            rows.push(row);  // Collect each row in the array
        });

        parser.on('end', async () => {
            console.log(`Finished reading all rows in: ${filePath}`);
            for (const row of rows) {
                await processRowWithPuppeteer(row);  // Process rows sequentially
            }
            resolve();  // Resolve when all rows have been processed
        });

        parser.on('error', (err) => reject(err));

        stream.pipe(parser); // Pipe the stream into the CSV parser
    });
}

// Function to read all CSV files in the directory one by one
async function readCSVFilesSequentially(directory) {
    try {
        // Read all CSV file names in the directory
        const files = fs.readdirSync(directory).filter(file => path.extname(file) === '.csv');

        for (const file of files) {
            const filePath = path.join(directory, file);
            console.log(`Reading file: ${file}`);
            await readCSVFileRowByRow(filePath);
        }
    } catch (err) {
        console.error('Error reading CSV files:', err);
    }
}

// Start reading CSV files
readCSVFilesSequentially(csvDirectory);
