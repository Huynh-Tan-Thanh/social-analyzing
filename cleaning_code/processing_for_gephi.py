import pandas as pd

# Đọc file thông tin thành viên
members_info = pd.read_excel("DoAn/group-analyzing/data/get_mem_info.xlsx")  # Đường dẫn tới file thông tin thành viên

# Đọc file ma trận quan hệ
relation_matrix = pd.read_excel("DoAn/group-analyzing/data/data_clean/relation_matrix.xlsx", index_col=0)  # Đường dẫn tới ma trận quan hệ

# Tạo file nodes.csv từ thông tin thành viên
nodes = members_info.rename(columns={"User ID": "Id", "Name": "Label"})
nodes_file_path = "DoAn/group-analyzing/data/data_for_gephi/nodes.csv"
nodes.to_csv(nodes_file_path, index=False)

# Tạo file edges.csv từ ma trận quan hệ
edges = []
for source in relation_matrix.index:
    for target in relation_matrix.columns:
        if relation_matrix.at[source, target] > 0:  # Chỉ lưu quan hệ có giá trị > 0
            edges.append({"Source": source, "Target": target, "Weight": relation_matrix.at[source, target]})

edges_df = pd.DataFrame(edges)
edges_file_path = "DoAn/group-analyzing/data/data_for_gephi/edges.csv"
edges_df.to_csv(edges_file_path, index=False)

# Thông báo hoàn tất
print("Nodes data đã được lưu tại:", nodes_file_path)
print("Edges data đã được lưu tại:", edges_file_path)
