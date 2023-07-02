import os
from apikey import API_KEY

import streamlit as st
from langchain import OpenAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.agents import create_csv_agent
from htmlTemplates import css, bot_template, user_template


def main():
    os.environ['OPENAI_API_KEY'] = API_KEY
    st.set_page_config(page_title="AutoGPT-Data Query", page_icon=":data:")
    st.write(css, unsafe_allow_html=True)

    st.header('Auto Data Query')

    with st.sidebar:
        st.subheader("Your Dataset")
        uploadedfile = st.file_uploader(
            "Upload your dataset here and click on 'Process'",
            accept_multiple_files=False,
        )
        if st.button("Process"):
            if uploadedfile is not None:
                filepath = os.path.join("data", uploadedfile.name)
                with open(filepath, "wb") as f:
                    f.write(uploadedfile.getbuffer())
                st.success("Dataset uploaded successfully!")
                st.session_state.filepath = filepath
            else:
                st.error("Please upload a dataset first!")

    if "filepath" in st.session_state:
        filepath = st.session_state.filepath
        loader = CSVLoader(filepath)
        data = loader.load()

        llm = OpenAI(temperature=0)  # type: ignore

        agent = create_csv_agent(llm, filepath, verbose=True)

        prompt = st.text_input('Describe your data query here to get the result:')

        if prompt:
            result = agent.run(prompt)  # type: ignore

            st.write(user_template.replace("{{MSG}}", prompt), unsafe_allow_html=True)
            st.write(bot_template.replace("{{MSG}}", result), unsafe_allow_html=True)
    else:
        st.warning("Please upload a dataset first!")


if __name__ == '__main__':
    main()
