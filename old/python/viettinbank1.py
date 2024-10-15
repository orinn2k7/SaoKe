import gc
import pdfplumber
import csv
import io
import sys
from pathlib import Path
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cấu hình chạy
PAGES_PER_CHUNK = 200


# Cấu hình PATH
mainDir = Path(__file__).parent
pdfPath = mainDir / "pdf" / "vtb_CT1111_10-12_09_2024.pdf"
csvPath = mainDir / "csv" / "vtb_CT1111_10-12_09_2024.csv"

# Cấu hình CSV
fieldNames = ['transaction_no', 'transaction_date', 'transaction_details', 'transaction_amount', 'transaction_note']
csvFile = open(csvPath, 'w', newline='')
writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
writer.writeheader()

# Xử lí từng trang trong khoảng start đến end
def process_pages(start_page, end_page):
    with pdfplumber.open(pdfPath) as pdfFile:
        for page_number in range(start_page, end_page):
            page = pdfFile.pages[page_number]
            transactions = []
            raw_transations = page.extract_table()

            # Trang 1 gồm cả title
            if page_number == 0:
                raw_transations = raw_transations[1:]

            # Xử lí từng giao dịch
            for [no, date, details, amount, note] in raw_transations:
                try:
                    transactions.append({
                        'transaction_no': no.strip(),
                        'transaction_date': date.strip().replace('\n', ' '),
                        'transaction_details': details.strip().replace('\n', ' '),
                        'transaction_amount': amount.replace(".", "").replace("\n-", ""),
                        'transaction_note': note.strip().replace('\n', ' ')
                    })
                except Exception as e:
                    print(f"Lỗi xử lý ({page_number + 1}/{len(pdfFile.pages)}): {[no, date, details, amount, note]}", flush=True)
                    continue

            # Ghi giao dịch vào CSV
            for transaction in transactions:
                writer.writerow(transaction)
            
            # Thông báo hoàn tất trang
            print(f'Hoàn tất ({page.page_number}/{len(pdfFile.pages)}): {len(transactions)} giao dịch!', flush=True)
            
            # Dọn rác 
            gc.collect()

            
# Hàm chính
def main():
    total_pages = len(pdfplumber.open(pdfPath).pages)
    start_page = 0
    
    while start_page < total_pages:
        end_page = min(start_page + PAGES_PER_CHUNK, total_pages)
        process_pages(start_page, end_page)
        start_page = end_page

# Khởi chạy code
if __name__ == "__main__":
    main()

    