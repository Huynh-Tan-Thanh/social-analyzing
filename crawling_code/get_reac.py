import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Hàm thiết lập và đăng nhập Facebook
def login_to_facebook(driver, email, password):
    driver.get("https://www.facebook.com/")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.NAME, "login").click()
    time.sleep(10)  # Chờ đăng nhập hoàn tất

def get_reactions_info(driver, url):
    driver.get(url)
    time.sleep(5)

    xpaths = [
        "//span[@class='xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk']",
        "//span[@class='xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk']//span[contains(text(), '2')]"
    ]

    for xpath in xpaths:
        try:
            reaction_button = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].click();", reaction_button)
            time.sleep(5)
            break
        except Exception as e:
            print(f"Failed for XPath: {xpath}, Error: {e}")

    user_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/user/')]")
    user_data = []
    for user in user_elements:
        try:
            user_name = user.text.strip()
            user_id = user.get_attribute("href").split("/user/")[1].split("/")[0]
            user_data.append({"Name": user_name, "User ID": user_id})
        except Exception as e:
            print(f"Error processing user: {e}")
    return user_data
def save_reactions_to_excel(data, post_id):
    filename = f"{post_id}_info.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data for post {post_id} saved to {filename}")

# Load danh sách Post ID từ file Excel
# list_post_id = pd.DataFrame(pd.read_excel("1280400922659065_posts_with_shared_content.xlsx"))
list_post_id = pd.DataFrame(pd.read_excel("get_post_info.xlsx"))
post_ids = list_post_id["post_id"].unique()
urls = [f"https://www.facebook.com/groups/1280400922659065/posts/{post_id}/" for post_id in post_ids]

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()

    email = input("Enter your Facebook email: ").strip()
    password = input("Enter your Facebook password: ").strip()

    try:
        login_to_facebook(driver, email, password)

        for post_id in post_ids:
            url = f"https://www.facebook.com/groups/1280400922659065/posts/{post_id}/"
            print(f"Processing URL: {url}")

            # Lấy thông tin reactions
            reactions_data = get_reactions_info(driver, url)

            # Lưu kết quả vào file {post_id}_info.xlsx
            save_reactions_to_excel(reactions_data, post_id)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
