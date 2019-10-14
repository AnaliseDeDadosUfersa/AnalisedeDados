from sklearn import svm, metrics
from CommonModel import CommonModel
import pandas as pd
import matplotlib.pyplot as plot


class ModelSVM(CommonModel):
    def __init__(self, link, positionTarget, language = "en"):
        super().__init__(link, positionTarget, svm.SVC(gamma = "scale"), language)
        
    def showBarGraph(self, esc):
        temp1 = pd.DataFrame(self.columnsUm)
        temp2 = pd.DataFrame(self.columnsZero)

        # tamanho das barras
        if (len(esc) <= 4):
            barWidth = 0.2
        else:
            barWidth = 0.3

        if (len(esc) > 1):
            if (len(esc) > 4):
                print("A-side")
                #teste de construção dos subplots
                if (len(esc) % 4 == 0):
                    c = int(len(esc) / 4)
                    tamFig = 5*c
                    fig, ax = plot.subplots(4, c, figsize = (tamFig,tamFig + tamFig * 0.2))
                else: 
                    c = int((len(esc) + (4 - (len(esc) % 4)) )/4)
                    tamFig = 5*c
                    print(c)
                    fig, ax = plot.subplots(4, c, figsize = (tamFig,tamFig + tamFig * 0.2))

                #contador de subplots
                cn = 0
                cx = 0

                for i in esc:
                    #valores 
                    v1 = temp1[i].value_counts().sort_index().values
                    v2 = temp2[i].value_counts().sort_index().values

                    #Localização
                    r1 = [x - (barWidth/2)for x in temp1[i].value_counts().sort_index().index]
                    r2 = [x + (barWidth/2) for x in temp2[i].value_counts().sort_index().index]

                    ax[cn, cx].bar ( r1, v1, label="Evaded", edgecolor = 'black', width = barWidth)
                    ax[cn, cx].plot( r1, v1, marker='x', linestyle = '--')
                    ax[cn, cx].bar ( r2, v2, label= "Concluding"   , edgecolor = 'black', width = barWidth)
                    ax[cn, cx].plot( r2, v2, marker='o', linestyle = '--')
                    for j in range(len(r1)):
                        ax[cn, cx].text(x = r1[j] - 0.1, y = v1[j] + 0.5, s = v1[j], size = 12 * c * 0.3)
                    for j in range(len(r2)):
                        ax[cn, cx].text(x = r2[j] - 0.1, y = v2[j] + 0.5, s = v2[j], size = 12 * c * 0.3)

                    ax[cn, cx].grid(True)
                    ax[cn, cx].legend()
                    ax[cn, cx].set_ylabel('Quant')
                    ax[cn, cx].set_title(self.data.data.columns[i])
                    if (cn == 3):
                        cn = 0
                        cx += 1
                    else:
                        cn += 1
                plot.xticks([r for r in range(len(v1))])
                plot.show()
            else:
                print("B-side")
                tamFig = 8
                fig, ax = plot.subplots(len(esc), figsize = (tamFig,tamFig + tamFig * 0.4))

                #contador de subplots
                cn = 0

                for i in esc:
                    #valores 
                    v1 = temp1[i].value_counts().sort_index().values
                    v2 = temp2[i].value_counts().sort_index().values

                    #Localização
                    r1 = [x - (barWidth/2)for x in temp1[i].value_counts().sort_index().index]
                    r2 = [x + (barWidth/2) for x in temp2[i].value_counts().sort_index().index]

                    ax[cn].bar ( r1, v1, label="Evaded", edgecolor = 'black', width = barWidth)
                    ax[cn].plot( r1, v1, marker='x', linestyle = '--')
                    ax[cn].bar ( r2, v2, label= "Concluding"   , edgecolor = 'black', width = barWidth)
                    ax[cn].plot( r2, v2, marker='o', linestyle = '--')
                    for j in range(len(r1)):
                        ax[cn].text(x = r1[j] - 0.1, y = v1[j] + 0.5, s = v1[j], size = 12)
                    for j in range(len(r2)):
                        ax[cn].text(x = r2[j] - 0.1, y = v2[j] + 0.5, s = v2[j], size = 12)

                    ax[cn].grid(True)
                    #plot.xticks([r for r in range(len(v1))])
                    ax[cn].legend()
                    ax[cn].set_title(self.data.data.columns[i])
                    cn += 1

                plot.show()
        else :
            print("C-side")
            for i in esc:
                #valores 
                v1 = temp1[i].value_counts().sort_index().values
                v2 = temp2[i].value_counts().sort_index().values

                #Localização
                r1 = [x - (barWidth/2) for x in temp1[i].value_counts().sort_index().index]
                r2 = [x + (barWidth/2) for x in temp2[i].value_counts().sort_index().index]

                plot.bar ( r1, v1, edgecolor = 'black', label="Evaded", width = barWidth)
                plot.plot( r1, v1, marker='x', linestyle = '--')
                plot.bar ( r2, v2,  label= "Concluding", edgecolor = 'black', width = barWidth)
                plot.plot( r2, v2, marker='o', linestyle = '--')

                for j in range(len(r1)):
                    plot.text(x = r1[j] - 0.1, y = v1[j] + 0.5, s = v1[j], size = 12)
                for j in range(len(r2)):
                    plot.text(x = r2[j] - 0.1, y = v2[j] + 0.5, s = v2[j], size = 12)

            #plot.xticks([r for r in range(len(v1))])
            plot.ylabel('Quat.')
            plot.xlabel('Var')
            plot.title(self.data.data.columns[esc])
            plot.legend()
            plot.grid(True)
            plot.show()