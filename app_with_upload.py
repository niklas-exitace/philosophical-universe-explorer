"""
Modified app that allows data upload on first run
"""

import streamlit as st
import os
import zipfile
import shutil
from pathlib import Path

# Check if data exists
data_path = Path("data/processed")
data_files = list(data_path.glob("*.json")) if data_path.exists() else []

if len(data_files) == 0:
    st.title("🚀 Welcome to Philosophical Universe Explorer!")
    st.markdown("""
    ### 📁 First Time Setup: Upload Episode Data
    
    The app needs episode data to function. Please upload the data file.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose episode_data.zip file",
        type=['zip'],
        help="This file contains all analyzed episode data"
    )
    
    if uploaded_file is not None:
        with st.spinner("📦 Extracting episode data..."):
            # Create data directory
            data_path.mkdir(parents=True, exist_ok=True)
            
            # Save and extract zip
            zip_path = Path("temp_data.zip")
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract files
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(data_path)
            
            # Clean up
            zip_path.unlink()
            
            st.success("✅ Data uploaded successfully! Reloading app...")
            st.balloons()
            st.experimental_rerun()
    
    st.markdown("---")
    st.info("""
    **Don't have the data file?**
    
    1. Run `python upload_data.py` locally to create it
    2. Or download from the original source
    3. The file should be named `episode_data.zip`
    """)
    
else:
    # Run the main app
    exec(open('app_complete.py').read())