# Importando bibliotecas essenciais para o funcionamento do script
import os
import streamlit as st # Importando a biblioteca Streamlit para criação de aplicações web
from langchain.llms import OpenAI # Importando o modelo de linguagem da OpenAI
from langchain.prompts import PromptTemplate # Importando a classe para templates de prompt
from langchain.chains import LLMChain, SequentialChain # Importando classes para criar cadeias de LLM
from langchain.memory import ConversationBufferMemory # Importando memória de buffer de conversação
from langchain_openai import ChatOpenAI
import requests # Importando a biblioteca para realizar requisições HTTP

# Configurando a chave de API da OpenAI no ambiente
os.environ['OPENAI_API_KEY'] = st.secrets["openai_api_key"]

headers = {
    'Authorization': 'Bearer ' + st.secrets["jina_api_key"] 
}

# Adicionar a imagem no cabeçalho
image_url = "https://analise.com/img/logo.png"
st.image(image_url, use_column_width=True)

# Adicionar o nome do aplicativo
st.subheader("Copy Generator - Análise Editorial")
link = st.text_input('🔗 Digite o link da matéria...') # Campo de entrada para o usuário escrever o tema

# Definindo templates de prompt para o título do vídeo e o roteiro
copy_template = PromptTemplate(
    input_variables = ['article'], 
    template = """
    Atue como um analista de social media especializado em linkedin, Escreva uma copy para um post no linkedin sobre o artigo... {article}
    
    <regras>
     - O texto deve ter no máximo 1500 caracteres
     - Sempre coloque uma CTA para a matéria completa com o endereço do link da matéria escrito, por exemplo: https:://.
     - Não utilize tags HTML
     - Termine o texto sempre provocando o leitor a interagir nos comentários com base em sua opinião.
     - Utilize sempre as hashtags #AnaliseEditorial #Direito #Juridico, adicione outras de acordo com o tema do artigo para que melhore o alcance do post.
    <regras>
    """
)

# Mostrando os resultados na tela se houver um prompt
if link:
    # Inicializando o modelo de linguagem com uma temperatura de 0.9
    #llm = OpenAI(temperature=0.9)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

    # Configurando a cadeia de LLM para gerar títulos
    copy_chain = LLMChain(llm=llm, prompt=copy_template, verbose=True, output_key='copy')
    article = requests.get('https://r.jina.ai/'+link, headers=headers)
    copy = copy_chain.run(article=article.text) # Gera a copy

    # Inicializando o wrapper da API Serper.dev
    #google_search = SerperAPIWrapper(api_key=st.secrets["serper_api_key"])

    st.write(copy) # Exibe o título gerado
