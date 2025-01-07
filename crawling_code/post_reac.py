from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from xpathclicker import XPathClicker
class FacebookGroupPostCrawl:
    def __init__(self, username, password, group_id, scroll_count):
        print("\n====== Facebook Group post Scraper ======")
        self.email = username
        self.password = password
        self.group_id = group_id
        self.scroll_count = scroll_count
        self.setup_driver()

    def setup_driver(self):
        try:
            chrome_options = Options()
            # chrome_options.add_argument("--headless") 
            chrome_options.add_argument("--disable-notifications") 
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
        except Exception as e:
            print(f"Error: {e}")

    def login(self):
        try:
            self.driver.get("https://www.facebook.com/")
            self.driver.implicitly_wait(10)
            self.driver.find_element(By.ID, "email").send_keys(self.email)
            self.driver.find_element(By.ID, "pass").send_keys(self.password)
            self.driver.find_element(By.NAME, "login").click()
            time.sleep(30)
            print('Login success')
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    def get_group_posts(self):
        """
        Get the posts of a group
        
        Try to get the posts of a Facebook group by scrolling the page and extracting the post elements
        """
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/?sorting_setting=RECENT_ACTIVITY")
            time.sleep(5)
            postlist = set()
            i=0
            count_loop = 0
            while len(postlist) <= self.scroll_count:
                check_len_postlist = len(postlist)
                print(f"Scroll {i+1}/{self.scroll_count}")
                self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5) 
                post_elements = self.driver.find_elements(By.XPATH, "//div[contains(@role, 'article')]")
                print(f"Found {len(post_elements)} post elements on scroll {i+1}")
                for post in post_elements:
                    try:
                        content = post.text.strip()
                        post_user = content.split('\n')[0]
                        post_content = content.split('\n')[1]
                        post_id_element = post.find_element(By.XPATH, ".//a[contains(@href, '/posts/')]")
                        post_id = post_id_element.get_attribute("href").split("/")[-2]
                        # print(f"Post ID: {post_id}, Post User: {post_user}, Post Content: {post_content}")
                        postlist.add((post_id,post_user,post_content))
                    except Exception as e:
                        continue
                print('-------------')
                print(f"Total post found: {len(postlist)}")
                print('-------------')
                if len(postlist) == check_len_postlist:
                    count_loop+=1
                    if count_loop == 10:
                        break
                i+=1
            return list(postlist)
        except Exception as e:
            print(f"{e}")
    def get_post_reactions(self,post_id):
        """
        Get the reactions of a post

        Try to get the reactions of a Facebook post by scrolling the page and extracting the reaction elements
        """
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/posts/{post_id}/") 
            time.sleep(10)
            self.driver.execute_script("return document.body.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            # Try to find the reaction button
            xpaths = [
            "//span[@class='xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk']",
            "//span[@class='xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk']//span[contains(text(), '2')]"
            ] 
            for xpath in xpaths:
                try:
                    reaction_button = self.driver.find_element(By.XPATH, xpath)
                    print("Found element with XPath:", xpath)
                    # Click the reaction button
                    self.driver.execute_script("arguments[0].click();", reaction_button)
                    time.sleep(5)
                    break
                except Exception as e:
                    print(f"Failed for XPath: {xpath}, Error: {e}")
            reactions = set()
            # Extract the reaction elements
            user_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/user/')]")
            for user in user_elements:
                try:
                    user_name = user.text.strip()
                    user_id = user.get_attribute("href").split("/user/")[1].split("/")[0]
                    # print(f"Name: {user_name}, User ID: {user_id}")
                    reactions.add((user_id,user_name))
                except Exception as e:
                    print(f"Error processing reaction: {e}")
                    continue
            return list(reactions)
        except Exception as e:
            print(f"Error fetching reactions: {e}")
            return []
    def get_post_comments(self, post_id: str):
        """
        Get the comments of a post

        Try to get the comments of a Facebook post by scrolling the page and extracting the comment elements
        """
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/posts/{post_id}/")
            time.sleep(10)
            self.driver.execute_script("return document.body.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            clicker = XPathClicker(self.driver)
            clicker.execute()
            comments = set()
            xpath = "//div[contains(@class, 'xwib8y2') and contains(@class, 'xn6708d') and contains(@class, 'x1ye3gou') and contains(@class, 'x1y1aw1k')]//a[contains(@href, '/user/')]"
            user_elements = self.driver.find_elements(By.XPATH, xpath)
            print(f"Found {len(user_elements)} comment elements")
            for user in user_elements:
                try:
                    print(user.text)
                    user_name = user.text.strip()
                    user_id = user.get_attribute("href").split("/user/")[1].split("/")[0]
                    print(f"Name: {user_name}, User ID: {user_id}")
                    comments.add((user_id, user_name))
                except Exception as e:
                    print(f"Error processing reaction: {e}")
            return list(comments)
        except Exception as e:
            print(f"Error fetching reactions: {e}")
            return []
    def get_detail_each_post_reactions(self, file_path):
        """
        Extract detailed reactions for each post from the given Excel file.

        This function reads post IDs from an Excel file, retrieves reactions for each post,
        and returns a list of tuples containing post ID and its reactions.

        Args:
            file_path (str): Path to the Excel file containing post IDs.

        Returns:
            list: A list of tuples, each containing a post ID and its reactions.
        """
        # Read data from the Excel file
        data = pd.read_excel(file_path)
        post_ids = data['post_id']
        print(post_ids)
        
        detailpost = set()
        
        # Iterate over each post ID
        for post in post_ids:
            try:
                # Get reactions for the current post
                post_reaction = self.get_post_reactions(post)
                # Add the post ID and its reactions to the detailpost set
                detailpost.add((post, tuple(post_reaction)))
            except Exception as e:
                print(f"Error processing post: {e}")
        
        # Convert the set to a list and return
        return list(detailpost)
    def get_detail_each_post_comments(self, file_path: str) -> list:
        """
        Extract detailed comments for each post from the given Excel file.

        This function reads post IDs from an Excel file, retrieves comments for each post,
        and returns a list of tuples containing post ID and its comments.

        Args:
            file_path (str): Path to the Excel file containing post IDs.

        Returns:
            list: A list of tuples, each containing a post ID and its comments.
        """
        # Read data from the Excel file
        data = pd.read_excel(file_path)
        post_ids = data['post_id']

        # Initialize a set to store the results
        detailpost = set()

        # Iterate over each post ID
        for post in post_ids:
            try:
                # Get comments for the current post
                post_reaction = self.get_post_comments(post)
                # Add the post ID and its comments to the detailpost set
                detailpost.add((post, tuple(post_reaction)))
            except Exception as e:
                # Print any errors that occur
                print(f"Error processing post: {e}")

        # Convert the set to a list and return
        return list(detailpost)
    def save_reactions_to_excel(self, detailpost):
        """
        Save reaction data to an Excel file.

        Args:
            detailpost (list): A list of tuples, each containing post ID and its reactions.
        """
        try:
            file_name = f"ex_reactions.xlsx"
            # Create a DataFrame from the detailpost list
            df = pd.DataFrame(detailpost, columns=["post_id", "list_reactions"])
            # Save the DataFrame to an Excel file
            df.to_excel(file_name, index=False)
            print(f"Reaction data saved to {file_name}")
        except Exception as e:
            # Print any errors that occur
            print(f"Error saving reactions to Excel: {e}")
def main():
    # Nhập thông tin tài khoản và cấu hình
    username = "nthuonggiang0226@gmail.com"
    password = "nguyenthihuonggiang"
    group_id = 786129610028652
    scroll_count = 20
    

    # Tạo đối tượng crawl
    fb_crawler = FacebookGroupPostCrawl(username, password, group_id, scroll_count)

    # Đăng nhập
    if not fb_crawler.login():
        print("Login failed. Please check your credentials.")
        return

    # Lấy bài đăng từ nhóm
    print("Fetching posts...")
    posts = fb_crawler.get_group_posts()
    if not posts:
        print("No posts found or failed to fetch posts.")
        fb_crawler.driver.quit()
        return

    # Lưu bài đăng vào Excel
    post_file = "group_posts.xlsx"
    pd.DataFrame(posts, columns=["post_id", "post_user", "post_content"]).to_excel(post_file, index=False)
    print(f"Posts saved to {post_file}")

    # Lấy lượt tương tác cho từng bài đăng
    print("Fetching reactions...")
    reactions = fb_crawler.get_detail_each_post_reactions(post_file)
    reaction_file = "post_reactions.xlsx"
    pd.DataFrame(reactions, columns=["post_id", "list_reactions"]).to_excel(reaction_file, index=False)
    print(f"Reactions saved to {reaction_file}")

    # Lấy bình luận cho từng bài đăng
    print("Fetching comments...")
    comments = fb_crawler.get_detail_each_post_comments(post_file)
    comment_file = "post_comments.xlsx"
    pd.DataFrame(comments, columns=["post_id", "list_comments"]).to_excel(comment_file, index=False)
    print(f"Comments saved to {comment_file}")

    # Đóng trình duyệt
    fb_crawler.driver.quit()
    print("All tasks completed successfully!")

if __name__ == "__main__":
    main()
