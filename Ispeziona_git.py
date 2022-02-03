from array import array
import json
from operator import le 
import os
from re import A 
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import numpy as np
import statistics as stats
from matplotlib.backends.backend_pdf import PdfPages


def numOfDays(date1, date2):
    return abs((date2-date1).days)

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '({v:d})'.format(v=val)
    return my_autopct

#Metodo per creare pie chart
def returnTuple(lista_iniziale):
    lista = []
    lista_finale = []
    var1,var2,var3,var4,var5 = 0,0,0,0,0
    for x in lista_iniziale:
        if x != 0:
            lista.append(x)

    for x in lista:
        if (x < 21):
            var1 = var1 + 1
        if(x > 20 and x < 41):
            var2 = var2 + 1
        if(x > 40 and x < 61):
            var3 = var3 + 1
        if(x > 60 and x < 81):
            var4 = var4 + 1
        if(x > 80 and x < 101):
            var5 = var5 + 1
    
    lista_finale.append(var1)
    lista_finale.append(var2)
    lista_finale.append(var3)
    lista_finale.append(var4)
    lista_finale.append(var5)

    len1 = len(lista)

    return lista_finale, len1


def inspection(folder_name, strategy_name):

    count = 0
    count1 = 0
    lista_Num_commit = []
    lista_Num_commit_real = []
    lista_count_commit = []
    g1_asseX = ['1-20 commit', '21-40 commit','41-60 commit','61-80 commit','81-100 commit','100+ commit']
    var = 0
    var1 = 0
    var2 = 0
    var3 = 0
    var4 = 0
    var5 = 0

    lista_numAutori_readme = []
    lista_numAutori_readme_real = []
    count_A = 0
    count_A1 = 0
    count_A2 = 0
    count_A3 = 0
    count_A4 = 0
    count_A5 = 0
    lista_count_autori = []
    g2_asseX = ['1 authors', '2-5 authors', '6-10 authors','11-20 authors','20-100 authors', '100+ authors']

    array_percentuale_autori_README = []
    array_percentuale_autori_README_real = []
    g2_lab = [0,10,20,30,40,50,60,70,80,90,100]
    percentuale = 0


    g3_lab = ['1-20 %','21-40 %','41-60 %','61-80 %','81-100 %']
    count_perc = 0
    count_perc1 = 0
    count_perc2 = 0
    count_perc3 = 0
    count_perc4 = 0
    array_count_PERC = []

    indice = 0
    array_media = []
    g4_asseX = [0,10,20,30,40,50,60,70,80,90,100]
    array_mediana = []

    array_all_commits = []
    array_com_count = []
    fasce_all_commits = ['1-10 000 Nc', '10 001-20 000 Nc', '20 001-30 000 Nc', '30 001- 40 000 Nc','40 000 + Nc']
    count_commit = 0
    count_commit1 = 0
    count_commit2 = 0
    count_commit3 = 0
    count_commit4 = 0

    percentuale1 = 0
    array_perc_aut = [] 

    percentuale2 = 0
    array_perc_aut1 = []

    percentuale3 = 0
    array_perc_aut2 = []


    lista_min_giorni = []
    lista_max_giorni = []

    if os.path.isdir(folder_name):
        print("La cartella", folder_name, "esiste")
        os.chdir(folder_name)

        for x in os.listdir():
            count = count + 1
            first_tms = 0
            last_tms = 0
            media = 0
            mediana = 0

            valore_max = 0
            valore_min = 0

            lista_giorni = []

            if ".json" in x:

                with open(x, 'r') as f:
                    data = json.load(f)
                    count1 = count1 + 1

                    lista_Num_commit.append(data['number_of_README_commits'])
                    lista_numAutori_readme.append(data['number_of_author_readme'])

                    if data['number_of_commits'] > 0:
                        array_all_commits.append(data['number_of_commits'])

                    if data['number_of_authors'] > 1:
                        percentuale = int((data['number_of_author_readme'] / data['number_of_authors']) * 100)
                        array_percentuale_autori_README.append(percentuale)
                    if data['number_of_authors'] > 1 and data['number_of_authors'] < 101:
                        percentuale1 = int((data['number_of_author_readme'] / data['number_of_authors']) * 100)
                        array_perc_aut.append(percentuale1)
                    if data['number_of_authors'] > 100 and data['number_of_authors'] < 501:
                        percentuale2 = int((data['number_of_author_readme'] / data['number_of_authors']) * 100)
                        array_perc_aut1.append(percentuale2)
                    if data['number_of_authors'] > 500 and data['number_of_authors'] < 1001:
                        percentuale3 = int((data['number_of_author_readme'] / data['number_of_authors']) * 100)
                        array_perc_aut2.append(percentuale3)
                    
                    if len(data['README_commits']) != 0:
                        #IMP = [0:10] e formato diverso, perchè le ore davano problemi col conteggio dei giorni
                        #ora la data non è cambiata, ma cambia solo orario che è fisso a mezzanotte e zero minuti e zero secondi
                        first_tms = datetime.strptime(data['first-commit-timestamp'][0:10], '%Y-%m-%d')
                        last_tms = datetime.strptime(data['last-commit-timestamp'][0:10], '%Y-%m-%d')
                        diff = numOfDays(first_tms, last_tms)
                        if diff != 0:
                            indice = indice + 1
                            for y in data['README_commits']:
                                cast_dateT = datetime.strptime(y['timestamp'][0:10], '%Y-%m-%d')
                                if(strategy_name == "before"):
                                    sottr = numOfDays(first_tms, cast_dateT)
                                    lista_giorni.append(sottr)
                                if(strategy_name == "after"):
                                    sottr1 = numOfDays(last_tms, cast_dateT)
                                    lista_giorni.append(sottr1)
                                if(strategy_name == "nearest"):
                                    sottr2 = numOfDays(first_tms, cast_dateT)
                                    sottr3 = numOfDays(last_tms, cast_dateT)
                                    val_min = min(sottr2, sottr3)
                                    lista_giorni.append(val_min)

        
                                                        
                            if lista_giorni:
                                media = int(np.average(lista_giorni))
                                mediana = stats.median(lista_giorni)
                                valore_min = min(lista_giorni)
                                valore_max = max(lista_giorni)
                            
                            percentuale = int((media / diff ) * 100)
                            if percentuale != 0:
                                array_media.append(percentuale) 

                            percentuale1 = int((mediana / diff) * 100)
                            if percentuale1 != 0:
                                array_mediana.append(percentuale1)

                            percentuale_min_giorno = (valore_min / diff) * 100
                            lista_min_giorni.append(percentuale_min_giorno)
   
                         
                            percentuale_max_giorno = int((valore_max / diff) * 100)
                            if percentuale_max_giorno != 0:
                                lista_max_giorni.append(percentuale_max_giorno)
            else:
                print("File che scarto")
            
        
        print("Numero di progetti che devono essere analizzati", indice)

        for x in lista_Num_commit:
            if x != 0:
                lista_Num_commit_real.append(x)

        ################################################################################################################################################################
        #GRAFICO N1 = pie chart in cui creo 6 classi per mostrare il numero di commit README
        for x in lista_Num_commit_real:
            if(x <= 20):
                var = var + 1
            if(x > 20 and x < 41):
                var1 = var1 + 1
            if(x > 40 and x < 61):
                var2 = var2 + 1
            if(x > 60 and x < 81):
                var3 = var3 + 1
            if(x > 80 and x < 101):
                var4 = var4 + 1
            if(x > 100):
                var5 = var5 +1 

        lista_count_commit.append(var)
        lista_count_commit.append(var1)
        lista_count_commit.append(var2)
        lista_count_commit.append(var3)
        lista_count_commit.append(var4)
        lista_count_commit.append(var5)

        fig1, ax1 = plt.subplots() 
        ax1.pie(lista_count_commit, labels = g1_asseX, radius = 1, autopct = '%0.0f%%')
        ax1.axis("equal")
        convert_len_to_str = str(len(lista_Num_commit_real))
        ax1.set_title("Pie chart about number of COMMIT who modified README about " + convert_len_to_str + " repository", fontsize = 9)
        ################################################################################################################################################################
        #GRAFICO N2 = pie chart in cui creo 5 classi per mostrare il numero di autori che modificano il README
        for x in lista_numAutori_readme:
            if x != 0:
                lista_numAutori_readme_real.append(x)
        
        for x in lista_numAutori_readme_real:
            if(x == 1):
                count_A = count_A + 1
            if(x > 1 and x < 6):
                count_A1 = count_A1 + 1
            if(x > 5 and x < 11):
                count_A2 = count_A2 + 1
            if(x > 10 and x < 21):
                count_A3 = count_A3 + 1
            if(x > 20 and x < 101):
                count_A4 = count_A4 + 1
            if(x > 100):
                count_A5 = count_A5 + 1

        lista_count_autori.append(count_A)
        lista_count_autori.append(count_A1)
        lista_count_autori.append(count_A2)
        lista_count_autori.append(count_A3)
        lista_count_autori.append(count_A4)
        lista_count_autori.append(count_A5)

        fig2, ax2 = plt.subplots() 
        ax2.pie(lista_count_autori, labels = g2_asseX, radius = 1, autopct = '%0.0f%%')
        ax2.axis("equal")
        convert_len_to_str1 = str(len(lista_numAutori_readme_real))
        ax2.set_title("Pie chart about number of AUTHOR who modified README about " + convert_len_to_str1 + " repository", fontsize = 9)

        fig9, ax9 = plt.subplots() 
        ax9.pie(lista_count_autori, labels = g2_asseX, radius = 1, autopct = make_autopct(lista_count_autori))
        ax9.axis("equal")
        ax9.set_title("Pie chart about number of AUTHOR who modified README about " + convert_len_to_str1 + " repository", fontsize = 9)
        ################################################################################################################################################################
        #GRAFICO N3 = histogram dove grafico le percentuali autori cioè A / B * 100 --> (num_autori_readme / num_autori_totali) * 100
        for x in array_percentuale_autori_README:
            if x != 0:
                array_percentuale_autori_README_real.append(x)
        
        fig3, ax3 = plt.subplots()
        ax3.hist(array_percentuale_autori_README_real, g2_lab, rwidth = 0.8, color = "skyblue")
        ax3.set_xticks(g2_lab, minor = False)
        ax3.set_xlabel("Percentages %")
        ax3.set_ylabel("Number of repository")
        len_stringa = str(len(array_percentuale_autori_README_real))
        ax3.set_title("Histogram compare between number_of_author_readme / number_of_authors on " + len_stringa + " repository", fontsize = 9)
        ################################################################################################################################################################
        #GRAFICO N4 = pie chart suddividendo le percentuali degli autori e dando però su grafico non le percentuali, ma quante volte si ripetono
        for x in array_percentuale_autori_README_real:
            if (x < 21):
                count_perc = count_perc + 1
            if(x > 20 and x < 41):
                count_perc1 = count_perc1 + 1
            if(x > 40 and x < 61):
                count_perc2 = count_perc2 + 1
            if(x > 60 and x < 81):
                count_perc3 = count_perc3 + 1
            if(x > 80 and x < 101):
                count_perc4 = count_perc4 + 1
            

        array_count_PERC.append(count_perc)
        array_count_PERC.append(count_perc1)
        array_count_PERC.append(count_perc2)
        array_count_PERC.append(count_perc3)
        array_count_PERC.append(count_perc4)

        fig4, ax4 = plt.subplots() 
        ax4.pie(array_count_PERC, labels = g3_lab, radius = 1, autopct = make_autopct(array_count_PERC))
        ax4.axis("equal")
        convert_len_to_str10 = str(len(array_percentuale_autori_README_real))
        ax4.set_title("Pie chart about partition of percentage on author who modified README " + convert_len_to_str10 + " repository", fontsize = 9)
        ################################################################################################################################################################
        #ANALISI TEMPORALE --> GRAFICO MEDIA
        fig5, ax5 = plt.subplots()
        ax5.hist(array_media, g4_asseX, rwidth = 0.8, color = "black")
        ax5.set_xticks(g4_asseX, minor = False)
        ax5.set_xlabel("Percentages %")
        ax5.set_ylabel("Number of repository")
        len_stringa10 = str(len(array_media))
        ax5.set_title("Histogram about result of percentage about average on " + len_stringa10 + " repository", fontsize = 9)
        ################################################################################################################################################################
        #GRAFICO MEDIA PLOT NORMALE
        array_media.sort()

        fig13, ax13 = plt.subplots()
        ax13.plot(array_media)
        ax13.set_xlabel("Len list of values %") #DUBBIO è giusta l'etichetta?
        ax13.set_ylabel("Percentages %")
        ax13.set_title("PLOT about result of percentage about average on " + len_stringa10 + " repository", fontsize = 9)
        ################################################################################################################################################################
        #GRAFICO HIST E PLOT OF MIN DAYS PERCENTAGES
        fig14, ax14 = plt.subplots()
        ax14.hist(lista_min_giorni, g4_asseX, rwidth = 0.8, color = "purple")
        ax14.set_xticks(g4_asseX, minor = False)
        ax14.set_xlabel("Percentages %")
        ax14.set_ylabel("Number of repository")
        len_stringa_100 = str(len(lista_min_giorni))
        ax14.set_title("Histogram about result of percentage of minor value days on " + len_stringa_100 + " repository", fontsize = 9)

        lista_min_giorni.sort()

        fig15, ax15 = plt.subplots()
        ax15.plot(lista_min_giorni)
        ax15.set_xlabel("Len list of values %")
        ax15.set_ylabel("Percentages %")
        ax15.set_title("PLOT about result of percentage about percentage on minimum days on " + len_stringa_100 + " repository", fontsize = 9)
        ################################################################################################################################################################
        #GRAFICO HIST E PLOT OF MAX DAYS PERCENTAGES
        fig16, ax16 = plt.subplots()
        ax16.hist(lista_max_giorni, g4_asseX, rwidth = 0.8, color = "orange")
        ax16.set_xticks(g4_asseX, minor = False)
        ax16.set_xlabel("Percentages %")
        ax16.set_ylabel("Number of repository")
        len_stringa_101 = str(len(lista_max_giorni))
        ax16.set_title("Histogram about result of percentage of max value days on " + len_stringa_101 + " repository", fontsize = 9)


        lista_max_giorni.sort()

        fig17, ax17 = plt.subplots()
        ax17.plot(lista_max_giorni)
        ax17.set_xlabel("Len list of values %")
        ax17.set_ylabel("Percentages %")
        ax17.set_title("PLOT about result of percentage about percentage on max days on " + len_stringa_101 + " repository", fontsize = 9)
        ################################################################################################################################################################
        #GRAFICO MEDIANA
        fig6, ax6 = plt.subplots()
        ax6.hist(array_mediana, g4_asseX, rwidth = 0.8, color = "red")
        ax6.set_xticks(g4_asseX, minor = False)
        ax6.set_xlabel("Percentages %")
        ax6.set_ylabel("Number of repository")
        len_stringa11 = str(len(array_mediana))
        ax6.set_title("Histogram about result of percentage about median on " + len_stringa11 + " repository", fontsize = 9)
        ################################################################################################################################################################
        #GRAFICO 7 = pie chart sui numeri commit
        for x in array_all_commits:
            if (x < 10001):
                count_commit = count_commit + 1
            if(x > 10000 and x < 20001):
                count_commit1 = count_commit1 + 1
            if(x > 20000 and x < 30001):
                count_commit2 = count_commit2 + 1
            if(x > 30000 and x < 40001):
                count_commit3 = count_commit3 + 1
            if(x > 40000):
                count_commit4 = count_commit4 + 1
        

        array_com_count.append(count_commit)
        array_com_count.append(count_commit1)
        array_com_count.append(count_commit2)
        array_com_count.append(count_commit3)
        array_com_count.append(count_commit4)

        fig7, ax7 = plt.subplots() 
        ax7.pie(array_com_count, labels = fasce_all_commits, radius = 1, autopct = '%0.0f%%')
        ax7.axis("equal")
        convert_len_to_str30 = str(len(array_all_commits))
        ax7.set_title("Pie chart about number of commits for all " + convert_len_to_str30 + " repository", fontsize = 9)
        ################################################################################################################################################################
        fig8, ax8 = plt.subplots() 
        ax8.pie(array_com_count, labels = fasce_all_commits, radius = 1, autopct = make_autopct(array_com_count))
        ax8.axis("equal")
        convert_len_to_str40 = str(len(array_all_commits))
        ax8.set_title("Pie chart about number of commits for all " + convert_len_to_str40 + " repository", fontsize = 9)
        ################################################################################################################################################################
        #GRAFICO UGUALE A FIG4 ma con 1 < x < 101 authors
        lista_tupla, len_tupla = returnTuple(array_perc_aut)
        fig10, ax10 = plt.subplots() 
        ax10.pie(lista_tupla, labels = g3_lab, radius = 1, autopct = make_autopct(lista_tupla))
        ax10.axis("equal")
        convert_len_to_str50 = str(len_tupla)
        ax10.set_title("Pie chart of percentage on " + convert_len_to_str50 + " repository who have a Num of authors between 1 and 100", fontsize = 9)
        ################################################################################################################################################################
        #GRAFICO UGUALE A FIG4 ma con 100 < x < 500 authors
        lista_tupla1, len_tupla1 = returnTuple(array_perc_aut1)
        fig11, ax11 = plt.subplots() 
        ax11.pie(lista_tupla1, labels = g3_lab, radius = 1, autopct = make_autopct(lista_tupla1))
        ax11.axis("equal")
        convert_len_to_str60 = str(len_tupla1)
        ax11.set_title("Pie chart of percentage on " + convert_len_to_str60 + " repository who have a Num of authors between 100 and 500", fontsize = 9)
        ################################################################################################################################################################
        #GRAFICO UGUALE A FIG4 ma con 500 < x < 1000 authors
        listaMetodo, lunghezzaLista = returnTuple(array_perc_aut2)
        fig12, ax12 = plt.subplots() 
        ax12.pie(listaMetodo, labels = g3_lab, radius = 1, autopct = make_autopct(listaMetodo))
        ax12.axis("equal")
        convert_len_to_str_10 = str(lunghezzaLista)
        ax12.set_title("Pie chart of percentage on " + convert_len_to_str_10 + " repository who have a Num of authors between 500 and 1000", fontsize = 9)
        ################################################################################################################################################################
        fig18, ax18 = plt.subplots()
        array_mediana.sort()
        ax18.plot(array_mediana)
        ax18.set_xlabel("Len list of values %") 
        ax18.set_ylabel("Percentages %")
        convert_len = str(len(array_mediana))
        ax18.set_title("PLOT about result of percentage about median on " + convert_len + " repository", fontsize = 9)
        ################################################################################################################################################################

        scanner_pdf = PdfPages('GRAFICI.pdf')
        scanner_pdf.savefig(fig7)
        scanner_pdf.savefig(fig8)
        scanner_pdf.savefig(fig1)
        scanner_pdf.savefig(fig2)
        scanner_pdf.savefig(fig9)
        scanner_pdf.savefig(fig4) 
        scanner_pdf.savefig(fig10)
        scanner_pdf.savefig(fig11)
        scanner_pdf.savefig(fig12)

        scanner_pdf.savefig(fig3)
        scanner_pdf.savefig(fig5)
        scanner_pdf.savefig(fig13)
        scanner_pdf.savefig(fig14)
        scanner_pdf.savefig(fig15)
        scanner_pdf.savefig(fig16)
        scanner_pdf.savefig(fig17)

        scanner_pdf.savefig(fig6)
        scanner_pdf.savefig(fig18)
        scanner_pdf.close()
        
        plt.show()

    else:
        print("La cartella non esiste")
        sys.exit()
################################################################################################################################################################
if(len(sys.argv) == 4 or len(sys.argv) > 4):
    print("Mi dispiace, ma hai inserito troppi valori di riga di comando")
    sys.exit()

if(len(sys.argv) < 3 ):
    print("Il campo non è stato passato da riga di comando, di conseguenza viene attiva la modalità interattiva")
    x = input("Inserire nome della cartella che contiene i file JSON: ")
    y = input("Inserire la strategia con cui si vuole fare l'analisi temporale before || after || nearest -->: ")
    if(y == "before" or y == "after" or y == "nearest"): 
        inspection(x,y)
    else:
        print("La strategia che hai inserito non rispetta quelle possibili, di conseguenza non è possibile eseguire il programma")
        sys.exit()
else:
    print("Valori inseriti correttamente per avviare l'esecuzione del programma")
    if(sys.argv[2] == "before" or sys.argv[2] == "after" or sys.argv[2] == "nearest"): 
        inspection(sys.argv[1], sys.argv[2])
    else:
        print("La strategia che hai inserito non rispetta quelle possibili, di conseguenza non è possibile eseguire il programma")
        sys.exit()