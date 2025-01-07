import pandas as pd
import ast

# Tải các tệp
group_posts = pd.read_excel('group_posts.xlsx')
vinhlinh_members = pd.read_excel('VinhLinh_member.xlsx')

# Kiểm tra tên cột
print("Các cột trong VinhLinh_member:", vinhlinh_members.columns)
print("Các cột trong group_posts:", group_posts.columns)

# Ánh xạ tên người đăng bài sang ID sử dụng dữ liệu từ VinhLinh_member
name_to_id_map = dict(zip(vinhlinh_members['Name'], vinhlinh_members['User ID']))
group_posts['post_user'] = group_posts['post_user'].map(name_to_id_map)

# =========== Thêm cột react bao gồm ID từ phản hồi và bình luận ===========

# Tải các tệp phản hồi (reactions) và bình luận (comments)
post_reactions = pd.read_excel('post_reactions.xlsx')
post_comments = pd.read_excel('post_comments.xlsx')

# Hàm trích xuất ID từ dữ liệu dạng chuỗi biểu diễn tuple
def extract_ids(column_data):
    ids = set()
    for entry in column_data:
        if pd.notnull(entry):  # Kiểm tra nếu dữ liệu không rỗng
            try:
                tuples = ast.literal_eval(entry)  # Chuyển đổi chuỗi thành tuple
                ids.update(t[0] for t in tuples if len(t) > 0)  # Lấy phần tử đầu tiên (ID)
            except (ValueError, SyntaxError):
                continue
    return ids

# Hàm trích xuất ID theo từng bài viết
def extract_ids_by_post(data, id_column, list_column):
    ids_by_post = {}
    for _, row in data.iterrows():
        post_id = row[id_column]
        if pd.notnull(row[list_column]):
            try:
                tuples = ast.literal_eval(row[list_column])  # Chuyển đổi chuỗi thành tuple
                ids = {t[0] for t in tuples if len(t) > 0}  # Lấy phần tử đầu tiên (ID)
                ids_by_post[post_id] = ids_by_post.get(post_id, set()).union(ids)
            except (ValueError, SyntaxError):
                continue
    return ids_by_post

# Trích xuất ID phản hồi và bình luận theo bài viết
reaction_ids_by_post = extract_ids_by_post(post_reactions, 'post_id', 'list_reactions')
comment_ids_by_post = extract_ids_by_post(post_comments, 'post_id', 'list_comments')

# Hợp nhất ID từ phản hồi và bình luận
merged_ids_by_post = {
    post_id: reaction_ids_by_post.get(post_id, set()).union(comment_ids_by_post.get(post_id, set()))
    for post_id in set(reaction_ids_by_post.keys()).union(comment_ids_by_post.keys())
}

# Thay thế cột react trong group_posts
group_posts['react'] = group_posts['post_id'].map(
    lambda post_id: ','.join(sorted(merged_ids_by_post.get(post_id, set())))
)

# Lưu file group_posts đã được cập nhật
group_posts_updated_with_react_path = 'group_posts_updated.xlsx'
group_posts.to_excel(group_posts_updated_with_react_path, index=False)

print("File đã được cập nhật và lưu tại:", group_posts_updated_with_react_path)
