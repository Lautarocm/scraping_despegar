from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
from provincias import provincias



# inicializar selenium
ruta = ChromeDriverManager(path="./chromedriver").install()

s = Service(ruta)

driver = webdriver.Chrome(service=s)

url = "https://www.despegar.com.ar/paquetes/"



cant_destinos = 0

ofertas = []



def abrir_pagina():
    driver.get(url)



def cerrar_modals():
    time.sleep(2)
    boton_banner = driver.find_element(By.CLASS_NAME, "lgpd-banner--button")
    boton_activar_notif = driver.find_element(By.CLASS_NAME, "shifu-3-icon-close")
    boton_login = driver.find_element(By.CLASS_NAME, "login-incentive--close")
    
    if boton_banner.is_displayed():
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(boton_banner)).click()
        print("cerrando banner")
    if boton_activar_notif.is_displayed():
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(boton_activar_notif)).click()
        print("cerrando modal de activar notificaciones")
    if boton_login.is_displayed():
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(boton_login)).click()
        print("cerrando modal de login")



def calcular_cant_destinos():
    global cant_destinos

    input_destino = driver.find_element(By.CLASS_NAME, "sbox-places-destination-override").find_element(By.TAG_NAME, "input")
    click_outside_input = driver.find_element(By.CLASS_NAME, "sbox5-title--2vZFL")
    
    input_destino.click()
    time.sleep(1)
    input_destino.send_keys("argentina")
    time.sleep(1)
    destinos = driver.find_element(By.CLASS_NAME, "ac-group-items").find_elements(By.TAG_NAME, "li")
    input_destino.clear()
    click_outside_input.click()
    cant_destinos = len(destinos)



def rellenar_busqueda(destino):    
    switch_fechas = driver.find_element(By.CLASS_NAME, "switch-container")
    boton_buscar = driver.find_element(By.CLASS_NAME, "sbox5-box-button-ovr--lX4PS")
    input_destino = driver.find_element(By.CLASS_NAME, "sbox-places-destination-override").find_element(By.TAG_NAME, "input")
    
    try:
        driver.find_element(By.CLASS_NAME, "sbox5-dates-v2-container")
        switch_fechas.click()
    except NoSuchElementException:
        pass
    
    input_destino.clear()
    time.sleep(1)
    input_destino.click()
    input_destino.send_keys("argentina")
    time.sleep(1)
    destinos = driver.find_element(By.CLASS_NAME, "ac-group-items").find_elements(By.TAG_NAME, "li")
    destinos[destino].click()
    boton_buscar.click()
    time.sleep(2)



def ver_mas_resultados():

    # boton_mejores = driver.find_element(By.CLASS_NAME, "section-4").find_element(By.TAG_NAME, "optional-link")

    titulos_h2 = driver.find_elements(By.TAG_NAME, "h2")
    for titulo in titulos_h2:
        if "oferta" in titulo.text:
            try:
                boton_ofertas = titulo.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.TAG_NAME, "optional-link").click()
            except NoSuchElementException:
                pass
    

    # boton_ofertas = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "section-5"))).find_element(By.TAG_NAME, "optional-link")

    # # WebDriverWait(driver, 20).until(EC.element_to_be_clickable(boton_mejores)).click()

    # boton_ofertas.click()



def obtener_ofertas():
    global ofertas

    # obtenemos el html
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # seccion_mejores = soup.find("div", class_="section-5")

    seccion_ofertas = soup.find("div", class_="section-4")

    # tarjetas_mejores = seccion_mejores.find_all("offer-card")

    tarjetas_ofertas = seccion_ofertas.find_all("offer-card")[0]

    ofertas.append(tarjetas_ofertas)
    print(len(ofertas))



def realizar_busquedas():
    calcular_cant_destinos()
    i = 1
    while i < cant_destinos:
        rellenar_busqueda(i)
        cerrar_modals()
        ver_mas_resultados()
        obtener_ofertas()
        i+=1



def crear_json():
    ofertas = {}



def resumen_ofertas():
    seccion = driver.find_element(By.CLASS_NAME,"section-4")

    ofertas = seccion.find_elements(By.TAG_NAME, "offer-card")

    for oferta in ofertas:
        hotel = oferta.find_element(By.CLASS_NAME, "offer-card-title").text
        dias = oferta.find_element(By.CLASS_NAME, "driver-text").text
        precio = int(oferta.find_element(By.CLASS_NAME, "offer-card-pricebox-price-amount").text.replace(".", ""))
        print(f"El hotel es el {hotel}, para {dias} y sale {precio}")
    


def scrap_despegar():
    abrir_pagina()
    cerrar_modals()
    realizar_busquedas()


scrap_despegar()

"""# boton para cerrar banner
boton_banner = driver.find_element(By.CLASS_NAME, "lgpd-banner--button")

WebDriverWait(driver, 20).until(EC.element_to_be_clickable(boton_banner)).click()"""



"""# cargamos datos para buscar paquetes
mensaje_notificaciones = driver.find_element(By.CLASS_NAME, "")"""