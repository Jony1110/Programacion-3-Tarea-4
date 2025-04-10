import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import HtmlTestRunner

class H2_Ver_Productos(unittest.TestCase):
    def test_ver_productos_con_zoom(self):
        service = Service(r"C:\chromedriver\chromedriver-win64\chromedriver.exe")
        driver = webdriver.Chrome(service=service)

        driver.get("https://www.saucedemo.com")
        time.sleep(1)

        # Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # Aplicar zoom out al 67%
        driver.execute_script("document.body.style.zoom='67%'")
        time.sleep(1)

        # Captura con zoom reducido
        driver.save_screenshot("fotos\H2_ver_productos.png")

        # Verificar que al menos 6 productos están presentes
        productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
        print(f"Productos encontrados: {len(productos)}")
        self.assertGreaterEqual(len(productos), 6)

        driver.quit()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reportes'))
