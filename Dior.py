import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION (Partie 1 & 5 du TP) ---
MARQUE_CIBLE = "Dior (Simulé)"
PLATEFORME = "E-commerce"
SITE_SOURCE = "Books to Scrape"
CATEGORIE = "Parfums & Cosmétiques"
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
NB_PAGES = 3

options = Options()
options.add_argument("--start-maximized")

# Initialisation automatique du driver pour éviter les erreurs de chemin
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- PRÉPARATION DU FICHIER CSV (Structure demandée) ---
colonnes = [
    "nom_produit", "marque", "prix", "categorie", "plateforme", 
    "site_source", "url_produit", "note", "nombre_avis", "disponibilite", "page"
]

with open("dior_books_complet.csv", "w", newline="", encoding="utf-8") as fichier:
    writer = csv.writer(fichier)
    writer.writerow(colonnes)

    for page in range(1, NB_PAGES + 1):
        url = BASE_URL.format(page)
        print(f"🐍 Scraping structuré {MARQUE_CIBLE} - Page {page}...")

        driver.get(url)
        time.sleep(2) # Temps suffisant pour ce site statique

        # Sur Books to Scrape, chaque produit est dans une balise <article>
        produits = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

        for p in produits:
            try:
                # 1. Nom du produit (attribut 'title' du lien)
                lien_element = p.find_element(By.CSS_SELECTOR, "h3 a")
                nom = lien_element.get_attribute("title")

                # 2. Prix (nettoyage simple)
                try:
                    prix_brut = p.find_element(By.CSS_SELECTOR, ".price_color").text
                    prix = prix_brut.replace("£", "").replace("Â", "").strip() + "€"
                except:
                    prix = "N/A"

                # 3. Note (extraite de la classe CSS)[cite: 2]
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

                # 5. Disponibilité (Partie 0 du TP)[cite: 2]
                try:
                    dispo = p.find_element(By.CSS_SELECTOR, ".instock.availability").text.strip()
                except:
                    dispo = "Out of stock"

                # 6. Nombre d'avis (Simulé car inexistant sur ce site)
                avis = "0"

                # Écriture dans le CSV en respectant ton format exact
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

        # Pause éthique entre les pages (Partie 5 du TP)[cite: 2]
        time.sleep(1)

driver.quit()
print(f"✅ Terminé ! Le fichier 'dior_books_complet.csv' contient les données structurées.")