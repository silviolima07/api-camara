import streamlit as st

from bokeh.models.widgets import Div

import pandas as pd

from PIL import Image

pd.set_option('precision',2)

import base64

import sys

import requests
import pandas as pd

import re


def download_link(df, texto1, texto2):
    if isinstance(df,pd.DataFrame):
        object_to_download = df.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{texto1}">{texto2}</a>'

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link
    return f'<a target="_blank" href="{link}">Link da vaga</a>' # ou {text} e irá mostrar o link clicável

def coletar_despesas(id_dep, id_leg):
 
  URL_desp = "https://dadosabertos.camara.leg.br/api/v2/deputados/"+str(id_dep)+"/despesas"

  #
  colunas = ['ano','cnpjCpfFornecedor','codDocumento','codLote','codTipoDocumento','dataDocumento','mes',
           'nomeFornecedor','numDocumento','numRessarcimento','parcela','tipoDespesa','tipoDocumento',
           'urlDocumento','valorDocumento','valorGlosa','valorLiquido'] 
  #
  #st.write("id_leg: "+id_leg)
  #st.write("id_dep: "+id_dep)


  print("id legislacao: ",id_leg)
  # defining a params dict for the parameters to be sent to the API
  PARAMS_despesas = {'idLegislatura':id_leg, 'ordem': 'ASC', 'ordenarPor':'ano'}
  # sending get request and saving the response as response object
  r_desp = requests.get(url = URL_desp, params = PARAMS_despesas)
  #
  # extracting data in json format
  data_desp = r_desp.json()
  print(data_desp)
  print("Despesas por legislatura: ",data_desp.keys())
  dados = data_desp['dados']
  print("Dados: ",dados)

  df = pd.DataFrame(dados, columns=colunas)  
  #df = pd.concat(dfs)
  df['id_dep'] = id_dep

  print(df)

  return df

    
def coletar_dados_leg(ids):
  
  # URL
  URL_LEG  = "https://dadosabertos.camara.leg.br/api/v2/legislaturas"
 
  colunas =  ["id", "uri","dataInicio", "dataFim"]
  #
  dfs = []

  for id in (ids):
      #st.write("id legislatura: " +str(id))
      # defining a params dict for the parameters to be sent to the API
      PARAMS_LEGS = {'id': id,'ordem':'DESC','ordenarPor':'id'}
      # sending get request and saving the response as response object
      r_legs = requests.get(url = URL_LEG, params = PARAMS_LEGS)
      #
      # extracting data in json format
      data_leg = r_legs.json()
      dados = data_leg['dados']

      dfs.append(pd.DataFrame(dados, columns=colunas))  
    
  df = pd.concat(dfs)

  return df

def main():

    """Indeed App """

    # Titulo do web app
    html_page = """
    <div style="background-color:blue;padding=30px">
        <p style='text-align:center;font-size:30px;font-weight:bold;color:white'>Camara de Deputados</p>
    </div>
              """
    st.markdown(html_page, unsafe_allow_html=True)
   
    html_page = """
    <div style="background-color:white;padding=20px">
        <p style='text-align:center;font-size:20px;font-weight:bold;color:blue'>Dados sobre Despesas</p>
    </div>
              """
    st.markdown(html_page, unsafe_allow_html=True)

    anos = ['2007','2008','2009','2010', '2011', '2012','2013', '2014', '2015', 
          '2016', '2017', '2018', '2019', '2020','2021']   
  
    ids_leg = [51,52,53,54,55,56]
    
    camara  = Image.open("Images/camara.jpeg")
    
    dados_abertos  = Image.open("Images/dados_abertos.jpeg")

    st.sidebar.image(camara,caption="", width=300)

    activities = ["Home","Escolher Deputado","About"]
    file_csv = ['CSV/indeed_Cientista_de_dados.csv','CSV/indeed_Analista_de_dados.csv', 'CSV/indeed_Engenheiro_de_Machine_Learning.csv',
                'CSV/indeed_Engenheiro_de_Dados.csv']
    choice = st.sidebar.selectbox("Selecione uma opção",activities)

    # Definir a data da última atualização



    ################################################################

    # COLETAR DADOS DAS LEGISLATURAS
    #print("Chamando coletar dados leg: ",ids)
    df_leg = coletar_dados_leg(ids_leg)

    df_leg[['anoInicial', 'mes']] = df_leg['dataInicio'].str.split('-', 1, expand=True)
    df_leg[['anoFinal','mes']] = df_leg['dataFim'].str.split('-', 1, expand=True)
   
    #st.table(df_leg[['id','anoInicial','anoFinal']])

    #df_leg['anoInicial'] = str(df_leg['dataInicio']).split('-')[0]
    #df_leg['anoFinal'] = str(df_leg['dataFim']).split('-')[0]
    #print("Tabela Legislaturas: ",df_leg)
    #st.sidebar.write("Legislaturas validas")
    df_leg['id_leg'] = df_leg['id']
    df_leg.drop(['id'], axis=1)
    #st.sidebar.table(df_leg[['id_leg', 'dataInicio', 'dataFim']])
    #if (df_leg.shape[0] > 0):
    #    st.table(df_leg)
    #else:
    #    st.write("Sem mandato")
    ###############################################################
    # COLETAR DADOS DOS DEPUTADOS
    URL_dep = "https://dadosabertos.camara.leg.br/api/v2/deputados"

    colunas_dep =  ["id", "uri","nome", "siglaPartido", "uriPartido","siglaUf", "idLegislatura", "urlFoto", "email"]

    PARAMS_dep = {'dataInicio':'2007-02-01', 'dataFim': '2023-01-31','ordem': 'ASC', 'ordenarPor':'nome',   'itens':9999}

    # sending get request and saving the response as response object
    r_dep = requests.get(url = URL_dep, params = PARAMS_dep)
    #
    # extracting data in json format
    data_dep = r_dep.json()
    dados = data_dep['dados']
   
    df_dep = pd.DataFrame(dados, columns=colunas_dep)
    

    #st.table(df_dep['nome_id_leg'])

    lista_dep = df_dep['nome']
    temp = []
    for i in lista_dep:
         temp.append(i.upper())
    #print(temp)
    lista_dep = temp
    df_dep['nome'] = lista_dep
    df_dep['nome_id_leg'] = df_dep['nome']+"---"+df_dep['id'].astype(str)+"---"+df_dep['idLegislatura'].astype(str)
    df_dep['nome_leg'] = df_dep['nome']+" ---> legislatura: "+df_dep['idLegislatura'].astype(str)
    lista_dep = df_dep['nome_id_leg']
    #
    df_dep['id_leg'] = df_dep['idLegislatura']
    df_dep.drop(['idLegislatura'], axis=1)
    print("Dados deputados: ", df_dep[['nome','id','id_leg']])
    
    
    ################################################################
       

    if choice == activities[0]:
       
        col1,col2 = st.beta_columns(2)
    
       
        #col1.header("Câmara de Deputados")
        col1.image(dados_abertos, width=700)
        
   

       
        
    elif choice == activities[1]: 
        
        dep_escolhido = st.selectbox("Deputados     ---     Id     --- Legislatura",lista_dep)
 
        nome, id_dep, id_leg = dep_escolhido.split('---')

        #st.write("Nome: "+nome)
        #st.write("id dep: "+id_dep)        
        #st.write("id_leg: "+id_leg)
        
        print("ID_DEP: ",id_dep)
        st.sidebar.image(
            "https://www.camara.leg.br/internet/deputado/bandep/"+str(id_dep).strip()+".jpg",
            width=300
        )
        deputado = df_dep.loc[df_dep['nome'] == nome.strip()]
        
        st.subheader("Mandatos")
        st.table(deputado[['siglaPartido','siglaUf', 'idLegislatura']])

        df_merged = pd.merge(df_dep,df_leg, on="id_leg")

        #st.write("Mandatos")
        #st.table(df_merged[['siglaPartido','id_leg', 'anoInicial', 'anoFinal']])     
        #mandatos = str(deputado['idLegislatura']).split()[1]
        #partido = str(deputado['siglaPartido']).split()[1]
        #uf      = str(deputado['siglaUf']).split()[1]

        #st.sidebar.write("Legislatura: "+ mandatos,"Partido: "+ partido, "UF: "+uf)
        
        lista_id_leg = [int(id_leg)]
        
        df_despesas = coletar_despesas(id_dep, id_leg)
        
        st.subheader("Gastos")
        if (df_despesas.shape[0] > 0):
            st.table(df_despesas[['ano','dataDocumento','mes',        'nomeFornecedor','tipoDespesa','valorDocumento','valorGlosa','valorLiquido']])
        else:
            st.write("Sem dados informados")
   
    elif choice == 'About':
        #st.sidebar.image(about,caption="", width=300, height= 200)
        st.subheader("Built with Streamlit")
        
        st.write("Dados coletados via API da Camara de Deputados do Brasil.")
        
        #st.write("Executados via crontab scripts realizam o scrap e atualização do app.")
        #st.write("Foram definidos 4 cargos apenas para validar o processo.")
        #st.write("O scrap para o cargo de Engenheiro de Machine Learning trouxe poucas linhas.")
        #st.write("Para os demais cargos, foram encontradas mais de 100 vagas, distribuídas em diversas páginas.")
        #st.write("Esse app traz as 10 primeiras páginas apenas.")
        ##st.subheader("Versão 02")
        ##st.write(" - incluído o link encurtado da vaga")
        
        st.subheader("by Silvio Lima")
        
        if st.button("Linkedin"):
            js = "window.open('https://www.linkedin.com/in/silviocesarlima/')"
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
   

   
    
    
if __name__ == '__main__':
    main()
