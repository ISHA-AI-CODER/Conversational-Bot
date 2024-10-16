import streamlit as st
import defines 
from dotenv import load_dotenv 


def main():
    load_dotenv()

    st.set_page_config(page_title='chat_with_documents', page_icon=':rocket:')

    if 'conversation' not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header('Chat with multiple documents :books:')
    promt = st.chat_input('Asking question ...')


    with st.sidebar:
        st.subheader('Your documents:')

        files = st.file_uploader('Upload your documents here:', accept_multiple_files=True, type=['pdf','txt'])

        if st.button('Start processing'):
            with st.spinner('Processing...'):
                # Get text
                raw_text = defines.read_files(files)

                # Chunk text
                chunked_text = defines.get_text_chunked(raw_text)

                # Create database
                vectorstore = defines.get_vectorstore(chunked_text)
                
                # Create conversation
                st.session_state.conversation = defines.get_conversation_chain(vectorstore)

                st.markdown('Done processing')

    if promt:
        defines.handle_user_input(st.session_state.conversation, promt)

if __name__=="__main__":
    main()
