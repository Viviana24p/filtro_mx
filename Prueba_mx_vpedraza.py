import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime

# Esta función intenta cerrar el banner que aparece para ingresar la ubicación.
def cerrar_banner_ubicacion():
    try:
        cerrar_banner = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Más tarde")]'))
        )
        cerrar_banner.click()
        time.sleep(1)
    except:
        pass

# Esta función toma capturas de pantalla en cada paso importante.
def tomar_captura(nombre):
    ruta_captura = os.path.join(carpeta_capturas, f"{nombre}.png")
    driver.save_screenshot(ruta_captura)

# Creamos la carpeta para guardar las capturas en el escritorio
fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
escritorio = os.path.join(os.environ['USERPROFILE'], 'Desktop')
carpeta_capturas = os.path.join(escritorio, f"capturas_{fecha_hora}")
os.makedirs(carpeta_capturas, exist_ok=True)

# Abrimos el navegador y vamos a Mercado Libre
driver = webdriver.Chrome()
driver.get("https://www.mercadolibre.com/")
time.sleep(3)
tomar_captura("01_inicio")

# Seleccionamos México
driver.find_element(By.PARTIAL_LINK_TEXT, "México").click()
time.sleep(3)
cerrar_banner_ubicacion()
tomar_captura("02_mexico")

# Buscamos "playstation 5"
search_box = driver.find_element(By.NAME, "as_word")
search_box.send_keys("playstation 5")
search_box.send_keys(Keys.RETURN)
time.sleep(3)
cerrar_banner_ubicacion()
tomar_captura("03_busqueda")

# Cerramos el banner de cookies si aparece
try:
    driver.find_element(By.CSS_SELECTOR, 'button.cookie-consent-banner-opt-out__action--key-accept').click()
    time.sleep(2)
    tomar_captura("04_cookies_cerradas")
except:
    pass

# Filtro "Nuevo"
driver.find_element(By.PARTIAL_LINK_TEXT, "Nuevo").click()
time.sleep(2)
cerrar_banner_ubicacion()
tomar_captura("05_filtro_nuevo")

# Filtro "Distrito Federal"
try:
    driver.find_element(By.PARTIAL_LINK_TEXT, "Distrito Federal").click()
    time.sleep(2)
    cerrar_banner_ubicacion()
    tomar_captura("06_filtro_distrito")
except:
    pass

# Ordenar por mayor precio
try:
    ordenar_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[@class="andes-dropdown__display-values" and text()="Más relevantes"]'))
    )
    ordenar_menu.click()
    time.sleep(1)
    cerrar_banner_ubicacion()

    mayor_precio_opcion = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//li[.//span[text()="Mayor precio"]]'))
    )
    driver.execute_script("arguments[0].click();", mayor_precio_opcion)
    time.sleep(3)
    cerrar_banner_ubicacion()
    tomar_captura("07_orden_mayor_precio")

except Exception as e:
    print("Error al ordenar:", e)

# Sacamos los primeros 5 productos y sus precios
titulos = driver.find_elements(By.CSS_SELECTOR, 'a.poly-component__title')[:5]
precios = driver.find_elements(By.CSS_SELECTOR, 'div.poly-price__current span.andes-money-amount__fraction')[:5]

tomar_captura("08_resultados")

# Creamos el archivo de texto con la fecha y hora
nombre_archivo = f"productos_{fecha_hora}.txt"
ruta_txt = os.path.join(escritorio, nombre_archivo)

# Guardamos la información en un archivo y la mostramos en la consola
datos = zip(titulos, precios)
with open(ruta_txt, "w", encoding="utf-8") as archivo:
    archivo.write("🛒 Primeros 5 productos (PRODUCTOS Y PRECIO):\n\n")
    if titulos and precios:
        for i, (titulo, precio) in enumerate(datos, 1):
            linea = f"{i}. {titulo.text} - ${precio.text}"
            print(linea)
            archivo.write(linea + "\n")
    else:
        print("No se pudo extraer la información.")
        archivo.write("No se pudo extraer la información.\n")

# Cerramos el navegador
driver.quit()
