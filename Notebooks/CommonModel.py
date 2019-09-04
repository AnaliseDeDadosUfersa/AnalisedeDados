from DataBase import DataBase
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split #para deixar o teste e o treinamento aleatorio
from sklearn import metrics
import pandas as pd
import numpy as np

# imports necessarios para se manipular xmls
import xml.etree.ElementTree as ET
import requests

class CommonModel:
    def __init__(self, link, positionTarget, modelSK, language = "en"):
        self.vect     = []         #Contem as colunas que não são target
        self.target   = []         #Contem a coluna target em forma de vetor
        self.totalVet = []         #contem o vetor de forma total
        self.model = modelSK       #model KNN
        self.zeroPositivo = []     #vetor que ira armazenar os testes positivos de 0
        self.umPositivo = []       #vetor que ira armazenar os testes positivos de 1
        self.columnsZero = {}      #colunas dos casos negativos
        self.columnsUm = {}        #colunas dos casos positivos  

        #variaveis de treinamento e teste
        self.x_train = []
        self.x_test  = []
        self.y_train = [] 
        self.y_test  = []

        try:
            self.__Strings = ET.parse("Xmls\\Strings_"+language+".xml").getroot()
            self.data      = DataBase(link, language) #Associação 
        except FileNotFoundError:
            print("File not found !!!")
            print("Language english defined.")
            self.__Strings = ET.parse("Xmls\\Strings_en.xml").getroot()
            self.data      = DataBase(link) #Associação 
        
        for i in range(0, len(self.data.data)):
                self.totalVet.append(list(self.data.data.iloc[i].values))
                
        self.defineTarget(positionTarget)
        
    def defineTarget(self, ind):
        self.vect   = []
        self.target = []
        temp = []
        for i in self.totalVet:
            self.target.append(int(i[ind]))
            for j in range(len(i)):
                if (j != ind):
                    temp.append(int(i[j]))
            self.vect.append(temp)
            temp = []
    
    def defineTest (self, pctTestSize):
        try:
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.vect, 
                    self.target, test_size = pctTestSize, random_state = 2) #define o treino e o teste   
        except IndexError:
            print(self.__Strings.find("CommonModel/defineTest/string[@name='s1']").text)

    def generalReport(self):
        #Mostra o resumo do modelo segundo a biblioteca sklearn.metrics
        print(self.__Strings.find("CommonModel/generalReport/string[@name='s1']").text)
        print(self.__Strings.find("CommonModel/generalReport/string[@name='s2']").text)
        print(metrics.classification_report(self.target, self.model.predict(self.vect)))
        print(self.__Strings.find("CommonModel/generalReport/string[@name='s2']").text)
        
    def matrixConfusion(self):
        print(self.__Strings.find("CommonModel/matrixConfusion/string[@name='s1']").text)
        print(self.__Strings.find("CommonModel/matrixConfusion/string[@name='s2']").text)
        for i in metrics.confusion_matrix(self.target, self.model.predict(self.vect)):
            print("       ", i)
        print(self.__Strings.find("CommonModel/matrixConfusion/string[@name='s2']").text)
        
    def subdivideEstados(self):
        #Contador de vetor
        x = 0 
        self.zeroPositivo = []
        self.umPositivo = []
        
        #Filtra os casos positivos de 0 e de 1
        for i in self.model.predict(self.vect):
            if (i == 0):
                self.zeroPositivo.append(self.vect[x])
                x += 1
            else:
                self.umPositivo.append(self.vect[x])
                x += 1
                
    def subdivideCaracteristicas(self):
        #Subdivide o vetor positivo e negativo em varios vetores de colunas
        self.columnsZero = {}
        self.columnsUm = {}
        
        for i in self.zeroPositivo:
            for j in range(len(i)):
                if i == self.zeroPositivo[0]:
                    self.columnsZero[j] = i[j:j+1]
                else:
                    self.columnsZero[j] += i[j:j+1]

        for i in self.umPositivo:
            for j in range(len(i)):
                if i == self.umPositivo[0]:
                    self.columnsUm[j] = i[j:j+1]
                else:
                    self.columnsUm[j] += i[j:j+1]
    
    def characteristicAtt(self, choice, trad):
            a = []
            b = []
                        
            t1 = len(pd.DataFrame(self.columnsUm[choice])[0].value_counts().sort_index().index)
            t2 = len(pd.DataFrame(self.columnsZero[choice])[0].value_counts().sort_index().index)
            fiUm = []
            fiZero = []
            
            if (t1 > t2):
                for i in range (t1):
                    fiUm.append(self.columnsUm[choice].count(i))
                    fiZero.append(self.columnsZero[choice].count(i))
            elif (t2 > t1):
                 for i in range (t1):
                    fiUm.append(self.columnsUm[choice].count(i))
                    fiZero.append(self.columnsZero[choice].count(i))
            else :
                for i in range (t1):
                    fiUm.append(self.columnsUm[choice].count(i))
                    fiZero.append(self.columnsZero[choice].count(i))
           
            vet    = [fiZero, fiUm]
            sum_p  = [len(self.columnsZero[choice]), len(self.columnsUm[choice])]
            total  = [d + c for d , c in zip(fiUm, fiZero)]
            
            #tem duas possiveis possições sempre
            positive_vet = vet[0]
            negative_vet = vet[1]

            positive_vet_sm = sum_p[0]
            negative_vet_sm = sum_p[1]

            """
            Test 1:

            print(positive_vet , ' =' ,positive_vet_sm)
            print(negative_vet , '=' ,negative_vet_sm)
            print('========================+')
            print(total, "\n")

            """
            for i in range(len(total)):
                a.append(self.naive(positive_vet[i]/positive_vet_sm, positive_vet_sm/len(self.data.data), total[i]/len(self.data.data)))
                b.append(self.naive(negative_vet[i]/negative_vet_sm, negative_vet_sm/len(self.data.data), total[i]/len(self.data.data)))

            """
            #test 2 : 

            print(a.index(np.array(a).max()))
            print(a,'\n')

            print(b.index(np.array(b).max()))
            print(b,'\n')
            """
            
            ##return [dados.traducao[escolha][str(a.index(np.array(a).max()))], dados.traducao[escolha][str(b.index(np.array(b).max()))]]
            return ([trad[a.index(np.array(a).max())][0], trad[b.index(np.array(b).max())][0]])
    
    def naive(self, pae, pe, pa):
        return((pae * pe)/pa) 