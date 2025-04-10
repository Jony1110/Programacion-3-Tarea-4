import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import HtmlTestRunner

class H1_Login_exitoso_Test(unittest.TestCase):
    def test_login_saucedemo(self):
        ruta_driver = r"C:\chromedriver\chromedriver-win64\chromedriver.exe"
        service = Service(ruta_driver)
        driver = webdriver.Chrome(service=service)

        # Paso 1: Abrir la página
        driver.get("https://www.saucedemo.com")
        time.sleep(2)

        # Paso 2: Ingresar credenciales
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        # Paso 3: Verificar acceso exitoso
        titulo = driver.title
        print("Título actual:", titulo)
        current_url = driver.current_url
        print("URL actual:", current_url)

        driver.save_screenshot("fotos\H1_login_exitoso_saucedemo.png")

        driver.quit()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reportes'))
