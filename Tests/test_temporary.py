import time
from selenium.webdriver.common.by import By
from base_page import BasePage
from Tests.conftest import driver

# ОТКРЫВАЕМ СТРАНИЧКУ, ждем 5 секунд, закрываем
def test_billy_al(driver):
    page = BasePage(driver, "https://billyal.netlify.app/")
    page.open()
    driver.save_screenshot('screenshot1.png')
    time.sleep(2)  # чтобы увидеть страницу
# находим элемент и кликаем по нему
    elements = driver.find_elements(By.CSS_SELECTOR, '.mx-3.my-1.text-dark.text-decoration-none.fw-bold')
    if elements:
        elements[1].click()  # клик по первому элементу
    else:
        print("Элементы не найдены")
    driver.save_screenshot('screenshot2.png')

    time.sleep(5)
