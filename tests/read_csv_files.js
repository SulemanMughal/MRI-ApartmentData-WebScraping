const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

// Directory where the CSV files are stored
const directoryPath = path.join(__dirname, 'output_batches'); // Replace with your directory

// Function to process a CSV file
function processCsvFile(filePath) {
    return new Promise((resolve, reject) => {
        console.log(`Processing file: ${filePath}`);
        
        const results = [];

        // Read and parse the CSV file
        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', (data) => {
                results.push(data);  // Store row data
            })
            .on('end', () => {
                console.log('Finished processing file:', filePath);
                console.log(results); // This will log all rows in the current file
                resolve();  // Resolve after processing the current file
            })
            .on('error', (error) => {
                console.error('Error reading file:', filePath, error);
                reject(error);  // Reject if there's an error
            });
    });
}

// Function to read all CSV files sequentially
async function readCsvFilesSequentially(directoryPath) {
    const csvFilePath = 'apartment_links.csv'; 
    const browser = await puppeteer.launch({ headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
     });
    try {
        // Read the directory to get the list of CSV files
        const files = fs.readdirSync(directoryPath);

        // Filter only CSV files
        const csvFiles = files.filter(file => path.extname(file) === '.csv');

        // Process each CSV file one by one
        for (const file of csvFiles) {
            const filePath = path.join(directoryPath, file);
            await processCsvFile(filePath);  // Wait for each file to finish processing
        }

        console.log('Finished processing all CSV files.');
    } catch (error) {
        console.error('Error processing CSV files:', error);
    }
}

// Start processing the files
readCsvFilesSequentially(directoryPath);
