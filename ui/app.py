import streamlit as st
import sys
import os
import json
import subprocess
import shutil

# Enable imports from root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.retriever import search
from llm.safe_generate import safe_generate
from migrate.python_to_go import convert_python_to_go

STYLING = """
<style>
    .stChatInput {position: fixed; bottom: 30px;}
    .block-container {padding-top: 2rem;}
    /* Hide the Streamlit Deploy button and Menu */
    .stDeployButton {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

def main():
    st.set_page_config(page_title="TeamBeta RAG & Migration", layout="wide")
    st.markdown(STYLING, unsafe_allow_html=True)

    st.sidebar.title("TeamBeta Toolkit")
    page = st.sidebar.radio("Navigate", ["RAG Chat", "Migration Assistant"])

    if page == "RAG Chat":
        render_rag_page()
    elif page == "Migration Assistant":
        render_migration_page()

def get_available_modules():
    vector_dir = os.path.join("vector_db")
    if os.path.exists(vector_dir):
        return [f.replace(".index", "") for f in os.listdir(vector_dir) if f.endswith(".index")]
    return []

def render_rag_page():
    st.title("Knowledge Base Chat")
    
    modules = get_available_modules()
    
    if not modules:
        st.warning("No knowledge modules found. Please build the vector index first.")
        # Optional: could keep a hidden way to build, but user asked for "before state"
        return

    selected_module = st.sidebar.selectbox("Select Module", modules)

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "context" in msg:
                with st.expander("View Retrieved Context"):
                    for i, chunk in enumerate(msg["context"]):
                        st.markdown(f"**Chunk {i+1}**")
                        st.text(chunk)

    if prompt := st.chat_input(f"Ask about {selected_module}..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Step 1: Retrieval
            with st.status("Retrieving context...", expanded=True) as status:
                context_chunks = search(prompt, selected_module)
                status.update(label="Context Retrieved", state="complete", expanded=False)
            
            # Step 2: Generation
            with st.spinner("Generating answer..."):
                context_str = "\n".join(context_chunks)
                full_prompt = f"""
You are an expert on the ERPNext {selected_module} module.

## Context
{context_str}

## Question
{prompt}
"""
                response = safe_generate(full_prompt)
                st.markdown(response)

        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "context": context_chunks
        })

def render_migration_page():
    st.title("Migration Assistant")
    
    tab1, tab2 = st.tabs(["Code Converter (Py - Go)", "Codebase Analyzer"])
    
    with tab1:
        st.subheader("Python to Go Converter")
        
        # Initialize Session State
        if "py_code_input" not in st.session_state:
            st.session_state.py_code_input = ""
        if "go_code_output" not in st.session_state:
            st.session_state.go_code_output = ""

        col1, col2 = st.columns(2)
        with col1:
            # Added key for callback access
            if "file_path_input" not in st.session_state:
                st.session_state.file_path_input = "data/sample.py"
            input_file = st.text_input("Python File Path", value="data/sample.py", key="file_path_input")
            
        if st.button("Load File"):
            if os.path.exists(input_file):
                with open(input_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    st.session_state.py_code_input = content
                
                if not content.strip():
                    st.warning(f"Loaded {os.path.basename(input_file)}, but the file is empty!")
                else:
                    st.success(f"Loaded {os.path.basename(input_file)}")
            else:
                st.error("File not found!")

        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("### Python Source")
            # Bind to session state
            py_code = st.text_area("Python Code", height=400, key="py_code_input")
            
        with col_b:
            st.markdown("### Go Output")
            # Bind to session state
            go_code = st.text_area("Go Code", height=400, key="go_code_output")

        def run_conversion():
            # Callback to handle conversion before render
            src = st.session_state.py_code_input
            path = st.session_state.file_path_input
            
            if not src.strip():
                st.warning("Please load or enter Python code first.")
                return

            try:
                # Note: Spinners inside callbacks might not render ideally in all versions, 
                # but let's try to keep the logic simple.
                generated_go = convert_python_to_go(path, code_content=src)
                st.session_state.go_code_output = generated_go
                # We don't need st.rerun() in a callback, it happens distinct from the script run
            except Exception as e:
                st.error(f"Conversion Failed: {e}")

        st.button("Convert to Go", on_click=run_conversion)

        if st.button("Run & Verify"):
            verify_execution(py_code, st.session_state.go_code_output)

    with tab2:
        st.subheader("Module Analyzer")
        module_name = st.text_input("Enter Module Name (e.g. accounts)")
        
        if st.button("Analyze Module"):
            with st.spinner("Analyzing AST..."):
                subprocess.run(["python", "Analyzer/analyzer.py", module_name])
                st.success("Analysis Complete!")
                
                # Load Results
                func_file = f"output/{module_name}_functions.json"
                if os.path.exists(func_file):
                    with open(func_file, "r") as f:
                        data = json.load(f)
                    st.metric("Functions Found", len(data))
                    st.dataframe(data)

def verify_execution(py_code, go_code):
    st.divider()
    st.write("### Execution Verification")
    
    # 1. Run Python
    try:
        py_res = subprocess.run(
            [sys.executable, "-c", py_code], 
            capture_output=True, text=True, timeout=5
        )
        st.code(py_res.stdout, language="text", line_numbers=True)
    except Exception as e:
        st.error(f"Python Execution Failed: {e}")
        return

    # 2. Run Go
    try:
        with open("temp.go", "w", encoding="utf-8") as f:
            f.write(go_code)
        
        go_res = subprocess.run(
            ["go", "run", "temp.go"],
            capture_output=True, text=True, timeout=5
        )
        st.code(go_res.stdout, language="text", line_numbers=True)
    except Exception as e:
        st.error(f"Go Execution Failed: {e}")
        return
    finally:
        if os.path.exists("temp.go"):
            try:
                os.remove("temp.go")
            except:
                pass

    # 3. Compare
    if py_res.stdout.strip() == go_res.stdout.strip():
        st.success("Outputs Match Perfectly!")
    else:
        st.error("Outputs Do Not Match")
        st.markdown("**Diff:**")
        # simple diff view could be added here

if __name__ == "__main__":
    main()
