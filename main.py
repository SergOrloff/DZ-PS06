# Разрабатываем программу с учётом всего того, что мы изучили.
# Мы будем парсить данные с сайта https://moscow.hh.ru/vacancies/programmist и сохранять их в csv-файл.

# Импортируем модуль со временем
# import time
# Импортируем модуль csv
# import csv
# Импортируем Selenium
# from selenium import webdriver
# from selenium.webdriver.common.by import By

from openpyxl import Workbook


# Инициализируем браузер
# driver = webdriver.Chrome()
# Если мы используем Chrome, пишем
# driver = webdriver.Chrome()
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

url = "https://tomsk.hh.ru/vacancies/programmist"

driver.get(url)

time.sleep(5)

vacancies = driver.find_elements(By.CLASS_NAME, "vacancy-card--z_UXteNo7bRGzxWVcL7y font-inter")

parsed_data = []

for vacancy in vacancies:
    try:
        title = vacancy.find_element(By.CSS_SELECTOR, "span.magritte-text___pbpft_3-0-13")
        company = vacancy.find_element(By.CSS_SELECTOR, "span.magritte-text___tkzIl_4-2-6")
        salary = vacancy.find_element(By.CSS_SELECTOR, "span.magritte-text___pbpft_3-0-13")
        link = vacancy.find_element(By.CSS_SELECTOR, "a.magritte-link___b4rEM_4-2-6").get_attribute("href")
    except:
        print("Parsing error")
        continue

    parsed_data.append([title.text, company.text, salary.text, link])

driver.quit()

# with open("hh.csv", "w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(["title", "company", "salary", "link"])
#     writer.writerows(parsed_data)

# Прописываем открытие нового файла, задаём ему название и форматирование
# 'w' означает режим доступа, мы разрешаем вносить данные в таблицу
with open("hh-tomsk_prog.csv", 'w',newline='', encoding='utf-8') as file:

# Используем модуль csv и настраиваем запись данных в виде таблицы
# Создаём объект
    writer = csv.writer(file)
# Создаём первый ряд
    writer.writerow(['Название вакансии', 'Название компании', 'Зарплата', 'Ссылка на вакансию'])

# Прописываем использование списка как источника для рядов таблицы
    writer.writerows(parsed_data)

# Чтение данных из CSV и запись в XLSX
# Создание нового Excel-файла
workbook = Workbook()
sheet = workbook.active

# Открытие CSV-файла для чтения
with open("hh-tomsk_prog.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
        # Добавление каждой строки из CSV в Excel
    for row in reader:
        sheet.append(row)
# Сохранение данных в XLSX-файл
workbook.save("hh-tomsk_prog.xlsx")
print(f"Данные перекодированы и сохранены в  файл 'hh-msk_prog.xlsx'")