import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import HtmlTestRunner
import time

class H5_Proceder_Checkout_Test(unittest.TestCase):
    def test_completar_compra(self):
        service = Service(r"C:\chromedriver\chromedriver-win64\chromedriver.exe")
        driver = webdriver.Chrome(service=service)

        driver.get("https://www.saucedemo.com")

        # Login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))

        # Agregar producto
        boton_agregar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        )
        driver.execute_script("arguments[0].click();", boton_agregar)

        # Ir al carrito
        carrito = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_link"))
        )
        driver.execute_script("arguments[0].click();", carrito)

        # Click en Checkout
        boton_checkout = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        driver.execute_script("arguments[0].click();", boton_checkout)

        # Llenar formulario
        try:
            WebDriverWait(driver, 10).until(EC.url_contains("/checkout-step-one.html"))

            campo_nombre = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "first-name"))
            )
            campo_apellido = driver.find_element(By.ID, "last-name")
            campo_zip = driver.find_element(By.ID, "postal-code")

            campo_nombre.clear()
            campo_apellido.clear()
            campo_zip.clear()

            campo_nombre.send_keys("Juan")
            campo_apellido.send_keys("Pérez")
            campo_zip.send_keys("10101")

            # Validar que los campos se llenaron
            self.assertEqual(campo_nombre.get_attribute("value"), "Juan")
            self.assertEqual(campo_apellido.get_attribute("value"), "Pérez")
            self.assertEqual(campo_zip.get_attribute("value"), "10101")

            time.sleep(1)  # Pequeña espera para evitar errores por timing

            boton_continuar = driver.find_element(By.ID, "continue")
            driver.execute_script("arguments[0].click();", boton_continuar)

            WebDriverWait(driver, 10).until(EC.url_contains("/checkout-step-two.html"))
            print("Formulario llenado y paso 2 confirmado.")
        except Exception as e:
            print("Error en el formulario:", e)
            driver.save_screenshot("error_formulario_checkout.png")
            self.fail("No se completó el formulario.")

        # Finalizar compra
        try:
            boton_finish = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "finish"))
            )
            driver.execute_script("arguments[0].click();", boton_finish)

            WebDriverWait(driver, 10).until(EC.url_contains("/checkout-complete.html"))
            print("¡Compra finalizada con éxito!")
        except Exception as e:
            print("Error al finalizar compra:", e)
            driver.save_screenshot("error_finalizar_checkout.png")
            self.fail("No se pudo finalizar la compra.")

        driver.save_screenshot("fotos\H5_compra_exitosa.png")
        driver.quit()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reportes'))
