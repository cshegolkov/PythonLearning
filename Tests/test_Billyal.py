from Tests.conftest import driver
from base_page import BasePage

def billyal(driver):
    page = BasePage(driver, "https://billyal.netlify.app/")
    page.open()

    input("Press Enter to quit...")  # Чтобы не закрылось сразу
    driver.quit()

