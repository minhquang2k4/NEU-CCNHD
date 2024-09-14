from selenium.webdriver.common.by import By # Để sử dụng phương thức find_element
from selenium.webdriver.support.ui import WebDriverWait # Để sử dụng hàm WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # Để sử dụng expected_conditions
from selenium.webdriver.edge.options import Options # Để sử dụng Options cho Edge
from selenium import webdriver # Để sử dụng webdriver
from csv import DictWriter # Ghi file csv
import time # Để sử dụng hàm sleep để tạm dừng chương trình
import os # Để sử dụng hàm path.exists kiểm tra file tồn tại

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

def main():
    print("start scraping")
    # Khởi tạo trình duyệt Edge    
    # Tạo đối tượng Options cho Edge
    options = Options()
    options.use_chromium = True  # Sử dụng phiên bản Chromium của Edge

    # chạy trình duyệt ở chế độ ẩn 
    # options.add_argument("headless")
    # hoặc 
    # chạy trình duyệt ở chế độ full screen
    options.add_argument("--start-maximized")

    # Khởi tạo trình duyệt Edge với các tùy chọn đã thiết lập
    driver = webdriver.Edge(options=options)

    try:
        driver.get("https://topdev.vn/")

        # tắt quảng cáo
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-close-new-year-modal"]'))
        ).click()


        # click vào nút IT JOBS
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div[1]/ul/li[1]/a'))
        ).click()

        # Cuộn trang cho đến khi không còn thêm nội dung
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            scroll_to_bottom(driver)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        
        time.sleep(10)
    finally:
        # Đóng trình duyệt
        driver.quit()

if __name__ == "__main__":
    main()