import pdfplumber
import re
import json
import csv
import io, sys
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

mainDir = Path(__file__).parent
pdfPath = mainDir / "pdf" / "vietcombank.pdf"
csvPath = mainDir / "csv" / "vietcombank.csv"

pdfFile = pdfplumber.open(pdfPath)
csvFile = open(csvPath, 'w', newline='', encoding='utf-8')

fieldNames = ['date', 'transaction_code', 'amount', 'transaction_detail']
writer = csv.DictWriter(csvFile, fieldnames=fieldNames)

date_regex = '(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|[0-2])\/\d{4}'
# Không dc bỏ dấu cách đâu nhé!
creditRegex = '(\d{1,3}(\.\d{3})*) '

for page in pdfFile.pages:
    start = False
    i = 0
    transaction = defaultdict(str)
    date = None

    text_chunks = page.extract_text().split('\n')
    for text_chunk in text_chunks:
        if text_chunk == 'Postal address: Telex : (0805) 411504 VCB - VT':
            break
        if text_chunk == 'Số CT/ Doc No' and not start:
            start = True
        elif start:
            matchDate = re.fullmatch(date_regex, text_chunk)
            if matchDate:
                i = 0
                if transaction['transaction_code']:
                    transaction['date'] = date
                    writer.writerow(transaction)    
                    print(f"✅ Thành công: {list(transaction.values())}")
                    transaction = defaultdict(str)
                date = matchDate.group(0)
            elif i == 0:
                amount, first_transaction_detail_line = text_chunk.split(' ', 1)
                transaction['amount'] = amount
                transaction['transaction_detail'] = first_transaction_detail_line
                matchCredit = re.match(creditRegex, first_transaction_detail_line)
                if matchCredit:
                    print(matchCredit.group(1))
                    transaction['transaction_detail'] = transaction['transaction_detail'].split(' ', 1)[1]
                i += 1 
            elif i == 1:
                transaction['transaction_code'] = text_chunk
                i += 1
            else:
                transaction['transaction_detail'] += ' ' + text_chunk

    if transaction['transaction_code']:
        transaction['date'] = date
        writer.writerow(transaction)
        print(f"✅ Thành công: {list(transaction.values())}")






        