import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import json


url = 'https://www.imdb.com/title/tt2527338/reviews?ref_=tt_urv'  

# Configura el navegador 
driver = webdriver.Chrome()
# Abre la página
driver.get(url)

# Inicializa una lista para almacenar las reseñas
reviews = []

# Realiza el scraping recursivo
while True:
    # Espera un momento para que la página se cargue completamente
    time.sleep(5)
    
    # Parsea el contenido de la página con BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Encuentra las secciones de reseñas en la página actual
    review_sections = soup.find_all('div', class_='lister-item-content')
    
    for review_section in review_sections:
        title_element = review_section.find('a', class_='title')
        if title_element:
            title = title_element.text.strip()
        else:
            title = "Título no encontrado"

        content_element = review_section.find('div', class_='text show-more__control')
        if content_element:
            content = content_element.text.strip()
        else:
            content = "Contenido no encontrado"

        reviews.append({'title': title, 'content': content})
    
    # Intenta hacer clic en el botón "Load More" si existe
    try:
        load_more_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Load More')]")
        load_more_button.click()
    except Exception as e:
        # Si no se encuentra el botón "Load More", se considera que se han recopilado todas las reseñas
        break

# Exportar a CSV
csv_file = 'reviews.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['title', 'content']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for review in reviews:
        writer.writerow(review)

# Exportar a JSON
json_file = 'reviews.json'
with open(json_file, 'w', encoding='utf-8') as file:
    json.dump(reviews, file, ensure_ascii=False, indent=4)

# Cerrar el navegador
driver.quit()

print(f'Se han recopilado {len(reviews)} reseñas y se han exportado a {csv_file} y {json_file}.')

