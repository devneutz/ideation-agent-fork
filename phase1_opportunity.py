"""
Phase 1: Opportunity Discovery
Guides user through understanding the opportunity they want to solve
"""

from typing import Dict, Any
from input_helpers import get_user_input, confirm


class OpportunityDiscovery:
    """Handles the opportunity discovery phase."""

    def __init__(self):
        self.opportunity = {}

    def execute(self) -> Dict[str, Any]:
        """Execute the opportunity discovery phase."""
        print("Let's understand the opportunity you want to address.\n")

        # Get main opportunity description
        self.opportunity["description"] = get_user_input(
            "What is the customer pain point, wish, or desire you want to solve?",
            required=True
        )

        print("\nGreat! Now let me ask some clarifying questions...\n")

        # Ask clarifying questions
        self.opportunity["who"] = get_user_input(
            "Who is experiencing this problem/desire? (e.g., specific user persona, role, or segment)",
            required=False
        )

        self.opportunity["context"] = get_user_input(
            "In which context or during the execution of which task does this occur?",
            required=False
        )

        self.opportunity["frequency"] = get_user_input(
            "How frequently does this problem/desire arise?",
            required=False
        )

        self.opportunity["impact"] = get_user_input(
            "What is the impact when this problem is not solved or desire is not met?",
            required=False
        )

        self.opportunity["current_solutions"] = get_user_input(
            "How are people currently trying to solve this or fulfill this desire?",
            required=False
        )

        self.opportunity["additional_notes"] = get_user_input(
            "Any other important context or details about this opportunity?",
            required=False
        )

        # Display summary
        print("\n" + "-" * 60)
        print("OPPORTUNITY SUMMARY")
        print("-" * 60)
        self._display_summary()

        # Confirm before proceeding
        if not confirm("\nDoes this accurately capture the opportunity?"):
            print("\nLet's refine the opportunity description...")
            return self.execute()  # Restart the phase

        return self.opportunity

    def _display_summary(self):
        """Display a formatted summary of the opportunity."""
        print(f"\nOpportunity: {self.opportunity['description']}")

        if self.opportunity.get("who"):
            print(f"\nWho: {self.opportunity['who']}")

        if self.opportunity.get("context"):
            print(f"\nContext: {self.opportunity['context']}")

        if self.opportunity.get("frequency"):
            print(f"\nFrequency: {self.opportunity['frequency']}")

        if self.opportunity.get("impact"):
            print(f"\nImpact: {self.opportunity['impact']}")

        if self.opportunity.get("current_solutions"):
            print(f"\nCurrent Solutions: {self.opportunity['current_solutions']}")

        if self.opportunity.get("additional_notes"):
            print(f"\nAdditional Notes: {self.opportunity['additional_notes']}")
