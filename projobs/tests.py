from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time
import random

# Esta clase realiza una prueba de extremo a extremo para registro y login usando Selenium
class RegistroYLoginTest(LiveServerTestCase):

    def setUp(self):
        # Configuramos las opciones de Chrome
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Si quieres correr sin abrir el navegador, descomenta esto
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Establece la ruta absoluta al ejecutable de chromedriver
        path = os.path.join(os.getcwd(), 'chromedriver.exe')
        service = Service(executable_path=path)

        # Instancia del navegador Chrome
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)  # Tiempo máximo de espera para encontrar elementos

        # Se generan datos aleatorios válidos para evitar conflictos
        numero_random = random.randint(1000, 9999)
        self.correo_prueba = f"test{numero_random}@gmail.com"  # Email único por prueba
        self.password_prueba = "Test1234"  # Requiere letras y números

    def test_registro_y_login(self):
        # Accede a la vista de formulario de registro
        self.driver.get(f'{self.live_server_url}/formulario/')

        # Completa los campos del formulario
        self.driver.find_element(By.NAME, 'nombre').send_keys('Selenium')
        self.driver.find_element(By.NAME, 'apellido').send_keys('Test')
        self.driver.find_element(By.NAME, 'correo').send_keys(self.correo_prueba)
        self.driver.find_element(By.NAME, 'password').send_keys(self.password_prueba)

        # Selecciona el rol 'Trabajador' (valor = 3)
        rol_select = self.driver.find_element(By.NAME, 'rol')
        for option in rol_select.find_elements(By.TAG_NAME, 'option'):
            if option.get_attribute('value') == '3':
                option.click()
                break

        # Adjunta una imagen si existe el archivo default.png en el directorio raíz
        foto_path = os.path.join(os.getcwd(), 'default.png')
        if os.path.exists(foto_path):
            self.driver.find_element(By.ID, 'foto').send_keys(foto_path)

        # Envía el formulario
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)  # Espera a que procese el registro

        # Accede al formulario de inicio de sesión
        self.driver.get(f'{self.live_server_url}/inicioSesion/')
        self.driver.find_element(By.NAME, 'correo').send_keys(self.correo_prueba)
        self.driver.find_element(By.NAME, 'password').send_keys(self.password_prueba)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)  # Espera a que cargue el dashboard

        # Valida que haya iniciado sesión buscando texto en el cuerpo de la página
        body_text = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Bienvenido', body_text)  # Asegúrate que "Bienvenido" exista en el HTML tras login

    def tearDown(self):
        # Cierra el navegador después de la prueba
        self.driver.quit()
