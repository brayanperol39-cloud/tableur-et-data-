import pandas as pd
import glob

# On récupère tous tes fichiers CSV de marques
fichiers = glob.glob("*_books_complet.csv")

# Fusion de tous les fichiers
df_final = pd.concat([pd.read_csv(f) for f in fichiers])

# Sauvegarde du fichier unique pour le client
df_final.to_csv("Data_Monitor_Client_Final.csv", index=False, encoding="utf-8")
print(f"✅ Fusion terminée : {len(fichiers)} fichiers regroupés.")