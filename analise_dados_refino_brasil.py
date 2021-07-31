# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 19:47:07 2020

@author: Bárbara Cynthia Carnaúba dos Santos
LinkedIn: https://www.linkedin.com/in/barbaracarnauba/
"""

# Análise de Dados de refino do Brasil de Jan/1990 até Set/2020

###------------------------------- Bibliotecas -----------------------------###

from funcs_data_analysis import df_padroniza, df_agrupa_serie_temporal
from funcs_data_analysis import plot_bar_cores, plot_serie_temporal
from funcs_data_analysis import plot_serie_temporal_multipla
import pandas as pd
import matplotlib.pyplot as plt
from IPython import get_ipython
get_ipython().magic('reset -sf') #limpa variáveis do workspace a cada execução
plt.close('all') #fecha todos os plots a cada execução

###-------------------- Carregando/Tratando Dados -------------------------###

# Dados de processamento de petróleo 1990-2020
df1 = pd.read_excel('dadosProcessamentoPetroleoBrasil1990-2019barris.xlsx') 
df2 = pd.read_excel('dadosProcessamentoPetroleoBrasil2020barris.xlsx') 
df_padroniza(df1)
df_padroniza(df2)
df =  pd.concat([df1,df2],ignore_index=True)

###-------------- Filtrando Dados, Agrupando e Plotando Gráficos ----------###

### Processamento total acumulado 1990-2020 por refinaria

df_cut_ref=df[['REFINARIA','TOTAL']]

df_cut_ref2=df_cut_ref.groupby(['REFINARIA'],as_index=False).sum().sort_values(
    by=['TOTAL'],ascending=False, ignore_index=True)

# Gráfico 1

plot_bar_cores('REFINARIA','TOTAL',df_cut_ref2,
               'Processamento de Petróleo (barris)',
               'Refinaria', 'Processamento Total Acumulado de 1990-2020')

##############################################################################

### Série temporal do processamento de petróleo 1990-2020

drop_cols = ['ESTADO','REFINARIA','UNIDADE','TOTAL','MATERIA PRIMA']
data, time_years = df_agrupa_serie_temporal(df,drop_cols,'ANO',1990)

# Figura 2 : Processamento somado de todas as refinarias ao longo dos anos
plot_serie_temporal(time_years,data,'Processamento 1990-2020','Anos',
                    'Processamento de petróleo 1990-2020'
                    ,'r')
##############################################################################
# Série temporal do processamento de petróleo na REPLAN 1990-2020

df_replan = df.query('REFINARIA == "REPLAN"')
data2, time_years2 = df_agrupa_serie_temporal(df_replan,drop_cols,'ANO',1990)

# Figura 3: Série temporal da REPLAN 1990-2020
plot_serie_temporal(time_years2,data2,'Processamento 1990-2020','Anos',
                    'Processamento de petróleo REPLAN 1990-2020'
                    ,'b')
##############################################################################

# Série temporal do processamento de petróleo na REDUC 1990-2020
df_reduc = df.query('REFINARIA == "REDUC"')
data3, time_years3 = df_agrupa_serie_temporal(df_reduc,drop_cols,'ANO',1990)

# Figura 4: Série temporal da REDUC 1990-2020
plot_serie_temporal(time_years3,data3,'Processamento 1990-2020','Anos',
                    'Processamento de petróleo REDUC 1990-2020'
                    ,'g')

##############################################################################

# Série temporal do processamento de petróleo por refinaria 1990-2020 TOP FIVE

lista_refinarias = list(pd.unique(df_cut_ref2['REFINARIA']))[0:5] #TOP FIVE
dict_refinarias = {}

for item in lista_refinarias:
    dict_refinarias[item] = df[(df.REFINARIA == item)]

# Figura 5 até Figura 21
dict_data = {}    
dict_time= {}    
for i in range(len(lista_refinarias)):
    dict_data[i], dict_time[i] = df_agrupa_serie_temporal(
        dict_refinarias[lista_refinarias[i]],drop_cols,'ANO',1990)
    
# produção em milhões de barris
for j in dict_data:
        dict_data[j] = dict_data[j]/10**6

plot_serie_temporal_multipla(dict_time,dict_data,'Processamento 1990-2020 (MMbbl)','Anos',
                    'Processamento de petróleo 1990-2020',lista_refinarias)

##############################################################################

# Série temporal do processamento de petróleo por refinaria 1990-2020 BOTTOM FIVE

lista_refinarias2 = list(pd.unique(df_cut_ref2['REFINARIA']))[12::] #TOP FIVE
dict_refinarias2 = {}

for item2 in lista_refinarias2:
    dict_refinarias2[item2] = df[(df.REFINARIA == item2)]

# Figura 5 até Figura 21
dict_data2 = {}    
dict_time2= {}    
for i2 in range(len(lista_refinarias2)):
    dict_data2[i2], dict_time2[i2] = df_agrupa_serie_temporal(
        dict_refinarias2[lista_refinarias2[i2]],drop_cols,'ANO',1990)

# produção em milhões de barris
for k in dict_data2:
        dict_data2[k] = dict_data2[k]/10**6

plot_serie_temporal_multipla(dict_time2,dict_data2,'Processamento 1990-2020 (MMbbl)','Anos',
                    'Processamento de petróleo 1990-2020',lista_refinarias2)

##############################################################################

# Série Temporal do Processamento de Petróleo Total por Tipo de Matéria Prima

materias_primas = list(pd.unique(df['MATERIA PRIMA']))
tipos_materia_prima=df['MATERIA PRIMA'].value_counts()
df_replan['MATERIA PRIMA'].value_counts()

dict_replan = {}

for item in materias_primas:
    dict_replan[item] = df_replan[(df_replan['MATERIA PRIMA'] == item)]
    
dict_data_replan = {}    
dict_time_replan= {}    
for i in range(len(materias_primas)):
    dict_data_replan[i], dict_time_replan[i] = df_agrupa_serie_temporal(
        dict_replan[materias_primas[i]],drop_cols,'ANO',1990)
    
# produção em milhões de barris
for j in dict_data_replan:
        dict_data_replan[j] = dict_data_replan[j]/10**6

plot_serie_temporal_multipla(dict_time_replan,dict_data_replan,
                             'Processamento 1990-2020 (MMbbl)','Anos',
                    'Processamento de petróleo 1990-2020',materias_primas)



