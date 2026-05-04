import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

MARQUE_CIBLE = "Chanel (Simulé)"
PLATEFORME = "E-commerce"
SITE_SOURCE = "Books to Scrape"
CATEGORIE = "Haute Parfumerie & Beauté"
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
NB_PAGES = 3

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

colonnes = [
    "nom_produit", "marque", "prix", "categorie", "plateforme", 
    "site_source", "url_produit", "note", "nombre_avis", "disponibilite", "page"
]

with open("chanel_books_complet.csv", "w", newline="", encoding="utf-8") as fichier:
    writer = csv.writer(fichier)
    writer.writerow(colonnes)

    for page in range(1, NB_PAGES + 1):
        url = BASE_URL.format(page)
        print(f"🐍 Scraping structuré {MARQUE_CIBLE} - Page {page}...")

        driver.get(url)
        time.sleep(2)

        produits = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

        for p in produits:
            try:

                lien_element = p.find_element(By.CSS_SELECTOR, "h3 a")
                nom = lien_element.get_attribute("title")

                try:
                    prix_brut = p.find_element(By.CSS_SELECTOR, ".price_color").text
                    # Nettoyage pour un format numérique propre[cite: 2]
                    prix = prix_brut.replace("£", "").replace("Â", "").strip() + "€"
                except:
                    prix = "N/A"

                try:
                    note_classe = p.find_element(By.CSS_SELECTOR, ".star-rating").get_attribute("class")
                    note = note_classe.replace("star-rating ", "") 
                except:
                    note = "N/A"

                try:
                    url_prod = lien_element.get_attribute("href")
                except:
                    url_prod = "N/A"

                try:
                    dispo_text = p.find_element(By.CSS_SELECTOR, ".instock.availability").text.strip()
                    dispo = "En stock" if "In stock" in dispo_text else "Hors stock"
                except:
                    dispo = "Hors stock"

                avis = "0"

                writer.writerow([
                    nom, 
                    MARQUE_CIBLE, 
                    prix, 
                    CATEGORIE, 
                    PLATEFORME, 
                    SITE_SOURCE, 
                    url_prod, 
                    note, 
                    avis, 
                    dispo, 
                    page
                ])

            except Exception:
                continue

        time.sleep(1)

driver.quit()
print(f"✅ Terminé ! Le fichier 'chanel_books_complet.csv' est prêt pour ton analyse.")