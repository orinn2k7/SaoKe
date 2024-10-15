import gc
import pdfplumber
import csv
import io
import sys
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


mainDir = Path(__file__).parent
pdfPath = mainDir / "pdf" / "vcb_11_09_2024.pdf"
csvPath = mainDir / "csv_new" / "vcb_11_09_2024.csv"

pdfFile = pdfplumber.open(pdfPath, )
print(pdfFile.pages[0].extract_table())

