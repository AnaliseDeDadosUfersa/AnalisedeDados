#### import pandas as pd
from functools import reduce
import math as mt
import matplotlib.pyplot as plot
import pandas as pd

# imports necessarios para se manipular xmls
import xml.etree.ElementTree as ET
import requests

class DataBase:
    def __init__ (self, link, language = "en"):
        try:
            self.data = pd.read_csv(link)                 #Aqui é onde esta os dados principais
            self.entropia = 0                             #Aqui estará a entropia do target
            self.header = list(self.data.keys())          #Aqui estará a lista de cabeçarios
            self.Translation = []                         #Aqui estará a lista de dicionario de traduçoes
            for i in range(len(self.header)):
                self.Translation.append(list(self.data[self.header[i]].value_counts().sort_index().keys())) #prenche a traducao com os elementos contidos na coluna
            try:
                self.__Strings = ET.parse("Xmls\\Strings_"+language+".xml").getroot()
            except FileNotFoundError:
                print("File not found !!!")
                print("Language english defined.")
                self.__Strings = ET.parse("Xmls\\Strings_en.xml").getroot()
        except:
            stri = ET.parse("Xmls\\Strings_en.xml").getroot()
            print(stri.find("DataBase/init/string[@name='s1']").text)#para qualquer erro causado ao carregar o arquivo o objeto não sera
                                                       #criado.
            
    def modifyString(self, palavra):
        #Esta função altera a string passada, retirando pontos, 
        #virgulas e barras e substituindo por espaços em brancos.
        temp = ""
        for i in str(palavra):
            if i.isalpha() or i.isnumeric() or i.isspace():
                temp += i
            else:
                temp += " "
        return temp
            
    def modifyData(self, dicionario, ind):
        #Este metodo recebe uma lista de dicionarios e altera os dados substituindo os dados presentes nele
        #pelos dados passados.
        
        #Utilizando um dicionario a função irá comparar se o dado de certo indice na coluna condiz com a chave do dicionario
        #em caso afirmativo o valor da chave sera atribuida a uma lista de valores no exato indice em que o dado indica.
        #O dicionario basicamente serve como um conversor.
        #Exemplo: 
        #    Supondo os seguintes dados em lista [maça, abacaxi, banana]. 
        #    O seguinte dicionario; {maça:maça-verde, Default: fruta}
        #    A saida da função será uma nova lista da seguinte ordem: [maça-verde, fruta, fruta] 
        
        #Os parametros estão relacionados aos Atributos filtros, basicamente se for encontrado um atributos Filtro dentro de 
        #dados sera atribuido o parametro do mesmo idice. O ultimo elemento do filtro é o elemento default, se todos falharem ele
        #sera atribuido.
        
        #Armazena os valores das chaves e as chaves em duas listas diferentes
        list_values = list(dicionario.values())
        keys        = list(dicionario.keys())
        
        for j in ind:                                   #Para cada indice passado, este indice se refere a coluna em numeros.
            for l in range(0, len(list_values)):        #Para cada lista de valores dentro da lista de valores
                for i in range(0, len(list_values[l])): #Para cada valor dentro da lista
                    for k in self.data[self.header[j]]: #Para cada valor dentro da lista de valores da coluna
                        if self.modifyString(list_values[l][i]).upper() in self.modifyString(k).upper():
                            self.data[self.header[j]] = self.data[self.header[j]].apply(lambda x: str(x).replace( str(k), keys[l]))
                if (l == len(list_values) - 1):
                    for k in self.data[self.header[j]]:
                        if k not in keys:
                            print(k)
                            self.data[self.header[j]] = self.data[self.header[j]].apply(lambda x: str(x).replace( str(k), keys[l]))
        #Altera a lista de tradução
        for i in ind:
            self.Translation[i] = self.convertDict(dicionario)
                        
    def modifyHeaderInd(self, list_header, ind):
        #Este metódo ira alterar os cabeçarios mardos pelo indice ind.
        temp = list(self.data.columns)
        for i in range(0, len(ind)):
            temp.remove(self.data.columns[i])
            temp.insert(i, list_header[i])
        #altera as colunas somente se o tamanho da nova lista for igual ao tamanho da lista anterior
        if len(temp) == len(self.data.columns):
            self.data.columns = temp
        else: 
            print(self.__Strings.find("DataBase/modifyHeader/string[@name='s1']").text)
            
    def modifyHeader(self, list_header):
        #altera as colunas somente se o tamanho da nova lista for igual ao tamanho da lista anterior
        if len(list_header) == len(self.data.columns):
            self.data.columns = list_header
        else: 
            return(self.__Strings.find("DataBase/modifyHeader/string[@name='s1']").text)
        self.header = list(self.data.keys())
    
    def restartTranslater(self):
        self.Translation = []
        for i in range(len(self.header)):
                self.Translation.append(list(self.data[self.header[i]].value_counts().sort_index().keys())) #prenche a traducao com os elementos contidos na coluna

    def dropColumn(self, ind):
        #Tira as colunas indicadas pela lista ind
        clone = self.data
        clonec = []
        clonec.extend(self.Translation)
        
        k = 0
        tamt = len(self.Translation)
        temp = 0
        for i in ind:
            clone = clone.drop(self.data.keys()[i], axis = 1)
            
            clonet = []
            
            #Verifica a ordem dos numeros para definir se deve-se subtrair ou não
            if temp > i:
                k = i
            else:
                k += i
            
            for j in range(len(clonec)):
                if j != k:
                    clonet.append(clonec[j])
            k = len(clonet) - tamt
            clonec = clonet
            temp = i
        msg = input(self.__Strings.find("DataBase/dropColumn/string[@name='s1']").text)
        if(msg.upper() == "Y"):
            self.data = clone
            self.Translation = clonec
            self.header = list(self.data.keys())
        else: 
            print(self.__Strings.find("DataBase/dropColumn/string[@name='s2']").text)
            
    def dropLines(self, ind):
        #Tira as linhas indicadas pela lista ind
        clone = self.data
        for i in ind:
            clone = clone.drop(i, axis = 0)
        msg = input(self.__Strings.find("DataBase/dropLines/string[@name='s1']").text)
        if(msg.upper() == "Y"):
            self.data = clone
        else: 
            print(self.__Strings.find("DataBase/dropLines/string[@name='s2']").text)
    
    def showGraphic(self, i):
        fig, ax = plot.subplots(figsize=(8, 5), subplot_kw=dict(aspect="equal"))
        
        a, b, c = ax.pie(self.data[self.header[i]].value_counts().sort_index().values, 
                           labels = self.data[self.header[i]].value_counts().sort_index().index, 
                           autopct = '%1.1f%%', labeldistance = 1.2, pctdistance = 0.8)
        
        alt = 0
        if len(self.Translation[i]) > 6:
            alt = -0.6
        else:
            alt = -0.3
        ax.legend(self.Translation[i], title= self.__Strings.find("DataBase/Legend/string[@name='s1']").text, loc= 8, bbox_to_anchor=(0, alt, 1, 0), ncol = 3)
        plot.setp(c, size=8, weight="bold")
        ax.set_title(self.header[i])
        plot.show()
        
    def showGraphict(self, i, j):
        fig, ax = plot.subplots(ncols = 2, figsize=(16, 4), subplot_kw=dict(aspect="equal"))
        
        a, b, c = ax[0].pie(self.data[self.header[i]].value_counts().sort_index().values, 
                           labels = self.data[self.header[i]].value_counts().sort_index().index, 
                           autopct = '%1.1f%%', labeldistance = 1.2, pctdistance = 0.8)
        
        d, f, g = ax[1].pie(self.data[self.header[j]].value_counts().sort_index().values, 
                           labels = self.data[self.header[j]].value_counts().sort_index().index, 
                           autopct = '%1.1f%%', labeldistance = 1.2, pctdistance = 0.8)
        
        ax[0].legend(self.Translation[i], title = (self.header[i]) ,  loc= 8 , bbox_to_anchor=(0, -0.3, 1, 0), ncol = 2)
        ax[1].legend(self.Translation[j], title = (self.header[j]) ,  loc= 8 , bbox_to_anchor=(0, -0.3, 1, 0), ncol = 2)
        
        plot.setp(c, size=8, weight="bold")
        plot.setp(g, size=8, weight="bold")
        
        ax[0].set_title(self.header[i])
        ax[1].set_title(self.header[j])
        
        plot.show()
    
    def showGraphicCompare(self, ind, list2, lab2, leg2):
        fig, ax = plot.subplots(ncols = 2, figsize=(16, 4), subplot_kw=dict(aspect="equal"))
        
        a, b, c = ax[0].pie(list2, labels = lab2, autopct = '%1.1f%%', labeldistance = 1.2, pctdistance = 0.8)
        
        d, f, g = ax[1].pie(self.data[self.header[ind]].value_counts().sort_index().values, 
                           labels = self.data[self.header[ind]].value_counts().sort_index().index, 
                           autopct = '%1.1f%%', labeldistance = 1.2, pctdistance = 0.8)
        alt1 = 0
        alt2 = 0

        if len(self.Translation[ind]) > 6:
            alt1 = -0.6
        else:
            alt1 = -0.3
            
        if len(leg2) > 6:
            alt2 = -0.6
        else:
            alt2 = -0.3
        
        ax[0].legend(leg2, title = self.__Strings.find("DataBase/Legend/string[@name='s1']").text ,  loc= 8 , bbox_to_anchor=(0, alt2, 1, 0), ncol = 2)
        ax[1].legend(self.Translation[ind], title = self.__Strings.find("DataBase/Legend/string[@name='s1']").text ,  loc= 8 , bbox_to_anchor=(0, alt1, 1, 0), ncol = 2)
        
        
        plot.setp(c, size=8, weight="bold")
        plot.setp(g, size=8, weight="bold")
        
        ax[0].set_title(self.header[ind]) 
        ax[1].set_title(self.header[ind])
 
        plot.show()
    
    def saveCsv(self, nome):
        try:
            self.data.to_csv(nome , sep = ',', index=False, encoding = 'utf-8', quotechar = '"', line_terminator = '\r\n')
        except:
            print(self.__Strings.find("DataBase/saveCsv/string[@name='s1']").text)
            
    def relationshipTable(self, ncoluna):
        tabel = {}
        l1 = list(self.data[self.header[0]].values)
        l2 = list(self.data[self.header[ncoluna]].values)
        
        qtl1 = list(self.data[self.header[0]].value_counts().sort_index().keys())
        qtl2 = list(self.data[self.header[ncoluna]].value_counts().sort_index().keys())
        
        ls = []
        
        for j in qtl1:
            ls = []
            for k in qtl2:
                temp = 0
                for i in range(0, len(l2)):
                    if l1[i] == j and l2[i] == k:
                        temp += 1
                ls.append(temp)
            tabel[j] = ls
            
        return tabel
    
    def relationshipTablein(self, xcoluna, ncoluna):
        tabela = {}
        l1 = list(self.data[self.header[xcoluna]].values)
        l2 = list(self.data[self.header[ncoluna]].values)
        
        qtl1 = list(self.data[self.header[xcoluna]].value_counts().sort_index().keys())
        qtl2 = list(self.data[self.header[ncoluna]].value_counts().sort_index().keys())
        
        ls = []
        
        for j in qtl1:
            ls = []
            for k in qtl2:
                temp = 0
                for i in range(0, len(l2)):
                    if l1[i] == j and l2[i] == k:
                        temp += 1
                ls.append(temp)
            tabela[j] = ls
            
        return tabela
    
    def gainInformation(self, ncoluna):
        #Rever esse calculo pois o valor deveria ser entre 0 e 1 nao esta batendo
        entropiaR = self.entropia
        valores = list(self.relationshipTable(ncoluna).values())
        soma = 0
        sm = []
        for i in valores:
            for j in i:
                soma += j
            
        for j in range(0, len(valores[0])):
            a = 0
            while(a < len(valores)):
                sm.append(valores[a][j])
                a += 1
            b = reduce(lambda x, y: x + y, sm)
            entropiaR -= (b / soma) * self.entropiaS(sm, soma)
            sm = []
        return entropiaR
    
    def setEntropia(self, ncoluna):
        #Define a entropia do sistema
        #Deve ser a entropia da coluna target
        self.entropia = self.entropiaS(self.data[self.header[ncoluna]].value_counts().values, len(self.data))
    
    def entropiaS(self, data, qt):
        #Rever esse calculo pois o valor deveria ser entre 0 e 1 nao esta batendo
        entropiaR = 0
        valores = data
        for j in valores:
            try:
                entropiaR -= (int(j) / qt) * mt.log2((int(j) / qt))
            except:
                entropiaR -= (int(j) / qt) * 0
        return entropiaR
    
    def convertDict(self, dicionario):
        listak = []
        for j in list(dicionario.values()):
            if len(j) > 1:
                listak.append(reduce(lambda x, y: x + " - " + y, j))
            else:
                listak.append(j[0])
        return listak

    
    def pdRelation(self, coluna, linha):
        dat = pd.DataFrame(self.relationshipTablein(coluna,linha))

        dat.index   = self.Translation[linha]
        dat.columns = self.Translation[coluna]
        return dat.sort_index()