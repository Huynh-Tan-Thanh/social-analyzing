import pandas as pd
from itertools import combinations
import numpy as np

# Bước 1: Đọc dữ liệu
vinhlinh_members = pd.read_excel('VinhLinh_member.xlsx')
group_posts_updated = pd.read_excel('group_posts_updated.xlsx')

# Lấy danh sách ID từ VinhLinh_members
member_ids = vinhlinh_members['User ID'].astype(str).tolist()

# Bước 3: Tạo ma trận quan hệ
# Khởi tạo ma trận với giá trị 0
relation_matrix = pd.DataFrame(
    data=0, index=member_ids, columns=member_ids
)

# Duyệt qua từng hàng của cột react trong group_posts_updated
for react in group_posts_updated['react']:
    if pd.notnull(react):
        # Chuyển react thành danh sách các ID
        ids = react.split(',')
        ids = [id_.strip() for id_ in ids]  # Loại bỏ khoảng trắng

        # Tạo tất cả các cặp kết hợp giữa các ID
        for id1, id2 in combinations(ids, 2):
            if id1 in member_ids and id2 in member_ids:
                # Tăng giá trị quan hệ giữa hai ID
                relation_matrix.loc[id1, id2] += 1
                relation_matrix.loc[id2, id1] += 1

# Bước 4: Lưu ma trận quan hệ
relation_matrix_path = 'relation_matrix.xlsx'
relation_matrix.to_excel(relation_matrix_path)

print(f"Ma trận quan hệ đã được lưu tại: {relation_matrix_path}")
