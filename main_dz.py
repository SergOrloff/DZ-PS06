import datetime
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

driver = webdriver.Chrome()
# Генерация уникального имени файла на основе текущей даты и времени
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"svet_output_{current_time}.csv"
xlsx_filename = f"svet_output_{current_time}.xlsx"


try:
    url = "https://www.divan.ru/category/svet"
    driver.get(url)

    # Ожидание загрузки элементов
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, '_Ud0k'))
    )

    lamps = driver.find_elements(By.CLASS_NAME, '_Ud0k')

    parsed_data = []
    if not lamps:
        print("Нет найденных светильников")
    else:
        for lamp in lamps:
            try:
                title = lamp.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]').text
                price = lamp.find_element(By.CSS_SELECTOR, 'span.ui-LD-ZU').text
                link = lamp.find_element(By.CSS_SELECTOR, 'link[itemprop="url"]').get_attribute('href')

                print(f"Title: {title}")
                print(f"Price: {price}")
                print(f"Link: {link}")

                parsed_data.append([title, price, link])
            except Exception as e:
                print(f"Произошла ошибка при парсинге: {e}")
                continue

finally:
    driver.quit()

if parsed_data:
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Название светильника', 'Цена', 'Ссылка на светильник'])
        writer.writerows(parsed_data)
        print(f"Данные о светильниках сохранены в  файл '{csv_filename}'")
else:
    print("Нет данных для записи в CSV")

# Чтение данных из CSV и запись в XLSX
# Создание нового Excel-файла
workbook = Workbook()
sheet = workbook.active

# Открытие CSV-файла для чтения
with open(csv_filename, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    # Добавление каждой строки из CSV в Excel
    for row in reader:
        sheet.append(row)

# Сохранение данных в XLSX-файл
workbook.save(xlsx_filename)
print(f"Данные перекодированы и сохранены в  файл '{xlsx_filename}'")