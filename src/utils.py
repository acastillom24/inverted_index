from glob import glob
from functools import reduce
import re

from pathlib import Path

def create_folders(paths):
    for path in paths:
        folder = Path(path)
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            print(f"Carpeta creada: {path}")

def clean_text(texto):
    '''
    Esta función limpia y tokeniza el texto en palabras individuales.
    El orden en el que se va limpiando el texto no es arbitrario.
    El listado de signos de puntuación se ha obtenido de: print(string.punctuation)
    y re.escape(string.punctuation)
    '''
    
    # Se convierte todo el texto a minúsculas
    nuevo_texto = texto.lower()
    # Eliminar tildes
    # nuevo_texto = re.sub(r'[á]', 'a', nuevo_texto)
    # nuevo_texto = re.sub(r'[é]', 'e', nuevo_texto)
    # nuevo_texto = re.sub(r'[í]', 'i', nuevo_texto)
    # nuevo_texto = re.sub(r'[ó]', 'o', nuevo_texto)
    # nuevo_texto = re.sub(r'[ú]', 'u', nuevo_texto)
    # nuevo_texto = re.sub(r'[ñ]', '#', nuevo_texto)
    # nuevo_texto = re.sub(r'[ü]', 'u', nuevo_texto)
    # nuevo_texto = re.sub(r'[ö]', 'u', nuevo_texto)
    # Eliminación de páginas web (palabras que empiezan por "http")
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    # Eliminación de signos de puntuación
    regex = '[\\“\\”\\’\\‘\\─\\—\\°\\¡\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\¿\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    nuevo_texto = re.sub(regex , ' ', nuevo_texto)
    nuevo_texto = re.sub(r'\s+', ' ', nuevo_texto).strip()
    nuevo_texto = re.sub(r'[\s\u200b\u2013]+', ' ', nuevo_texto).strip()
    # Eliminación de números
    nuevo_texto = re.sub("\d+", ' ', nuevo_texto)
    # Eliminación de espacios en blanco múltiples
    nuevo_texto = re.sub("\\s+", ' ', nuevo_texto)
    # Tokenización por palabras individuales
    nuevo_texto = nuevo_texto.split(sep = ' ')
    # Eliminación de tokens con una longitud < 2
    nuevo_texto = [token for token in nuevo_texto if len(token) > 1]
    
    return(nuevo_texto)

def parse_texts(path='/content/corpus/*.txt'):
    """_summary_

    Parameters
    ----------
    path : str, optional
        _description_, by default '/content/corpus/*.txt'

    Returns
    -------
    _type_
        _description_
    """
    texts, words = {}, set()
    for file in glob(path):
        with open(file, 'r') as f:
            txt = f.read()
            words |= set(clean_text(txt))
            texts[file.split('\\')[-1]] = txt
    return texts, words

# funcion para buscar los terminos en el indice creado
def term_search(inverted_index, terms):
    term_list = [inverted_index.get(term, set()) for term in terms]
    flattened_term_list = [item for sublist in term_list for item in (sublist if isinstance(sublist, list) else [sublist])]
    if any(term == set() for term in flattened_term_list):
        return set()
    return list(reduce(set.intersection, map(set, term_list)))

class InvertedIndex:
    def __init__(self, doc):
        self.doc = doc
        self.lines = 1
        self.arr = []
    
    def Display_docs(self):
        return self.doc
    
    def Number_of_docs(self):
        for word in self.doc:
            if word == '\n':
                self.lines += 1
        return self.lines

    def Split_docs(self):
        for i in range(self.lines):
            self.arr.append(self.doc.split('\n')[i])
        return self.arr

    def Tokenization(self):
        self.doc = self.doc.lower()
        tokens = self.doc.split()
        return tokens

    def Stopping(self):
        stop_words = open('StopWords.txt', 'r').read()
        stop_words = stop_words.split()

        NewList = []
        # Remove special characters
        tokens = self.Tokenization()
        for doc in tokens:
            Newdoc = "".join(ch for ch in doc if ch.isalnum())
            NewList.append(Newdoc)
            
            # Remove stopring words
            after_stopping = [token for token in NewList if token not in stop_words]

        return after_stopping

    def Inverted_Index(self):
        Inverted_index = {}
        after_stopping = self.Stopping()
        for token in after_stopping:
            for i in range(self.lines):
                if token in self.arr[i]:
                    if token in Inverted_index:
                        Inverted_index[token].add(i+1)
                    else:
                        Inverted_index[token] = {i+1}

        return Inverted_index

    def Indexer(self):
        indexer = {}
        after_stopping = self.Stopping()
        for token in after_stopping:
            for i in range(self.lines):
                if token in self.arr[i]:
                    indexer[token] = i+1

        return indexer

    def Term_squences(self):
        indexer = self.Indexer()
        return sorted(indexer.items(), key=lambda x: x[1])

    def Sorting_Alphabetically(self):
        indexer = self.Indexer()
        return sorted(indexer.items(), key=lambda x: x[0])

    def Term_Frequency(self):
        Term_frequancy = {}
        Inverted_index = self.Inverted_Index()
        for term in Inverted_index:
            Term_frequancy[term] = term
            Term_frequancy[term] = len(Inverted_index[term])

        return Term_frequancy