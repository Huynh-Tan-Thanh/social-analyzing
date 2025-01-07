import pandas as pd

# Đọc file Excel đã tải lên
relation_matrix_path = "relation_matrix.xlsx"
vinhlinh_member_path = "VinhLinh_member.xlsx"

# Đọc dữ liệu từ các file Excel
relation_matrix = pd.read_excel(relation_matrix_path, index_col=0)
vinhlinh_member = pd.read_excel(vinhlinh_member_path)

# Chuyển đổi ma trận quan hệ thành danh sách các cạnh (edges)
edges = relation_matrix.stack().reset_index()
edges.columns = ['Source', 'Target', 'Weight']

# Lọc bỏ các mối quan hệ không có giá trị (Weight = 0)
edges = edges[edges['Weight'] > 0]

# Gắn thông tin thành viên vào danh sách nút (nodes)
nodes = vinhlinh_member.rename(columns={'User ID': 'ID', 'Name': 'Label'})

# Lưu danh sách nút (nodes) và cạnh (edges) ra file CSV
nodes_output_path = "nodes.csv"
edges_output_path = "edges.csv"

# Ghi dữ liệu ra file
nodes.to_csv(nodes_output_path, index=False, encoding='utf-8-sig')
edges.to_csv(edges_output_path, index=False, encoding='utf-8-sig')


# Đường dẫn các file kết quả
print("File nodes được lưu tại:", nodes_output_path)
print("File edges được lưu tại:", edges_output_path)
