"""
Phase 3: Evaluation Criteria Setup
Define and weight criteria for evaluating ideas
"""

from typing import Dict, Any, List
from config import Config
from input_helpers import get_user_input, confirm, get_rating


class CriteriaSetup:
    """Handles the evaluation criteria setup phase."""

    def __init__(self, config: Config):
        self.config = config
        self.criteria = {}

    def execute(self) -> Dict[str, Any]:
        """Execute the criteria setup phase."""
        print("Let's define criteria for evaluating ideas.\n")

        # Show default criteria
        print("Default criteria:")
        for i, criterion in enumerate(self.config.default_criteria, 1):
            print(f"  {i}. {criterion}")

        # Ask if user wants to use defaults or customize
        use_defaults = confirm("\nWould you like to use these default criteria?")

        if use_defaults:
            criteria_list = self.config.default_criteria.copy()
        else:
            criteria_list = self._get_custom_criteria()

        # Get importance ratings for each criterion
        print("\nNow, let's rate the importance of each criterion.")
        print("Rate each from 1 (least important) to 5 (most important)\n")

        criteria_with_weights = {}
        for criterion in criteria_list:
            weight = get_rating(f"Importance of '{criterion}':", min_val=1, max_val=5)
            criteria_with_weights[criterion] = weight

        # Store criteria
        self.criteria["criteria_list"] = criteria_list
        self.criteria["weights"] = criteria_with_weights

        # Display summary
        self._display_summary()

        return self.criteria

    def _get_custom_criteria(self) -> List[str]:
        """Get custom criteria from user."""
        print("\nLet's define your custom criteria.")
        print("You can add 1-10 criteria. Enter an empty line when done.\n")

        criteria = []
        for i in range(10):
            if i == 0:
                criterion = get_user_input(
                    f"Criterion {i+1}:",
                    required=True
                )
            else:
                criterion = get_user_input(
                    f"Criterion {i+1} (or press Enter to finish):",
                    required=False
                )

            if not criterion:
                break

            criteria.append(criterion)

        if len(criteria) == 0:
            print("No criteria provided. Using default criteria.")
            return self.config.default_criteria.copy()

        return criteria

    def _display_summary(self):
        """Display a summary of criteria and weights."""
        print("\n" + "-" * 60)
        print("EVALUATION CRITERIA SUMMARY")
        print("-" * 60 + "\n")

        max_weight = max(self.criteria["weights"].values())

        print("Criteria (sorted by importance):\n")
        sorted_criteria = sorted(
            self.criteria["weights"].items(),
            key=lambda x: x[1],
            reverse=True
        )

        for criterion, weight in sorted_criteria:
            bars = "█" * weight + "░" * (5 - weight)
            star = " ⭐" if weight == max_weight else ""
            print(f"  {criterion}")
            print(f"    {bars} {weight}/5{star}\n")
