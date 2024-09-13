const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');
const csvWriter = require('csv-write-stream');
const url = require('url');


// List of URLs to scrape
const urls = [
    'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=4291A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=1616A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=1842A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=1946A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=3545A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=2040A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=2483A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=4506A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=2215A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=1304A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=3551A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=4981A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=4903A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=2013A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=4462A&MODE2=StartFromTop_Directory&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowTop.asp?CLEAROPTIONS=Y&VIP=010',
    // 'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=2916C&MODE2=StartFromTop_Directory&VIP=010'
    // Add more URLs here
];

// Initialize the CSV writer
const writer = csvWriter({ headers: ["Property Name", "Address", "Type", "Price", "Size (sf)","Floor Plan", "Description"] });
writer.pipe(fs.createWriteStream('apartment_data.csv'));

async function scrapeWebsiteWithCookies(page, targetUrl) {
    // const browser = await puppeteer.launch({ headless: true });
    // const page = await browser.newPage();

    try {
        // Load the cookies from the file
        const cookiesString = fs.readFileSync('cookies.json', 'utf8');
        const cookies = JSON.parse(cookiesString);
        await page.setCookie(...cookies);

        // Navigate to the protected page
        await page.goto(targetUrl, { waitUntil: 'networkidle2' });

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

        
        // extract paratment-id
        // AptFontMargin
        // const apartment_id_html = await page.evaluate(() => {
        //     // Using XPath to select the element with class 'apartments' and id 'first'
        //     const element = document.evaluate(
        //         "//div[contains(@class, 'AptFontMargin') and @id='first']",
        //         document,
        //         null,
        //         XPathResult.FIRST_ORDERED_NODE_TYPE,
        //         null
        //     ).singleNodeValue;
            
        //     return element ? element.outerHTML : null;
        // });

        const apartmentID = await page.evaluate(() => {
            // Use XPath to find the parent element
            const parentElement = document.evaluate(
                "//div[contains(@class, 'AptFontMargin')]",
                document,
                null,
                XPathResult.FIRST_ORDERED_NODE_TYPE,
                null
            ).singleNodeValue;
        
            if (parentElement) {
                // Now use another XPath relative to the parent element to select the child 'ID' element
                const element = document.evaluate(
                    ".//font[contains(text(), 'ID:')]", // XPath relative to the parent element
                    parentElement, // Parent element
                    null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE,
                    null
                ).singleNodeValue;
        
                // Get the next sibling node, which contains the 'ID'
                const apartmentIDText = element ? element.nextSibling.nodeValue.trim() : null;
        
                return apartmentIDText; // Return the extracted ID value
            } else {
                return null;
            }
        });
        
        console.log(apartmentID); // Logs the 'ID' value (e.g., '4291A')
        


        // console.log(apartmentID);  // Logs '4291A'



  const html = await page.evaluate(() => {
    const element = document.evaluate(
        '/html/body/table/tbody/tr[3]/td/font/form/table[2]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td[1]/div/font/font[1]/b', 
        document, 
        null, 
        XPathResult.FIRST_ORDERED_NODE_TYPE, 
        null
    ).singleNodeValue;
    return element ? element.outerHTML : null;
});

if (!html) {
    throw new Error('Failed to find the element using the provided XPath.');
}

// Use XPath to select the specific content and get its outerHTML
const htmlAddress = await page.evaluate(() => {
    const element = document.evaluate(
        '/html/body/table/tbody/tr[3]/td/font/form/table[2]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td[1]/div/font', 
        document, 
        null, 
        XPathResult.FIRST_ORDERED_NODE_TYPE, 
        null
    ).singleNodeValue;
    return element ? element.outerHTML : null;
});

if (!html) {
    throw new Error('Failed to find the element using the provided XPath.');
}
        // Load the selected HTML into Cheerio
        const $1 = cheerio.load(html);

        // const $Address = cheerio.load(htmlAddress)

        // console.debug($Address.text().trim())
        // console.debug(htmlAddress)

        // Load the selected HTML into Cheerio
        const $Address = cheerio.load(htmlAddress);
        // /html/body/table/tbody/tr[3]/td/font/form/table[2]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td[1]/div/font/text()[2]
        // /html/body/table/tbody/tr[3]/td/font/form/table[2]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td[1]/div/font/text()[2]

        // Extract the address from the selected HTML
        // const addressGet = $Address('font').contents().filter(function() {
        //     return this.nodeType === 3 ;
        // }).text().trim();
        let addressGet = '';
        $Address('br').each((index, element) => {
            const nextNode = element.nextSibling;
            if (nextNode && nextNode.nodeType === 3) { // NodeType 3 is a text node
                addressGet = nextNode.nodeValue.trim();
                return false; // Break the loop once we find the address
            }
        });

        const propertyName = $1.text().trim() || "";  // Replace with correct selector if needed
        const address = addressGet || "";  // Replace with correct selector if needed
        
        // console.debug(propertyName, address)

          // Use XPath to select the specific content and get its outerHTML
          const descriptionHTML = await page.evaluate(() => {
            const element = document.evaluate(
                '/html/body/table/tbody/tr[3]/td/font/form/table[2]/tbody/tr/td[1]/table/tbody/tr/td/a[1]/table[2]', 
                document, 
                null, 
                XPathResult.FIRST_ORDERED_NODE_TYPE, 
                null
            ).singleNodeValue;
            return element ? element.outerHTML : null;
        });

        if (!descriptionHTML) {
            throw new Error('Failed to find the element using the provided XPath.');
        }

        
        // console.debug(descriptionHTML)
        // Load the selected HTML into Cheerio
        const $Description = cheerio.load(descriptionHTML);

        // Extract useful information
        // Extract useful information
        const deposit = $Description('font:contains("Deposit:")').first().text().replace(/Deposit:/, '').trim();
        
        // const fees = $Description('font:contains("Fees:")').text().replace(/Fees:/, '').trim();
        // const terms = $Description('font:contains("Terms:")').text().replace(/Terms:/, '').trim();
        // const officeHours = $Description('font:contains("Office Hrs:")').text().replace(/Office Hrs:/, '').trim();
        // const pets = $Description('font:contains("Pets:")').parent().text().replace(/Pets:/, '').trim();
        // const schoolDistrict = $Description('font:contains("School District:")').parent().text().replace(/School District:/, '').trim();
        // const elementary = $Description('font:contains("Elem:")').next().text().trim();
        // const intermediate = $Description('font:contains("Int:")').next().text().trim();
        // const middleSchool = $Description('font:contains("Mid:")').next().text().trim();
        // const highSchool = $Description('font:contains("High:")').next().text().trim();

        


        // Log the extracted information
        // console.log('Deposit:', deposit);
        // console.log('Fees:', fees);
        // console.log('Terms:', terms);
        // console.log('Office Hours:', officeHours);
        // console.log('Pets:', pets);
        // console.log('School District:', schoolDistrict);
        // console.log('Elementary School:', elementary);
        // console.log('Intermediate School:', intermediate);
        // console.log('Middle School:', middleSchool);
        // console.log('High School:', highSchool);
        // Extract Property Name and Address
        


        const description = $1('.main-content .info-block').text().trim();  // Replace with correct selector if needed

        const $ = cheerio.load(content);


        // Extract the image path
        // const imagePath = $('img[name="IMAGE_Floorplan"]').attr('src');
        
        // // Save the image path as a string
        // console.log('Image Path:', imagePath);
        // Extract the relative image path
        const relativeImagePath = $('img[name="IMAGE_Floorplan"]').attr('src');
        
        // Ensure full URL
        const baseURL = 'https://www.apartmentdata.com';
        const fullImagePath = url.resolve(baseURL, relativeImagePath);

        // Save the full image path as a string
        // console.log('Full Image Path:', fullImagePath);
        
$('table.Apt2').each((index, element) => {
    const type = $(element).find('b').first().text().trim();  // Extract the main type (e.g., 1 Bedroom, 2 Bedrooms, etc.)

    $(element).find('tr[onmouseover]').each((idx, row) => {
        const typeDetail = $(row).find('td').eq(0).text().trim();  // Extract the specific type detail (e.g., 1x1, 2x2, etc.)
        const price = $(row).find('td').eq(1).text().trim();  // Extract the price
        const size = $(row).find('td').eq(2).text().trim();  // Extract the size

        const fullType = `${type} ${typeDetail}`;  // Combine the main type and detail type into a single value
        // console.debug(`${type} `)
        if(`${type}` !== "Type"){
            // Write the combined data to the CSV file in a single row
        writer.write({
            "Property Name": propertyName,
            "Address": address,
            "Type": fullType,  // Combined type (e.g., "1 Bedroom 1x1")
            "Price": price,
            "Size (sf)": size,
            "Floor Plan"  : fullImagePath,
            "Description": deposit || ""
        });    
        }
        
    });
});
        

        

    } catch (error) {
        console.error('Error during scraping:', error);
    } finally {
        // Close the browser
        // await browser.close();
    }
}

async function main() {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    for (const targetUrl of urls) {
        await scrapeWebsiteWithCookies(page, targetUrl);
    }

    await browser.close();
    writer.end();
    console.log('Scraping completed. Data saved to apartment_data.csv');
}

main();

// Run the scraping function
// scrapeWebsiteWithCookies().then(() => {
//     writer.end();  // End the CSV writer stream
//     console.log('Scraping completed. Data saved to apartment_data.csv');
// });