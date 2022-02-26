import Bio
from Bio.Seq import Seq
from Bio import Entrez
import re
import numpy as np
import pandas as pd
def download_pubmed(keyword):
    """ Esta funcion sirve  para descargar la data con el keyword Ecuador genomics de PubMe"""
    Entrez.email = "gualapuro.moises@gmail.com"
    handle = Entrez.esearch(db = "pubmed", term = keyword, usehistory = "y", retmax = 1000)
    record = Entrez.read(handle)
    handle.close()
   
    
    return record



def mining_pubs(tipo, identificadores):
    """Esta función con dos parametros permite obtener
    un dataframe segun los 3 tipos de identificadores
    DP- recupera el año de publicación del artículo
    AU -recupera el número de autores por PMID
    AD-recupera el conteo de autores por país, de una data proveniente
    de PubMed con el  keyword Ecuador genomics"""
    #if tipo == "AD":
    data = []
    for i in identificadores:  
        handle = Entrez.efetch(db = "pubmed",
                      rettype = "medline",
                      retmode = "text",
                      retstart = 0,
                       retmax = 543,
                       id = i)
        result = handle.read()
        handle.close()
        result = re.sub('United States', 'USA', result) 
        result = re.sub('United Kingdom', 'UK', result)
        year =  re.findall(r'DP  - (\d{4})', result)
        country = re.findall(r'PL  - (\w+)', result)
        autors = re.findall(r'AU  - ', result)
        num_autor = len(autors)
        data.append([i,year[0], country[0], num_autor ])
    data = np.array(data)
    if tipo == "DP":
        dataframe = pd.DataFrame(data)

        return dataframe[[0,1]]
    
    elif tipo == "AU":
        dataframe = pd.DataFrame(data)

        return dataframe[[0,3]]
    
    elif tipo == "AD":
        dataframe = pd.DataFrame(data)

        return dataframe[[2,3]]