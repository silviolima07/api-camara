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

def coletar_despesas(id_dep, anos):
  #anos = ['2009','2010', '2011', '2012','2050','2013', '2014', '2015', 
  #        '2016', '2017', '2018', '2019', '2020','2021']
  #
  URL_desp = "https://dadosabertos.camara.leg.br/api/v2/deputados/"+str(id_dep)+"/despesas"
  #
  colunas = ['ano','cnpjCpfFornecedor','codDocumento','codLote','codTipoDocumento','dataDocumento','mes',
           'nomeFornecedor','numDocumento','numRessarcimento','parcela','tipoDespesa','tipoDocumento',
           'urlDocumento','valorDocumento','valorGlosa','valorLiquido'] 
  #
  dfs = []

  for i, j in enumerate(anos):
    # i indice da posicao
    # j valor do ano naquela posicao
    # defining a params dict for the parameters to be sent to the API
    PARAMS_despesas = {'ano':j,   'itens':9999}
    # sending get request and saving the response as response object
    r_desp = requests.get(url = URL_desp, params = PARAMS_despesas)
    #
    # extracting data in json format
    data_desp = r_desp.json()
    dados = data_desp['dados']
    print("Dados: ",dados)

    dfs.append(pd.DataFrame(dados, columns=colunas))  
    
    df = pd.concat(dfs)
    df['id_dep'] = id_dep

    print(df)

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

    anos = ['2009','2010', '2011', '2012','2013', '2014', '2015', 
          '2016', '2017', '2018', '2019', '2020','2021']   


    camara  = Image.open("Images/camara.jpeg")
    
    dados_abertos  = Image.open("Images/dados_abertos.jpeg")

    st.sidebar.image(camara,caption="", width=600)

    activities = ["Home","Escolher Deputado","About"]
    file_csv = ['CSV/indeed_Cientista_de_dados.csv','CSV/indeed_Analista_de_dados.csv', 'CSV/indeed_Engenheiro_de_Machine_Learning.csv',
                'CSV/indeed_Engenheiro_de_Dados.csv']
    choice = st.sidebar.selectbox("Selecione uma opção",activities)

    # Definir a data da última atualização

    ###############################################################
    # COLETAR DADOS DOS DEPUTADOS
    URL_dep = "https://dadosabertos.camara.leg.br/api/v2/deputados"
    
    colunas_dep =  ["id", "uri","nome", "siglaPartido", "uriPartido","siglaUf", "idLegislatura", "urlFoto", "email"]

    PARAMS_dep = {'dataInicio':'1999-02-01', 'ordem': 'ASC', 'ordenarPor':'nome',   'itens':9999}

    # sending get request and saving the response as response object
    r_dep = requests.get(url = URL_dep, params = PARAMS_dep)
    #
    # extracting data in json format
    data_dep = r_dep.json()
    dados = data_dep['dados']

    df_dep = pd.DataFrame(dados, columns=colunas_dep)
    lista_dep = df_dep['nome']
    ################################################################
    
       

    if choice == activities[0]:
       
        col1,col2 = st.beta_columns(2)
    
       
        #col1.header("Câmara de Deputados")
        col1.image(dados_abertos, width=700,height=500)
        
   

       
        
    elif choice == activities[1]: 
        
        dep_escolhido = st.selectbox("Deputados",lista_dep)

        deputado = df_dep.loc[df_dep['nome'] == dep_escolhido]
        deputado.to_csv("deputado.csv")

        ano_escolhido = st.selectbox("Ano",anos)
        print("Ano escolhido:",ano_escolhido)
        lista_ano = [str(ano_escolhido)]
        
        dep_id = str(deputado['id']).split()[1]
        #
        st.sidebar.image(
            "https://www.camara.leg.br/internet/deputado/bandep/"+dep_id+".jpg",
            width=300
        )        

        partido = str(deputado['siglaPartido']).split()[1]
        uf      = str(deputado['siglaUf']).split()[1]

        st.sidebar.write("Partido: "+ partido, "UF: "+uf)
        
        
        df_despesas = coletar_despesas(dep_id, lista_ano)
        if (df_despesas.shape[0] > 0):
            st.table(df_despesas[['ano','dataDocumento','mes',        'nomeFornecedor','tipoDespesa','valorDocumento','valorGlosa','valorLiquido']])
        else:
            st.write("Sem dados")
   
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
