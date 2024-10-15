import pandas as pd
import io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Đọc hai file CSV
df1 = pd.read_csv('./csv/vcb_0011001932418_2024.09.26.csv')
df2 = pd.read_csv('./csv/vtb_CT1111_2024.09.18.csv')

df1['bank'] = 'VCB'
df2['bank'] = 'VTB'

# Bỏ qua cột transaction_no nếu nó tồn tại
if 'transaction_no' in df1.columns:
    df1 = df1.drop('transaction_no', axis=1)
if 'transaction_no' in df2.columns:
    df2 = df2.drop('transaction_no', axis=1)

# Merge hai DataFrame
merged_df = pd.concat([df1, df2], axis=0, ignore_index=True)

columns = ['bank'] + [col for col in merged_df.columns if col != 'bank']
merged_df = merged_df[columns]
# Lưu kết quả vào file CSV mới
merged_df.to_csv('merged_file.csv', index=False)

print("Đã merge thành công và lưu vào file 'merged_file.csv'")