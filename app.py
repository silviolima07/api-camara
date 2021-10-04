import streamlit as st

import streamlit.components.v1 as component

from bokeh.models.widgets import Div

import pandas as pd

import numpy as np

from PIL import Image

import altair as alt

pd.set_option('precision',0)

import base64

import sys

import requests
import pandas as pd

import time

import matplotlib

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import unicodedata

@st.cache(suppress_st_warning=False) 



def remove_accents(input_str):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', input_str)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href



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
      #print("data_dep:", data_dep)
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
  #print("Id_dep:", id_dep)
  
  for i in (anos):
      #print("Ano: ", i)
  
      PARAMS_desp = {'ano':i,'itens':9999}
      # sending get request and saving the response as response object
      r_desp = requests.get(url = URL_desp, params = PARAMS_desp)
      # extracting data in json forma
      data_desp = r_desp.json()
      dados_desp = data_desp['dados']
      #print("Shape:",pd.DataFrame(dados_desp, columns=coluna).shape)
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
        <p style='text-align:center;font-size:30px;font-weight:bold;color:white'>Análise dos Gastos Declarados</p>
    </div>
              """
    st.markdown(html_page, unsafe_allow_html=True)
   
    #html_page = """
    #<div style="background-color:white;padding=20px">
    #    <p style='text-align:center;font-size:18px;font-weight:bold;color:blue'>Nas legislaturas onde foi Eleito </p>
    #</div>
    #          """
    #st.markdown(html_page, unsafe_allow_html=True)


    anos = ['2007','2008','2009','2010', '2011', '2012','2013', '2014', '2015', 
          '2016', '2017', '2018', '2019', '2020','2021']   
  
    ids_leg = [51,52,53,54,55,56]
    
    camara  = Image.open("Images/camara.jpeg")
    
    dados_abertos  = Image.open("Images/dados_abertos.jpeg")

    pbi = Image.open("Images/PBI.png")

    st.sidebar.image(camara,caption="", width=300)

    activities = ["Home","Escolher Deputado","Top N Gastos","Legislaturas Pesquisadas","Power BI","About"]
   
    choice = st.sidebar.selectbox("Selecione uma opção",activities)

   
    flag = False


    ################################################################

    # COLETAR DADOS DAS LEGISLATURAS
    #print("Chamando coletar dados leg: ",ids)
    df_leg = coletar_dados_leg(ids_leg)

    df_leg[['anoInicial', 'mes']] = df_leg['dataInicio'].str.split('-', 1, expand=True)
    df_leg[['anoFinal','mes']] = df_leg['dataFim'].str.split('-', 1, expand=True)
   

    df_leg['id_leg'] = df_leg['id']
    df_leg.drop(['id'], axis=1)
  
    ###############################################################
    # COLETAR DADOS DOS DEPUTADOS
    
    df_nome = pd.read_csv("nomes.csv", encoding='iso-8859-1')
    
    lista_nome = df_nome['nome']
    lista_nome_unique = list(set(lista_nome))
    df_nome_unique = pd.DataFrame()
    df_nome_unique['nome'] = lista_nome_unique
    df_nome_unique.sort_values('nome', ascending=True, inplace=True)
    
    lista_nome_unique = df_nome_unique['nome']

    df_dep3 = pd.read_csv("df_dep_legs_51_56.csv", encoding='iso-8859-1')
    df_dep3_nome_id = df_dep3[['nome','id']]
   

    temp = []
    for i in lista_nome:
         temp.append(i.upper())
    df_dep3['nome'] = temp
    df_dep3_nome_id['nome'] = temp
  

    df_dep3_nome_id.drop_duplicates(inplace=True)
    
    

    dict_dep = df_dep3_nome_id.set_index('nome').to_dict()['id']

    df_dep_nome = pd.DataFrame()
    df_dep_nome = df_dep3['nome']
    
 
    
    #lista_dep = df_dep3_nome_id['nome']
    lista_dep = lista_nome_unique
    #print("Lista dep:", lista_dep)
    #
    df_dep3['id_leg'] = df_dep3['idLegislatura']
    df_dep3.drop(['idLegislatura'], axis=1)
    #print("Dados deputados: ", df_dep3[['nome','id','id_leg']])
    
    
    ################################################################
       

    if choice == activities[0]:
       
        col1,col2 = st.columns(2)
    
       
        #col1.header("Câmara de Deputados")
        col1.image(dados_abertos, width=700)
        
   

       
        
    elif choice == activities[1]:
 
        df_dep_unique = pd.DataFrame(lista_dep, columns=['nome'])
        df_dep_unique['nome_dep'] = df_dep_unique['nome']
        df_dep_unique.set_index('nome', inplace=True)
        lista_dep = df_dep_unique['nome_dep']
       
        st.subheader("Deputados")
        dep_escolhido = st.selectbox("Escolha",lista_dep)

        flag = True

        if st.sidebar.button('Pesquisar'):

            id_dep = dict_dep.get(dep_escolhido)
        
            st.sidebar.image(
                "https://www.camara.leg.br/internet/deputado/bandep/"+str(id_dep).strip()+".jpg",
                width=300
            )
            deputado = df_dep3.loc[df_dep3['nome'] == dep_escolhido]
            deputado['Legislatura'] = deputado['idLegislatura']
            deputado['Partido'] = deputado['siglaPartido']
            deputado['Uf'] = deputado['siglaUf']
            deputado.set_index('Legislatura', inplace=True)
            total_mandatos = str(deputado.shape[0])
            
            
            st.sidebar.write("Mandatos legislativos exercidos") 
           

            st.sidebar.table(deputado[['Partido','Uf']])

            anos = ['2007','2008','2009','2010', '2011', '2012','2013', '2014', '2015','2016', '2017', '2018', '2019', '2020','2021']
            id_legs = [51,52, 53,54,55,56]
            URL_desp = "https://dadosabertos.camara.leg.br/api/v2/deputados/"+str(id_dep)+"/despesas"
            coluna_desp = ['ano','cnpjCpfFornecedor','codDocumento','codLote','codTipoDocumento','dataDocumento','mes',
           'nomeFornecedor','numDocumento','numRessarcimento','parcela','tipoDespesa','tipoDocumento',
           'urlDocumento','valorDocumento','valorGlosa','valorLiquido'] 

            st.subheader("Gastos")
            st.text("Coletando dados via API na Camara de deputados, aguarde terminar...")
            st.text("-> https://dadosabertos.camara.leg.br/api/v2/deputados/idDep/despesas?idLegislatura")

            df_desp = trazer_dados_desp(URL_desp,id_dep, coluna_desp)

            #print("df_desp:", df_desp.shape)
            #df_despesas = df_desp
            df_desp.to_csv("/tmp/despesas.csv")
            df_despesas = pd.read_csv("/tmp/despesas.csv", decimal=",")

            temp = df_despesas
            temp['nome'] = dep_escolhido
            temp['id_dep'] = dict_dep.get(dep_escolhido)
               
                
            #temp[['id_dep','nome','dataDocumento',        'nomeFornecedor','tipoDespesa','valorLiquido']].to_csv("gastos.csv")
        
            
            bar = st.progress(0)
        
            for i in range(26):
                bar.progress(i * 4)
                # wait
                time.sleep(0.4)

            if (df_despesas.shape[0] > 0):
                
                temp = df_despesas
                temp['nome'] = dep_escolhido
                temp['id_dep'] = dict_dep.get(dep_escolhido)
                df_despesas['DateTime'] = pd.to_datetime(df_despesas['dataDocumento'])
                df_despesas['Dia'] = df_despesas['DateTime'].dt.day
                df_despesas['Mes'] = df_despesas['DateTime'].dt.month
                df_despesas['Ano'] = df_despesas['DateTime'].dt.year
                df_despesas['Ano'] = df_despesas['Ano'].replace(".0",'')

                df_despesas['Ano'] = df_despesas['Ano'].astype(str)
                df_despesas['Ano'] = df_despesas['Ano'].replace(".0",'')
                df_despesas['Ano'] = df_despesas['Ano'].replace("nan",'2019')
                
                
                df_despesas['Ano/Mes'] = df_despesas['DateTime'].dt.strftime('%Y/%m')
     
                df_despesas['nomeFornecedor'] = (df_despesas['nomeFornecedor']).str.upper()
                df_despesas['tipoDespesa'] = (df_despesas['tipoDespesa']).str.upper()
                df_despesas['nomeFornecedor'] = (df_despesas['nomeFornecedor']).str.strip()
                df_despesas['tipoDespesa'] = (df_despesas['tipoDespesa']).str.strip()
                df_despesas['nomeFornecedor'] = df_despesas['nomeFornecedor'].replace(".",'')
                df_despesas['tipoDespesa'] = df_despesas['tipoDespesa'].replace(".",'')

                tipo=[]
                for i in df_despesas['tipoDespesa']:
                   #print(i)
                   tipo.append(remove_accents(i))
                #print(tipo)
                df_despesas['tipoDespesa'] = tipo

                nomeForn =[]
                for i in df_despesas['nomeFornecedor']:
                    #print(i)
                    tempfor = remove_accents(i)
                    tempfor2 = tempfor.replace(".",'')
                    nomeForn.append(tempfor2)
                df_despesas['nomeFornecedor'] = nomeForn
                
                temp[['id_dep','nome','Ano/Mes','dataDocumento',        'nomeFornecedor','tipoDespesa','valorLiquido']].to_csv("/tmp/gastos.csv") 

                
                df_despesas['valorLiquido'] = df_despesas['valorLiquido'].fillna(0)
                #print("Valor Liquido:", df_despesas['valorLiquido'])
                df_despesas['Reais'] = df_despesas['valorLiquido'].astype(float)

                           
                #df_despesas['dataDocumento']= pd.to_datetime(df_despesas['dataDocumento'],format='%Y-%m-%d')
                

                #st.table(df_despesas['Ano-Mes'])
                #print("Ano:", str(df_despesas['Ano']).split('.')[0])
                #print(df_despesas.columns)

                #aggr_reais = df_despesas.groupby(['Ano','nomeFornecedor', 'tipoDespesa']).agg({'Reais':'sum'})
                #print("aggr_reais:", aggr_reais.columns)
               
                df_despesas['Total R$'] = df_despesas.groupby(['Ano','nomeFornecedor','tipoDespesa'])["Reais"].transform('sum')
                df_despesas['Total R$'] = df_despesas['Total R$'].fillna(0)

                total=[]
                for i in df_despesas['Total R$']:
                   temp = str(i)
                   temp = temp.split('.')[0]
                   total.append(temp) 
                df_despesas['Total R$'] = total
                
                ano = []
                for i in df_despesas['Ano']:
                    temp = str(i)
                    temp = temp.replace(".0", "")
                    ano.append(temp)
                df_despesas["Ano"] = ano

                print("df_despesas:", df_despesas)

                df_despesas02 = df_despesas[['Ano','nomeFornecedor','tipoDespesa','Total R$']]
                #df_despesas02['Ano'] = df_despesas02['Ano'].astype(int)

                #df_despesas['Count'] = df_despesas.groupby(['Ano','nomeFornecedor','tipoDespesa'])["nomeFornecedor"].transform('count')
          
                #print("Count:", df_despesas)

                df_despesas02.dropna(inplace=True)
               
                df_despesas02.drop_duplicates(inplace=True)
           
                
               
                total_declaracoes = df_despesas02.shape[0]
                #print("Total declarações de gastos:", df_despesas02.shape)        
   
                #print("df_despesas:", df_despesas02[['Ano','nomeFornecedor','tipoDespesa', 'Total']])
                
                st.subheader("Declarações de gastos")
                st.write("Mandatos: "+total_mandatos)
                st.write("Agrupadas por: ano, fornecedor e tipo de despesa: ")
                st.table(df_despesas02[['Ano','nomeFornecedor','tipoDespesa', 'Total R$']])
                #st.table(aggr_reais)
                #print(df_despesas_aggr[['Ano',        'nomeFornecedor','tipoDespesa','valorLiquido','Reais']])
            
                bar = st.progress(0)
        
                for i in range(26):
                    bar.progress(i * 4)
                    #wait
                    time.sleep(0.2)
            
                #st.markdown(get_table_download_link(df_despesas), unsafe_allow_html=True)
                #download_link(df, texto1, texto2)
                nome = dep_escolhido.replace(' ','-')+".csv"
                st.markdown(download_link(df_despesas02[['Ano','nomeFornecedor','tipoDespesa','Total R$']], nome, nome), unsafe_allow_html=True)
                
                deputado = dep_escolhido
                st.header(deputado)
                st.subheader("Gráficos")
                
                #import seaborn as sns
                
                # Load the example tips dataset
                data = df_despesas
                data['Ano'] = data['Ano'].astype('int32')
                data['Total R$'] = data['Total R$'].astype('float32')

                y= data['Total R$']
                x= data['Ano']

                
                plt.rcdefaults()
                fig, ax = plt.subplots()
                
                ax.bar(x, y, align='center',color ='maroon')
                
                ax.set_ylabel('Total R$') 
                ax.set_xlabel('Ano') 
                ax.set_title('Total de Gastos por Ano')
                plt.savefig('Images/plt.png')
                plot = Image.open("Images/plt.png")
                st.image(plot,caption="", width=700)
                #st.pyplot()
                ############################################

                fig1, ax1 = plt.subplots()
                ax1.set_title('Boxplot das Despesas Listadas')
                ax1.boxplot(data['Total R$'])
                ax1.set_xlabel('Total R$') 
                plt.savefig('Images/boxplot.png')
                plot2 = Image.open("Images/boxplot.png")
                st.image(plot2,caption="", width=700)

                ##############################################

                # Figure Size
                #import matplotlib.pyplot as plt
                #import numpy as np
                #import seaborn as sns
                #sns.countplot(y="Ano", hue = "nomeFornecedor", data=data)
                
                #st.write(data[['tipoDespesa', 'Total R$']].drop_duplicates())
                #fig = plt.figure(figsize =(20, 8))
                #plt.ylabel('Total R$',fontsize = 20) 
                #plt.xlabel('Total Gasto',fontsize=12) 
                #plt.title('Total de Gastos por Tipo de Despesa',fontsize = 20)
                #plt.bar(data['tipoDespesa'], data['Total R$'],align='center',color ='maroon')
                #plt.xticks(rotation=90)
                #plt.legend(loc=4,prop={'size': 8})
                #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                #plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                #mode="expand", borderaxespad=0, ncol=3)
                #plt.legend(loc='#upper center', bbox_to_anchor=(0.5, -0.05),
                #fancybox=True, shadow=True, ncol=5)
                
                # Show Plot
                #plt.savefig('Images/plt_despesa.png')
                #plot3 = Image.open("Images/plt_despesa.png")
                #st.image(plot3,caption="", width=700)


                #fig,ax = plt.subplots()
                #ax.bar(data['tipoDespesa'], data['Total R$'],align='center',color ='maroon')
                #x_legend = data['tipoDespesa']
                #t = ax.text(.7,.2,x_legend)
                #fig.subplots_adjust(right=.65)

                
                # Show Plot
                #plt.savefig('Images/plt_despesa01.png')
                #plot4 = Image.open("Images/plt_despesa01.png")
                #st.image(plot4,caption="", width=700)
 
                


#######################################################3

           

                #st.subheader("Basic Math")
                #df_despesas02['Total Reais'] = pd.to_numeric(df_despesas02['Total R$'])

                #agg_func_describe = {'Total Reais': ['sum', 'median', 'std']}
                #df_math = df_despesas02.groupby(['tipoDespesa']).agg(agg_func_describe)
                #st.write(df_math)
                
                 
                #st.subheader("Selection - Min Max")
                #agg_func_selection = {'Total Reais': [np.min, np.max]}
                #df_selection = df_despesas02.groupby(['tipoDespesa']).agg(agg_func_selection)
                #print("Columns", df_selection.columns)
                #df_selection.rename(columns={'Total Reais amin':'Valor Minimo', 'Total Reais amax':'Valor Maximo'})
                #df_selection = df_selection.rename(columns={'amin': 'Minimo', 'amax': 'Maximo'})
                #df_selection.index.set_names(["Valor Minimo", "Valor Maximo"], inplace=True)
                #st.write(df_selection)

                #################

                #df_idxmax = df_despesas02.loc[df_despesas02.reset_index().groupby(['nomeFornecedor'])['Total Reais'].idxmax()]

                #df_idxmax = df_despesas02.loc[df_despesas02.reset_index().groupby(['nomeFornecedor'])['Total R$'].idxmax()]

                
                #df_idxmax = df_despesas02.groupby(level=0).apply(lambda group: group.nlargest(1, columns='Total Reais')).reset_index(level=-1, drop=True)
                #st.table(df_idxmax)

                #from scipy.stats import mode
                #st.subheader("Mode")
                #agg_func_stats = {'Total Reais': [mode, pd.Series.mode]}
                #df_stat = df_despesas02.groupby(['tipoDespesa']).agg(agg_func_stats)
                #st.table(df_stat)
                
            else:
                st.write("Sem dados informados")
       
        

    elif choice == "Legislaturas Pesquisadas":
        st.subheader("Periodos pesquisados")
       
        bar = st.progress(0)
        
        for i in range(26):
                bar.progress(i * 4)
                #wait
                time.sleep(0.2)
        df_leg = pd.read_csv("df_leg_51-56.csv")
        df_leg.set_index('id', inplace=True)
        
        st.table(df_leg[['dataInicio', 'dataFim']])
        bar = st.progress(0)
        
        for i in range(26):
                bar.progress(i * 4)
                #wait
                time.sleep(0.01)

    elif choice == "Top N Gastos":
        
   
        
        df_gastos = pd.read_csv("/tmp/gastos.csv", decimal=".")
        df_gastos['Reais'] = df_gastos["valorLiquido"]
        nome = list(set(df_gastos['nome']))
        nome = str(nome).replace("['",'')
        nome = str(nome).replace("']",'')
        
        id_dep = list(set(df_gastos['id_dep']))
        id_dep = str(id_dep).split(':')
        
        id_dep = str(id_dep).replace("['",'')
        id_dep = str(id_dep).replace("']",'')
        id_dep = str(id_dep).replace("[",'')
        id_dep = str(id_dep).replace("]",'')
        #st.write(id_dep)
        
        st.subheader(nome)
        x = st.sidebar.slider('Top-N Gastos', min_value = 1, max_value=7, value = 3 )
        st.markdown("# Top "+str(x))
            
        st.subheader("Maiores despesas por tipo")  
        
        df_gastos['Tipo Despesa    /    Reais'] = df_gastos['Reais'].astype(int)
        df_serie = df_gastos.groupby(['tipoDespesa'])['Tipo Despesa    /    Reais'].sum().nlargest(x)
        df = df_serie.to_frame().sort_values(by='Tipo Despesa    /    Reais', ascending=False)
        st.table(df.style.format('{:.0f}'))
        
        st.subheader("Maiores despesas por fornecedores")
        
        df_gastos['Fornecedor    /    Reais'] = df_gastos['Reais'].astype(int)
        df_serie = df_gastos.groupby(['nomeFornecedor'])['Fornecedor    /    Reais'].sum().nlargest(x)
        df = df_serie.to_frame().sort_values(by='Fornecedor    /    Reais', ascending=False)
        st.table(df.style.format('{:.0f}'))
       
        st.subheader("Maiores qtdes de serviços prestados por fornecedor")
        df_gastos['Fornecedor    /    Quantidade'] = df_gastos['nomeFornecedor']
        
        st.table(df_gastos['Fornecedor    /    Quantidade'].value_counts().head(x))

        st.subheader("Maiores qtdes de serviços prestados por tipo de despesa")
        df_gastos['Tipo Despesa    /    Quantidade'] = df_gastos['tipoDespesa']

        st.table(df_gastos['Tipo Despesa    /    Quantidade'].value_counts().head(x))
        
        
   
        st.sidebar.image(
                "https://www.camara.leg.br/internet/deputado/bandep/"+str(id_dep).strip()+".jpg",
                width=300
            )
        
        
        #st.table(df_gastos[['dataDocumento',        'nomeFornecedor','tipoDespesa','valorLiquido']])

        bar = st.progress(0)
        
        for i in range(26):
                bar.progress(i * 4)
                #wait
                time.sleep(0.2)
       
    elif choice == 'Power BI':
        if st.button("Abrir análises usando Power BI"):
            js = "window.open('https://app.powerbi.com/view?r=eyJrIjoiZDJmYmIxYzMtNzkwYy00NTYxLTkzZTUtYTFmYTRiMTE4ZWNiIiwidCI6ImFmZmE4YzZlLWE1YTUtNDhjMS04MjYxLWU0MDZmZWE3YmNiNiJ9&pageName=ReportSectiona55da1d5c48609dc6067')"
            #js = "window.open('https://app.powerbi.com/view?r=eyJrIjoiMTc4ZGI2NmEtOTkzZi00ODhmLWE5ODQtMjAwZDFhYWFmODkyIiwidCI6IjQwZjQ2YmVkLWNjZTItNGVkMi04YzQ5LTRhYzU5M2M1MDcwOCJ9&pageName=ReportSectiona55da1d5c48609dc6067')"
            #js = "window.open('https://app.powerbi.com/view?r=eyJrIjoiZDJmYmIxYzMtNzkwYy00NTYxLTkzZTUtYTFmYTRiMTE4ZWNiIiwidCI6ImFmZmE4YzZlLWE1YTUtNDhjMS04MjYxLWU0MDZmZWE3YmNiNiJ9&pageName=ReportSectiona55da1d5c48609dc6067')"
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
        
        st.image(pbi,caption="", width=700)

    elif choice == 'About':
        #st.sidebar.image(about,caption="", width=300, height= 200)
        st.subheader("Built with Streamlit")
        
        st.write("Dados coletados via API da Camara de Deputados do Brasil.")
        st.write("https://dadosabertos.camara.leg.br/swagger/api.html")
        st.subheader("Observação")
        st.write("-> Foram feitos tratamentos diferentes nas bases de gastos.")
        st.write("-> Isso explica a diferença de valores apresentados no app e no Power BI")
        
        #st.subheader("9 Tipos de Despesas:")
        #st.write("-> MANUTENÇÃO DE ESCRITÓRIO DE APOIO À ATIVIDADE PARLAMENTAR")
        #st.write("-> AQUISIÇÃO OU LOC. DE SOFTWARE; SERV. POSTAIS; ASS.")
        #st.write("-> DIVULGAÇÃO DA ATIVIDADE PARLAMENTAR")
        #st.write("-> AQUISIÇÃO DE MATERIAL DE ESCRITÓRIO")
        #st.write("-> COMBUSTÍVEIS E LUBRIFICANTES")
        #st.write("-> PASSAGEM AÉREA - REEMBOLSO")
        #st.write("-> PASSAGEM AÉREA - RPA")
        #st.write("-> SERVIÇOS POSTAIS")
        #st.write("-> TELEFONIA")
        
        st.subheader("by Giovana Titoto / Claudio Soares / Silvio Lima")
        
        #if st.button("Linkedin"):
        #    js = "window.open('https://www.linkedin.com/in/silviocesarlima/')"
        #    html = '<img src onerror="{}">'.format(js)
        #    div = Div(text=html)
        #    st.bokeh_chart(div)
   
    

     
    
    
if __name__ == '__main__':
    main()
