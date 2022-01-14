from pydriller import Repository, Git
from datetime import datetime
from datetime import date
import requests #apro cartella --> terminale --> e digito pip install requests
import json 
import os
import shutil

#Leggo file
array_project = open("test.txt").read().splitlines()



############CREARE CARTELLA CHE SE ESISTE GIA' LA SOVRASCRIVO############
name_folder = "JSON_file"
if os.path.exists(name_folder):
    shutil.rmtree(name_folder)
os.makedirs(name_folder)
#######################################

#cambio cartella di riferimento con quella appeana creata
#cambio cartella cosi i file vengono salvati direttamente li senza che sia necessario fare un move
os.chdir(name_folder)

index = 0
dizionario = {}


for progetto in array_project:
    #inizializzo qua cosi ogni volta che riparte il ciclo per un URL si pulisce array
    array_time = [] 
    countReadMe = 0
    array_autori = []
    array_autori_readme = []
    array_commit = []

    x  = str(progetto)
    nome_progetto = x.split("/")[-1]
    stato_url = requests.get(x)
    if(stato_url.status_code == 404):
        print("STATUS CODE 404")
    else:
        print("STATUS CODE 200")
        for commit in Repository(x, only_in_branch='origin/master').traverse_commits():
            index  = index + 1
            array_time.append(commit.committer_date)
            array_autori.append(commit.author.name)
            
            for modified_file in commit.modified_files:
                if "README" in modified_file.filename:
                    countReadMe = countReadMe + 1
                    array_autori_readme.append(commit.author.name)
                    current_commit = {
                        'hash': str(commit.hash),
                        'author_name': str(commit.author.name),
                        'timestamp': str(commit.committer_date),
                        'message': str(commit.msg),
                        'number_mod_file': len(commit.modified_files),
                        'progressive_commit_number': index
                    }

                    array_commit.append(current_commit)
                elif "readme" in modified_file.filename:
                    countReadMe = countReadMe + 1
                    array_autori_readme.append(commit.author.name)
                    current_commit = {
                        'hash': str(commit.hash),
                        'author_name': str(commit.author.name),
                        'timestamp': str(commit.committer_date),
                        'message': str(commit.msg),
                        'number_mod_file': len(commit.modified_files),
                        'progressive_commit_number': index
                    }

                    array_commit.append(current_commit)
            
        dizionario['project'] = nome_progetto
        dizionario['url'] = x
        dizionario['first-commit-timestamp'] = str(array_time[0])
        dizionario['last-commit-timestamp'] = str(array_time[-1])
        dizionario['number_of_commits'] = index
        dizionario['number_of_README_commits'] = countReadMe
        dizionario['list_of_author_names'] = list(dict.fromkeys(array_autori))
        dizionario['number_of_author'] = len(list(dict.fromkeys(array_autori)))
        dizionario['number_of_author_readme'] = len(list(dict.fromkeys(array_autori_readme)))
        dizionario['manifest_commits'] = array_commit

        # print("NUMERO COMMIT", index)

        #creo file JSON
        # print(txt2.split("/")[-1] + ".json") --> prendo ultimo 
        nome_progetto_json = nome_progetto + ".json"
        diz_to_json = json.dumps(dizionario, indent = 4)

        with open(nome_progetto_json, 'w') as file:
            file.write(diz_to_json) 
            file.close()
        
        print("Close")


