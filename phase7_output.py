"""
Phase 7: Output Generation
Display results and save selected ideas to file
"""

import os
from datetime import datetime
from typing import List, Dict, Any
from config import Config
from input_helpers import confirm, get_user_input


class OutputGeneration:
    """Handles output display and file generation."""

    def __init__(self, config: Config):
        self.config = config

    def execute(
        self,
        ideas: List[Dict[str, Any]],
        opportunity: Dict[str, Any],
        context: Dict[str, Any],
        criteria: Dict[str, Any]
    ):
        """Execute the output generation phase."""

        # Display all ideas
        self._display_all_ideas(ideas)

        # Display force ranking
        self._display_force_ranking(ideas)

        # Ask which ideas to save
        print("\n" + "=" * 60)
        print("SAVE IDEAS")
        print("=" * 60 + "\n")

        save_all = confirm("Would you like to save all ideas to a file?")

        if save_all:
            self._save_ideas_to_file(ideas, opportunity, context, criteria)
        else:
            # Ask which specific ideas to save
            selected_indices = self._select_ideas_to_save(ideas)
            if selected_indices:
                selected_ideas = [ideas[i] for i in selected_indices]
                self._save_ideas_to_file(selected_ideas, opportunity, context, criteria)
            else:
                print("\nNo ideas saved.")

    def _display_all_ideas(self, ideas: List[Dict[str, Any]]):
        """Display all generated ideas."""
        print("Generated Ideas:\n")

        for i, idea in enumerate(ideas, 1):
            print("=" * 60)
            print(f"IDEA {i}: {idea['title']}")
            print("=" * 60)
            print(idea['content'])
            print(f"\nScore: {idea['score']}/100")
            if idea.get('rank'):
                print(f"Rank: #{idea['rank']}")
            print()

    def _display_force_ranking(self, ideas: List[Dict[str, Any]]):
        """Display the top 3 force-ranked ideas."""
        ranked_ideas = [idea for idea in ideas if idea.get('rank')]
        ranked_ideas.sort(key=lambda x: x['rank'])

        if not ranked_ideas:
            return

        print("\n" + "=" * 60)
        print("TOP 3 FORCE RANKED IDEAS")
        print("=" * 60 + "\n")

        for idea in ranked_ideas[:3]:
            print(f"{idea['rank']}. {idea['title']}")
            print(f"   Score: {idea['score']}/100")

            # Extract reasoning if available
            if "**Force Ranking Reasoning:**" in idea['content']:
                reasoning = idea['content'].split("**Force Ranking Reasoning:**")[1].split("**")[0].strip()
                print(f"   Reasoning: {reasoning[:200]}...")

            print()

    def _select_ideas_to_save(self, ideas: List[Dict[str, Any]]) -> List[int]:
        """Let user select which ideas to save."""
        print("Which ideas would you like to save?")
        print("Enter the idea numbers separated by commas (e.g., 1,3,5)")
        print(f"Available ideas: 1-{len(ideas)}")

        response = get_user_input("Idea numbers:", required=False)

        if not response:
            return []

        # Parse the response
        try:
            indices = []
            for num_str in response.split(","):
                num = int(num_str.strip())
                if 1 <= num <= len(ideas):
                    indices.append(num - 1)  # Convert to 0-based index
                else:
                    print(f"Warning: Ignoring invalid idea number: {num}")

            return indices

        except ValueError:
            print("Invalid format. No ideas saved.")
            return []

    def _save_ideas_to_file(
        self,
        ideas: List[Dict[str, Any]],
        opportunity: Dict[str, Any],
        context: Dict[str, Any],
        criteria: Dict[str, Any]
    ):
        """Save selected ideas to a markdown file."""

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ideation_session_{timestamp}.md"
        filepath = os.path.join(self.config.output_dir, filename)

        # Build markdown content
        content = self._build_markdown_output(ideas, opportunity, context, criteria)

        # Write to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"\n✓ Ideas saved to: {filepath}")
            print(f"  ({len(ideas)} idea(s) saved)")

        except Exception as e:
            print(f"\n✗ Error saving file: {str(e)}")

    def _build_markdown_output(
        self,
        ideas: List[Dict[str, Any]],
        opportunity: Dict[str, Any],
        context: Dict[str, Any],
        criteria: Dict[str, Any]
    ) -> str:
        """Build markdown-formatted output."""

        parts = [
            "# Ideation Session Output",
            f"\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "\n---\n",
            "## Opportunity",
            f"\n**Problem/Desire:** {opportunity.get('description', 'N/A')}",
        ]

        if opportunity.get('who'):
            parts.append(f"\n**Who:** {opportunity['who']}")
        if opportunity.get('context'):
            parts.append(f"\n**Context:** {opportunity['context']}")

        # Add context section
        parts.append("\n---\n")
        parts.append("## Context")

        if context.get('icp'):
            parts.append(f"\n### Target Audience\n{context['icp']}")
        if context.get('primary_metric'):
            parts.append(f"\n### Primary Metric\n{context['primary_metric']}")

        # Add evaluation criteria
        parts.append("\n---\n")
        parts.append("## Evaluation Criteria\n")

        sorted_criteria = sorted(
            criteria['weights'].items(),
            key=lambda x: x[1],
            reverse=True
        )

        for criterion, weight in sorted_criteria:
            parts.append(f"- {criterion}: {weight}/5")

        # Add force ranking
        ranked_ideas = [idea for idea in ideas if idea.get('rank')]
        if ranked_ideas:
            parts.append("\n---\n")
            parts.append("## Top 3 Force Ranked Ideas\n")

            ranked_ideas.sort(key=lambda x: x['rank'])
            for idea in ranked_ideas[:3]:
                parts.append(f"\n{idea['rank']}. **{idea['title']}** (Score: {idea['score']}/100)")

        # Add all ideas
        parts.append("\n---\n")
        parts.append("## Generated Ideas\n")

        for i, idea in enumerate(ideas, 1):
            parts.append(f"\n### Idea {i}: {idea['title']}\n")
            parts.append(f"**Score:** {idea['score']}/100")
            if idea.get('rank'):
                parts.append(f" | **Rank:** #{idea['rank']}")
            parts.append(f"\n\n{idea['content']}\n")

        # Add footer
        parts.append("\n---\n")
        parts.append("*Generated by Ideation Agent*")

        return "\n".join(parts)
