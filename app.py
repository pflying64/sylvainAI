
import streamlit as st
from openai import OpenAI
import time

# Initialize OpenAI client
client = OpenAI()

# ANASAEA SEO SEARCH ENGINE Assistant ID
ASSISTANT_ID = "asst_P5TO2T0CLrDSbsSspmNWLTw9"

def get_assistant_response(thread, user_message):
   # Add the user message to the thread
   client.beta.threads.messages.create(
       thread_id=thread.id,
       role="user",
       content=user_message
   )

   # Run the Assistant
   run = client.beta.threads.runs.create(
       thread_id=thread.id,
       assistant_id=ASSISTANT_ID
   )

   # Wait for the completion
   while run.status != "completed":
       time.sleep(1)
       run = client.beta.threads.runs.retrieve(
           thread_id=thread.id,
           run_id=run.id
       )

   # Get the assistant's messages
   messages = client.beta.threads.messages.list(thread_id=thread.id)
   
   # Return the latest assistant message
   for msg in messages:
       if msg.role == "assistant":
           return msg.content[0].text.value
   
   return "No response received"

def main():
   st.set_page_config(
       page_title="ANASAEA Art Search",
       page_icon="🎨",
       layout="wide"
   )

   st.title("🎨 ANASAEA Art Search Engine")
   st.markdown("Explore our artists and their artworks through natural conversation")
   
   # Initialize thread in session state
   if "thread" not in st.session_state:
       st.session_state.thread = client.beta.threads.create()
       st.session_state.messages = []

   # Display chat history
   for message in st.session_state.messages:
       with st.chat_message(message["role"]):
           st.markdown(message["content"])

   # Chat input
   if prompt := st.chat_input("Search for artists, styles, prices, or ask how to use ANASAEA..."):
       # Display user message
       with st.chat_message("user"):
           st.markdown(prompt)
       st.session_state.messages.append({"role": "user", "content": prompt})

       # Get and display assistant response
       with st.chat_message("assistant"):
           with st.spinner("Searching ANASAEA database..."):
               response = get_assistant_response(st.session_state.thread, prompt)
               st.markdown(response)
               st.session_state.messages.append({"role": "assistant", "content": response})

   # Sidebar with instructions and examples
   with st.sidebar:
       st.title("Help & Examples")
       
       # Usage Instructions Tab
       st.markdown("### How to Use ANASAEA")
       st.markdown("""
       You can ask about:
       - How to browse and purchase artworks
       - How the platform works
       - Instructions for artists and buyers
       - Platform features and functionalities
       
       Example questions:
       - "How do I purchase an artwork?"
       - "How can artists join ANASAEA?"
       - "What are the payment methods?"
       - "How does the art authentication work?"
       """)
       
       st.markdown("### Art Search Examples")
       st.markdown("""
       Search our collection by:
       - Available artworks under specific prices
       - Artists from specific countries
       - Artworks in particular styles
       - Details about specific artists
       
       Example queries:
       - "Show me abstract paintings under $5000"
       - "Tell me about French artists"
       - "What artworks are currently available?"
       - "Show me landscape paintings"
       """)
       
       st.divider()
       
       # Reset button with confirmation
       if st.button("Start New Search"):
           st.session_state.thread = client.beta.threads.create()
           st.session_state.messages = []
           st.rerun()

if __name__ == "__main__":
   main()
