from pydriller import Repository, Git
from datetime import datetime
from datetime import date
#How to install requests = pip install requests
import requests 
import json 
import os
import shutil
import sys

#Metodo extraction =  dato il nome del file.txt che deve contenere URL di repository e dato il nome con cui 
#si vuole chiamare la cartella di output --> restituisce tanti file JSON quanti repository con status code 200 sono presenti dentro al file.txt
def extraction(file_name, folder_name):
    #IF per controllare che il file inserito esista
    if os.path.isfile(file_name):
        print("Il file che hai inserito", file_name, "esiste")
        #IF per controllare se la cartella esiste, la sovrascrivo, altrimenti la creo direttamente
        if os.path.isdir(folder_name):
            shutil.rmtree(folder_name)
        os.makedirs(folder_name)
        print("Cartella", folder_name, "creata con successo")
        print()
        
        #Definisco variabili
        index_404 = 0
        index_200 = 0
        index = 0
        dizionario = {}
        index_pack_json = 0

        #Apro il file passato come paramentro in modalità lettura
        with open(file_name, 'r') as file:

            lines = file.readlines()

            for x in lines:

                array_time = [] 
                countReadMe = 0
                array_autori = []
                array_autori_readme = []
                array_commit = []

                URL = x.strip() #rimuovo potenziali spazi bianchi
                nome_url = URL.split("/")[-1]
                stato_url = requests.get(URL)

                #Controllo se l'URL passato sia valido o meno
                if(stato_url.status_code == 404):
                    print(URL, "--> status code 404")
                    index_404 = index_404 + 1
                else:
                    print(URL, "--> status code 200")
                    index_200 = index_200 + 1
                    #Per ogni URL vado a prendere le varie informazioni per poter creare i file JSON
                    for commit in Repository(URL).traverse_commits():

                        index = index + 1 
                        array_time.append(commit.committer_date)
                        array_autori.append(commit.author.email) #EMAIL

                        for modified_file in commit.modified_files:

                            if "json" in modified_file.filename.lower():
                                index_pack_json = index_pack_json + 1

                            if "readme" in modified_file.filename.lower():
                                countReadMe = countReadMe + 1
                                array_autori_readme.append(commit.author.email) #EMAIL
                                current_commit = {
                                    'hash': str(commit.hash),
                                    'author_email': str(commit.author.email), #EMAIL
                                    'timestamp': str(commit.committer_date),
                                    'message': str(commit.msg),
                                    'number_modified_files': len(commit.modified_files),
                                    'progressive_commit_number': index,
                                }

                                array_commit.append(current_commit)

                    
                    #Salvo in un dizionario tutte le informazioni che mi servono per poter creare il file JSON
                    dizionario['project'] = nome_url
                    dizionario['url'] = URL
                    dizionario['first-commit-timestamp'] = str(array_time[0])
                    dizionario['last-commit-timestamp'] = str(array_time[-1])
                    dizionario['number_of_commits'] = index
                    dizionario['number_of_manifest_commits'] = index_pack_json
                    dizionario['number_of_README_commits'] = countReadMe
                    dizionario['list_of_author_emails'] = list(dict.fromkeys(array_autori))
                    dizionario['number_of_authors'] = len(list(dict.fromkeys(array_autori)))
                    dizionario['number_of_author_readme'] = len(list(dict.fromkeys(array_autori_readme)))
                    dizionario['README_commits'] = array_commit

                    #Creo nome che dovrò avere il file JSON di output
                    nome_json_file = nome_url + ".json"
                    #Cast del dizionario per poterlo scrivere in formato JSON
                    diz_to_json = json.dumps(dizionario, indent = 4)
                    #Scrivo per ogni URL con status code 200 il relativo file JSON e la vado a salvare nella cartella passata in input dall'utente
                    with open(os.path.join(folder_name,nome_json_file), "w") as JS_file:
                        JS_file.write(diz_to_json) 
                        JS_file.close()

            #Print per fare il recap di quello che è accaduto durante l'esecuzione
            print()
            print("Il numero di repository processati sono -->", len(lines))
            print("Sono stati creati un numero di file JSON pari a -->", index_200)
            print("Numero URL che hanno dato errore 404 -->",index_404)
            print("Numero di URL che NON hanno dato errore -->", index_200)
    else:
        #Se il file che passo in input non esiste --> il programma non puà andare in esecuzione
         print("File NON esiste non posso proseguire")
         sys.exit()



#Se per sbaglio un utente passa più paramentri di quelli che servono, il programma terminerà
if(len(sys.argv) == 4 or len(sys.argv) > 4):
    print("Mi dispiace, ma hai inserito troppi valori di riga di comando")
    sys.exit()

#IF che serve per far partire l'esecuzione in maniera interattiva (nel caso in cui i parametri non vengano passati da riga di comando)
#oppure in maniera automatica.
if(len(sys.argv) < 3):
    print("I campi non sono stati passati da riga di comando, di conseguenza si è attivata la modalità interattiva")
    x = input("Inserire nome file: ")
    y = input("Inserire nome cartella: ")
    extraction(x,y)
else:
    extraction(sys.argv[1],sys.argv[2])




