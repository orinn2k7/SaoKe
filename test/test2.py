import gc
import pdfplumber
import csv
import io
import sys
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Thời gian bắt đầu
start_time = datetime.now()

# Cấu hình PATH
mainDir = Path(__file__).parent
pdfPath = mainDir / "pdf" / "vcb_11_09_2024.pdf"
csvPath = mainDir / "csv_new" / "vcb_11_09_2024.csv"

# Cấu hình FILE
fieldNames = ['transaction_no', 'transaction_date', 'transaction_details', 'transaction_amount']

# Hàm xử lý mỗi trang
def process_page(page_num, pdf_path=pdfPath):  # Nhận đường dẫn file PDF
    with pdfplumber.open(pdf_path) as pdfFile:  # Mỗi process mở file PDF riêng
        page = pdfFile.pages[page_num]
        raw_transations = page.extract_table()
        transactions = []

        if page_num == 0:
            raw_transations = raw_transations[1:]

        for [no, date, amount, details] in raw_transations:
            try:
                transactions.append({
                    'transaction_no': no.strip(),
                    'transaction_date': date.strip().replace('\n', ' '),
                    'transaction_details': details.strip().replace('\n', ' '),
                    'transaction_amount': amount.replace(".", "").replace("\n-", ""),
                })
            except Exception as e:
                print(f"Lỗi xử lý ({page_num + 1}/{len(pdfFile.pages)}): {[no, date, details, amount]}", flush=True)
                continue

        return page_num, transactions

# Xử lý song song và sắp xếp kết quả
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor, open(csvPath, 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writeheader()

        total_pages = len(pdfplumber.open(pdfPath).pages)
        results = executor.map(process_page, range(total_pages))

        # Sắp xếp kết quả theo số trang
        sorted_results = sorted(results, key=lambda x: x[0])

        for _, transactions in sorted_results:
            for transaction in transactions:
                writer.writerow(transaction)
            print(f'Hoàn tất trang {_+1}/{total_pages}', flush=True)

    # Thời gian kết thúc
    end_time = datetime.now()
    print(f"Thời gian xử lý: {(end_time - start_time).total_seconds()} giây", flush=True)