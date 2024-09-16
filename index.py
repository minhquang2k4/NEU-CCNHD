from selenium.webdriver.common.by import By # Để sử dụng phương thức find_element
from selenium.webdriver.common.action_chains import ActionChains # Để sử dụng ActionChains cho hover
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
        driver.get("https://www.fahasa.com/")

        # Tìm kiếm element theo xpath
        element = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div[2]/div/div[2]')

        # Hover chuột vào element để hiện dropdown menu
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        
        # chuyển đến trang 
        element = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div/ul/li[1]/a')
        element.click()

        links = []        
        
        # lặp đến khi ko tìm thấy nút next nữa
        # while True:
            # Lấy danh sách sản phẩm
        products = driver.find_elements(By.CSS_SELECTOR, '#products_grid > li')
        for product in products:
            # Lấy link sản phẩm
            link = product.find_element(By.CSS_SELECTOR, 'div.item-inner > div.ma-box-content > div.products.clearfix > div.product-images-container > a').get_attribute('href')
            print(link)

        time.sleep(10)
    finally:
        # Đóng trình duyệt
        driver.quit()

if __name__ == "__main__":
    main()