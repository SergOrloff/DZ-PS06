# Разрабатываем программу с учётом всего того, что мы изучили.
# Мы будем парсить данные с сайта https://moscow.hh.ru/vacancies/programmist и сохранять их в csv-файл.

# Импортируем модуль со временем
import time
# Импортируем модуль csv
import csv
# Импортируем Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

from openpyxl import Workbook


# Инициализируем браузер
driver = webdriver.Chrome()
# Если мы используем Chrome, пишем
# driver = webdriver.Chrome()

# В отдельной переменной указываем сайт, который будем просматривать
url = "https://tomsk.hh.ru/vacancies/programmist"

# Открываем веб-страницу
driver.get(url)

# Задаём 3 секунды ожидания, чтобы веб-страница успела прогрузиться
time.sleep(3)

# Находим все карточки с вакансиями с помощью названия класса
# Названия классов берём с кода сайта vacancy-card--hhzAtjuXrYFMBMspDjrF
vacancies = driver.find_elements(By.CLASS_NAME, 'vacancy-card--hhzAtjuXrYFMBMspDjrF')

# Выводим вакансии на экран
print(vacancies)
# Создаём список, в который потом всё будет сохраняться
parsed_data = []

# Перебираем коллекцию вакансий
# Используем конструкцию try-except, чтобы "ловить" ошибки, как только они появляются
for vacancy in vacancies:
   try:
       # # Находим названия вакансии
       # title = vacancy.find_element(By.CSS_SELECTOR, 'span.vacancy-name--SYbxrgpHgHedVTkgI_cA').text
       # # Находим названия компаний
       # company = vacancy.find_element(By.CSS_SELECTOR, 'span.company-info-text--O32pGCRW0YDmp3BHuNOP').text
       # # Находим зарплаты
       # salary = vacancy.find_element(By.CSS_SELECTOR, 'span.compensation-text--cCPBXayRjn5GuLFWhGTJ').text
       # # Находим ссылку с помощью атрибута 'href'
       # link = vacancy.find_element(By.CSS_SELECTOR, 'a.bloko-link').get_attribute('href')

       title = vacancy.find_element(By.CSS_SELECTOR, 'span.magritte-text___tkzIl_4-3-1').text
       # company = vacancy.find_element(By.CSS_SELECTOR, 'span.company-info-text--O32pGCRW0YDmp3BHuNOP').text
       # salary = vacancy.find_element(By.CSS_SELECTOR, 'span.compensation-text--cCPBXayRjn5GuLFWhGTJ').text
       link = vacancy.find_element(By.CSS_SELECTOR, 'a.magritte-link___b4rEM_4-3-1').get_attribute('href')
       # Извлечение названия компании
       company = vacancy.find_element(By.CSS_SELECTOR, 'span.magritte-text___tkzIl_4-3-1').text

       # Извлечение информации о заработной плате
       salary = vacancy.find_element(By.CSS_SELECTOR, 'div.compensation-labels_magritte--Ygc18cwREyuZ91K3GL03').text

   # Находим элементы внутри вакансий по значению

       parsed_data.append([title, company, salary, link])

   # Вставляем блок except на случай ошибки - в случае ошибки программа попытается продолжать
   except Exception as e:(
       print(f"Произошла ошибка при парсинге: {e}"))
   # continue

   finally:
# Закрываем подключение браузер
       driver.quit()

# Прописываем открытие нового файла, задаём ему название и форматирование
# 'w' означает режим доступа, мы разрешаем вносить данные в таблицу
with open("hh-msk_prog.csv", 'w',newline='', encoding='utf-8') as file:

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