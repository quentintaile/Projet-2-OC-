import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

base_url = 'https://books.toscrape.com/'
url_base_livre = 'https://books.toscrape.com/catalogue/'

# Créer les dossiers pour stocker les données et les images
os.makedirs('feuilles_donnees', exist_ok=True)
os.makedirs('images', exist_ok=True)

# Fonction pour extraire les catégories de livres du site et leur URL
def extraire_categories():
    url = base_url + 'index.html'
    reponse = requests.get(url)
    soupe = BeautifulSoup(reponse.content, 'html.parser')
    categories = soupe.find('ul', class_='nav-list').find('ul').find_all('a')
    return [(cat.text.strip(), base_url + cat['href']) for cat in categories]
# Retourne une liste  contenant le nom de chaque catégorie et son URL complète.

# Fonction pour extraire les données d'un livre depuis sa page de produit
# Paramètres : rl_produit : Lien vers la page produit du livre
def extraire_donnees_livre(url_produit):
    reponse_produit = requests.get(url_produit)
    soupe_produit = BeautifulSoup(reponse_produit.content, 'html.parser')
# Retourne un dictionnaire avec les informations extraites du livre.

    # Extraire les informations spécifiques du produit
    # Récupérer le code universel du produit (UPC) si disponible
    code_produit = soupe_produit.find('th', string='UPC').find_next_sibling('td').text if soupe_produit.find('th', string='UPC') else 'Non disponible'
    
    # Récupérer les prix TTC et HT, et vérifier leur présence
    prix_ttc = soupe_produit.find('th', string='Price (incl. tax)').find_next_sibling('td').text if soupe_produit.find('th', string='Price (incl. tax)') else 'Non disponible'
    prix_ht = soupe_produit.find('th', string='Price (excl. tax)').find_next_sibling('td').text if soupe_produit.find('th', string='Price (excl. tax)') else 'Non disponible'
    
    # Récupérer la disponibilité en stock
    disponibilite = soupe_produit.find('th', string='Availability').find_next_sibling('td').text.strip() if soupe_produit.find('th', string='Availability') else 'Non disponible'
    
    # Récupérer la description du produit si elle est présente
    description = soupe_produit.find('meta', {'name': 'description'})['content'].strip() if soupe_produit.find('meta', {'name': 'description'}) else 'No description available'
    
    # Récupérer la catégorie du livre depuis la navigation breadcrumb
    categorie = soupe_produit.find('ul', class_='breadcrumb').find_all('li')[2].text.strip() if soupe_produit.find('ul', class_='breadcrumb') else 'Non disponible'

    # Extraction de la note en fonction des étoiles
    note_element = soupe_produit.find('p', class_='star-rating')
    if note_element:
        note_texte = note_element['class'][1]
        note = convertir_note_en_nombre(note_texte)
    else:
        note = 'Non disponible'

    # Extraction de l'URL de l'image 
    url_miniature = base_url + soupe_produit.find('img')['src'].replace('../', '')

    # Retourner les informations
    return {
        'product_page_url': url_produit,
        'universal_product_code (upc)': code_produit,
        'title': soupe_produit.h1.text,
        'price_including_tax': prix_ttc,
        'price_excluding_tax': prix_ht,
        'number_available': disponibilite,
        'product_description': description,
        'category': categorie,
        'review_rating': note,
        'image_url': url_miniature
    }

# Fonction pour convertir le texte de la note en un nombre
def convertir_note_en_nombre(texte_note):
    dictionnaire_notes = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }
    return dictionnaire_notes.get(texte_note, 0)

# Fonction pour sauvegarder l'image miniature
def sauvegarder_image_miniature(url, titre):
    reponse = requests.get(url)
    titre_sanitaire = "".join([c if c.isalnum() else "_" for c in titre])
    chemin_image = os.path.join('images', f"{titre_sanitaire}.jpg")
    with open(chemin_image, 'wb') as fichier:
        fichier.write(reponse.content)
    return chemin_image

# Fonction pour récupérer les livres de toutes les pages d'une catégorie
def extraire_livres_par_categorie(url_categorie):
    page = 1  # Initialiser la page à 1
    livres = []
    while True:
        # Construire l'URL de la page (gérer la pagination)
        url_page = url_categorie.replace('index.html', f'page-{page}.html') if page > 1 else url_categorie
        reponse = requests.get(url_page)
        
        # Si le statut n'est pas 200, fin de la pagination
        if reponse.status_code != 200:
            break
        soupe = BeautifulSoup(reponse.content, 'html.parser')
        
        # Récupérer tous les livres sur la page
        for livre in soupe.find_all('article', class_='product_pod'):
            lien = url_base_livre + livre.h3.a['href'].replace('../../../', '')  # Corriger le lien
            donnees_livre = extraire_donnees_livre(lien)
            sauvegarder_image_miniature(donnees_livre['image_url'], donnees_livre['title'])  # Sauvegarder l'image miniature
            livres.append(donnees_livre)
        
        print(f"Page {page} extraite pour la catégorie")
        page += 1  # Passer à la page suivante
    return livres

# Extraire les catégories et parcourir chaque catégorie
categories = extraire_categories()
for nom_categorie, lien_categorie in categories:
    print(f"Extraction des données pour la catégorie : {nom_categorie}")
    livres = extraire_livres_par_categorie(lien_categorie)
    
    # Sauvegarder les données dans un fichier CSV pour chaque catégorie
    if livres:
        df = pd.DataFrame(livres)
        df.to_csv(f'feuilles_donnees/{nom_categorie}.csv', index=False)
        print(f"Données sauvegardées pour la catégorie {nom_categorie}")

print("Scraping terminé")
