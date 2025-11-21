"""
Phase 6: Idea Generation
Use AI to generate innovative solution ideas
"""

import json
from typing import List, Dict, Any, Optional
from config import Config


class IdeaGeneration:
    """Handles AI-powered idea generation."""

    def __init__(self, config: Config, use_mock: bool = False):
        self.config = config
        self.use_mock = use_mock

    def execute(
        self,
        opportunity: Dict[str, Any],
        context: Dict[str, Any],
        criteria: Dict[str, Any],
        competitive_insights: List[Dict[str, Any]],
        example_ideas: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute the idea generation phase."""

        print(f"DEBUG: use_mock = {self.use_mock}")
        print(f"DEBUG: provider = {self.config.get_model_provider()}")

        if self.use_mock:
            print("DEBUG: Using mock mode (use_mock=True)")
            return self._generate_mock_ideas(opportunity, criteria)

        # Use real AI generation
        print("Generating ideas using AI...")
        print("This may take a moment...\n")

        try:
            provider = self.config.get_model_provider()
            print(f"DEBUG: Attempting to use provider: {provider}")

            if provider == "anthropic":
                print("DEBUG: Calling _generate_with_anthropic()")
                return self._generate_with_anthropic(
                    opportunity, context, criteria, competitive_insights, example_ideas
                )
            elif provider == "openai":
                print("DEBUG: Calling _generate_with_openai()")
                return self._generate_with_openai(
                    opportunity, context, criteria, competitive_insights, example_ideas
                )
            else:
                print(f"DEBUG: Provider is '{provider}' - using mock generation")
                print("No API key configured. Using mock generation.")
                return self._generate_mock_ideas(opportunity, criteria)

        except Exception as e:
            print(f"ERROR during AI generation: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            print("Falling back to mock generation...\n")
            return self._generate_mock_ideas(opportunity, criteria)

    def _generate_with_anthropic(
        self,
        opportunity: Dict[str, Any],
        context: Dict[str, Any],
        criteria: Dict[str, Any],
        competitive_insights: List[Dict[str, Any]],
        example_ideas: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate ideas using Anthropic's Claude API."""
        from anthropic import Anthropic

        print(f"  Using model: {self.config.model}")
        print(f"  API key configured: {'Yes' if self.config.anthropic_api_key else 'No'}")

        client = Anthropic(api_key=self.config.anthropic_api_key)

        # Build the prompt
        prompt = self._build_generation_prompt(
            opportunity, context, criteria, competitive_insights, example_ideas
        )
        print(f"  Prompt length: {len(prompt)} characters")

        # Call API with extended thinking for better quality
        # Note: When using thinking:
        #   - temperature MUST be 1.0 (API enforced, despite docs)
        #   - max_tokens must be > thinking.budget_tokens
        # Recommended: 16k+ thinking budget for complex tasks
        print("  (Using extended thinking for higher quality ideas...)")
        thinking_budget = 10000  # 10k tokens for thorough analysis
        message = client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,  # 20000 > 10000
            temperature=1.0,  # REQUIRED by API when thinking is enabled
            thinking={
                "type": "enabled",
                "budget_tokens": thinking_budget
            },
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Parse response - handle both thinking and text content blocks
        response_text = ""
        for block in message.content:
            if block.type == "text":
                response_text += block.text

        print(f"  Response length: {len(response_text)} characters")

        ideas = self._parse_ideas_from_response(response_text, criteria)

        print(f"✓ Generated {len(ideas)} ideas\n")
        return ideas

    def _generate_with_openai(
        self,
        opportunity: Dict[str, Any],
        context: Dict[str, Any],
        criteria: Dict[str, Any],
        competitive_insights: List[Dict[str, Any]],
        example_ideas: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate ideas using OpenAI's API."""
        from openai import OpenAI

        client = OpenAI(api_key=self.config.openai_api_key)

        # Build the prompt
        prompt = self._build_generation_prompt(
            opportunity, context, criteria, competitive_insights, example_ideas
        )

        # Call API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )

        # Parse response
        response_text = response.choices[0].message.content
        ideas = self._parse_ideas_from_response(response_text, criteria)

        print(f"✓ Generated {len(ideas)} ideas\n")
        return ideas

    def _build_generation_prompt(
        self,
        opportunity: Dict[str, Any],
        context: Dict[str, Any],
        criteria: Dict[str, Any],
        competitive_insights: List[Dict[str, Any]],
        example_ideas: List[Dict[str, Any]]
    ) -> str:
        """Build the prompt for AI idea generation."""

        prompt_parts = [
            "You are an expert product strategist and innovation consultant. Your task is to generate 7-10 innovative solution ideas for a specific customer opportunity.",
            "\n## OPPORTUNITY",
            f"\nProblem/Desire: {opportunity.get('description', 'N/A')}",
        ]

        if opportunity.get('who'):
            prompt_parts.append(f"Who: {opportunity['who']}")
        if opportunity.get('context'):
            prompt_parts.append(f"Context: {opportunity['context']}")
        if opportunity.get('impact'):
            prompt_parts.append(f"Impact: {opportunity['impact']}")

        # Add context
        prompt_parts.append("\n## PRODUCT CONTEXT")

        if context.get('icp'):
            prompt_parts.append(f"\nTarget Audience:\n{context['icp']}")
        if context.get('vision'):
            prompt_parts.append(f"\nProduct Vision:\n{context['vision']}")
        if context.get('product_description'):
            prompt_parts.append(f"\nProduct Description:\n{context['product_description']}")
        if context.get('primary_metric'):
            prompt_parts.append(f"\nPrimary Metric:\n{context['primary_metric']}")
        if context.get('constraints'):
            prompt_parts.append(f"\nConstraints:\n{context['constraints']}")

        # Add competitive insights
        if competitive_insights:
            prompt_parts.append("\n## COMPETITIVE INSIGHTS")
            for insight in competitive_insights:
                prompt_parts.append(f"\n- {insight['url']}")
                if insight.get('notes'):
                    prompt_parts.append(f"  {insight['notes']}")

        # Add example ideas
        prompt_parts.append("\n## EXAMPLE IDEAS (for calibration)")
        for i, example in enumerate(example_ideas, 1):
            prompt_parts.append(f"\n{i}. {example['description']}")

        # Add evaluation criteria
        prompt_parts.append("\n## EVALUATION CRITERIA")
        prompt_parts.append("\nGenerated ideas should be optimized for:")
        for criterion, weight in criteria['weights'].items():
            prompt_parts.append(f"- {criterion} (importance: {weight}/5)")

        # Add instructions
        prompt_parts.append("\n## INSTRUCTIONS")
        prompt_parts.append("""
Generate 7-10 innovative solution ideas. For each idea, provide:

1. **Title**: A clear, compelling title (5-10 words)
2. **Description**: A detailed explanation of the solution (2-4 paragraphs)
3. **How it addresses the opportunity**: Specific connection to the problem/desire
4. **Expected impact**: How it drives the primary metric
5. **Implementation considerations**: Key aspects to consider

Format each idea as follows:

---
### IDEA [NUMBER]: [TITLE]

**Description:**
[Detailed description]

**How it addresses the opportunity:**
[Explanation]

**Expected impact:**
[Impact analysis]

**Implementation considerations:**
[Key considerations]

---

After all ideas, provide:

## TOP 3 FORCE RANKED IDEAS

Rank the top 3 ideas and explain your reasoning based on the evaluation criteria.

1. **[Idea Title]** - [Reasoning]
2. **[Idea Title]** - [Reasoning]
3. **[Idea Title]** - [Reasoning]
""")

        return "\n".join(prompt_parts)

    def _parse_ideas_from_response(
        self,
        response_text: str,
        criteria: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Parse ideas from AI response."""
        ideas = []

        # Split by idea markers
        idea_sections = response_text.split("### IDEA")

        for section in idea_sections[1:]:  # Skip first split (before first idea)
            lines = section.strip().split("\n")

            # Extract title from first line
            title_line = lines[0] if lines else ""
            # Remove number prefix (e.g., "1: " or "1. ")
            title = title_line.split(":", 1)[-1].strip() if ":" in title_line else title_line

            # Extract full text
            full_text = "\n".join(lines[1:]).strip()

            # Calculate a simple score (mock for now)
            score = self._calculate_idea_score(full_text, criteria)

            ideas.append({
                "title": title,
                "content": full_text,
                "score": score,
                "rank": None  # Will be set later
            })

        # Extract force ranking if present
        if "TOP 3 FORCE RANKED" in response_text or "FORCE RANKED IDEAS" in response_text:
            ranking_section = response_text.split("TOP 3")[1] if "TOP 3" in response_text else ""
            self._apply_force_ranking(ideas, ranking_section)

        return ideas

    def _calculate_idea_score(self, idea_text: str, criteria: Dict[str, Any]) -> float:
        """Calculate a simple score for an idea based on criteria."""
        # Simple heuristic: longer, more detailed ideas score higher
        base_score = min(len(idea_text) / 1000, 1.0)

        # Weight by criteria importance
        total_weight = sum(criteria['weights'].values())
        weighted_score = base_score * (total_weight / len(criteria['weights']))

        return round(weighted_score * 100, 1)

    def _apply_force_ranking(self, ideas: List[Dict[str, Any]], ranking_text: str):
        """Apply force ranking to ideas based on AI response."""
        # Simple pattern matching for ranked ideas
        for i, idea in enumerate(ideas[:3]):
            idea["rank"] = i + 1

    def _generate_mock_ideas(
        self,
        opportunity: Dict[str, Any],
        criteria: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate mock ideas for testing without API."""
        print("Generating mock ideas (API not configured)...\n")

        mock_ideas = [
            {
                "title": "Smart Notification System",
                "content": """**Description:**
Implement an intelligent notification system that learns from user behavior to deliver timely, relevant updates without overwhelming users.

**How it addresses the opportunity:**
Directly addresses user frustration with notification overload by using ML to predict optimal timing and relevance.

**Expected impact:**
Expected to increase user engagement by 25% while reducing notification dismissal rate by 40%.

**Implementation considerations:**
Requires user behavior tracking, ML model development, and A/B testing infrastructure.""",
                "score": 85.0,
                "rank": 1
            },
            {
                "title": "Contextual Quick Actions",
                "content": """**Description:**
Add context-aware quick actions that appear based on user's current task and historical patterns.

**How it addresses the opportunity:**
Reduces friction in common workflows by anticipating user needs and surfacing relevant actions.

**Expected impact:**
Could reduce time-to-task completion by 30% for power users.

**Implementation considerations:**
Needs careful UX design to avoid cluttering interface. Requires usage analytics.""",
                "score": 82.0,
                "rank": 2
            },
            {
                "title": "Collaborative Templates Library",
                "content": """**Description:**
Create a community-driven template library where users can share and discover pre-built workflows.

**How it addresses the opportunity:**
Addresses the cold start problem for new users and accelerates productivity.

**Expected impact:**
Expected to improve new user activation rate by 35%.

**Implementation considerations:**
Requires moderation system, quality controls, and discovery mechanisms.""",
                "score": 78.0,
                "rank": 3
            },
            {
                "title": "Automated Workflow Suggestions",
                "content": """**Description:**
Analyze user behavior to automatically suggest workflow optimizations and automation opportunities.

**How it addresses the opportunity:**
Helps users discover efficiency gains they might not know exist.

**Expected impact:**
Could increase feature adoption by 20% and reduce manual repetitive tasks.

**Implementation considerations:**
Requires sophisticated pattern recognition and non-intrusive suggestion UI.""",
                "score": 75.0,
                "rank": None
            },
            {
                "title": "Cross-Platform Sync Intelligence",
                "content": """**Description:**
Smart synchronization that prioritizes and batches updates based on connection quality and device state.

**How it addresses the opportunity:**
Addresses frustration with slow syncing and conflicts across devices.

**Expected impact:**
Expected to reduce sync-related support tickets by 50%.

**Implementation considerations:**
Complex technical implementation requiring robust conflict resolution.""",
                "score": 72.0,
                "rank": None
            }
        ]

        return mock_ideas[:7]  # Return 7 mock ideas
