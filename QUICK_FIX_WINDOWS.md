# 🔧 Quick Fix for API Key Issue

## The Problem
GitHub detected your OpenAI API key in `config/settings.yaml` and blocked the push for security.

## The Fix (Copy & Paste These Commands)

### 1. Edit the config file to remove the API key:
```cmd
notepad config\settings.yaml
```

Find this line (around line 6):
```yaml
openai_key: "sk-proj-xxxxx..."
```

Change it to:
```yaml
openai_key: ""
```

Save and close notepad.

### 2. Commit the fix:
```cmd
git add config/settings.yaml
git commit -m "Remove API key from config"
```

### 3. Push again:
```cmd
git push origin main
```

## That's it! 

Your repository will now be live at:
https://github.com/niklas-exitace/philosophical-universe-explorer

Next step: Deploy to Streamlit Cloud! 🚀