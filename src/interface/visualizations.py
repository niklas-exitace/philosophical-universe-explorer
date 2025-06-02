"""Advanced visualization components for Project Simone"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import colorsys
from datetime import datetime
import random


class ConceptNetworkVisualizer:
    """Creates stunning interactive concept network visualizations"""
    
    def __init__(self, concept_mapper):
        self.concept_mapper = concept_mapper
        self.graph = concept_mapper.concept_graph
        
    def create_universe_visualization(self, 
                                    max_nodes: int = 100,
                                    min_connections: int = 2,
                                    highlight_concept: Optional[str] = None) -> go.Figure:
        """Create an interactive 3D concept universe"""
        
        # Filter nodes by importance
        node_importance = nx.degree_centrality(self.graph)
        top_nodes = sorted(node_importance.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
        top_node_names = [node for node, _ in top_nodes]
        
        # Create subgraph
        subgraph = self.graph.subgraph(top_node_names)
        
        # Calculate 3D layout using spring algorithm
        pos_2d = nx.spring_layout(subgraph, k=3, iterations=50)
        
        # Add third dimension with some randomness for depth
        pos_3d = {}
        for node, (x, y) in pos_2d.items():
            z = np.random.normal(0, 0.3)  # Add depth variation
            pos_3d[node] = (x, y, z)
        
        # Prepare node traces
        node_x = []
        node_y = []
        node_z = []
        node_text = []
        node_color = []
        node_size = []
        
        for node in subgraph.nodes():
            x, y, z = pos_3d[node]
            node_x.append(x)
            node_y.append(y)
            node_z.append(z)
            
            # Node properties
            node_data = self.graph.nodes[node]
            occurrences = node_data.get('count', 1)
            
            # Create hover text
            hover_text = f"<b>{node}</b><br>"
            hover_text += f"Occurrences: {occurrences}<br>"
            hover_text += f"Connections: {subgraph.degree(node)}"
            node_text.append(hover_text)
            
            # Color based on centrality
            centrality = node_importance.get(node, 0)
            color_value = centrality
            node_color.append(color_value)
            
            # Size based on occurrences
            node_size.append(10 + occurrences * 3)
        
        # Prepare edge traces
        edge_x = []
        edge_y = []
        edge_z = []
        
        for edge in subgraph.edges():
            x0, y0, z0 = pos_3d[edge[0]]
            x1, y1, z1 = pos_3d[edge[1]]
            
            # Add edge with some curvature
            t = np.linspace(0, 1, 10)
            # Add slight curve to edges
            curve_height = 0.1 * np.sin(np.pi * t)
            
            for i in range(len(t)):
                edge_x.append(x0 + t[i] * (x1 - x0))
                edge_y.append(y0 + t[i] * (y1 - y0))
                edge_z.append(z0 + t[i] * (z1 - z0) + curve_height[i])
            
            edge_x.append(None)
            edge_y.append(None)
            edge_z.append(None)
        
        # Create figure
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color='rgba(125, 125, 125, 0.3)', width=1),
            hoverinfo='none',
            showlegend=False
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter3d(
            x=node_x, y=node_y, z=node_z,
            mode='markers+text',
            marker=dict(
                size=node_size,
                color=node_color,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title="Centrality",
                    tickvals=[],
                    ticktext=[]
                ),
                line=dict(width=1, color='white')
            ),
            text=[node for node in subgraph.nodes()],
            textposition="top center",
            textfont=dict(size=10, color='white'),
            hovertext=node_text,
            hoverinfo='text',
            showlegend=False
        ))
        
        # Highlight specific concept if provided
        if highlight_concept and highlight_concept in subgraph.nodes():
            hx, hy, hz = pos_3d[highlight_concept]
            fig.add_trace(go.Scatter3d(
                x=[hx], y=[hy], z=[hz],
                mode='markers',
                marker=dict(
                    size=30,
                    color='red',
                    symbol='diamond',
                    line=dict(width=3, color='white')
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Update layout for dark theme
        fig.update_layout(
            scene=dict(
                xaxis=dict(showgrid=False, zeroline=False, visible=False),
                yaxis=dict(showgrid=False, zeroline=False, visible=False),
                zaxis=dict(showgrid=False, zeroline=False, visible=False),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=700,
            hoverlabel=dict(
                bgcolor="rgba(0, 0, 0, 0.8)",
                font_size=14,
                font_family="Inter"
            )
        )
        
        # Add camera controls
        camera = dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
        fig.update_layout(scene_camera=camera)
        
        return fig
    
    def create_concept_connections_graph(self, concept: str, depth: int = 2) -> go.Figure:
        """Create a radial graph showing connections from a specific concept"""
        
        if concept not in self.graph:
            return go.Figure().add_annotation(text="Concept not found", showarrow=False)
        
        # Get neighbors up to specified depth
        nodes = {concept}
        for _ in range(depth):
            new_nodes = set()
            for node in nodes:
                new_nodes.update(self.graph.neighbors(node))
            nodes.update(new_nodes)
        
        # Create subgraph
        subgraph = self.graph.subgraph(nodes)
        
        # Calculate radial layout
        pos = self._radial_layout(subgraph, concept)
        
        # Create figure
        fig = go.Figure()
        
        # Add edges
        for edge in subgraph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            weight = subgraph[edge[0]][edge[1]].get('weight', 1)
            
            fig.add_trace(go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(
                    width=min(weight, 5),
                    color='rgba(100, 100, 200, 0.5)'
                ),
                hoverinfo='skip',
                showlegend=False
            ))
        
        # Add nodes
        for node in subgraph.nodes():
            x, y = pos[node]
            node_data = self.graph.nodes[node]
            
            # Determine node properties
            if node == concept:
                color = 'gold'
                size = 40
            else:
                distance = nx.shortest_path_length(subgraph, concept, node)
                color = ['lightblue', 'lightgreen', 'lightcoral'][min(distance - 1, 2)]
                size = 30 - distance * 5
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(
                    size=size,
                    color=color,
                    line=dict(width=2, color='white')
                ),
                text=node,
                textposition="top center",
                hovertext=f"{node}<br>Occurrences: {node_data.get('count', 0)}",
                hoverinfo='text',
                showlegend=False
            ))
        
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=600,
            margin=dict(l=0, r=0, t=40, b=0),
            title=dict(
                text=f"Concept Connections: {concept}",
                font=dict(size=24, color='white'),
                x=0.5
            )
        )
        
        return fig
    
    def _radial_layout(self, graph, center_node):
        """Create a radial layout with center_node at the center"""
        pos = {}
        pos[center_node] = (0, 0)
        
        # Get nodes by distance from center
        distances = nx.single_source_shortest_path_length(graph, center_node)
        
        # Group nodes by distance
        layers = {}
        for node, dist in distances.items():
            if dist not in layers:
                layers[dist] = []
            layers[dist].append(node)
        
        # Position nodes in concentric circles
        for dist, nodes in layers.items():
            if dist == 0:
                continue
            
            radius = dist * 0.5
            angle_step = 2 * np.pi / len(nodes)
            
            for i, node in enumerate(nodes):
                angle = i * angle_step
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                pos[node] = (x, y)
        
        return pos


class TimelineVisualizer:
    """Creates timeline visualizations for concept evolution"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        
    def create_concept_evolution_timeline(self, concepts: List[str]) -> go.Figure:
        """Create timeline showing how concepts appear across episodes"""
        
        # Get episodes sorted by date
        episodes = self.data_manager.get_all_episodes(valid_only=True)
        episodes.sort(key=lambda x: x.processed_date)
        
        # Track concept appearances
        timeline_data = []
        
        for episode in episodes:
            episode_concepts = [
                c.get('concept', '') 
                for c in episode.philosophical_content.get('concepts_explored', [])
                if isinstance(c, dict)
            ]
            
            for concept in concepts:
                if concept in episode_concepts:
                    timeline_data.append({
                        'date': episode.processed_date,
                        'concept': concept,
                        'episode': episode.title,
                        'complexity': episode.episode_metrics.get('complexity_score', 0)
                    })
        
        if not timeline_data:
            return go.Figure().add_annotation(text="No data found for selected concepts", showarrow=False)
        
        df = pd.DataFrame(timeline_data)
        
        # Create figure
        fig = go.Figure()
        
        # Add trace for each concept
        for concept in concepts:
            concept_df = df[df['concept'] == concept]
            
            fig.add_trace(go.Scatter(
                x=concept_df['date'],
                y=concept_df['complexity'],
                mode='markers+lines',
                name=concept,
                marker=dict(size=10),
                line=dict(width=2),
                hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Complexity: %{y:.1f}<extra></extra>',
                text=concept_df['episode']
            ))
        
        fig.update_layout(
            title="Concept Evolution Over Time",
            xaxis_title="Episode Date",
            yaxis_title="Episode Complexity",
            hovermode='x unified',
            template='plotly_dark',
            height=500
        )
        
        return fig
    
    def create_philosophical_journey_map(self, episodes: List[str]) -> go.Figure:
        """Create a journey map through selected episodes"""
        
        # Get episode data
        episode_objects = []
        for ep_id in episodes:
            ep = self.data_manager.get_episode(ep_id)
            if ep:
                episode_objects.append(ep)
        
        if not episode_objects:
            return go.Figure().add_annotation(text="No episodes found", showarrow=False)
        
        # Create connections based on shared concepts
        connections = []
        for i in range(len(episode_objects) - 1):
            ep1 = episode_objects[i]
            ep2 = episode_objects[i + 1]
            
            concepts1 = set([c.get('concept', '') for c in ep1.philosophical_content.get('concepts_explored', [])])
            concepts2 = set([c.get('concept', '') for c in ep2.philosophical_content.get('concepts_explored', [])])
            
            shared = concepts1 & concepts2
            connections.append(len(shared))
        
        # Create figure
        fig = go.Figure()
        
        # Add path
        x = list(range(len(episode_objects)))
        y = [ep.episode_metrics.get('complexity_score', 5) for ep in episode_objects]
        
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            line=dict(color='cyan', width=3),
            marker=dict(size=15, color='gold'),
            showlegend=False
        ))
        
        # Add episode labels
        for i, ep in enumerate(episode_objects):
            fig.add_annotation(
                x=i,
                y=y[i],
                text=ep.title[:30] + "...",
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-40,
                bgcolor='rgba(0,0,0,0.8)',
                bordercolor='white',
                borderwidth=1
            )
        
        # Add connection strength
        for i, strength in enumerate(connections):
            fig.add_annotation(
                x=i + 0.5,
                y=(y[i] + y[i+1]) / 2,
                text=f"{strength} shared concepts",
                showarrow=False,
                bgcolor='rgba(100,100,200,0.8)',
                bordercolor='white',
                borderwidth=1,
                font=dict(size=10)
            )
        
        fig.update_layout(
            title="Philosophical Journey Map",
            xaxis=dict(showticklabels=False, title="Journey Progress"),
            yaxis_title="Complexity Level",
            template='plotly_dark',
            height=500
        )
        
        return fig