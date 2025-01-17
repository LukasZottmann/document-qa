import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💛 PublixBot")
st.write(
    "Olá, sou uma inteligência artificial pré-treinada desenvolvida pelo Instituto Publix para armazenar documentos importantes e te dar respostas com base neles."
    "Para usar esse aplicativo, você vai precisa de uma chave da API da OpenAI, onde você pode conseguir [aqui](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Por favor adicione sua chave da API do OpenAI para continuar.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=[".pdf"],
        accept_multiple_files = True
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Faça uma pergunta sobre os documentos!",
        placeholder="Você consegue me fazer um resumo?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        documents = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's some documents: {documents} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
