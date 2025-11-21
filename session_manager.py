"""
Session Manager - Orchestrates the ideation workflow
"""

from typing import Dict, Any, Optional
from config import Config
from phase1_opportunity import OpportunityDiscovery
from phase2_context import ContextGathering
from phase3_criteria import CriteriaSetup
from phase4_competitive import CompetitiveAnalysis
from phase5_examples import ExampleCollection
from phase6_generation import IdeaGeneration
from phase7_output import OutputGeneration


class SessionManager:
    """Manages the ideation session state and workflow."""

    def __init__(self, config: Config):
        self.config = config
        self.state: Dict[str, Any] = {
            "opportunity": {},
            "context": {},
            "criteria": {},
            "competitive_insights": [],
            "example_ideas": [],
            "generated_ideas": [],
            "phase": 1
        }

    def run(self):
        """Run the complete ideation session."""
        print("Let's start your ideation session!\n")

        # Phase 1: Opportunity Discovery
        print("=" * 60)
        print("PHASE 1: OPPORTUNITY DISCOVERY")
        print("=" * 60 + "\n")
        phase1 = OpportunityDiscovery()
        self.state["opportunity"] = phase1.execute()

        # Phase 2: Context Gathering
        print("\n" + "=" * 60)
        print("PHASE 2: CONTEXT GATHERING")
        print("=" * 60 + "\n")
        phase2 = ContextGathering()
        self.state["context"] = phase2.execute()

        # Phase 3: Evaluation Criteria Setup
        print("\n" + "=" * 60)
        print("PHASE 3: EVALUATION CRITERIA")
        print("=" * 60 + "\n")
        phase3 = CriteriaSetup(self.config)
        self.state["criteria"] = phase3.execute()

        # Phase 4: Competitive Analysis (Optional)
        print("\n" + "=" * 60)
        print("PHASE 4: COMPETITIVE ANALYSIS (OPTIONAL)")
        print("=" * 60 + "\n")
        phase4 = CompetitiveAnalysis()
        self.state["competitive_insights"] = phase4.execute()

        # Phase 5: Example Collection
        print("\n" + "=" * 60)
        print("PHASE 5: EXAMPLE IDEAS")
        print("=" * 60 + "\n")
        phase5 = ExampleCollection()
        self.state["example_ideas"] = phase5.execute()

        # Phase 6: Idea Generation
        print("\n" + "=" * 60)
        print("PHASE 6: GENERATING IDEAS")
        print("=" * 60 + "\n")

        # Check if API key is available
        if not self.config.has_api_key():
            print("WARNING: No API key found for Anthropic or OpenAI.")
            print("Please set ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable.")
            print("Or add MY_API_KEY to the .env file in the ideation-agent directory.")
            print("\nFor now, generating mock ideas for demonstration purposes...")
            phase6 = IdeaGeneration(self.config, use_mock=True)
        else:
            print(f"✓ API key detected. Provider: {self.config.get_model_provider()}")
            phase6 = IdeaGeneration(self.config, use_mock=False)

        self.state["generated_ideas"] = phase6.execute(
            self.state["opportunity"],
            self.state["context"],
            self.state["criteria"],
            self.state["competitive_insights"],
            self.state["example_ideas"]
        )

        # Phase 7: Output Generation
        print("\n" + "=" * 60)
        print("PHASE 7: RESULTS & OUTPUT")
        print("=" * 60 + "\n")
        phase7 = OutputGeneration(self.config)
        phase7.execute(
            self.state["generated_ideas"],
            self.state["opportunity"],
            self.state["context"],
            self.state["criteria"]
        )

        print("\n" + "=" * 60)
        print("SESSION COMPLETE")
        print("=" * 60)
        print("\nThank you for using Ideation Agent!")
