import requests
from bs4 import BeautifulSoup
import csv
import time

URL_CIBLE = "https://books.toscrape.com/catalogue/page-1.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
FICHIER_CSV = "resultats_scraping.csv"

def lancer_scraping():
    print(f"Début de l'extraction sur : {URL_CIBLE}...")
    
    try:
        response = requests.get(URL_CIBLE, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            print("Connexion réussie (Statut 200).")
            soup = BeautifulSoup(response.text, "html.parser")

            articles = soup.find_all("article", class_="product_pod")

            with open(FICHIER_CSV, "w", newline="", encoding="utf-8") as fichier:
                writer = csv.writer(fichier)
                # En-tête avec les 4 champs requis par le TP
                writer.writerow(["titre", "prix", "note", "disponibilite"])
                
                for art in articles:
                    try:

                        titre = art.find("h3").find("a")["title"]

                        prix = art.find("p", class_="price_color").text.strip()

                        note_classe = art.find("p", class_="star-rating")["class"]
                        note = note_classe[1] 

                        dispo = art.find("p", class_="availability").text.strip()

                        writer.writerow([titre, prix, note, dispo])
                        
                    except Exception:
                        continue
            
            print(f"Succès ! Le fichier '{FICHIER_CSV}' a été créé.")
            time.sleep(1) 
            
        else:
            print(f"Échec de connexion. Code HTTP : {response.status_code}")

    except Exception as e:
        print(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    lancer_scraping()