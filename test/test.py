import gc
import pdfplumber
import csv
import io
import sys
from pathlib import Path
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Thòi gian bắt đầu
start_time =datetime.now()

# Cấu hình PATH
mainDir = Path(__file__).parent
pdfPath = mainDir / "pdf" / "vcb_11_09_2024.pdf"
csvPath = mainDir / "csv_new" / "vcb_11_09_2024.csv"

# Cấu hình FILE
fieldNames = ['transaction_no', 'transaction_date', 'transaction_details', 'transaction_amount']
pdfFile = pdfplumber.open(pdfPath)
csvFile = open(csvPath, 'w', newline='')
writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
writer.writeheader()

# # THời gian khởi tạo xong
# init_time = datetime.now()
# print(f"Thời gian khởi tạo: {(init_time - start_time).total_seconds()} giây", flush=True)

# Xử lí các trang
for i in range(0, len(pdfFile.pa)):
    page = pdfFile.pages[i]
    raw_transations = page.extract_table()
    transactions = []

    if i == 0:
        init_time = datetime.now()
        print(f"Thời gian khởi tạo: {(init_time - start_time).total_seconds()} giây", flush=True)
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
            print(f"Lỗi xử lý ({i + 1}/{len(pdfFile.pages)}): {[no, date, details, amount]}", flush=True)
            continue

    for transaction in transactions:
        writer.writerow(transaction)
    
    print(f'Hoàn tất ({page.page_number}/{len(pdfFile.pages)}): {len(transactions)} giao dịch!', flush=True)

    gc.collect()

    

