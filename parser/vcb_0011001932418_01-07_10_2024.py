import pdfplumber
import re
import json
import csv
import io, sys
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pdfPath = "./pdf/vcb_0011001932418_01-07_10_2024.pdf"
csvPath = "./csv/vcb_0011001932418_01-07_10_2024.csv"

pdfFile = pdfplumber.open(pdfPath)
csvFile = open(csvPath, 'w', newline='', encoding='utf-8')

fieldNames = ['transaction_no', 'transaction_date', 'transaction_amount', 'transaction_details']
writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
writer.writeheader()

date_regex = r'^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/(\d{4})$'
time_regex = r'^([01]?\d|2[0-3]):([0-5]?\d):([0-5]?\d)$'
amount_regex = r'^\d{1,3}(\.\d{3})*,\d{2}$'

for page in pdfFile.pages:
    start = False
    transaction = defaultdict(str)

    text_chunks = page.extract_text().split('\n')
    for text_chunk in text_chunks:
        if text_chunk == 'Postal address: Telex : (0805) 411504 VCB - VT':
            break
        if text_chunk == 'STT Ngày giờ giao dịch Số tiền ghi nợ Số tiền ghi có Tên người chuyển Nội dung chi tiết' and not start:
            start = True
        elif start:
            splited_text = text_chunk.split(" ")
            # print(splited_text)
            if (len(splited_text) >= 4 and splited_text[0].isdigit() and re.fullmatch(date_regex, splited_text[1]) and re.fullmatch(time_regex, splited_text[2]) and re.fullmatch(amount_regex, splited_text[3])):
                # Nếu giao dịch cũ đã tồn tại   
                if transaction['transaction_no']: 
                    writer.writerow(transaction)
                    print(f"✅ Thành công: {list(transaction.values())}")
                    transaction = defaultdict(str)  
                
                # Ghi giao dịch mới
                transaction['transaction_no'] = splited_text[0]
                transaction['transaction_date'] = splited_text[1] + " " + splited_text[2]
                transaction['transaction_amount'] = splited_text[3]
                transaction['transaction_details'] = " ".join(text_chunk.split(' ')[4:])
            else:
                # Ghi details giao dịch
                transaction['transaction_details'] += ' ' + text_chunk
    
        # Ghi lại giao dịch chuối cùng
        if transaction['transaction_no']: 
            writer.writerow(transaction)
            print(f"✅ Thành công: {list(transaction.values())}")
        