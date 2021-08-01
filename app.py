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


def trazer_dados_dep(url_dep,coluna_dep):
  anos = ['2007','2008','2009','2010', '2011', '2012','2013', '2014', '2015', 
          '2016', '2017', '2018', '2019', '2020','2021']
  URL_dep = url_dep
  coluna = coluna_dep
  dfs_dep=[]
  for ano in (anos):
      print("ano: ",ano)
      
      PARAMS_dep = {'ano': int(ano), 'ordem': 'ASC', 'ordenarPor':'idLegislatura'}

      # sending get request and saving the response as response object
      r_dep = requests.get(url = URL_dep, params = PARAMS_dep)
      #
      
      data_dep = r_dep.json()
      print("data_dep:", data_dep)
      """
      dados_dep = data_dep['dados']
      dfs_dep.append(pd.DataFrame(dados_dep, columns=coluna))

  df_dep = pd.concat(dfs_dep)
  return df_dep
      """


def trazer_dados_desp(url_desp,id_dep, coluna_desp):

  #https://dadosabertos.camara.leg.br/api/v2/deputados/141422/despesas?idLegislatura=51&ordem=ASC&ordenarPor=ano

  anos = ['2007','2008','2009','2010', '2011', '2012','2013', '2014', '2015', 
          '2016', '2017', '2018', '2019', '2020','2021']
  URL_desp = url_desp
  coluna = coluna_desp
  dfs_desp=[]
  print("Id_dep:", id_dep)
  
  for i in (anos):
      print("Ano: ", i)
  
      PARAMS_desp = {'ano':i,'itens':9999}
      # sending get request and saving the response as response object
      r_desp = requests.get(url = URL_desp, params = PARAMS_desp)
      # extracting data in json forma
      data_desp = r_desp.json()
      dados_desp = data_desp['dados']
      print("Shape:",pd.DataFrame(dados_desp, columns=coluna).shape)
      dfs_desp.append(pd.DataFrame(dados_desp, columns=coluna))

  df_desp = pd.concat(dfs_desp)
  df_desp['id_dep'] = id_dep
  return df_desp.reset_index(drop=True)

    
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

    #df_dep = trazer_dados_dep(URL_dep, colunas_dep)
    
    #id_legs = [51,52, 53,54,55,56]
    #
    #df_dep = trazer_dados_dep(URL_dep, id_legs, colunas_dep )
    #print("URL_dep: ", URL_dep)
    #df_dep.rename(columns={"id": "id_dep"},inplace=True)
    #df_dep['nome'] = str(df_dep['nome']).upper()

    #print("df_dep:",df_dep.shape)


    #print("Id_dep: ", id_dep)

    
    
    PARAMS_dep = {'dataInicio':'2007-02-01', 'dataFim': '2023-01-31','ordem': 'ASC', 'ordenarPor':'nome',   'itens':9999}

    # sending get request and saving the response as response object
    r_dep = requests.get(url = URL_dep, params = PARAMS_dep)
    #
    # extracting data in json format
    data_dep = r_dep.json()
    dados = data_dep['dados']
   
    df_dep = pd.DataFrame(dados, columns=colunas_dep)
    df_dep2 = pd.DataFrame()
    df_dep2[['nome','id']] = df_dep[['nome','id']]

    lista_nome = df_dep2['nome']
    temp = []
    for i in lista_nome:
         temp.append(i.upper())
    df_dep2['nome'] = temp

    df_dep2.drop_duplicates(inplace=True)
    df_dep2.to_csv("deputado.csv")

    dict_dep = df_dep2.set_index('nome').to_dict()['id']

    #st.write(dict_dep.get('ABEL MESQUITA JR.'))
    
    print("df_dep:", df_dep.shape)
    #st.table(df_dep['nome_id_leg'])
    
    lista_dep = df_dep2['nome']
    print("Lista dep:", lista_dep)
    #df_dep1 = df_dep[['id','nome']]
    #lista_dep2 = set(df_dep1)
    #df = pd.DataFrame(lista_dep2,columns=['nome', 'id'])
    #df_dep2 = df_dep[['nome','id']]
    #st.table(df)
    
    temp = []
    for i in lista_dep:
         temp.append(i.upper())
    #print(temp)
    
    lista_dep = temp
    #df_dep['nome'] = lista_dep
    #df_dep['nome_id_leg'] = df_dep['nome']+"---"+df_dep['id'].astype(str)
    #df_dep['nome_leg'] = df_dep['nome']+" ---> legislatura: "+df_dep['idLegislatura'].astype(str)
    #lista_dep = df_dep['nome_id_leg']
    
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
 
        df_dep_unique = pd.DataFrame(lista_dep, columns=['nome'])
        df_dep_unique['nome_dep'] = df_dep_unique['nome']
        df_dep_unique.set_index('nome', inplace=True)
        lista_dep = df_dep_unique['nome_dep']
        #st.table(df_dep_unique)
        #st.write(lista_nome)
        #st.table(pd.DataFrame(lista_nome, id_dep))
        st.subheader("Deputados")
        dep_escolhido = st.selectbox("Escolha",lista_dep)
 
        #nome, id_dep= dep_escolhido.split('---')

        #st.write("dep_escolhido: "+dep_escolhido)
        #st.write("id dep: "+id_dep)        
        #st.write("id_leg: "+id_leg)

        #st.write(dict_dep.get('ABEL MESQUITA JR.'))
        #st.write("Id Dep Escolhido na selecao:"+ str(dict_dep.get(dep_escolhido)))
        id_dep = dict_dep.get(dep_escolhido)
        
        #print("ID_DEP: ",id_dep)
        st.sidebar.image(
            "https://www.camara.leg.br/internet/deputado/bandep/"+str(id_dep).strip()+".jpg",
            width=300
        )
        #st.write("dep_escolhido: "+dep_escolhido)
        deputado = df_dep.loc[df_dep['nome'] == dep_escolhido]
        #dep = deputado.set_index('siglaPartido', inplace=True)
        st.subheader("Mandatos")

        st.table(deputado[['siglaPartido','siglaUf', 'idLegislatura']])
        #st.subheader("Mandatos")
        #st.write(deputado[['siglaPartido','siglaUf', 'idLegislatura']])
        #st.table(deputado[['siglaPartido','siglaUf', 'idLegislatura']])

        #df_merged = pd.merge(df_dep,df_leg, on="id_leg")
        

        #st.table(df_dep)

        #st.table(df_merged[['siglaPartido','id_leg', 'anoInicial', 'anoFinal']])     
        #mandatos = str(deputado['idLegislatura']).split()[1]
        #partido = str(deputado['siglaPartido']).split()[1]
        #uf      = str(deputado['siglaUf']).split()[1]

        #st.sidebar.write("Legislatura: "+ mandatos,"Partido: "+ partido, "UF: "+uf)
        
        #lista_id_leg = [int(id_leg)]
        
        #df_despesas = coletar_despesas(id_dep, id_leg)
        anos = ['2007','2008','2009','2010', '2011', '2012','2013', '2014', '2015','2016', '2017', '2018', '2019', '2020','2021']
        id_legs = [51,52, 53,54,55,56]
        URL_desp = "https://dadosabertos.camara.leg.br/api/v2/deputados/"+str(id_dep)+"/despesas"
        coluna_desp = ['ano','cnpjCpfFornecedor','codDocumento','codLote','codTipoDocumento','dataDocumento','mes',
           'nomeFornecedor','numDocumento','numRessarcimento','parcela','tipoDespesa','tipoDocumento',
           'urlDocumento','valorDocumento','valorGlosa','valorLiquido'] 

        #dfs = []
        #for ano in (anos):
        #    print("ANO:",ano)
        df_desp = trazer_dados_desp(URL_desp,id_dep, coluna_desp)

        #df_desp = pd.concat(dfs)

        #df_desp['id_dep'] = id_dep
        print("df_desp:", df_desp.shape)
        df_despesas = df_desp
        
        st.subheader("Gastos")
        if (df_despesas.shape[0] > 0):
            total_declaracoes = df_despesas.shape[0]
            st.write("Total de declarações de gasto em todos mandatos: "+str(total_declaracoes))
            st.table(df_despesas[['dataDocumento',        'nomeFornecedor','tipoDespesa','valorDocumento','valorGlosa','valorLiquido']])
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
