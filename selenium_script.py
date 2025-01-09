from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import datetime
import time
import requests

def scrape_trends():
    # Configure WebDriver with ProxyMesh (Update with your ProxyMesh credentials)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Navigate to X login page
        driver.get("https://x.com/login")

        # Login process
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        email_input.send_keys("zakariyask28@gmail.com")  # Replace with your email
        email_input.send_keys(Keys.RETURN)

        username_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username_input.send_keys("zakariyask28")  # Replace with your username
        username_input.send_keys(Keys.RETURN)

        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys("Zak@twitter123")  # Replace with your password
        password_input.send_keys(Keys.RETURN)

        # Wait for login to complete and page to load fully
        time.sleep(5)

        # Debugging: print the page source to inspect the page structure (use this to adjust your XPath)
        print(driver.page_source)

        # Scrape trending topics
        # trends_section = WebDriverWait(driver, 15).until(
        #     EC.presence_of_element_located((By.XPATH, "//section[contains(@aria-label, 'Timeline: Trending now')]//span"))
        # )

        # Locate and collect top 5 trending topics
        trending_topics = driver.find_elements(By.XPATH, "//div[contains(@aria-label, 'Timeline: Trending now')]//div")
        trending_topics = [trend.text for trend in trending_topics[:5] if trend.text.strip()]

        if not trending_topics:
            raise Exception("Trending topics not found or page structure changed.")

        # Get current IP address using ProxyMesh
        ip_address = requests.get('https://api.ipify.org').text

        # Capture timestamp
        timestamp = datetime.datetime.now()

        # Prepare the result to store in MongoDB
        result = {
            "unique_id": str(timestamp.timestamp()),
            "trends": trending_topics,
            "date_time": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": ip_address
        }

        # Save result in MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["trend_data"]
        collection = db["trends"]
        inserted_result = collection.insert_one(result)

        # Convert the inserted ObjectId to a string for serialization
        result["_id"] = str(inserted_result.inserted_id)

        print("Trending topics scraped and saved successfully.")
        return result

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

    finally:
        driver.quit()

if __name__ == "__main__":
    data = scrape_trends()
    print(data)
