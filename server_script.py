import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

# 1. Функция для парсинга данных с Geekbench Browser для Single и Multi-Core
def get_geekbench_scores():
    url = "https://browser.geekbench.com/processor-benchmarks"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Настраиваем Selenium для работы с динамическим контентом
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_driver_path = "D:/chromedriver-win64/chromedriver.exe"  # путь до драйвера
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    time.sleep(5)  # Ждём загрузки страницы

    # Парсинг обеих таблиц: Single-Core и Multi-Core
    processors = {}

    # Парсим таблицу Single-Core
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for row in soup.select('#single-core .benchmark-chart-table tr'):
        processor_cell = row.find('td', class_='name')
        score_cell = row.find('td', class_='score')
        if processor_cell and score_cell:
            processor_name = processor_cell.find('a').text.strip()
            score = int(score_cell.text.strip().replace(',', ''))
            processors[processor_name] = {'single_core': score}

    # Переключаемся на Multi-Core таблицу
    driver.find_element(By.LINK_TEXT, "Multi-Core").click()
    time.sleep(2)  # Ждём переключения на Multi-Core таблицу

    # Парсим таблицу Multi-Core
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for row in soup.select('#multi-core .benchmark-chart-table tr'):
        processor_cell = row.find('td', class_='name')
        score_cell = row.find('td', class_='score')
        if processor_cell and score_cell:
            processor_name = processor_cell.find('a').text.strip()
            score = int(score_cell.text.strip().replace(',', ''))
            if processor_name in processors:
                processors[processor_name]['multi_core'] = score

    driver.quit()
    return processors

# 2. Функция для парсинга цен процессоров с нескольких URL
def get_processor_prices():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(executable_path="D:\chromedriver-win64\chromedriver.exe")  # Update the path accordingly
    driver = webdriver.Chrome(service=service, options=chrome_options)

    prices = {}
    urls = {}  # Store URLs along with prices

    url_list = [
        "https://zheleza.net/cpu/lga1700_cat/",
        "https://zheleza.net/cpu/socket_cpu_am5/",
        "https://zheleza.net/cpu/lga_1200/",
        "https://zheleza.net/cpu/am4_cat/",
        "https://zheleza.net/cpu/s1150-cpu/",
        "https://zheleza.net/cpu/lga1151-v2/",
        "https://zheleza.net/cpu/s2011v3-cpu/"
    ]

    for url in url_list:
        driver.get(url)
        time.sleep(2)
        products = driver.find_elements(By.CLASS_NAME, "product-item")

        for product in products:
            try:
                # Extract name, price, and link
                name = product.find_element(By.CLASS_NAME, "title").text.strip()
                price_text = product.find_element(By.CLASS_NAME, "price-block").text.strip()
                price = int(re.sub(r'[^\d]', '', price_text))
                product_url = product.find_element(By.CLASS_NAME, "title").get_attribute("href").strip()

                clean_name = clean_processor_name(name)

                # Store price and URL if it doesn't exist, or if the new price is cheaper
                if clean_name not in prices or price < prices[clean_name]:
                    prices[clean_name] = price
                    urls[clean_name] = product_url  # Store the URL for the processor
            except Exception as e:
                print(f"Error processing product: {e}")
                continue

    driver.quit()
    return prices, urls

# 3. Функция для очистки названия процессоров
def clean_processor_name(name):
    name = name.lower()
    name = re.sub(r'\s*(oem|box|процессор|ghz|s1700,)\s*', '', name)
    name = re.sub(r'[\s\-]+', '', name)
    return name.strip()

# 4. Функция для получения TDP процессора
def get_tdp_from_passmark(processor_name):
    base_url = "https://www.cpubenchmark.net/cpu.php?cpu="
    processor_url_name = processor_name.replace(" ", "+").replace("@", "%40")
    full_url = base_url + processor_url_name
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(full_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        strong_elements = soup.find_all('strong')
        for strong in strong_elements:
            if 'Typical TDP' in strong.text:
                tdp_info = strong.next_sibling.strip() if strong.next_sibling else None
                if tdp_info:
                    return int(re.sub(r'[^\d]', '', tdp_info))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TDP for {processor_name}: {e}")
    return None


def main():
    processors = get_geekbench_scores()
    prices, urls = get_processor_prices()  # Now we also get URLs

    with open('static/processor_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Processor', 'Single Core', 'Multi Core', 'Price', 'TDP', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for proc, scores in processors.items():
            price = prices.get(clean_processor_name(proc), None)
            url = urls.get(clean_processor_name(proc), None)  # Get URL for the processor

            # Only write to CSV if price > 0
            if price is not None and price > 0:
                tdp = get_tdp_from_passmark(proc)
                writer.writerow({
                    'Processor': proc,
                    'Single Core': scores['single_core'],
                    'Multi Core': scores['multi_core'],
                    'Price': price,
                    'TDP': tdp if tdp is not None else '',
                    'URL': url if url is not None else ''  # Write URL to CSV
                })
                print(f"Processed: {proc}")



if __name__ == "__main__":
    main()

