const pdf_table_extractor = require("pdf-table-extractor");
const fs = require('fs');
const { createObjectCsvWriter } = require('csv-writer');

const FILE_NAME = 'vcb_0011001932418_2024.09.11'

const csvWriter = createObjectCsvWriter({
    path: `./csv/${FILE_NAME}.csv`,
    header: [
        { id: "transaction_no", title: "transaction_no" },
        { id: "transaction_date", title: "transaction_date" },
        { id: "transaction_details", title: "transaction_details" },
        { id: "transaction_amount", title: "transaction_amount" },
    ],
    append: false
});

function extractPDF(filePath) {
    return new Promise((resolve, reject) => {
        pdf_table_extractor(filePath, resolve, reject);
    });
}

const processPDF = async () => {
    try {
        const result = await extractPDF(`./pdf/${FILE_NAME}.pdf`);
        console.warn("Xử lí tệp thành công. Tiến hành xử lí dữ liệu...");
        const pages = result.pageTables;

        for (const page of pages) {
            let rows = page.tables;
            if (page.page === 1) {
                rows = rows.slice(1)
            }

            const transactionsPerPage = rows.map(row => ({
                transaction_no: row[0].replaceAll('\n', ''),
                transaction_date: row[1].replaceAll('\n', ''),
                transaction_amount: row[2].replaceAll('.', '').replaceAll('\n', ''),
                transaction_details: row[3].replaceAll('\n', '').replaceAll(/\s+/g, ' '),
            }))

            await csvWriter.writeRecords(transactionsPerPage)
            console.log(`✅ Thành công (${page.page}/${pages.length}): ${transactionsPerPage.length} bản ghi.`)
        };
    } catch (err) {
        console.error('Error:', err);
    }
};

processPDF();