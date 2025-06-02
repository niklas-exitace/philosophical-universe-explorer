# 🌌 Philosophical Universe Explorer

An AI-powered interactive exploration tool for philosophical content from the Mondlandung podcast. Discover connections between ideas, track the evolution of concepts, and engage in deep philosophical discussions with Claude Opus 4.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🌐 3D Concept Universe
- Interactive visualization of 1,704 philosophical concepts
- Explore connections between ideas
- Zoom, rotate, and click for details

### 📚 Episode Explorer
- Browse 71 analyzed episodes
- Search and filter by concepts, themes, or complexity
- Deep dive into individual episodes

### 📈 Evolution of Ideas
- Track how concepts develop across episodes
- Timeline visualizations
- Identify philosophical patterns

### 💬 AI-Powered Chat
- Powered by Claude Opus 4 (Anthropic's most advanced model)
- Content-aware responses with episode references
- Ask questions like "When did we discuss consciousness?"

### 🛤️ Learning Journeys
- Create personalized paths through philosophical concepts
- AI-generated learning recommendations
- Progress tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/philosophical-universe-explorer.git
cd philosophical-universe-explorer
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Run the application
```bash
streamlit run app_complete.py
```

The app will open at `http://localhost:8501`

## 🔑 API Keys

The app works with OpenAI out of the box. For enhanced chat features with Claude Opus 4:

1. Get an Anthropic API key from [console.anthropic.com](https://console.anthropic.com)
2. Add it to your `.env` file or enter it in the app's chat interface

## 📁 Project Structure

```
philosophical-universe-explorer/
├── app_complete.py          # Main Streamlit application
├── src/
│   ├── core/               # Core business logic
│   │   ├── engine.py       # Main orchestration engine
│   │   ├── data_manager.py # Episode data management
│   │   └── config.py       # Configuration management
│   ├── interface/          # UI components
│   │   ├── chat_interface_enhanced.py  # AI chat
│   │   └── visualizations.py          # 3D visualizations
│   └── analysis/           # Analysis modules
├── data/
│   └── processed/          # Analyzed episode data
├── config/                 # Configuration files
├── requirements.txt        # Python dependencies
└── .streamlit/            # Streamlit configuration
```

## 🎨 Screenshots

### Concept Universe
![Concept Universe](docs/images/universe.png)

### Episode Explorer
![Episode Explorer](docs/images/episodes.png)

### AI Chat
![AI Chat](docs/images/chat.png)

## 🚢 Deployment

### Streamlit Cloud (Recommended)

1. Fork this repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io)
3. Deploy directly from your GitHub repo
4. Add API keys in Streamlit Cloud secrets

### Heroku

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

### Docker

```bash
docker build -t philosophical-universe .
docker run -p 8501:8501 philosophical-universe
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` - For fallback chat functionality
- `ANTHROPIC_API_KEY` - For Claude Opus 4 chat (optional)
- `STREAMLIT_SERVER_PORT` - Server port (default: 8501)

### Data Configuration

Episode data is stored in `data/processed/`. The app expects JSON files with analyzed episode content.

## 📊 Data Summary

- **Episodes Analyzed**: 71
- **Unique Concepts**: 1,704
- **Philosophical Themes**: 339
- **Total Insights**: 1,000+

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Mondlandung Podcast for the philosophical content
- Anthropic for Claude Opus 4
- Streamlit for the amazing framework
- The open-source community

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

Made with ❤️ and 🤔 by [Your Name]