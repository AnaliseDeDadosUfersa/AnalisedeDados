from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import ComplementNB
from sklearn.model_selection import train_test_split #para deixar o teste e o treinamento aleatorio
from sklearn.metrics import accuracy_score
from sklearn import metrics
from CommonModel import CommonModel
import pandas as pd
import numpy as np

# imports necessarios para se manipular xmls
import xml.etree.ElementTree as ET
import requests

class ModelNaive(CommonModel):
        def __init__(self, link, positionTarget, language = "en"):
            try:
                self.__Strings = ET.parse("Xmls\\Strings_"+language+".xml").getroot()
                super().__init__(link, positionTarget, GaussianNB(), language)
            except FileNotFoundError:
                print("File not found !!!")
                print("Language english defined.")
                self.__Strings = ET.parse("Xmls\\Strings_en.xml").getroot()
                super().__init__(link, positionTarget, GaussianNB(), "en")

        def defineModel(self, choice):
            #instancia um dos 4 modelos de naive bayes definidos pelo sklearn
            if(choice == 1):
                self.model = GaussianNB()
            elif(choice == 2):
                self.model = BernoulliNB(binarize = True)
            elif(choice == 3):
                self.model = MultinomialNB()
            elif(choice == 4):
                self.model = ComplementNB()
            else:
                print(self.__Strings.find("ModelNB/defineModel/string[@name='s1']").text)
        
        def allModel(self):
            #instancia os 4 modelos de naive bayes definidos pelo sklearn
            model1 = GaussianNB()
            model2 = BernoulliNB(binarize = True)
            model3 = MultinomialNB()
            model4 = ComplementNB()
            self.model = [model1, model2, model3, model4]
        
        def trainModel(self, pctTestSize):
            try:
                self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.vect, self.target, test_size = pctTestSize, random_state = 2) #define o treino e o teste   
            except:
                print(self.__Strings.find("ModelNB/trainModel/string[@name='s1']").text)
            if(len(self.model) == 4):
                #treino do modelo
                    for i in range(len(self.model)):
                        self.model[i].fit(self.x_train, self.y_train)
                        print(self.model[i])
            else:
                self.model.fit(self.x_train, self.y_train)
                
        def errorModel(self):
            if (len(self.model) == 4):
                for i in range(len(self.model)):
                    print(type(self.model[i]))
                    print(self.__Strings.find("ModelNB/errorModel/string[@name='s1']").text, (self.model[i].predict(self.x_test) != self.y_test).sum())
            else:
                print(type(self.model))
                print(self.__Strings.find("ModelNB/errorModel/string[@name='s1']").text, (self.model.predict(self.x_test) != self.y_test).sum()) 
                
        def errorModelInd(self, begin, end):
                if(len(self.model) == 4):
                    for i in range(len(self.model)):
                        print(self.__Strings.find("ModelNB/errorModelInd/string[@name='s1']").text, i, self.__Strings.find("ModelNB/errorModelInd/string[@name='s2']").text, (self.model[i].predict(self.vect[begin:end]) != self.target[begin:end]).sum())
                else:
                    print(self.__Strings.find("ModelNB/errorModelInd/string[@name='s3']").text, (self.model.predict(self.vect[begin:end]) != self.target[begin:end]).sum())
                
        def compareModel(self, begin, end):
            try:
                print(self.__Strings.find("ModelNB/compareModel/string[@name='s1']").text)
                print(self.__Strings.find("ModelNB/compareModel/string[@name='bar']").text)
                print(self.__Strings.find("ModelNB/compareModel/string[@name='s2']").text , self.__Strings.find("ModelNB/compareModel/string[@name='space']").text, self.__Strings.find("ModelNB/compareModel/string[@name='s3']").text, 
                self.__Strings.find("ModelNB/compareModel/string[@name='space']").text, self.__Strings.find("ModelNB/compareModel/string[@name='s4']").text, self.__Strings.find("ModelNB/compareModel/string[@name='space']").text, 
                      self.__Strings.find("ModelNB/compareModel/string[@name='s5']").text, "  ", self.__Strings.find("ModelNB/compareModel/string[@name='s6']").text )
                for i in range(begin , end):
                    print(str(i).zfill(2),"       ", self.model[0].predict([self.x_test[i]]) , "             " , 
                          self.model[1].predict([self.x_test[i]]), "              ",self.model[2].predict([self.x_test[i]]), "               ",
                          self.model[3].predict([self.x_test[i]]),"        " ,self.y_test[i])
                print(self.__Strings.find("ModelNB/compareModel/string[@name='bar']").text)
                print(self.__Strings.find("ModelNB/compareModel/string[@name='s7']").text, (self.model[0].predict(self.x_test[begin:end]) != self.y_test[begin:end]).sum(), "               ",
                      (self.model[1].predict(self.x_test[begin:end]) != self.y_test[begin:end]).sum(), "                " ,
                      (self.model[2].predict(self.x_test[begin:end]) != self.y_test[begin:end]).sum(),"                 ", 
                      (self.model[3].predict(self.x_test[begin:end]) != self.y_test[begin:end]).sum())
                print(self.__Strings.find("ModelNB/compareModel/string[@name='s8']").text, len(self.x_test[begin:end]), self.__Strings.find("ModelNB/compareModel/string[@name='s9']").text)
            except  ValueError:
                print(self.__Strings.find("ModelNB/compareModel/string[@name='s10']").text)
            except IndexError:
                print(self.__Strings.find("ModelNB/compareModel/string[@name='s11']").text, len(self.x_test))
                
        def probabilitySucessModel(self):
            if (len(self.model) == 4):
                for i in range(len(self.model)):
                    print(self.__Strings.find("ModelNB/probabilitySucessModel/string[@name='s1']").text,i," : ", self.model[i].score(self.x_test, self.y_test) * 100, "%")
            else:
                print(self.__Strings.find("ModelNB/probabilitySucessModel/string[@name='s1']").text, self.model.score(self.x_test, self.y_test) * 100, "%")
            
        def probabilitySucessModelInd(self, begin, end):
            if(len(self.model) == 4):
                try:
                    for i in range(len(self.model)):
                        print(self.__Strings.find("ModelNB/probabilitySucessModelInd/string[@name='s1']").text,i,":", self.model[i].score(self.vect[begin:end], self.target[begin:end])*100, "%.")
                except IndexError:
                    print(self.__Strings.find("ModelNB/probabilitySucessModelInd/string[@name='s2']").text, len(self.x_test))
                except ValueError:
                    print(self.__Strings.find("ModelNB/probabilitySucessModelInd/string[@name='s3']").text)
            else:
                try:
                    print(self.__Strings.find("ModelNB/probabilitySucessModelInd/string[@name='s4']").text, self.model.score(self.vect[begin:end], self.target[begin:end])*100, "%.")
                except IndexError:
                    print(self.__Strings.find("ModelNB/probabilitySucessModelInd/string[@name='s2']").text, len(self.x_test))
                except ValueError:
                    print(self.__Strings.find("ModelNB/probabilitySucessModelInd/string[@name='s3']").text)
        
        #sobrescrita
        def generalReport(self):
            #Mostra o resumo do modelo segundo a biblioteca sklearn.metrics
            if (len(self.model) == 4):
                for i in range(len(self.model)):
                    print(self.__Strings.find("ModelNB/generalReport/string[@name='s1']").text, self.data.modifyString(str(type(self.model[i]))).split()[-1] ," :")
                    print(self.__Strings.find("CommonModel/generalReport/string[@name='s2']").text)
                    print(metrics.classification_report(self.target, self.model[i].predict(self.vect)))
                    print(self.__Strings.find("CommonModel/generalReport/string[@name='s2']").text)
            else:
                print(self.__Strings.find("CommonModel/generalReport/string[@name='s1']").text)
                print(self.__Strings.find("CommonModel/generalReport/string[@name='s2']").text)
                print(metrics.classification_report(self.target, self.model.predict(self.vect)))
                print(self.__Strings.find("CommonModel/generalReport/string[@name='s2']").text)
        
        #sobrescrita
        def matrixConfusion(self):
            if (len(self.model) == 4):
                for i in range(len(self.model)):
                    print(self.__Strings.find("ModelNB/matrixConfusion/string[@name='s1']").text, self.data.modifyString(str(type(self.model[i]))).split()[-1]," : ")
                    print(self.__Strings.find("CommonModel/matrixConfusion/string[@name='s2']").text)
                    for i in metrics.confusion_matrix(self.target, self.model[i].predict(self.vect)):
                        print("       ", i)
                    print(self.__Strings.find("CommonModel/matrixConfusion/string[@name='s2']").text)
            else: 
                print(self.__Strings.find("CommonModel/matrixConfusion/string[@name='s1']").text)
                print(self.__Strings.find("CommonModel/matrixConfusion/string[@name='s2']").text)
                for i in metrics.confusion_matrix(self.target, self.model.predict(self.vect)):
                    print("       ", i)
                print(self.__Strings.find("CommonModel/matrixConfusion/string[@name='s2']").text)
        
        #sobrescrita
        def subdivideEstados(self):
            #Contador de vetor
            x = 0 
            self.zeroPositivo = []
            self.umPositivo   = []
            
            if (len(self.model) == 4):
                for i in range(len(self.model)):
                    temp1 = [] #ira armazenar os vetores onde o preditor for igual a 0
                    temp2 = [] #ira armazenar os vetores onde o preditor for igual a 1
                    for j in self.model[i].predict(self.vect):
                        if (j == 0):
                            temp1.append(self.vect[x])
                            x += 1
                        else:
                            temp2.append(self.vect[x])
                            x += 1
                    #salva os temporarios
                    self.zeroPositivo.append(temp1)
                    self.umPositivo.append(temp2)
                    x = 0
            else:
                #Filtra os casos positivos de 0 e de 1
                for i in self.model.predict(self.vect):
                    if (i == 0):
                        self.zeroPositivo.append(self.vect[x])
                        x += 1
                    else:
                        self.umPositivo.append(self.vect[x])
                        x += 1
        
        #sobrescrita
        def subdivideCaracteristicas(self):
            #Subdivide o vetor positivo e negativo em varios vetores de colunas
            self.columnsZero = {}
            self.columnsUm   = {}
            
            if (len(self.model) == 4):
                for k in range(len(self.model)):
                    temp1 = {}
                    temp2 = {}
                    for i in self.zeroPositivo[k]:
                        for j in range(len(i)):
                            if i == self.zeroPositivo[k][0]:
                                temp1[j] = i[j:j+1]
                            else:
                                temp1[j] += i[j:j+1]

                    for i in self.umPositivo[k]:
                        for j in range(len(i)):
                            if i == self.umPositivo[k][0]:
                                temp2[j] = i[j:j+1]
                            else:
                                temp2[j] += i[j:j+1]
                    
                    if (k == 0):
                        x = 0
                        for i in temp1.values():
                            self.columnsZero[x] = [i]
                            x += 1
                        x = 0
                        for i in temp2.values():
                            self.columnsUm[x] = [i]
                            x += 1
                    else:
                        x = 0
                        for i in temp1.values():
                            self.columnsZero[x] += [i]
                            x += 1
                        x = 0
                        for i in temp2.values():
                            self.columnsUm[x] += [i]
                            x += 1

            else:
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

        #sobrescrita
        def characteristicAtt(self, choice, trad):
            
            if (len(self.model) == 4):
                umP = []
                zeroP = []
                for k in range(len(self.model)):
                    a = []
                    b = []
                    t1 = len(pd.DataFrame(self.columnsUm[choice][k])[0].value_counts().sort_index().index)
                    t2 = len(pd.DataFrame(self.columnsZero[choice][k])[0].value_counts().sort_index().index)
                    fiUm = []
                    fiZero = []
                    
                    if (t1 > t2):
                        for i in range (t1):
                            fiUm.append(self.columnsUm[choice][k].count(i))
                            fiZero.append(self.columnsZero[choice][k].count(i))
                    elif (t2 > t1):
                        for i in range (t1):
                            fiUm.append(self.columnsUm[choice][k].count(i))
                            fiZero.append(self.columnsZero[choice][k].count(i))
                    else :
                        for i in range (t1):
                            fiUm.append(self.columnsUm[choice][k].count(i))
                            fiZero.append(self.columnsZero[choice][k].count(i))
                
                    vet    = [fiZero, fiUm]
                    sum_p  = [len(self.columnsZero[choice][k]), len(self.columnsUm[choice][k])]
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
                    zeroP.append(trad[a.index(np.array(a).max())][0])
                    umP.append(trad[b.index(np.array(b).max())][0])
                    ##return [dados.traducao[escolha][str(a.index(np.array(a).max()))], dados.traducao[escolha][str(b.index(np.array(b).max()))]]
                    ##return ([trad[a.index(np.array(a).max())][0], trad[b.index(np.array(b).max())][0]])
                
                return [zeroP, umP]
            else : 
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