# %% Importamos las bibliotecas necesarias
from src.utils import parse_texts, term_search, create_folders
import json
from pprint import pprint as pp
import os
import re
import yaml

# Carga archivo yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Declaración de variables globales
FOLDERS_TO_CREATE_FOLDERS = config["path_to_create_folders"]
PATH_TO_LOAD = config["path_to_load_texts"]
PATH_TO_SAVE = config["path_to_save_inverted_index"]

def generate_inverted_index(path_to_load, path_to_save):
    texts, words = parse_texts(path_to_load)
    inverted_index = {
        word: list(
            set(txt for txt, wrds in texts.items() if word in wrds.lower())
            ) 
        for word in words
    }

    with open(path_to_save, "w", encoding="utf-8") as f:
        json.dump(inverted_index, f, ensure_ascii=False, indent=4)
        
    print("El índice fue creado....")

def main(terms):
    create_folders(FOLDERS_TO_CREATE_FOLDERS)
    
    if not os.path.isfile(PATH_TO_SAVE):
        generate_inverted_index(PATH_TO_LOAD, PATH_TO_SAVE)
        
    with open(PATH_TO_SAVE, "r", encoding="utf-8") as f:
        inverted_index = json.load(f)
        
    # Carga del índice invertido    
    print('\nTerm Search for: ' + repr(terms))
    pp(sorted(term_search(inverted_index, terms)))

if __name__ == "__main__":
    terms = input("Ingrese el termino(s) a buscar: ")
    terms_list = re.split(r'[ ,]+', terms)
    main(terms_list)
