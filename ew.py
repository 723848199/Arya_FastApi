import pandas as pd
import openpyxl as op
# import xlrd as xr
import xlwt as xw

# 讀取excel文件
data = pd.read_excel("data.xlsx", sheet_name="Sheet1")
print(data)

# 创建数据
data = {
    'Name': ['Alice', 'Bob'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
}

# 创建DataFrame
df = pd.DataFrame(data)

# 写入Excel文件
df.to_excel("output.xlsx", index=False)

# 打印DataFrame
# print(data)
