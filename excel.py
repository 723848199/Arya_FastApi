import pandas as pd
import openpyxl

# 读取Excel文件
data = pd.read_excel("data.xlsx")
a1 = data[:, 15]
# 打印DataFrame
print(a1)

# 创建数据
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
}

# 创建DataFrame
# df = pd.DataFrame(data)

# # 写入Excel文件
# df.to_excel("output.xlsx", index=False)
#
# # 打开Excel文件
# wb = openpyxl.load_workbook("data.xlsx")
#
# # 获取指定Sheet
# sheet = wb["Sheet1"]

# 修改单元格数据
sheet["A1"] = "Updated Value"

# 添加新的Sheet
new_sheet = wb.create_sheet("Sheet2")

# 保存修改后的Excel文件
wb.save("data_modified.xlsx")
