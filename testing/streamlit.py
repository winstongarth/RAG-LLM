import testing.streamlit as st
from testing.streamlit_module import process_query  

"""

RUN COMMAND: streamlit run app/streamlit.py

"""

def main():
    st.title("Document Query Tool")

    # Mode selection
    mode = st.selectbox("Choose a mode:", ["answer", "summarize"], index=0)

    # User input for the query
    query_text = st.text_area("Enter your query here:", height=150)
    if query_text:
        # Button to trigger processing
        if st.button("Process"):
            with st.spinner("Processing..."):
                response, sources = process_query(mode, query_text)  
                st.write("### Response")
                st.write(response)
                st.write("### Sources")
                st.write(sources)

if __name__ == "__main__":
    main()