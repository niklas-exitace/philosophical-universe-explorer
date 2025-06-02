# Deployment Guide - Philosophical Universe Explorer

## 🚀 Quick Start (Local)

### 1. Install Dependencies
```bash
cd project_simone
pip install -r requirements.txt
```

### 2. Set API Keys (Optional)
Create a `.env` file:
```env
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
```

Or set them in the app's sidebar when running.

### 3. Run the App
```bash
streamlit run app_complete.py
```

The app will open at `http://localhost:8501`

## 🌐 Sharing with Friends

### Option 1: Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from your GitHub repository
4. Share the public URL with friends!

### Option 2: Ngrok (Quick Local Sharing)
1. Install ngrok: `pip install pyngrok`
2. Run the app: `streamlit run app_complete.py`
3. In another terminal: `ngrok http 8501`
4. Share the ngrok URL with friends

### Option 3: Cloud Deployment

#### Heroku
1. Create `Procfile`:
```
web: sh setup.sh && streamlit run app_complete.py
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

#### Google Cloud Run
1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD streamlit run app_complete.py --server.port 8080
```

2. Deploy:
```bash
gcloud run deploy --source .
```

## 📱 Features Overview

### 🏠 Home
- Beautiful animated title
- Key statistics
- Concept cloud visualization
- Recent philosophical insights

### 📚 Episode Explorer
- Search and filter episodes
- Sort by date, complexity, or concept count
- Detailed episode information
- Concept tags for each episode

### 🌌 Concept Universe
- Interactive 3D visualization
- Explore concept relationships
- Highlight specific concepts
- See connection strengths

### 📈 Idea Evolution
- Track concepts over time
- See how ideas develop
- Episode timeline visualization
- Complexity progression

### 💭 Philosophical Chat
- AI-powered discussions
- Supports Anthropic Claude
- Context-aware responses
- Save chat history

### 🗺️ Learning Journeys
- Create personalized paths
- Goal-oriented learning
- Visual journey maps
- Step-by-step guidance

## 🔧 Configuration

### Performance Tuning
Edit `config/settings.yaml`:
- Adjust `max_nodes` for concept visualization
- Change `chunk_size` for analysis
- Modify `cache_ttl` for response caching

### Theming
Edit `.streamlit/config.toml`:
- Change color scheme
- Adjust fonts
- Modify layout settings

## 🤝 Sharing Tips

1. **Provide Context**: Share a brief explanation of what the podcast is about
2. **Suggest Starting Points**: Recommend specific episodes or concepts to explore
3. **API Keys**: Either provide temporary keys or ask users to use their own
4. **Performance**: For large groups, consider using a cloud deployment

## 📊 Resource Requirements

- **Memory**: 2-4GB RAM recommended
- **Storage**: ~500MB for app + cache
- **Network**: Stable connection for API calls
- **Browser**: Modern browser with WebGL support

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'src'"**
   - Make sure you're running from the project_simone directory
   - Check that `__init__.py` files exist in all subdirectories

2. **API Key Errors**
   - Verify keys are set correctly
   - Check API quota/limits
   - Try the fallback OpenAI mode

3. **Visualization Not Loading**
   - Ensure plotly is installed: `pip install plotly`
   - Try refreshing the browser
   - Check browser console for errors

4. **Slow Performance**
   - Reduce max_nodes in concept visualization
   - Clear cache if it's too large
   - Use cloud deployment for better resources

## 🎉 Enjoy Exploring!

Share the philosophical universe with friends and embark on intellectual journeys together!