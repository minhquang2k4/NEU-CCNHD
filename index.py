from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from csv import DictWriter 
from concurrent.futures import ThreadPoolExecutor
import time 
import os 
import threading

def main():
    # Khởi tạo trình duyệt Edge    
    options = Options()
    options.use_chromium = True
    options.add_argument("--start-maximized")
    driver = webdriver.Edge(options=options)

    try:
        driver.get("https://www.fahasa.com/")
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div[1]/div[2]/div/div[2]'))
        )
        # Hover chuột vào element để hiện dropdown menu
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        # Chuyển đến trang cần crawl
        element = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/div/ul/li[1]/a')
        element.click()

        links = []        
        # lặp đến khi ko tìm thấy nút next nữa
        # sửa thành lặp 3 lần để test

        i = 1

        while True:
            if i == 2:
                break
            i += 1
            time.sleep(2)
            products = driver.find_elements(By.CSS_SELECTOR, '#products_grid > li')

            for product in products:
                # Lấy link sản phẩm
                print(product)
                link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
                links.append(link)

            # next page
            try:
                time.sleep(2)
                next_button = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '#pagination .icon-turn-right'))
                )
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                next_button.click()
            except:
                # Nếu không tìm thấy nút "Next" thì thoát khỏi vòng lặp
                break

        data = []
        # Lặp qua các link sản phẩm để lấy thông tin chi tiết
        for link in links:
            driver.get(link)
            try:
                title = driver.find_element(By.CSS_SELECTOR, '#product_view_kasitoo > div > div.product-essential-detail-parent > div.product-essential-detail > div.block-content-product-detail.block-product-view-mobile > h1.fhs_name_product_desktop').text
            except:
                title = ''
            try:
                salePrice = driver.find_element(By.CSS_SELECTOR, '#catalog-product-details-price > div > p.special-price > span.price').text
            except:
                salePrice = ''
            try:
                fullPrice = driver.find_element(By.CSS_SELECTOR, '#catalog-product-details-price > div > p.old-price > span.price').text
            except:
                fullPrice = ''
            try:
                bookID = driver.find_element(By.CSS_SELECTOR, '.data_sku').text
            except:
                bookID = ''
            try:
                supplier = driver.find_element(By.CSS_SELECTOR, '.data_supplier > .attribute_link_container > .xem-chi-tiet').text
            except:
                supplier = ''
            try:
                author = driver.find_element(By.CSS_SELECTOR, '.data_author > .attribute_link_container').text
            except:
                author = ''
            try:
                translator = driver.find_element(By.CSS_SELECTOR, '.data_translator').text
            except:
                translator = ''
            try:
                publisher = driver.find_element(By.CSS_SELECTOR, '.data_publisher').text
            except:
                publisher = ''
            try:
                year = driver.find_element(By.CSS_SELECTOR, '.data_publish_year').text
            except:
                year = ''
            try:
                language = driver.find_element(By.CSS_SELECTOR, '.data_language > .attribute_link_container').text
            except:
                language = ''
            try:
                weight = driver.find_element(By.CSS_SELECTOR, '.data_weight').text
            except:
                weight = ''
            try:
                size = driver.find_element(By.CSS_SELECTOR, '.data_size').text
            except:
                size = ''
            try:
                page = driver.find_element(By.CSS_SELECTOR, '.data_qty_of_page').text
            except:
                page = ''
            try:
                coverType = driver.find_element(By.CSS_SELECTOR, '.data_book_layout > .attribute_link_container').text
            except:
                coverType = ''
            try:
                description = driver.find_element(By.CSS_SELECTOR, '#desc_content').text
            except:
                description = ''

            rowData = {
                'Title': title,
                'Sale Price': salePrice,
                'Full Price': fullPrice,
                'Book ID': bookID,
                'Supplier': supplier,
                'Author': author,
                'Translator': translator,
                'Publisher': publisher,
                'Year': year,
                'Language': language,
                'Weight': weight,
                'Size': size,
                'Page': page,
                'Cover Type': coverType,
                'Description': description
            }

            data.append(rowData)

        print('data: ', data)

        csv_file = 'data.csv'
        fieldnames = ['Title', 'Sale Price', 'Full Price', 'Book ID', 'Supplier', 'Author', 'Translator', 'Publisher', 'Year', 'Language', 'Weight', 'Size', 'Page', 'Cover Type', 'Description']

        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


    except Exception as e:
        print(e)
    finally:
        # Đóng trình duyệt
        driver.quit()

if __name__ == "__main__":
    main()