import os
from apikey import API_KEY

import streamlit as st
from langchain import OpenAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.agents import create_csv_agent

os.environ['OPENAI_API_KEY'] = API_KEY
st.title('Auto Data Query')

prompt = st.text_input('Describe your data query here to get the result:')

filepath = "data/bank_customer_data.csv"
loader = CSVLoader(filepath)
data = loader.load()

llm = OpenAI(temperature=0)  # type: ignore

agent = create_csv_agent(llm, filepath, verbose=True)

if prompt:
    result = agent.run(prompt)
    # agent.run("What is the total number of customers in each country?")
    # agent.run("Show to customer that have top 10 credit score?")

    st.write(result)
