"""
Phase 2: Context Gathering
Collects product and business context from the user
"""

from typing import Dict, Any
from input_helpers import get_input_with_file_option


class ContextGathering:
    """Handles the context gathering phase."""

    def __init__(self):
        self.context = {}

    def execute(self) -> Dict[str, Any]:
        """Execute the context gathering phase."""
        print("Now let's gather context about your product and business.\n")
        print("For each item, you can type directly, provide a file/folder path, or skip.\n")

        # ICP / Target Audience
        print("\n" + "-" * 60)
        print("1. ICP / TARGET AUDIENCE")
        print("-" * 60)
        self.context["icp"] = get_input_with_file_option(
            "Describe your Ideal Customer Profile (ICP) or target audience:",
            required=False
        )

        # Product Vision & Strategy
        print("\n" + "-" * 60)
        print("2. PRODUCT VISION & STRATEGY")
        print("-" * 60)
        self.context["vision"] = get_input_with_file_option(
            "What is your product vision and strategy?",
            required=False
        )

        # Product Category & Description
        print("\n" + "-" * 60)
        print("3. PRODUCT CATEGORY & DESCRIPTION")
        print("-" * 60)
        self.context["product_description"] = get_input_with_file_option(
            "Describe your product category and what your product does:",
            required=False
        )

        # Primary Product Metric
        print("\n" + "-" * 60)
        print("4. PRIMARY PRODUCT METRIC")
        print("-" * 60)
        self.context["primary_metric"] = get_input_with_file_option(
            "What is the #1 product metric you're trying to drive by addressing this opportunity?",
            required=False
        )

        # Constraints
        print("\n" + "-" * 60)
        print("5. CONSTRAINTS")
        print("-" * 60)
        self.context["constraints"] = get_input_with_file_option(
            "Are there areas where you don't want to play, or any other important constraints?",
            required=False
        )

        # Display summary
        self._display_summary()

        return self.context

    def _display_summary(self):
        """Display a summary of gathered context."""
        print("\n" + "-" * 60)
        print("CONTEXT SUMMARY")
        print("-" * 60)

        items_provided = 0

        if self.context.get("icp"):
            items_provided += 1
            print(f"\n✓ ICP/Target Audience: Provided ({len(self.context['icp'])} chars)")

        if self.context.get("vision"):
            items_provided += 1
            print(f"✓ Product Vision: Provided ({len(self.context['vision'])} chars)")

        if self.context.get("product_description"):
            items_provided += 1
            print(f"✓ Product Description: Provided ({len(self.context['product_description'])} chars)")

        if self.context.get("primary_metric"):
            items_provided += 1
            print(f"✓ Primary Metric: Provided ({len(self.context['primary_metric'])} chars)")

        if self.context.get("constraints"):
            items_provided += 1
            print(f"✓ Constraints: Provided ({len(self.context['constraints'])} chars)")

        print(f"\nTotal context items provided: {items_provided}/5")
