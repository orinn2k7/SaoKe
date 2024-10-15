const pdf_table_extractor = require("pdf-table-extractor");
const fs = require('fs');
const { createObjectCsvWriter } = require('csv-writer');

function extractPDF(filePath) {
    return new Promise((resolve, reject) => {
        pdf_table_extractor(filePath, resolve, reject);
    });
}

const processPDF = async () => {
    try {
        const result = await extractPDF("./pdf/vtb_CT1111_23_09_2024.pdf");
        console.warn("Xử lí tệp thành công. Tiến hành xử lí dữ liệu...");

        const pages = result.pageTables;
        const transactions = [];

        pages.forEach(page => {
            let rows = page.tables;
            if (page.page === 1) {
                rows = rows.slice(2)
            }
            
            rows.forEach(row => {
                const transaction = {
                    transaction_no: row[0].replaceAll('\n', ''),
                    transaction_date: row[1].replaceAll('\n', ''),
                    transaction_details: row[2].replaceAll('\n', ''),
                    transaction_amount: row[4].replaceAll('.', '').replaceAll('\n', ''),
                    transaction_offset_name: row[5].replaceAll('\n', ''),
                    transaction_account_number: row[6].replaceAll('\n', '')
                };
                transactions.push(transaction);
            });
        });

        const csvWriter = createObjectCsvWriter({
            path: "./csv/vtb_CT1111_23_09_2024.csv",
            header: [
                { id: "transaction_no", title: "transaction_no" },
                { id: "transaction_date", title: "transaction_date" },
                { id: "transaction_details", title: "transaction_details" },
                { id: "transaction_amount", title: "transaction_amount" },
                { id: "transaction_offset_name", title: "transaction_offset_name" },
                { id: "transaction_account_number", title: "transaction_account_number" },
            ],
        });

        // console.log(transactions)
        
        await csvWriter.writeRecords(transactions);
        console.log('CSV file đã được tạo thành công.');
    } catch (err) {
        console.error('Error:', err);
    }
};

processPDF();