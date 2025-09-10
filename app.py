import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

st.title(" Chat via Groq + LangChain")

# Entrada da API Key
api_key = st.text_input("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",type="password")

# Seleção de modelo
model = st.sidebar.selectbox(
    "Selecione o modelo:",
    ["deepseek-r1-distill-llama-70b"])

# Entrada do prompt
prompt = st.text_area("Digite sua pergunta: Olá quem é você?")

if st.button ("Gerar respota"):
    if not api_key:
        st.error("Por favor, insira sua API Key.")
    else:
        try:   
            llm = ChatGroq(api_key=api_key, model=model)

            #Template de prompt
            template = ChatPromptTemplate.from_messages ([
                ("system", "Você é um vendedor profissional e deve sempre responder em português do Brasil."),
                ("human", "{prompt}")
            ])

            # Cria a cadeia
            chain = template | llm

            # Executa cadeia

            with st.spinner("Gerando resposta..."):
                res = chain.invoke({"prompt": prompt})
                st.success ("Resposta gerada com sucesso!")
                st.write("### Resposta:")
                st.write(res.content)

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")


