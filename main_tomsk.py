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

with open("hh.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["title", "company", "salary", "link"])
    writer.writerows(parsed_data)