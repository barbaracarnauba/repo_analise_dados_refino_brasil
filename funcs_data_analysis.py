# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 19:47:30 2020

@author: Bárbara Cynthia Carnaúba dos Santos
LinkedIn: https://www.linkedin.com/in/barbaracarnauba/
"""

"""
Este script apresenta funções para análise de dados, com o objetivo de auto-
matizar trabalhos repetivos, linhas de códigos que repetem-se na maioria das 
análises exploratórias de dados como: uniformização de dados e labels (veri-
ficação de acentuação e espaços brancos em strings), agrupamentos de dados,
gráficos de barras customizados, séries temporais simples e múltiplas 
customizadas etc.

"""
###------------------------------- Bibliotecas -----------------------------###

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import chardet
import unidecode

###---------------------------- Funções -----------------------------------###

def df_encoding_read(file_name,pular_linhas=0):
    
    """
    Esta função busca a codificação do arquivo a ser lido (excel ou csv) e 
    faz a leitura do arquivo.
    
    Input:
    file_name (str): nome do arquivo com a extensão
    pular_linhas (int) [opcional]: número de linhas que se deseja pular no df
    
    """
    
    with open(file_name,'rb') as f: # buscando encoding do arquivo
        res = chardet.detect(f.read()) # dicionário com encoding
    
    file_excel1 = 'xlsx'
    file_excel2 = 'xls'
    file_csv = 'csv'
    
    if (file_name.endswith(file_excel1)) or (file_name.endswith(file_excel2)):
        
        df = pd.read_excel(file_name,encoding=res['encoding'], skiprows = range(0,pular_linhas))
    if file_name.endswith(file_csv) :
        
        df = pd.read_csv(file_name,encoding=res['encoding'], skiprows = range(0,pular_linhas))
        
    return df
    
def df_padroniza(df):
    
    """
    Essa função (1) verifica se há NaN e dublicatas, (2) se houver NaN os subs-
    titui por zeros, (3) se houver duplicas, as elimina, (4) normaliza todas 
    as strings presentes no dataframe, removendo acentos e espaços em branco
    antes e depois das strings.
    
    Parâmetros de entrada: Dataframe
    Saída: None
    
    """ 
    
    num_NaN=df.isna().sum().sum() # Verificando se há valores faltantes
    num_duplicates=df.duplicated().sum() # Verificando se há duplicatas
    
    if num_NaN != 0:
        df.fillna(value=0,inplace=True)
        
    if num_duplicates !=0:
        df.drop_duplicates(inplace=True)
    
    # Removendo acentos dos nomes (str) das colunas
    colunas = list(df.columns)
    new_cols =[]
    for name in colunas:
        new=unidecode.unidecode(name)
        new_cols.append(new)
    
    df.columns = new_cols
    
    # Removendo acentos dos valores (str) das colunas
    
    cols = df.select_dtypes(include=[np.object]).columns
    df[cols] = df[cols].apply(lambda x: x.str.normalize('NFKD').str.encode(
        'ascii', errors='ignore').str.decode('utf-8'))
    
    # Removendo espaços em braco (antes e depois) dos valores (str) das colunas

    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    
##############################################################################

def num_str2float(df,colunas):
    
    """
    Esta função converteos números de um dataframe que estão formatados como 
    strings para float.
    
    Input:
    df (dataframe): dataframe que deseja-se mudar os números de string para float
    colunas (lista): lista de colunas de deseja-se alterar
    
    Output: None

    """
    for i in colunas:
        df[i]=df[i].str.replace(',','.').astype('float64')
    
##############################################################################
    
def df_agrupa_serie_temporal(df,colunas,variavel,ano_inicial):
        
    """
    Essa função realiza filtros e agrupamentos em um datrafame
    
    Input:
    df: dataframe que deseja-se filtrar
    colunas (lista de strings): colunas que deseja-se remover do dataframe
    variavel (string): variavel com a qual deseja-se realizar o agrupamento
    ano_inicial (int): ano que inicia a série temporal
    Output:
    Vetor Y de dados da série temporal
    Vetor X de dados de tempo
    
    """
    
    df_meses=df.drop(columns=colunas)
    df_cut_meses=df_meses.groupby([variavel],as_index=False).sum()
    df_cut_meses=df_cut_meses.drop(columns=[variavel])
    data=df_cut_meses.values
    data=data.flatten()
    data=data[:-4] #Não há dados para os últimos 4 meses de 2020 para os dados 
    # de produção de petróleo e não há dados para os últimos 3 meses de 2020
    # para os dados de processamento de petróleo. Essa linha de código pode 
    # ser omitida
    time = np.arange(len(data)) #
    init_year = ano_inicial
    time_years = time/12 + init_year
    
    return data, time_years

##############################################################################
    
def plot_serie_temporal(tempo,ydata,ylab,xlab,titulo,cor):
    
    """
    Função para plotar gráfico de linha para séries temporais
    
    Parâmetros:
    tempo (array 1d de float): dados de tempo 
    ydata (array 1d de float): dados da série temporal
    ylab (string) : rótulo do eixo y
    xlab (string) : rótulo do eixo x
    titulo (string) : titulo do grafico
    cor (string): inicial para cor da linha: azul: 'b'; vermelho: 'r' ...
    
    """
    
    plt.figure()
    plt.plot(tempo,ydata,cor)
    plt.title(titulo)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig(titulo + 'png') 
##############################################################################        
    
def plot_serie_temporal_multipla(tempo,ydata,ylab,xlab,titulo,lista_labels):
    
    """
    Função para plotar gráfico de linha para séries temporais
    
    Parâmetros:
    tempo (dict de arrays 1d de float): dados de tempo 
    ydata (dict de arrays 1d de float): dados da série temporal
    ylab (string) : rótulo do eixo y
    xlab (string) : rótulo do eixo x
    titulo (string) : titulo do grafico
    lista_labels (list): mudar nome do titulo por gráfico
    cor (string): inicial para cor da linha: azul: 'b'; vermelho: 'r' ...
    
    """
    
    plt.figure()
    for i in range(len(lista_labels)):
        plt.plot(tempo[i],ydata[i],label=lista_labels[i])
        plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title(titulo.format(lista_labels[i]))
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig(titulo + 'png') 

##############################################################################

def plot_bar_cores(xval,yval,dados,ylab,xlab,titulo):
    
    """
    Função para plotar gráfico de barras a partir de colunas de dataframes e
    colore de vermelho a coluna de maior valor, de azul a de menor valor e de 
    cinza as demais colunas.
    
    Parâmetros:
    xval (string) : coluna do dataframe que será o eixo x
    yval  (string) : coluna do dataframe que será o eixo y
    dados (dataframe) : dataframe que é a base dos dados de xval e yval
    ylab (string) : rótulo do eixo y
    xlab (string) : rótulo do eixo x
    titulo (string) : titulo do grafico
    
    """
    
    cores= ['red' if (y == dados[yval].max()) else
             'blue' if (y == dados[yval].min()) else 
             'grey' for y in dados[yval] ]
      
    plt.figure()
    sns.barplot(x = xval, y = yval, data = dados, palette= cores ,ci=None)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.title(titulo)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.savefig(titulo + 'png') 
    
##############################################################################   

def plot_dispersao(xdata,ydata,xlab, ylab,titulo):
    
    """
    Função de dispersão para  comparar dois conjuntos de dados
    
    Parâmetros: 
    xdata (array 1d de float): dados para o eixo x
    ydata (array 1d de float): dados para o eixo y
    ylab (string) : rótulo do eixo y
    xlab (string) : rótulo do eixo x
    titulo (string) : titulo do grafico
    
    """
    
    plt.figure()
    plt.scatter(xdata, ydata)
    plt.title(titulo)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig(titulo + 'png') 
    
##############################################################################  

def plot_line(df,xdata,ydata,xlab, ylab,titulo):
    
    """
    Gráfico de linha simples que só utiliza duas colunas do dataframe, não
    necessitando de filtros ou groupby
    
    Parâmetros:
    df (dataframe): dataframe que deseja-se plotar colunas
    xdata (str): dados para o eixo x -> coluna do df
    ydata (str): dados para o eixo y -> coluna do df
    ylab (string) : rótulo do eixo y
    xlab (string) : rótulo do eixo x
    titulo (string) : titulo do grafico
    
    """
    
    plt.figure()
    sns.lineplot(x=xdata, y=ydata, data=df)
    plt.title(titulo)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig(titulo + 'png') 
##############################################################################  

def plot_multi_line(df,xdata,cols,xlab,ylab,titulo):
    
    """
    Gráfico de múltiplas linhas simples que só utiliza duas colunas do dataframe,
    não necessitando de filtros ou groupby
    
    Parâmetros:
    df (dataframe): dataframe que deseja-se plotar colunas
    xdata (str): dados para o eixo x -> coluna do df
    cols (lista de str): dados para os eixos y -> colunas do df
    ylab (string) : rótulo do eixo y
    xlab (string) : rótulo do eixo x
    titulo (string) : titulo do grafico
    
    """
    
    plt.figure()
    for i in range(len(cols)):
        #sns.lineplot(x=xdata, y=cols[i], data=df,label=cols[i][0:10],sort=True)
        plt.plot(df[xdata].values,df[cols[i]].values,label=cols[i][0:10])
        plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title(titulo)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig(titulo + 'png') 
        
##############################################################################