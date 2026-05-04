import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION (Adaptée pour Estée Lauder) ---
MARQUE_CIBLE = "Estée Lauder (Simulé)"
PLATEFORME = "E-commerce"
SITE_SOURCE = "Books to Scrape"
CATEGORIE = "Luxe & Cosmétiques"
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
NB_PAGES = 3

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Initialisation du driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- PRÉPARATION DU FICHIER CSV ---
colonnes = [
    "nom_produit", "marque", "prix", "categorie", "plateforme", 
    "site_source", "url_produit", "note", "nombre_avis", "disponibilite", "page"
]

# Nom du fichier spécifique pour Estée Lauder
with open("estee_lauder_books_complet.csv", "w", newline="", encoding="utf-8") as fichier:
    writer = csv.writer(fichier)
    writer.writerow(colonnes)

    for page in range(1, NB_PAGES + 1):
        url = BASE_URL.format(page)
        print(f"🐍 Scraping structuré {MARQUE_CIBLE} - Page {page}...")

        driver.get(url)
        time.sleep(2) 

        # On cible les blocs produits (balise article)
        produits = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

        for p in produits:
            try:
                # 1. Nom du produit
                lien_element = p.find_element(By.CSS_SELECTOR, "h3 a")
                nom = lien_element.get_attribute("title")

                # 2. Prix
                try:
                    prix_brut = p.find_element(By.CSS_SELECTOR, ".price_color").text
                    # On nettoie et on convertit symboliquement en Euros
                    prix = prix_brut.replace("£", "").replace("Â", "").strip() + "€"
                except:
                    prix = "N/A"

                # 3. Note
                try:
                    note_classe = p.find_element(By.CSS_SELECTOR, ".star-rating").get_attribute("class")
                    note = note_classe.replace("star-rating ", "")
                except:
                    note = "N/A"

                # 4. URL Produit
                try:
                    url_prod = lien_element.get_attribute("href")
                except:
                    url_prod = "N/A"

                # 5. Disponibilité
                try:
                    dispo_text = p.find_element(By.CSS_SELECTOR, ".instock.availability").text.strip()
                    dispo = "En stock" if "In stock" in dispo_text else "Hors stock"
                except:
                    dispo = "Hors stock"

                # 6. Nombre d'avis (Simulé)
                avis = "0"

                # Écriture dans le CSV
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

        time.sleep(1) # Pause éthique entre les pages

driver.quit()
print(f" Terminé ! Le fichier 'estee_lauder_books_complet.csv' est prêt.")