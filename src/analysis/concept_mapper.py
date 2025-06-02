"""Concept mapping and relationship analysis"""

import logging
from typing import Dict, List, Any, Tuple
import networkx as nx
from collections import defaultdict

logger = logging.getLogger(__name__)


class ConceptMapper:
    """Maps relationships between philosophical concepts across episodes"""
    
    def __init__(self, data_manager):
        """Initialize concept mapper"""
        self.data_manager = data_manager
        self.concept_graph = nx.Graph()
        self._build_concept_graph()
    
    def _build_concept_graph(self):
        """Build a graph of concept relationships"""
        logger.info("Building concept graph...")
        
        # Get all episodes
        episodes = self.data_manager.get_all_episodes(valid_only=True)
        
        # Track concept co-occurrences
        for episode in episodes:
            concepts = episode.philosophical_content.get('concepts_explored', [])
            concept_names = [c.get('concept', '') for c in concepts if isinstance(c, dict) and c.get('concept')]
            
            # Add nodes
            for concept in concept_names:
                if not self.concept_graph.has_node(concept):
                    self.concept_graph.add_node(concept, episodes=[], count=0)
                
                # Update node data
                self.concept_graph.nodes[concept]['episodes'].append(episode.episode_id)
                self.concept_graph.nodes[concept]['count'] += 1
            
            # Add edges for co-occurring concepts
            for i in range(len(concept_names)):
                for j in range(i + 1, len(concept_names)):
                    concept1, concept2 = concept_names[i], concept_names[j]
                    
                    if self.concept_graph.has_edge(concept1, concept2):
                        self.concept_graph[concept1][concept2]['weight'] += 1
                        self.concept_graph[concept1][concept2]['episodes'].append(episode.episode_id)
                    else:
                        self.concept_graph.add_edge(concept1, concept2, weight=1, episodes=[episode.episode_id])
        
        logger.info(f"Built concept graph with {self.concept_graph.number_of_nodes()} concepts and "
                   f"{self.concept_graph.number_of_edges()} relationships")
    
    def map_single_concept(self, concept: str) -> Dict[str, Any]:
        """Map relationships for a single concept"""
        if not self.concept_graph.has_node(concept):
            # Try case-insensitive search
            for node in self.concept_graph.nodes():
                if node.lower() == concept.lower():
                    concept = node
                    break
            else:
                return {'error': f'Concept "{concept}" not found'}
        
        # Get concept data
        node_data = self.concept_graph.nodes[concept]
        
        # Get related concepts
        neighbors = list(self.concept_graph.neighbors(concept))
        related_concepts = []
        
        for neighbor in neighbors:
            edge_data = self.concept_graph[concept][neighbor]
            related_concepts.append({
                'concept': neighbor,
                'strength': edge_data['weight'],
                'shared_episodes': edge_data['episodes']
            })
        
        # Sort by relationship strength
        related_concepts.sort(key=lambda x: x['strength'], reverse=True)
        
        # Get episodes where concept appears
        episodes = []
        for ep_id in node_data['episodes']:
            episode = self.data_manager.get_episode(ep_id)
            if episode:
                # Find concept details in episode
                concept_details = None
                for c in episode.philosophical_content.get('concepts_explored', []):
                    if isinstance(c, dict) and c.get('concept', '').lower() == concept.lower():
                        concept_details = c
                        break
                
                episodes.append({
                    'episode_id': ep_id,
                    'title': episode.title,
                    'definition': concept_details.get('definition_given', '') if concept_details else '',
                    'application': concept_details.get('practical_application', '') if concept_details else ''
                })
        
        return {
            'concept': concept,
            'occurrences': node_data['count'],
            'episodes': episodes,
            'related_concepts': related_concepts[:10],  # Top 10 related
            'centrality_score': nx.degree_centrality(self.concept_graph).get(concept, 0),
            'clustering_coefficient': nx.clustering(self.concept_graph).get(concept, 0)
        }
    
    def map_all_concepts(self) -> Dict[str, Any]:
        """Create a comprehensive concept map"""
        # Calculate various graph metrics
        degree_centrality = nx.degree_centrality(self.concept_graph)
        betweenness_centrality = nx.betweenness_centrality(self.concept_graph)
        clustering = nx.clustering(self.concept_graph)
        
        # Get top concepts by different metrics
        top_by_frequency = sorted(
            [(node, data['count']) for node, data in self.concept_graph.nodes(data=True)],
            key=lambda x: x[1], reverse=True
        )[:20]
        
        top_by_centrality = sorted(
            degree_centrality.items(),
            key=lambda x: x[1], reverse=True
        )[:20]
        
        top_by_betweenness = sorted(
            betweenness_centrality.items(),
            key=lambda x: x[1], reverse=True
        )[:20]
        
        # Find concept clusters
        clusters = self._find_concept_clusters()
        
        # Find strongly connected concept pairs
        strong_connections = []
        for edge in self.concept_graph.edges(data=True):
            if edge[2]['weight'] >= 3:  # Appeared together 3+ times
                strong_connections.append({
                    'concepts': [edge[0], edge[1]],
                    'strength': edge[2]['weight'],
                    'episodes': edge[2]['episodes']
                })
        
        strong_connections.sort(key=lambda x: x['strength'], reverse=True)
        
        return {
            'total_concepts': self.concept_graph.number_of_nodes(),
            'total_relationships': self.concept_graph.number_of_edges(),
            'top_concepts_by_frequency': [{'concept': c, 'count': cnt} for c, cnt in top_by_frequency],
            'top_concepts_by_centrality': [{'concept': c, 'score': s} for c, s in top_by_centrality],
            'top_concepts_by_betweenness': [{'concept': c, 'score': s} for c, s in top_by_betweenness],
            'concept_clusters': clusters,
            'strong_connections': strong_connections[:20],
            'graph_density': nx.density(self.concept_graph),
            'average_clustering': nx.average_clustering(self.concept_graph)
        }
    
    def _find_concept_clusters(self) -> List[Dict[str, Any]]:
        """Find clusters of related concepts"""
        # Use community detection if graph is large enough
        if self.concept_graph.number_of_nodes() < 5:
            return []
        
        try:
            # Find connected components
            clusters = []
            for component in nx.connected_components(self.concept_graph):
                if len(component) >= 3:  # Only meaningful clusters
                    cluster_subgraph = self.concept_graph.subgraph(component)
                    
                    # Find most central concept in cluster
                    centrality = nx.degree_centrality(cluster_subgraph)
                    central_concept = max(centrality.items(), key=lambda x: x[1])[0]
                    
                    clusters.append({
                        'size': len(component),
                        'concepts': list(component),
                        'central_concept': central_concept,
                        'density': nx.density(cluster_subgraph)
                    })
            
            # Sort by size
            clusters.sort(key=lambda x: x['size'], reverse=True)
            return clusters[:10]  # Top 10 clusters
            
        except Exception as e:
            logger.error(f"Error finding concept clusters: {e}")
            return []
    
    def find_concept_path(self, concept1: str, concept2: str) -> Dict[str, Any]:
        """Find conceptual path between two concepts"""
        # Normalize concept names
        concept1_norm = None
        concept2_norm = None
        
        for node in self.concept_graph.nodes():
            if node.lower() == concept1.lower():
                concept1_norm = node
            if node.lower() == concept2.lower():
                concept2_norm = node
        
        if not concept1_norm or not concept2_norm:
            return {'error': 'One or both concepts not found'}
        
        try:
            # Find shortest path
            path = nx.shortest_path(self.concept_graph, concept1_norm, concept2_norm)
            
            # Get episodes for each connection in path
            path_details = []
            for i in range(len(path) - 1):
                edge_data = self.concept_graph[path[i]][path[i + 1]]
                path_details.append({
                    'from': path[i],
                    'to': path[i + 1],
                    'shared_episodes': edge_data['episodes'],
                    'strength': edge_data['weight']
                })
            
            return {
                'concept1': concept1_norm,
                'concept2': concept2_norm,
                'path': path,
                'path_length': len(path) - 1,
                'path_details': path_details
            }
            
        except nx.NetworkXNoPath:
            return {
                'concept1': concept1_norm,
                'concept2': concept2_norm,
                'error': 'No path found between concepts'
            }
    
    def export_for_visualization(self) -> Dict[str, Any]:
        """Export graph data for visualization"""
        nodes = []
        edges = []
        
        # Export nodes
        for node, data in self.concept_graph.nodes(data=True):
            nodes.append({
                'id': node,
                'label': node,
                'size': data['count'],
                'episodes': len(data['episodes'])
            })
        
        # Export edges
        for edge in self.concept_graph.edges(data=True):
            edges.append({
                'source': edge[0],
                'target': edge[1],
                'weight': edge[2]['weight']
            })
        
        return {
            'nodes': nodes,
            'edges': edges
        }