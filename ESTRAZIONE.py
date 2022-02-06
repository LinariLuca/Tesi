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
def extraction(file_name, folder_name, filtro_name):
    print("NOME FILTRO INSERITO", filtro_name)
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

        #Apro il file passato come paramentro in modalità lettura
        with open(file_name, 'r') as file:

            lines = file.readlines()

            for x in lines:

                array_time = [] 
                count_selected_commits = 0
                array_autori_selected_commit = []
                array_autori = []
                array_commit = []
                
                array_commit_hash = []
                array_senza_duplicati_hash = []
                index_progressive = 0
                dizionario = {}

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
                    list_of_commit = Repository(URL).traverse_commits()
                    NUMERO_COMMIT = len(list(list_of_commit))

                    for commit in Repository(URL).traverse_commits():
                        index_progressive = index_progressive + 1
                        array_time.append(commit.committer_date)
                        array_autori.append(commit.author.email)

                        for modified_file in commit.modified_files:
                            if filtro_name in modified_file.filename.lower():
                                array_commit_hash.append(commit.hash)

                        for x in list(dict.fromkeys(array_commit_hash)):
                            #If per prendere informazioni dei soli commit che mi interessano
                            if x in commit.hash:
                                print("SONO QUA", x)
                                array_autori_selected_commit.append(commit.author.email)
                                current_commit = {
                                    'hash': str(commit.hash),
                                    'author_email': str(commit.author.email),
                                    'timestamp': str(commit.committer_date),
                                    'message': str(commit.msg), 
                                    'number_modified_files': len(commit.modified_files),
                                    'progressive_commit_number': index_progressive
                                }

                                array_commit.append(current_commit)


                    print()
                    #########
                    dizionario['project'] = nome_url
                    dizionario['url'] = URL
                    dizionario['number_of_commits'] = NUMERO_COMMIT
                    dizionario['first-commit-timestamp'] = str(array_time[0])
                    dizionario['last-commit-timestamp'] = str(array_time[-1])
                    dizionario['number_of_authors'] = len(list(dict.fromkeys(array_autori)))
                    dizionario['list_of_author_emails'] = list(dict.fromkeys(array_autori))
                    dizionario['number_of_author_selected'] = len(list(dict.fromkeys(array_autori_selected_commit)))
                    dizionario['number_of_SELECTED_commits'] = len(list(dict.fromkeys(array_commit_hash)))
                    dizionario['SELECTED_commits'] = array_commit

                    #########
                    nome_json_file = nome_url + ".json"
                    diz_to_json = json.dumps(dizionario, indent = 4)
                    with open(os.path.join(folder_name,nome_json_file), "w") as JS_file:
                        JS_file.write(diz_to_json) 
                        JS_file.close()
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
if(len(sys.argv) == 5 or len(sys.argv) > 5):
    print("Mi dispiace, ma hai inserito troppi valori di riga di comando")
    sys.exit()

#IF che serve per far partire l'esecuzione in maniera interattiva (nel caso in cui i parametri non vengano passati da riga di comando)
#oppure in maniera automatica.
if(len(sys.argv) < 4):
    print("I campi non sono stati passati da riga di comando, di conseguenza si è attivata la modalità interattiva")
    x = input("Inserire nome file: ")
    y = input("Inserire nome cartella: ")
    z = input("Inserire parametro per controllo file: ")
    extraction(x,y,z)
else:
    extraction(sys.argv[1],sys.argv[2], sys.argv[3])




