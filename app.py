import streamlit as st
from openai import OpenAI
import time

client = OpenAI(api_key=st.secrets["openai"]["api_key"])
ASSISTANT_ID = st.secrets["openai"]["assistant_id"]

def get_assistant_response(thread, user_message, message_placeholder):
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run.status == 'completed':
                break
            elif run.status == 'failed':
                raise Exception("Run failed")
            time.sleep(0.5)

        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        response = messages.data[0].content[0].text.value
        message_placeholder.markdown(response)
        return response

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        message_placeholder.error(error_msg)
        return error_msg

def main():
    st.set_page_config(
        page_title="SYLVAIN LEVY",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
        <style>
        .main-title {
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 2.5em;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 0;
            font-weight: 300;
        }
        .subtitle {
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 1.5em;
            color: #E0E0E0;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 300;
        }
        .version {
            font-family: 'Helvetica Neue', sans-serif;
            color: #808080;
            text-align: center;
            font-size: 1.1em;
            margin-top: -1rem;
            margin-bottom: 2rem;
        }
        
        .stApp {
            color: #E0E0E0;
        }
        
        .stChatMessage {
            background-color: #2D2D2D;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .stChatInputContainer {
            border-color: #404040;
            max-width: 80% !important;
            margin: auto;
        }
        
        .css-1d391kg {
            background-color: #252526;
        }
        
        .stButton>button {
            background-color: #404040;
            color: #FFFFFF;
            border: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #505050;
        }

        /* User icon */
        .stChatMessage.user [data-testid="StChatMessageAvatar"] div {
            background-color: transparent !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext x='50' y='65' fill='%23E0E0E0' font-family='Didot, serif' font-size='70' font-style='italic' text-anchor='middle'%3EU%3C/text%3E%3C/svg%3E") !important;
            background-size: contain !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
        }

        /* Assistant icon */
        .stChatMessage.assistant [data-testid="StChatMessageAvatar"] div {
            background-color: transparent !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext x='50' y='65' fill='%23E0E0E0' font-family='Didot, serif' font-size='70' font-style='italic' text-anchor='middle'%3EK%3C/text%3E%3C/svg%3E") !important;
            background-size: contain !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    def add_bg_from_local(image_file):
        import base64
        import os
        
        if os.path.exists(image_file):
            with open(image_file, 'rb') as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                
                st.markdown(
                    f"""
                    <style>
                    .stApp {{
                        background-image: url("data:image/jpg;base64,{b64}");
                        background-size: cover;
                        background-position: center;
                        background-repeat: no-repeat;
                        background-attachment: fixed;
                    }}
                    
                    .stApp::before {{
                        content: "";
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background-color: rgba(30, 30, 30, 0.85);
                        z-index: -1;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
    
    add_bg_from_local('background.jpg')

    st.markdown('<h1 class="main-title">SYLVAIN LEVY</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">Art and Technologies</h2>', unsafe_allow_html=True)
    st.markdown('<p class="version">α V 0.1</p>', unsafe_allow_html=True)

    st.markdown(
        "Hello, I'm Karen, Sylvain's daughter. Ask me anything about his pioneering work in art collection and digital technologies..."
    )

    if "thread" not in st.session_state:
        st.session_state.thread = client.beta.threads.create()
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about Sylvain's work in art and technology..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = get_assistant_response(st.session_state.thread, prompt, message_placeholder)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()