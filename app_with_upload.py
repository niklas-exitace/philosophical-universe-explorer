"""
Modified app that allows data upload on first run
"""

import streamlit as st
import os
import zipfile
import shutil
from pathlib import Path
import sys

# MUST be the first Streamlit command
st.set_page_config(
    page_title="Philosophical Universe - Project Simone",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
                # Check if files are in a subdirectory
                file_list = zip_ref.namelist()
                
                # If all files are in a subdirectory, extract to parent
                if all('/' in f for f in file_list if not f.endswith('/')):
                    # Files are in subdirectory, extract to temp and move
                    temp_extract = Path("temp_extract")
                    zip_ref.extractall(temp_extract)
                    
                    # Find JSON files and move them
                    for json_file in temp_extract.rglob("*.json"):
                        target = data_path / json_file.name
                        shutil.move(str(json_file), str(target))
                    
                    # Clean up temp directory
                    shutil.rmtree(temp_extract)
                else:
                    # Files are at root level, extract directly
                    zip_ref.extractall(data_path)
            
            # Clean up
            zip_path.unlink()
            
            # Verify extraction
            extracted_files = list(data_path.glob("*.json"))
            st.success(f"✅ Data uploaded successfully! Extracted {len(extracted_files)} episode files.")
            
            if extracted_files:
                st.info(f"Sample files: {', '.join([f.name for f in extracted_files[:3]])}")
            
            st.balloons()
            st.rerun()
    
    st.markdown("---")
    st.info("""
    **Don't have the data file?**
    
    1. Run `python upload_data.py` locally to create it
    2. Or download from the original source
    3. The file should be named `episode_data.zip`
    """)
    
else:
    # Run the main app
    st.success(f"✅ Found {len(data_files)} episode data files!")
    
    # Import and run the main app properly
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Import after data is ready
    from app_complete import main
    main()