import json 
import csv
import os 
import shutil
import sys

#TRACCIA = File che deve essere lanciato dopo Analisi.py, se venisse lanciato prima, non andrebbe in esecuzione.
#In Valutazione dati tutti i file JSON crea un unico file CSV, che contiene alcune informazioni
#riguardanti i progetti.

#creo lista per salvare i dizionari con le informazioni che mi servono
lista = [] 

#Variabile di controllo per andare a verificare se il programma possa essere lanciato o meno
controllo = False

for percorso in os.listdir():
    elemento = str(percorso)
    if "JSON" in elemento:
        print("CIAOOOOOO")
        if os.path.exists(elemento):
            print("SONO DENTRO A PRIMO IF")
            os.chdir(elemento)
            controllo = True
        else:
            controllo = False

#Blocco programma se non esiste il file JSON_files
if controllo:
    pass
else:
    print("Non posso lanciare il programma poichè non è presenta la cartella JSON_files")
    sys.exit()

#Dopo aver settato la cartella JSON_file come principale vado a leggere tutti i file JSON che ci sono
#e salvo in un dizionario che successivamente viene aggiunto ad una lista.
for json_file in os.listdir():
    if "json" in json_file:
        #apro file
        with open(json_file, 'r') as file:
            data = json.load(file)
            currentDiz = {
                "Project": data['project'],
                "Num_commits": data['number_of_commits'],
                "Num_commits_README": data['number_of_README_commits']
            }

            lista.append(currentDiz)
            
#Esco dalla cartella JSON_file perchè non voglio inserire i file CSV dentro alla stessa cartella dei file JSON
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)


#Creo cartella CSV_file per tutti il file CSV contenente tutti le informazioni dai file JSON
name_folder = "CSV_file"
if os.path.exists(name_folder):
    shutil.rmtree(name_folder)
os.makedirs(name_folder)

#Setto la cartella CSV_file come principale, cosi che il file prodotto venga inserito direttamente in essa
os.chdir(name_folder)


#Scrivo file output.csv
with open('output.csv', 'w') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Project', 'Num_tot_commits', 'Num_commits_readme'])
    for x in lista:
        values = list(x.values())
        # print(values)
        csv_writer.writerow(values)


#Controllo che esista per dare un messaggio di verifica
if os.path.exists('output.csv'):
    print("File creato con successo")
else:
    print("File NON creato con successo")
        

