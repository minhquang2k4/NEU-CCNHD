from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from csv import DictWriter 
import time 
import os 

def main():
    # Khởi tạo trình duyệt Edge    
    # Tạo đối tượng Options cho Edge
    options = Options()
    options.use_chromium = True  # Sử dụng phiên bản Chromium của Edge

    # chạy trình duyệt ở chế độ full screen
    options.add_argument("--start-maximized")

    # Khởi tạo trình duyệt Edge với các tùy chọn đã thiết lập
    driver = webdriver.Edge(options=options)

    try:
        driver.get("https://www.fahasa.com/")

        # Tìm kiếm element theo xpath
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div[1]/div[2]/div/div[2]'))
        )

        # Hover chuột vào element để hiện dropdown menu
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        
        # chuyển đến trang 
        element = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div/ul/li[1]/a')
        element.click()

        links = []        
        # lặp đến khi ko tìm thấy nút next nữa
        while True:
            time.sleep(2)
            products = driver.find_elements(By.CSS_SELECTOR, '#products_grid > li')

            for product in products:
                # Lấy link sản phẩm
                print(product)
                link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
                links.append(link)
            print("links: ", len(links))
            print(links)

            # next page
            try:
                time.sleep(2)
                next_button = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '#pagination .icon-turn-right'))
                )
                # cuộn trang đến nút "Next"
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                # Click vào nút "Next"
                next_button.click()
            except:
                # Nếu không tìm thấy nút "Next" thì thoát khỏi vòng lặp
                break

        time.sleep(10)
    finally:
        # Đóng trình duyệt
        driver.quit()

if __name__ == "__main__":
    main()