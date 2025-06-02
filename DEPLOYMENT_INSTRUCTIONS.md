# Deployment Instructions for Project Simone

## 🚀 Steps to Deploy with Data

### 1. Create the Episode Data ZIP File (locally)

```bash
cd project_simone
python create_data_zip.py
```

This will create `episode_data.zip` containing all your analyzed episode files.

### 2. Push Code Changes to GitHub

```bash
git push origin main
```

### 3. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Select your repository: `niklaskobi/simone_v2`
3. Set the main file path to: `app_with_upload.py`
4. Click "Deploy"

### 4. Upload Data to Your App

1. Once deployed, visit your app URL
2. You'll see the upload interface
3. Upload the `episode_data.zip` file you created in step 1
4. The app will extract the files and reload with your data

### 5. Set Your API Key

1. Click the "🔑 API Key" section in the sidebar
2. Enter your Anthropic API key
3. The app will remember it for your session

## 📝 What Changed

### Fixed Issues:
- ✅ Config now uses deployment-friendly paths
- ✅ Data upload handles nested zip structures properly
- ✅ Better debugging info during upload
- ✅ Deployment config prioritized over local config

### New Files:
- `config/settings_deployment.yaml` - Deployment-specific configuration
- `create_data_zip.py` - Helper to create data zip file
- `app_with_upload.py` - Main app with upload functionality

## 🔧 Troubleshooting

### If data doesn't load after upload:
1. Check the browser console for errors
2. Try refreshing the page
3. Re-upload the zip file
4. Check that the zip contains JSON files at the root level

### If you see "No episodes found":
1. Make sure your zip file contains the episode JSON files
2. Verify files aren't in a nested folder within the zip
3. Check that files have `.json` extension

## 📦 Creating the Data ZIP

The `create_data_zip.py` script:
- Finds all episode JSON files
- Excludes index and checkpoint files
- Creates a flat zip with just the episode files
- Shows file count and size

Make sure to adjust the `source_path` in the script if your data is in a different location.

## 🎉 Success!

Once everything is set up, you'll have:
- A fully deployed philosophical exploration app
- All your episode data loaded
- Interactive visualizations working
- Chat functionality with Claude Opus 4
- Shareable URL for your friends

Enjoy exploring the philosophical universe! 🌌