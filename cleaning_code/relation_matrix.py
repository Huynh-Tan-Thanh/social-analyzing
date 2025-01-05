import pandas as pd
import numpy as np
import os
from itertools import combinations

def extract_post_id(file_name):
    """Trích xuất ID bài post từ tên file."""
    base_name = os.path.basename(file_name)  # Lấy tên file (không kèm đường dẫn)
    return base_name.split("_")[0]  # Lấy phần trước "_clean.xlsx"

def build_relation_matrix_from_files(file_list):
    # Lưu thông tin từng bài post và các thành viên đã react
    reactions_data = {}

    for file in file_list:
        post_id = extract_post_id(file)  # Trích xuất ID bài post từ tên file
        df = pd.read_excel(file)
        members = df["User ID"].unique()  # Lấy danh sách các User ID từ file
        reactions_data[post_id] = set(members)  # Gán danh sách User ID vào ID bài post

    # Hợp nhất danh sách tất cả các thành viên
    all_members = set()
    for members in reactions_data.values():
        all_members.update(members)
    all_members = list(all_members)  # Chuyển sang list để đánh index

    # Tạo ma trận quan hệ
    member_index = {user_id: idx for idx, user_id in enumerate(all_members)}
    matrix_size = len(all_members)
    relation_matrix = np.zeros((matrix_size, matrix_size), dtype=int)

    # Cập nhật ma trận dựa trên quan hệ bài post
    for post_id, members in reactions_data.items():
        for user1, user2 in combinations(members, 2):
            idx1, idx2 = member_index[user1], member_index[user2]
            relation_matrix[idx1, idx2] = 1
            relation_matrix[idx2, idx1] = 1  # Ma trận đối xứng

    # Chuyển ma trận thành DataFrame
    relation_df = pd.DataFrame(relation_matrix, index=all_members, columns=all_members)
    return relation_df

# Danh sách file Excel chứa thông tin bài post và thành viên react
file_list = [
    "data/data_clean/1283943162304841_info_cleaned.xlsx",
    "data/data_clean/1292648841434273_info_cleaned.xlsx",
    "data/data_clean/1289832881715869_info_cleaned.xlsx",
    "data/data_clean/1318294142203076_info_cleaned.xlsx",
    "data/data_clean/1295218211177336_info_cleaned.xlsx",
    "data/data_clean/1283943162304841_info_cleaned.xlsx",
    "data/data_clean/1425326991499790_info_cleaned.xlsx",
    "data/data_clean/1289369675095523_info_cleaned.xlsx",
    "data/data_clean/1319622732070217_info_cleaned.xlsx",
]

# Tạo ma trận quan hệ
relation_matrix_df = build_relation_matrix_from_files(file_list)

# Xuất kết quả ra file Excel
output_file = "D:/MangXH/DoAn/group-analyzing/data/data_clean/relation_matrix.xlsx"
relation_matrix_df.to_excel(output_file)
print(f"Relation matrix saved to {output_file}")
