import os
import pandas as pd

# Đường dẫn thư mục chứa file đầu vào và lưu kết quả
input_folder = "D:/MangXH/DoAn/group-analyzing/data"
output_folder = "D:/MangXH/DoAn/group-analyzing/data/data_clean" # Thư mục lưu file kết quả
os.makedirs(output_folder, exist_ok=True)

# Danh sách các file cần xử lý
files = [
    "1284806905551800_info.xlsx",
    "1292648841434273_info.xlsx",
    "1289832881715869_info.xlsx",
    "1318294142203076_info.xlsx",
    "1295218211177336_info.xlsx",
    "1283943162304841_info.xlsx",
    "1425326991499790_info.xlsx",
    "1289369675095523_info.xlsx",
    "1319622732070217_info.xlsx",
]

# Hàm xử lý loại bỏ trùng lặp dựa trên cột Name và xóa các hàng không có tên
def clean_data(file_path, output_path):
    # Đọc file Excel và xử lý cột "User ID" như chuỗi
    df = pd.read_excel(file_path, dtype={"User ID": str})
    
    # Loại bỏ các hàng không có tên (giá trị NaN hoặc chuỗi rỗng)
    df = df[df["Name"].notna()]  # Loại bỏ NaN
    df = df[df["Name"].str.strip() != ""]  # Loại bỏ chuỗi rỗng
    
    # Loại bỏ các hàng trùng lặp dựa trên cột "Name"
    df_cleaned = df.drop_duplicates(subset="Name")
    
    # Lưu file đã xử lý
    df_cleaned.to_excel(output_path, index=False)

# Xử lý từng file trong danh sách
for file_name in files:
    input_file = os.path.join(input_folder, file_name)
    output_file = os.path.join(output_folder, file_name.replace(".xlsx", "_cleaned.xlsx"))
    
    try:
        clean_data(input_file, output_file)
        print(f"Processed: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")
