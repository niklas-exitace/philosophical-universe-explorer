# 🚀 Super Easy Windows Deployment Guide

## 📁 Step 1: Open the Right Folder

```cmd
cd C:\Users\Niklas\PycharmProjects\Mondlandung\project_simone
```

## 📋 Step 2: Prepare Files

```cmd
copy requirements_minimal.txt requirements.txt
move README_GITHUB.md README.md
```

## 🌐 Step 3: Create GitHub Repository

1. Open your browser and go to: https://github.com/new
2. Name it: `philosophical-universe-explorer`
3. Make it **Public**
4. DON'T add any files (no README, no .gitignore)
5. Click "Create repository"

## 📤 Step 4: Push to GitHub

Copy and paste these commands one by one:

```cmd
git init
git add .
git commit -m "Initial commit: Philosophical Universe Explorer"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/philosophical-universe-explorer.git
git push -u origin main
```

**IMPORTANT**: Replace `YOUR_USERNAME` with your actual GitHub username!

## 🎯 Step 5: Deploy to Streamlit Cloud (Super Easy!)

1. Go to: https://share.streamlit.io
2. Click "New app"
3. Sign in with GitHub
4. Select your repository
5. Main file: `app_complete.py`
6. Click "Deploy!"

## 🔑 Step 6: Add Your API Keys

After deployment:
1. Click "Manage app" → "Settings" → "Secrets"
2. Add this (replace with your actual keys):

```
OPENAI_API_KEY = "sk-proj-xxxxx"
ANTHROPIC_API_KEY = "sk-ant-xxxxx"
```

3. Click "Save"

## ✅ DONE!

Your app will be live at:
```
https://your-app-name.streamlit.app
```

## 🆘 Troubleshooting

### "git is not recognized"
Install Git for Windows: https://git-scm.com/download/win

### "Access denied" pushing to GitHub
Make sure you're logged in to Git:
```cmd
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

### Need GitHub token?
1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select "repo" scope
4. Use token as password when pushing

---

That's it! Your app will be live in about 2-3 minutes! 🎉