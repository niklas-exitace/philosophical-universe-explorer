"""
Project Simone - Complete Philosophical Universe Explorer
Enhanced version with all features integrated
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure page
st.set_page_config(
    page_title="Philosophical Universe - Project Simone",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import components after path setup
from src.core import SimoneEngine
from src.interface.visualizations import ConceptNetworkVisualizer, TimelineVisualizer
from src.interface.chat_interface_enhanced import EnhancedPhilosophicalChat

# Enhanced CSS with animations
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
    
    /* Glass morphism cards */
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
    
    /* Concept tags */
    .concept-tag {
        display: inline-block;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .concept-tag:hover {
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Chat interface */
    .chat-message {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .user-message {
        background: rgba(102, 126, 234, 0.2);
        margin-left: 20%;
    }
    
    .ai-message {
        background: rgba(175, 66, 97, 0.2);
        margin-right: 20%;
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
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
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
        st.session_state.engine = SimoneEngine()
if 'chat_interface' not in st.session_state:
    st.session_state.chat_interface = EnhancedPhilosophicalChat(
        st.session_state.engine.data_manager,
        st.session_state.engine.config
    )
if 'concept_viz' not in st.session_state:
    st.session_state.concept_viz = ConceptNetworkVisualizer(
        st.session_state.engine.concept_mapper
    )
if 'timeline_viz' not in st.session_state:
    st.session_state.timeline_viz = TimelineVisualizer(
        st.session_state.engine.data_manager
    )
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_concepts' not in st.session_state:
    st.session_state.selected_concepts = []

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
        
        st.markdown("---")
        st.markdown("### 🌟 About")
        st.markdown("""
        **Philosophical Universe Explorer**  
        Powered by Project Simone  
        
        💡 *Tip: Add your Anthropic API key in the Chat section for enhanced AI discussions*
        """)
    
    # Main content area
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'episodes':
        show_episodes_page()
    elif st.session_state.page == 'episode_detail':
        show_episode_detail_page()
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
        st.markdown(f"""
        <div class="metric">
            <div class="metric-value">{stats['valid_episodes']}</div>
            <div class="metric-label">Episodes Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-value">{stats['total_concepts']}</div>
            <div class="metric-label">Unique Concepts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-value">{stats['avg_complexity']:.1f}</div>
            <div class="metric-label">Complexity Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-value">{stats['avg_concepts_per_episode']:.1f}</div>
            <div class="metric-label">Concepts/Episode</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Top concepts cloud
    st.markdown("## 🌟 Philosophical Concepts Cloud")
    
    concepts = st.session_state.engine.data_manager.get_all_concepts()
    top_concepts = list(concepts.items())[:30]
    
    # Create concept cloud
    concept_html = '<div style="text-align: center; padding: 2rem;">'
    for concept, count in top_concepts:
        size = min(2.5, 0.8 + count * 0.2)
        opacity = min(1, 0.4 + count * 0.1)
        concept_html += f'<span class="concept-tag" style="font-size: {size}rem; opacity: {opacity}; margin: 0.5rem;">{concept}</span>'
    concept_html += '</div>'
    
    st.markdown(concept_html, unsafe_allow_html=True)
    
    # Recent insights
    st.markdown("## 💡 Recent Insights")
    
    # Get a few recent episodes
    recent_episodes = st.session_state.engine.data_manager.get_all_episodes(valid_only=True)[:3]
    
    for episode in recent_episodes:
        if episode.unique_insights:
            insight = episode.unique_insights[0] if episode.unique_insights else "No insights available"
            st.markdown(f"""
            <div class="glass-card">
                <h4>{episode.title}</h4>
                <p style="font-style: italic; color: #f3ec78;">"{insight}"</p>
            </div>
            """, unsafe_allow_html=True)

def show_episodes_page():
    """Episode explorer page"""
    st.markdown("# 📚 Episode Explorer")
    st.markdown("Dive deep into individual philosophical discussions")
    
    # Get all episodes
    episodes = st.session_state.engine.data_manager.get_all_episodes(valid_only=True)
    
    # Search and filter
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search = st.text_input("🔍 Search episodes", placeholder="Enter keywords...")
    with col2:
        sort_by = st.selectbox("Sort by", ["Date", "Complexity", "Title", "Concepts"])
    with col3:
        min_complexity = st.slider("Min Complexity", 0, 10, 0)
    
    # Filter episodes
    if search:
        episodes = [ep for ep in episodes if search.lower() in ep.title.lower() or 
                   search.lower() in ep.content_analysis.get('summary', {}).get('brief', '').lower()]
    
    episodes = [ep for ep in episodes if ep.episode_metrics.get('complexity_score', 0) >= min_complexity]
    
    # Sort episodes
    if sort_by == "Date":
        episodes.sort(key=lambda x: x.processed_date, reverse=True)
    elif sort_by == "Complexity":
        episodes.sort(key=lambda x: x.episode_metrics.get('complexity_score', 0), reverse=True)
    elif sort_by == "Concepts":
        episodes.sort(key=lambda x: x.episode_metrics.get('concepts_count', 0), reverse=True)
    else:
        episodes.sort(key=lambda x: x.title)
    
    # Display episodes
    for episode in episodes:
        with st.expander(f"**{episode.title}**", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Summary:** {episode.content_analysis.get('summary', {}).get('brief', 'No summary available')}")
                
                # Show top concepts
                concepts = episode.philosophical_content.get('concepts_explored', [])[:5]
                if concepts:
                    concept_tags = ' '.join([f'<span class="concept-tag">{c.get("concept", "")}</span>' 
                                           for c in concepts if isinstance(c, dict)])
                    st.markdown(concept_tags, unsafe_allow_html=True)
            
            with col2:
                st.metric("Complexity", f"{episode.episode_metrics.get('complexity_score', 0):.1f}/10")
                st.metric("Concepts", episode.episode_metrics.get('concepts_count', 0))
                
                if st.button("Deep Dive", key=f"dive_{episode.episode_id}"):
                    st.session_state.selected_episode = episode
                    st.session_state.page = 'episode_detail'
                    st.rerun()

def show_episode_detail_page():
    """Show detailed analysis of a single episode"""
    if 'selected_episode' not in st.session_state:
        st.warning("No episode selected. Please go back to Episode Explorer.")
        if st.button("← Back to Episodes"):
            st.session_state.page = 'episodes'
            st.rerun()
        return
    
    episode = st.session_state.selected_episode
    
    # Back button
    if st.button("← Back to Episodes"):
        st.session_state.page = 'episodes'
        st.rerun()
    
    st.markdown(f"# 📚 {episode.title}")
    
    # Episode metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Complexity", f"{episode.episode_metrics.get('complexity_score', 0):.1f}/10")
    with col2:
        st.metric("Concepts", episode.episode_metrics.get('concepts_count', 0))
    with col3:
        st.metric("Themes", len(episode.content_analysis.get('secondary_topics', [])))
    with col4:
        st.metric("Insights", len(episode.unique_insights))
    
    # Deep dive analysis
    st.markdown("## 🧘 Philosophical Deep Dive")
    
    with st.spinner("🤔 Generating deep philosophical analysis..."):
        deep_dive = st.session_state.chat_interface.get_episode_deep_dive(episode.episode_id)
        st.markdown(deep_dive)
    
    # Key concepts
    st.markdown("## 💡 Key Concepts Explored")
    concepts = episode.philosophical_content.get('concepts_explored', [])
    
    for concept in concepts[:10]:
        if isinstance(concept, dict):
            with st.expander(f"**{concept.get('concept', 'Unknown')}**"):
                st.markdown(concept.get('description', 'No description available.'))
    
    # Unique insights
    st.markdown("## 💡 Unique Insights")
    for i, quote in enumerate(episode.unique_insights[:5]):
        st.markdown(f"> 🗨️ *\"{quote}\"*")
    
    # Key takeaways
    st.markdown("## 🎯 Key Takeaways")
    takeaways = episode.listener_value.get('key_takeaways', [])
    for takeaway in takeaways[:5]:
        st.markdown(f"- {takeaway}")
    
    # Thinkers referenced
    if episode.philosophical_content.get('thinkers_referenced'):
        st.markdown("## 👥 Philosophical Traditions")
        thinkers = ', '.join(episode.philosophical_content['thinkers_referenced'])
        st.markdown(f"This episode connects to the work of: **{thinkers}**")
    
    # Questions for reflection
    st.markdown("## ❓ Questions for Reflection")
    if st.button("🎲 Generate Thought-Provoking Question"):
        question = st.session_state.chat_interface.generate_philosophical_question(episode.episode_id)
        st.info(question)

def show_universe_page():
    """Concept universe visualization page"""
    st.markdown("# 🌌 Concept Universe")
    st.markdown("Explore the interconnected web of philosophical ideas")
    
    # Controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_concept = st.text_input("🔍 Highlight concept", placeholder="Enter concept name...")
    with col2:
        max_nodes = st.slider("Max concepts", 20, 200, 50)
    with col3:
        min_connections = st.slider("Min connections", 1, 10, 2)
    
    # Create visualization
    with st.spinner("🌌 Rendering the philosophical universe..."):
        fig = st.session_state.concept_viz.create_universe_visualization(
            max_nodes=max_nodes,
            min_connections=min_connections,
            highlight_concept=search_concept if search_concept else None
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Concept details
    if search_concept:
        concept_data = st.session_state.engine.concept_mapper.map_single_concept(search_concept)
        
        if 'error' not in concept_data:
            st.markdown(f"## 🔍 Concept Details: {concept_data['concept']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Occurrences", concept_data['occurrences'])
            with col2:
                st.metric("Centrality", f"{concept_data['centrality_score']:.3f}")
            with col3:
                st.metric("Clustering", f"{concept_data['clustering_coefficient']:.3f}")
            
            # Related concepts
            st.markdown("### 🔗 Related Concepts")
            related_html = '<div>'
            for rel in concept_data['related_concepts'][:10]:
                related_html += f'<span class="concept-tag">{rel["concept"]} ({rel["strength"]})</span>'
            related_html += '</div>'
            st.markdown(related_html, unsafe_allow_html=True)
            
            # Episodes featuring this concept
            st.markdown("### 📚 Episodes Exploring This Concept")
            for ep_info in concept_data['episodes'][:5]:
                st.markdown(f"**{ep_info['title']}**")
                if ep_info['definition']:
                    st.markdown(f"*Definition:* {ep_info['definition']}")

def show_evolution_page():
    """Idea evolution timeline page"""
    st.markdown("# 📈 Evolution of Ideas")
    st.markdown("Track how philosophical concepts develop across episodes")
    
    # Concept selector
    all_concepts = list(st.session_state.engine.data_manager.get_all_concepts().keys())
    
    selected_concepts = st.multiselect(
        "Select concepts to track",
        all_concepts,
        default=st.session_state.selected_concepts or all_concepts[:3],
        max_selections=5
    )
    
    if selected_concepts:
        st.session_state.selected_concepts = selected_concepts
        
        # Create timeline visualization
        fig = st.session_state.timeline_viz.create_concept_evolution_timeline(selected_concepts)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show episodes for each concept
        st.markdown("## 📚 Episodes by Concept")
        
        tabs = st.tabs(selected_concepts)
        
        for i, concept in enumerate(selected_concepts):
            with tabs[i]:
                episodes = st.session_state.engine.data_manager.get_episodes_by_concept(concept)
                
                for episode in episodes[:10]:
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4>{episode.title}</h4>
                        <p>{episode.content_analysis.get('summary', {}).get('brief', '')}</p>
                        <small>Complexity: {episode.episode_metrics.get('complexity_score', 0):.1f}/10</small>
                    </div>
                    """, unsafe_allow_html=True)

def show_chat_page():
    """Philosophical chat interface"""
    st.markdown("# 💭 Philosophical Chat")
    st.markdown("Explore ideas through conversation with AI that has access to all episode content")
    
    # API Key input in sidebar
    with st.sidebar:
        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input(
            "Anthropic API Key (optional)",
            type="password",
            help="Enter your Anthropic API key for enhanced chat. Your key is stored only for this session."
        )
        
        if api_key:
            st.success("✅ API key configured for this session")
        else:
            st.info("💡 Using fallback mode. Add Anthropic API key for full chat capabilities.")
    
    # Initialize chat interface if not exists or if API key changed
    if 'chat_interface' not in st.session_state or st.session_state.get('last_api_key') != api_key:
        st.session_state.chat_interface = EnhancedPhilosophicalChat(
            st.session_state.engine.data_manager,
            st.session_state.engine.config,
            api_key=api_key
        )
        st.session_state.last_api_key = api_key
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat interface
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message user-message"><b>You:</b> {message["content"]}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message ai-message"><b>Philosophy Guide:</b> {message["content"]}</div>', 
                          unsafe_allow_html=True)
    
    # Input area
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input("Ask a philosophical question...", key="chat_input")
    
    with col2:
        if st.button("Send", type="primary"):
            if user_input:
                # Add user message
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input
                })
                
                # Get response with content search
                with st.spinner("🤔 Searching through episodes and contemplating..."):
                    response = st.session_state.chat_interface.chat_with_content(
                        user_input,
                        conversation_history=st.session_state.chat_history
                    )
                
                # Add AI response
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
                
                st.rerun()
    
    # Quick actions
    st.markdown("### 💡 Quick Questions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("What is happiness?"):
            st.session_state.chat_history.append({'role': 'user', 'content': 'What does the podcast say about happiness?'})
            response = st.session_state.chat_interface.chat_with_content('What does the podcast say about happiness?')
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col2:
        if st.button("Meaning of life"):
            st.session_state.chat_history.append({'role': 'user', 'content': 'How does the podcast explore the meaning of life?'})
            response = st.session_state.chat_interface.chat_with_content('How does the podcast explore the meaning of life?')
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col3:
        if st.button("Clear chat"):
            st.session_state.chat_history = []
            st.rerun()

def show_journey_page():
    """Learning journey builder"""
    st.markdown("# 🗺️ Learning Journeys")
    st.markdown("Create personalized paths through philosophical concepts")
    
    # Journey builder
    col1, col2 = st.columns(2)
    
    with col1:
        all_concepts = list(st.session_state.engine.data_manager.get_all_concepts().keys())[:50]
        starting_concept = st.selectbox("Starting concept", all_concepts)
    
    with col2:
        learning_goals = [
            "Deep understanding",
            "Practical application",
            "Historical context",
            "Contemporary relevance",
            "Personal growth"
        ]
        goal = st.selectbox("Learning goal", learning_goals)
    
    if st.button("Create Journey", type="primary"):
        with st.spinner("🗺️ Mapping your philosophical journey..."):
            # Create learning path
            journey = st.session_state.chat_interface.create_learning_path(
                starting_concept,
                goal,
                max_episodes=5
            )
            
            # Visualize journey
            if journey:
                episode_ids = [step['episode_id'] for step in journey]
                fig = st.session_state.timeline_viz.create_philosophical_journey_map(episode_ids)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show journey steps
                st.markdown("## 📚 Your Learning Path")
                
                for i, step in enumerate(journey):
                    st.markdown(f"""
                    <div class="glass-card">
                        <h3>Step {i+1}: {step['title']}</h3>
                        <p><b>Why this episode:</b> {step['reason']}</p>
                        <p><b>Key concepts:</b> {', '.join(step.get('concepts', []))}</p>
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()