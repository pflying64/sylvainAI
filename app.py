import streamlit as st
from openai import OpenAI
import time

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["env"]["OPENAI_API_KEY"])

ASSISTANT_ID = "asst_hXc1J6AmWynMBSpFLThNznEl"

def get_assistant_response(thread, user_message, message_placeholder):
    """
    Get response from the assistant and display it in real-time
    """
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    stream = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
        stream=True
    )

    current_text = ""
    for event in stream:
        if event.event == "thread.message.delta":
            delta = event.data.delta.content[0].text.value
            current_text += delta
            message_placeholder.markdown(current_text)

    return current_text

def main():
    # Page configuration with dark theme
    st.set_page_config(
        page_title="Sylvain DB",
        page_icon="📚",
        layout="centered"
    )

    # Set background image
    def add_bg_from_local(image_file):
        import base64
        
        def get_base64_of_bin_file(bin_file):
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()

        bin_str = get_base64_of_bin_file(image_file)
        
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            
            /* Dark overlay for better readability */
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
    
    # Add local background image
    add_bg_from_local('background.jpg')

    # Custom CSS for dark mode and elegant styling
    st.markdown("""
        <style>
        /* Base styles */
        .stApp {
            color: #E0E0E0;
        }
        
        /* Header styling */
        .main-header {
            font-family: 'Helvetica Neue', sans-serif;
            color: #FFFFFF;
            font-weight: 300;
            margin-bottom: 2rem;
        }
        
        /* Chat message container */
        .stChatMessage {
            background-color: #2D2D2D;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        /* Chat input styling */
        .stChatInputContainer {
            border-color: #404040;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #252526;
        }
        
        /* Button styling */
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
        </style>
    """, unsafe_allow_html=True)

    # Main title with custom styling
    st.markdown('<h1 class="main-header">Sylvain DB</h1>', unsafe_allow_html=True)
    st.markdown(
        "Explore the art world through the knowledge of renowned collector Sylvain Levy",
        help="Ask questions about art collections, artists, exhibitions, and more"
    )

    # Initialize chat session
    if "thread" not in st.session_state:
        st.session_state.thread = client.beta.threads.create()
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about art collections, artists, exhibitions..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = get_assistant_response(st.session_state.thread, prompt, message_placeholder)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Minimal sidebar with essential information
    with st.sidebar:
        st.markdown("### About Sylvain DB")
        st.markdown("""
        This AI assistant embodies the knowledge and expertise of Sylvain Levy, 
        offering insights into art collection, curation, and appreciation.
        """)
        
        st.divider()
        
        if st.button("New Conversation", type="primary"):
            st.session_state.thread = client.beta.threads.create()
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()