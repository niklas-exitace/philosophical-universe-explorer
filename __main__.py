"""Command-line interface for Project Simone"""

import click
import logging
from pathlib import Path
from src.core import SimoneEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def cli(ctx):
    """Project Simone - Intelligent Philosophical Content Analysis"""
    ctx.ensure_object(dict)
    ctx.obj['engine'] = SimoneEngine()


@cli.command()
@click.pass_context
def stats(ctx):
    """Show statistics about analyzed content"""
    engine = ctx.obj['engine']
    stats = engine.get_statistics()
    
    click.echo("\n📊 Project Simone Statistics")
    click.echo("=" * 40)
    click.echo(f"Total Episodes: {stats['total_episodes']}")
    click.echo(f"Valid Episodes: {stats['valid_episodes']}")
    click.echo(f"Failed Episodes: {stats['failed_episodes']}")
    click.echo(f"Unique Concepts: {stats['total_concepts']}")
    click.echo(f"Philosophers Mentioned: {stats['total_philosophers']}")
    click.echo(f"Average Complexity: {stats['avg_complexity']:.2f}/10")
    click.echo(f"Avg Concepts/Episode: {stats['avg_concepts_per_episode']:.1f}")


@cli.command()
@click.option('--concept', '-c', help='Generate map for specific concept')
@click.option('--output', '-o', help='Output file path')
@click.pass_context
def concepts(ctx, concept, output):
    """Generate concept map"""
    engine = ctx.obj['engine']
    
    click.echo(f"\n🗺️  Generating concept map{' for: ' + concept if concept else ''}...")
    
    concept_map = engine.generate_concept_map(concept)
    
    if output:
        import json
        with open(output, 'w') as f:
            json.dump(concept_map, f, indent=2)
        click.echo(f"✅ Concept map saved to: {output}")
    else:
        # Display summary
        if concept:
            click.echo(f"\nConcept: {concept_map.get('concept', 'Unknown')}")
            click.echo(f"Occurrences: {concept_map.get('occurrences', 0)}")
            click.echo(f"Related Concepts: {len(concept_map.get('related_concepts', []))}")
        else:
            click.echo(f"\nTotal Concepts: {concept_map.get('total_concepts', 0)}")
            click.echo(f"Total Relationships: {concept_map.get('total_relationships', 0)}")
            click.echo("\nTop Concepts by Frequency:")
            for item in concept_map.get('top_concepts_by_frequency', [])[:5]:
                click.echo(f"  - {item['concept']}: {item['count']} times")


@cli.command()
@click.option('--topic', '-t', help='Focus on specific topic')
@click.option('--episodes', '-e', multiple=True, help='Specific episode IDs')
@click.option('--output', '-o', help='Output file path')
@click.pass_context
def insights(ctx, topic, episodes, output):
    """Generate philosophical insights"""
    engine = ctx.obj['engine']
    
    click.echo(f"\n💡 Generating insights{' for: ' + topic if topic else ''}...")
    
    insights = engine.generate_insights(topic, list(episodes) if episodes else None)
    
    if output:
        import json
        with open(output, 'w') as f:
            json.dump(insights, f, indent=2)
        click.echo(f"✅ Insights saved to: {output}")
    else:
        # Display summary
        click.echo(f"\nTopic: {insights.get('topic', 'General')}")
        click.echo(f"Episodes Analyzed: {insights.get('episode_count', 0)}")
        
        if insights.get('meta_insights'):
            click.echo("\nKey Insights:")
            for insight in insights['meta_insights'][:3]:
                click.echo(f"  • {insight}")


@cli.command()
@click.argument('question')
@click.option('--episode', '-e', help='Ask about specific episode')
@click.pass_context
def ask(ctx, question, episode):
    """Ask a question about the philosophical content"""
    engine = ctx.obj['engine']
    
    if episode:
        engine.set_current_episode(episode)
        context = 'episode'
    else:
        context = 'all'
    
    click.echo(f"\n🤔 Processing your question...")
    answer = engine.ask_question(question, context)
    
    click.echo(f"\n💭 Answer:\n{answer}")


@cli.command()
@click.option('--format', '-f', type=click.Choice(['json', 'csv']), default='json')
@click.option('--output', '-o', help='Output file path')
@click.pass_context
def export(ctx, format, output):
    """Export insights and analysis"""
    engine = ctx.obj['engine']
    
    click.echo(f"\n📤 Exporting insights in {format} format...")
    
    filepath = engine.export_insights(format, Path(output) if output else None)
    
    click.echo(f"✅ Exported to: {filepath}")


@cli.command()
@click.pass_context
def serve(ctx):
    """Launch the web interface"""
    click.echo("\n🚀 Launching Project Simone web interface...")
    click.echo("Note: Web interface not yet implemented")
    # TODO: Implement Streamlit interface launcher


if __name__ == '__main__':
    cli()