import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from datetime import datetime

# Iniciar navegador
driver = webdriver.Chrome()
driver.get("https://www.mercadolibre.com/")
time.sleep(3)

# Seleccionar país
driver.find_element(By.PARTIAL_LINK_TEXT, "México").click()
time.sleep(3)

# Buscar producto
search_box = driver.find_element(By.NAME, "as_word")
search_box.send_keys("playstation 5")
search_box.send_keys(Keys.RETURN)
time.sleep(3)

# Cerrar banner de cookies si aparece
try:
    driver.find_element(By.CSS_SELECTOR, 'button.cookie-consent-banner-opt-out__action--key-accept').click()
    time.sleep(2)
except:
    pass

# Filtro: Nuevo
driver.find_element(By.PARTIAL_LINK_TEXT, "Nuevo").click()
time.sleep(2)

# Filtro: Distrito Federal
try:
    driver.find_element(By.PARTIAL_LINK_TEXT, "Distrito Federal").click()
    time.sleep(2)
except:
    pass

# Ordenar por menor precio
try:
    driver.find_element(By.CSS_SELECTOR, "div.andes-dropdown__trigger").click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//li[contains(., "Menor precio")]').click()
    time.sleep(3)
except:
    pass

# Extraer datos
titulos = driver.find_elements(By.CSS_SELECTOR, 'a.poly-component__title')[:5]
precios = driver.find_elements(By.CSS_SELECTOR, 'div.poly-price__current span.andes-money-amount__fraction')[:5]

# Guardar en el escritorio con fecha y hora
fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
escritorio = os.path.join(os.environ['USERPROFILE'], 'Desktop')
nombre_archivo = f"productos_{fecha_hora}.txt"
ruta_txt = os.path.join(escritorio, nombre_archivo)

with open(ruta_txt, "w", encoding="utf-8") as archivo:
    archivo.write("🛒 Primeros 5 productos (PRODUCTOS Y PRECIO):\n\n")
    if titulos and precios:
        for i in range(min(len(titulos), len(precios))):
            archivo.write(f"{i+1}. {titulos[i].text} - ${precios[i].text}\n")
    else:
        archivo.write("No se pudo extraer la información.\n")

# Cerrar navegador automáticamente
driver.quit()