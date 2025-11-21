"""
Phase 5: Example Collection
Collect seed ideas from the user to understand their expectations
"""

from typing import List, Dict, Any
from input_helpers import get_user_input


class ExampleCollection:
    """Handles the example idea collection phase."""

    def __init__(self):
        self.examples = []

    def execute(self) -> List[Dict[str, Any]]:
        """Execute the example collection phase."""
        print("To help calibrate the idea generation, please provide 1-5 example ideas.\n")
        print("These don't need to be your best ideas - they help me understand:")
        print("  • The level of detail you're looking for")
        print("  • The types of solutions you're interested in")
        print("  • The scope and scale of ideas\n")
        print("You can provide 1-5 ideas. Enter an empty response when done.\n")

        for i in range(5):
            print(f"\n" + "-" * 60)
            print(f"EXAMPLE IDEA {i + 1}/5 (or press Enter to finish)")
            print("-" * 60)

            idea_text = get_user_input(
                "Describe the idea:",
                required=(i == 0),  # Only first idea is required
                multiline=True
            )

            if not idea_text and i > 0:
                print(f"\nFinished with {i} example idea(s).")
                break

            self.examples.append({
                "id": i + 1,
                "description": idea_text
            })

        # Analyze patterns
        self._analyze_patterns()

        # Display summary
        self._display_summary()

        return self.examples

    def _analyze_patterns(self):
        """Analyze patterns in example ideas."""
        # Simple analysis of example characteristics
        total_length = sum(len(ex["description"]) for ex in self.examples)
        avg_length = total_length // len(self.examples)

        # Store analysis
        for example in self.examples:
            example["word_count"] = len(example["description"].split())
            example["char_count"] = len(example["description"])

        self.pattern_analysis = {
            "avg_length": avg_length,
            "avg_word_count": sum(ex["word_count"] for ex in self.examples) // len(self.examples),
            "detail_level": "detailed" if avg_length > 300 else "concise" if avg_length > 100 else "brief"
        }

    def _display_summary(self):
        """Display a summary of collected examples."""
        print("\n" + "-" * 60)
        print("EXAMPLE IDEAS SUMMARY")
        print("-" * 60 + "\n")

        print(f"✓ Collected {len(self.examples)} example ideas")
        print(f"\nPattern Analysis:")
        print(f"  • Average length: {self.pattern_analysis['avg_length']} characters")
        print(f"  • Average words: {self.pattern_analysis['avg_word_count']} words")
        print(f"  • Detail level: {self.pattern_analysis['detail_level']}")

        print("\nExample ideas preview:")
        for i, example in enumerate(self.examples, 1):
            preview = example["description"][:80]
            if len(example["description"]) > 80:
                preview += "..."
            print(f"  {i}. {preview}")

    def get_pattern_analysis(self) -> Dict[str, Any]:
        """Get the pattern analysis results."""
        return self.pattern_analysis
