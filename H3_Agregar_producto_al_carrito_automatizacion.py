import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import HtmlTestRunner
import time

class H3_Agregar_Carrito_Test(unittest.TestCase):
    def test_agregar_producto_carrito(self):
        service = Service(r"C:\chromedriver\chromedriver-win64\chromedriver.exe")
        driver = webdriver.Chrome(service=service)

        driver.get("https://www.saucedemo.com")

        # Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))
        print("Login exitoso. En inventario.")

        try:
            boton_agregar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
            )
            # Forzar el clic con JavaScript
            driver.execute_script("arguments[0].click();", boton_agregar)
            print("Se hizo clic en 'Add to cart'")
        except Exception as e:
            print("No se pudo hacer clic en 'Add to cart':", e)
            driver.save_screenshot("error_add_to_cart.png")
            self.fail("Falló al hacer clic en 'Add to cart'")

        try:
            WebDriverWait(driver, 15).until(
                EC.invisibility_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack"))
            )
        except:
            print("El botón 'Add to cart' no desapareció a tiempo")

        try:
            boton_remover = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.ID, "remove-sauce-labs-backpack"))
            )
            self.assertTrue(boton_remover.is_displayed())
            print("El botón 'Remove' apareció correctamente")
        except Exception as e:
            print("No se encontró el botón 'Remove':", e)
            driver.save_screenshot("error_remove_button.png")
            self.fail("Falló al verificar el botón 'Remove'")

        try:
            carrito_badge = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
            )
            print(f"Productos en el carrito: {carrito_badge.text}")
            self.assertEqual(carrito_badge.text, "1")
        except Exception as e:
            print("No se encontró el badge del carrito:", e)
            driver.save_screenshot("error_carrito.png")
            self.fail("Falló al verificar el número del carrito")

        driver.save_screenshot("fotos\H3_agregar_producto_al_carrito.png")
        driver.quit()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reportes'))
