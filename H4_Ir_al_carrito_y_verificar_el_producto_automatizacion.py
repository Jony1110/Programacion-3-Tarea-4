import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import HtmlTestRunner
import time

class H4_Verificar_Carrito_Test(unittest.TestCase):
    def test_producto_en_carrito(self):
        service = Service(r"C:\chromedriver\chromedriver-win64\chromedriver.exe")
        driver = webdriver.Chrome(service=service)

        driver.get("https://www.saucedemo.com")

        # Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))
        print("Login exitoso. En inventario.")

        # Agregar producto al carrito
        try:
            boton_agregar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
            )
            driver.execute_script("arguments[0].click();", boton_agregar)
            print("Se hizo clic en 'Add to cart'")
        except Exception as e:
            print("No se pudo hacer clic en 'Add to cart':", e)
            driver.save_screenshot("error_add_to_cart_H4.png")
            self.fail("Error al agregar el producto al carrito.")

        # Ir al carrito
        try:
            icono_carrito = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_link"))
            )
            driver.execute_script("arguments[0].click();", icono_carrito)
            time.sleep(1)
            if "/cart.html" not in driver.current_url:
                raise Exception("No se redirigió al carrito")
            print("Se accedió al carrito.")
        except Exception as e:
            print("Error al acceder al carrito:", e)
            driver.save_screenshot("error_ir_al_carrito_H4.png")
            self.fail("No se pudo acceder al carrito.")

        # Verificar que el producto esté en el carrito
        try:
            producto = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
            )
            print("Producto en el carrito:", producto.text)
            self.assertIn("Sauce Labs Backpack", producto.text)
        except Exception as e:
            print("Producto no encontrado en el carrito:", e)
            driver.save_screenshot("error_producto_en_carrito_H4.png")
            self.fail("El producto no está en el carrito.")

        driver.save_screenshot("fotos\H4_final_carrito.png")
        driver.quit()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reportes'))
