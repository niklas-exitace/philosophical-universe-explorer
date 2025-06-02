"""
Project Simone - Philosophical Universe Explorer
A beautiful, interactive app for exploring philosophical podcast content
"""

import streamlit as st
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure page
st.set_page_config(
    page_title="Philosophical Universe - Project Simone",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
    }
    
    /* Main title animation */
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #f3ec78, #af4261, #f3ec78);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        text-align: center;
        margin-bottom: 0;
    }
    
    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        font-size: 1.2rem;
        text-align: center;
        color: #a8a8b3;
        margin-top: -10px;
    }
    
    /* Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Navigation cards */
    .nav-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
    }
    
    .nav-card:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border-color: rgba(255,255,255,0.4);
    }
    
    /* Metric displays */
    .metric {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 600;
        color: #f3ec78;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #a8a8b3;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 30px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(15, 12, 41, 0.95);
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'engine' not in st.session_state:
    with st.spinner("🌌 Initializing the Philosophical Universe..."):
        from src.core import SimoneEngine
        st.session_state.engine = SimoneEngine()

def main():
    """Main app logic"""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        pages = {
            'home': {'icon': '🏠', 'name': 'Overview'},
            'episodes': {'icon': '📚', 'name': 'Episode Explorer'},
            'universe': {'icon': '🌌', 'name': 'Concept Universe'},
            'evolution': {'icon': '📈', 'name': 'Idea Evolution'},
            'chat': {'icon': '💭', 'name': 'Philosophical Chat'},
            'journey': {'icon': '🗺️', 'name': 'Learning Journeys'}
        }
        
        for page_id, page_info in pages.items():
            if st.button(f"{page_info['icon']} {page_info['name']}", 
                        key=f"nav_{page_id}",
                        use_container_width=True):
                st.session_state.page = page_id
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        stats = st.session_state.engine.get_statistics()
        st.metric("Episodes", stats['total_episodes'])
        st.metric("Concepts", stats['total_concepts'])
        st.metric("Avg Complexity", f"{stats['avg_complexity']:.1f}/10")
    
    # Main content area
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'episodes':
        show_episodes_page()
    elif st.session_state.page == 'universe':
        show_universe_page()
    elif st.session_state.page == 'evolution':
        show_evolution_page()
    elif st.session_state.page == 'chat':
        show_chat_page()
    elif st.session_state.page == 'journey':
        show_journey_page()

def show_home_page():
    """Show the home/overview page"""
    # Animated title
    st.markdown('<h1 class="main-title">Philosophical Universe</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Explore the depths of wisdom from Mondlandung Podcast</p>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Statistics overview
    stats = st.session_state.engine.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric">
            <div class="metric-value">{}</div>
            <div class="metric-label">Episodes Analyzed</div>
        </div>
        """.format(stats['valid_episodes']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric">
            <div class="metric-value">{}</div>
            <div class="metric-label">Unique Concepts</div>
        </div>
        """.format(stats['total_concepts']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric">
            <div class="metric-value">{:.1f}</div>
            <div class="metric-label">Complexity Score</div>
        </div>
        """.format(stats['avg_complexity']), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric">
            <div class="metric-value">{:.1f}</div>
            <div class="metric-label">Concepts/Episode</div>
        </div>
        """.format(stats['avg_concepts_per_episode']), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation cards
    st.markdown("## 🧭 Explore the Universe")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("", key="card_episodes", help="Browse and select episodes"):
            st.session_state.page = 'episodes'
            st.rerun()
        st.markdown("""
        <div class="nav-card">
            <h3>📚 Episode Explorer</h3>
            <p>Browse through episodes, read summaries, and dive deep into specific discussions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("", key="card_universe", help="Explore concept connections"):
            st.session_state.page = 'universe'
            st.rerun()
        st.markdown("""
        <div class="nav-card">
            <h3>🌌 Concept Universe</h3>
            <p>Visualize the interconnected web of philosophical concepts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("", key="card_chat", help="Chat about philosophy"):
            st.session_state.page = 'chat'
            st.rerun()
        st.markdown("""
        <div class="nav-card">
            <h3>💭 Philosophical Chat</h3>
            <p>Ask questions and explore ideas with AI assistance</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Top concepts preview
    st.markdown("## 🔝 Top Philosophical Concepts")
    
    concepts = st.session_state.engine.data_manager.get_all_concepts()
    top_concepts = list(concepts.items())[:12]
    
    cols = st.columns(4)
    for i, (concept, count) in enumerate(top_concepts):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 1rem;">
                <h4>{concept}</h4>
                <p style="color: #a8a8b3;">{count} occurrences</p>
            </div>
            """, unsafe_allow_html=True)

def show_episodes_page():
    """Episode explorer page"""
    st.markdown("# 📚 Episode Explorer")
    st.markdown("Select episodes to explore their philosophical content")
    
    # Get all episodes
    episodes = st.session_state.engine.data_manager.get_all_episodes(valid_only=True)
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search episodes", placeholder="Enter keywords...")
    with col2:
        sort_by = st.selectbox("Sort by", ["Date", "Complexity", "Title"])
    
    # Filter episodes
    if search:
        episodes = [ep for ep in episodes if search.lower() in ep.title.lower()]
    
    # Sort episodes
    if sort_by == "Date":
        episodes.sort(key=lambda x: x.processed_date, reverse=True)
    elif sort_by == "Complexity":
        episodes.sort(key=lambda x: x.episode_metrics.get('complexity_score', 0), reverse=True)
    else:
        episodes.sort(key=lambda x: x.title)
    
    # Display episodes in a grid
    for i in range(0, len(episodes), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(episodes):
                episode = episodes[i + j]
                with cols[j]:
                    with st.container():
                        st.markdown(f"""
                        <div class="glass-card">
                            <h3>{episode.title}</h3>
                            <p style="color: #a8a8b3; font-size: 0.9rem;">
                                {episode.content_analysis.get('summary', {}).get('brief', 'No summary available')}
                            </p>
                            <div style="margin-top: 1rem;">
                                <span class="metric-label">Complexity: {episode.episode_metrics.get('complexity_score', 0):.1f}/10</span>
                                <span class="metric-label" style="margin-left: 1rem;">Concepts: {episode.episode_metrics.get('concepts_count', 0)}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"Explore", key=f"explore_{episode.episode_id}"):
                            st.session_state.selected_episode = episode
                            st.session_state.show_episode_detail = True
                            st.rerun()
    
    # Episode detail modal
    if hasattr(st.session_state, 'show_episode_detail') and st.session_state.show_episode_detail:
        show_episode_detail()

def show_episode_detail():
    """Show detailed episode information"""
    episode = st.session_state.selected_episode
    
    # Close button
    if st.button("← Back to Episodes"):
        st.session_state.show_episode_detail = False
        st.rerun()
    
    st.markdown(f"# {episode.title}")
    
    # Tabs for different aspects
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Summary", "🧠 Concepts", "💡 Wisdom", "🔗 Connections"])
    
    with tab1:
        st.markdown("### Brief Summary")
        st.info(episode.content_analysis.get('summary', {}).get('brief', 'No summary available'))
        
        st.markdown("### Detailed Analysis")
        st.write(episode.content_analysis.get('summary', {}).get('detailed', 'No detailed analysis available'))
    
    with tab2:
        st.markdown("### Philosophical Concepts Explored")
        concepts = episode.philosophical_content.get('concepts_explored', [])
        for concept in concepts[:10]:
            if isinstance(concept, dict):
                st.markdown(f"""
                <div class="glass-card">
                    <h4>{concept.get('concept', 'Unknown')}</h4>
                    <p><strong>Definition:</strong> {concept.get('definition_given', 'No definition provided')}</p>
                    <p><strong>Application:</strong> {concept.get('practical_application', 'No application described')}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Practical Wisdom")
        wisdom = episode.practical_wisdom
        
        if wisdom.get('life_advice'):
            st.markdown("**Life Advice:**")
            for advice in wisdom['life_advice'][:5]:
                st.markdown(f"• {advice}")
        
        if wisdom.get('mindset_shifts'):
            st.markdown("**Mindset Shifts:**")
            for shift in wisdom['mindset_shifts'][:5]:
                st.markdown(f"• {shift}")
    
    with tab4:
        st.markdown("### Related Episodes")
        # Find related episodes by shared concepts
        current_concepts = [c.get('concept', '') for c in episode.philosophical_content.get('concepts_explored', []) if isinstance(c, dict)]
        
        related = []
        for other_ep in st.session_state.engine.data_manager.get_all_episodes(valid_only=True):
            if other_ep.episode_id != episode.episode_id:
                other_concepts = [c.get('concept', '') for c in other_ep.philosophical_content.get('concepts_explored', []) if isinstance(c, dict)]
                shared = set(current_concepts) & set(other_concepts)
                if len(shared) >= 2:
                    related.append((other_ep, len(shared)))
        
        related.sort(key=lambda x: x[1], reverse=True)
        
        for rel_ep, shared_count in related[:5]:
            st.markdown(f"**{rel_ep.title}** - {shared_count} shared concepts")

def show_universe_page():
    """Concept universe visualization page"""
    st.markdown("# 🌌 Concept Universe")
    st.markdown("Explore the interconnected web of philosophical concepts")
    
    # This is a placeholder - in the next file I'll implement the actual visualization
    st.info("Interactive concept network visualization will be implemented here")

def show_evolution_page():
    """Idea evolution timeline page"""
    st.markdown("# 📈 Evolution of Ideas")
    st.markdown("Track how philosophical concepts develop across episodes")
    
    # This is a placeholder - will be implemented
    st.info("Timeline visualization of concept evolution will be implemented here")

def show_chat_page():
    """Philosophical chat interface"""
    st.markdown("# 💭 Philosophical Chat")
    st.markdown("Ask questions about the podcast content and explore ideas")
    
    # This is a placeholder - will implement Anthropic integration
    st.info("Chat interface with Anthropic Claude will be implemented here")

def show_journey_page():
    """Learning journey builder"""
    st.markdown("# 🗺️ Learning Journeys")
    st.markdown("Create personalized paths through philosophical concepts")
    
    # This is a placeholder
    st.info("Journey builder will be implemented here")

if __name__ == "__main__":
    main()