"""
Phase 4: Competitive Analysis (Optional)
Gather insights from competitors or alternative solutions
"""

from typing import List, Dict, Any
from input_helpers import get_user_input, confirm


class CompetitiveAnalysis:
    """Handles the competitive analysis phase."""

    def __init__(self):
        self.insights = []

    def execute(self) -> List[Dict[str, Any]]:
        """Execute the competitive analysis phase."""
        print("Would you like to review competitors, user alternatives, or other")
        print("interesting players for inspiration?\n")

        analyze = confirm("Include competitive analysis?")

        if not analyze:
            print("\nSkipping competitive analysis.")
            return []

        print("\nGreat! Let's gather some competitive intelligence.\n")
        print("Please provide URLs to competitors or alternative solutions.")
        print("You can add multiple URLs (enter empty line when done).\n")

        urls = []
        while True:
            url = get_user_input(
                f"URL {len(urls) + 1} (or press Enter to finish):",
                required=False
            )

            if not url:
                break

            # Validate URL format (basic check)
            if not (url.startswith("http://") or url.startswith("https://")):
                print("Please enter a valid URL starting with http:// or https://")
                continue

            urls.append(url)

        if not urls:
            print("\nNo URLs provided. Skipping competitive analysis.")
            return []

        # For each URL, gather manual notes
        print(f"\n{len(urls)} URL(s) provided.")
        print("\nFor each competitor, please provide your observations or notes:")
        print("(This will help inform the idea generation)\n")

        for i, url in enumerate(urls, 1):
            print(f"\n{i}. {url}")
            notes = get_user_input(
                "What's interesting about this competitor/alternative?",
                required=False,
                multiline=True
            )

            self.insights.append({
                "url": url,
                "notes": notes
            })

        # Display summary
        self._display_summary()

        return self.insights

    def _display_summary(self):
        """Display a summary of competitive insights."""
        print("\n" + "-" * 60)
        print("COMPETITIVE INSIGHTS SUMMARY")
        print("-" * 60 + "\n")

        for i, insight in enumerate(self.insights, 1):
            print(f"{i}. {insight['url']}")
            if insight['notes']:
                # Show first 100 chars of notes
                preview = insight['notes'][:100]
                if len(insight['notes']) > 100:
                    preview += "..."
                print(f"   Notes: {preview}\n")
