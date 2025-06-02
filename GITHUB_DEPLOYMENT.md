# 🚀 GitHub Deployment Guide

This guide will help you deploy your Philosophical Universe Explorer to GitHub and various hosting platforms.

## 📁 Step 1: Prepare Your GitHub Repository

### 1.1 Create a New Repository on GitHub

1. Go to [github.com](https://github.com) and log in
2. Click the "+" icon in the top right → "New repository"
3. Name it: `philosophical-universe-explorer`
4. Description: "AI-powered exploration of philosophical content"
5. Make it **Public** (required for free Streamlit Cloud hosting)
6. Don't initialize with README (we already have one)
7. Click "Create repository"

### 1.2 Prepare Your Local Files

Before pushing to GitHub, ensure sensitive data is protected:

1. **Check .gitignore** - Already created with proper exclusions
2. **Remove any API keys** from code - They should only be in `.env`
3. **Use minimal requirements** for deployment:
   ```bash
   cp requirements_minimal.txt requirements.txt
   ```

### 1.3 Initialize Git and Push

```bash
# Navigate to your project folder
cd /mnt/c/Users/Niklas/PycharmProjects/Mondlandung/project_simone

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Philosophical Universe Explorer"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/philosophical-universe-explorer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🌐 Step 2: Deploy to Streamlit Cloud (Recommended)

### 2.1 Sign Up for Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

### 2.2 Deploy Your App
1. Click "New app"
2. Select your repository: `YOUR_USERNAME/philosophical-universe-explorer`
3. Branch: `main`
4. Main file path: `app_complete.py`
5. Click "Deploy"

### 2.3 Add Secrets (API Keys)
1. In Streamlit Cloud, go to your app settings
2. Click "Secrets" in the left sidebar
3. Add your secrets in TOML format:
   ```toml
   OPENAI_API_KEY = "your-openai-key-here"
   ANTHROPIC_API_KEY = "your-anthropic-key-here"
   ```
4. Click "Save"

Your app will be available at: `https://YOUR_APP_NAME.streamlit.app`

## 🚢 Alternative: Deploy to Heroku

### Prerequisites
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- Heroku account

### Steps
```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Set buildpack
heroku buildpacks:set heroku/python

# Set environment variables
heroku config:set OPENAI_API_KEY=your-key-here
heroku config:set ANTHROPIC_API_KEY=your-key-here

# Deploy
git push heroku main

# Open your app
heroku open
```

## 🐳 Alternative: Deploy with Docker

### Build and Run Locally
```bash
# Build the Docker image
docker build -t philosophical-universe .

# Run with environment variables
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your-key \
  -e ANTHROPIC_API_KEY=your-key \
  philosophical-universe
```

### Deploy to Cloud Services
- **Google Cloud Run**: Push to Container Registry and deploy
- **Azure Container Instances**: Push to Azure Container Registry
- **AWS ECS**: Push to ECR and create a service

## 🔐 Security Best Practices

### Never Commit Secrets
- ✅ Use environment variables
- ✅ Use `.gitignore` to exclude `.env` files
- ✅ Use platform-specific secret management

### API Key Management
- **Streamlit Cloud**: Use Secrets management
- **Heroku**: Use Config Vars
- **Docker**: Use environment variables or secrets

### Data Protection
- Large data files are excluded from git
- Use cloud storage for large datasets if needed

## 📝 Post-Deployment Checklist

- [ ] App loads without errors
- [ ] API keys are properly configured
- [ ] Chat functionality works
- [ ] Visualizations render correctly
- [ ] Data loads properly
- [ ] No sensitive information in logs

## 🆘 Troubleshooting

### "Module not found" errors
- Ensure all dependencies are in `requirements.txt`
- Use `requirements_minimal.txt` for deployment

### API key errors
- Check that environment variables are set correctly
- Verify keys are valid and have proper permissions

### Memory errors
- Streamlit Cloud has memory limits
- Consider optimizing data loading
- Use caching where possible

### Data not loading
- Ensure `data/processed/` folder contains JSON files
- Check file permissions
- Verify relative paths work in deployment

## 📧 Need Help?

If you encounter issues:
1. Check the deployment logs
2. Verify all environment variables
3. Test locally first
4. Open an issue on GitHub

---

Good luck with your deployment! 🚀