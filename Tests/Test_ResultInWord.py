import time
import os
import getpass
from selenium.webdriver.common.by import By
from selenium import webdriver
from docx import Document
from docx.shared import Inches

def generate_docx_report(driver):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    document = Document()

    document.add_heading('Отчет о тестировании', level=0)
    document.add_paragraph(f'Дата и время: {timestamp}')

    # Получение информации об исполнителе из ОС
    executor = getpass.getuser()
    document.add_paragraph(f'Исполнитель: {executor}')

    document.add_heading('Тест: Открытие страниц и создание скриншотов', level=1)
    document.add_paragraph('Статус: Выполнен (предположительно успешно, если не было ошибок)')
    document.add_heading('Шаги:', level=2)

    try:
        driver.get("https://billyal.netlify.app/")
        driver.maximize_window()
        driver.save_screenshot('screenshot1.png')
        document.add_paragraph('1. Открыта страница: https://billyal.netlify.app/')
        document.add_paragraph('Скриншот 1:')
        document.add_picture('screenshot1.png', width=Inches(6))
        time.sleep(2)

        elements = driver.find_elements(By.CSS_SELECTOR, '.mx-3.my-1.text-dark.text-decoration-none.fw-bold')
        if elements:
            elements[1].click()
            document.add_paragraph('2. Найден и кликнут элемент.')
            driver.save_screenshot('screenshot2.png')
            document.add_paragraph('3. Открыта вторая страница.')
            document.add_paragraph('Скриншот 2:')
            document.add_picture('screenshot2.png', width=Inches(6))
        else:
            document.add_paragraph('2. Внимание: Элементы для клика не найдены.')

        time.sleep(5)
    except Exception as e:
        document.add_paragraph(f'Произошла ошибка во время выполнения теста: {e}', style='List Bullet')

    document.save('test_report.docx')
    print("Word отчет сохранен в файле test_report.docx")

def test_billy_al(driver):
    generate_docx_report(driver)