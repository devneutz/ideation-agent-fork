# Ideation Agent

An interactive CLI application that guides you through a structured ideation process to generate innovative solutions for customer opportunities.

## Overview

The Ideation Agent is a Python-based CLI tool that uses AI (Claude or GPT-4) to generate creative solution ideas based on:
- Customer opportunity/problem definition
- Product context and strategy
- Evaluation criteria
- Competitive insights
- Example ideas for calibration

## Features

- **7-Phase Structured Process**: Guides you through opportunity discovery, context gathering, criteria setup, competitive analysis, example collection, AI-powered idea generation, and output formatting
- **Flexible Input Methods**: Type directly, load from files/folders, or skip optional sections
- **AI-Powered Generation**: Uses Anthropic Claude or OpenAI GPT-4 to generate 7-10 innovative ideas
- **Smart Evaluation**: Force-ranks top 3 ideas based on your custom criteria
- **Markdown Output**: Saves ideas to well-formatted markdown files

## Installation

1. **Navigate to the ideation-agent directory:**
   ```bash
   cd "subagents/ideation-agent"
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up API key**:

   **Recommended: Use .env file**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your API key
   # MY_API_KEY=sk-ant-api03-your-actual-key-here
   ```

   **Alternative: Environment variable**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   # or
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Usage

Run the ideation agent:

```bash
python3 ideation_agent.py
```

The agent will guide you through 7 phases:

### Phase 1: Opportunity Discovery
- Describe the customer pain point, wish, or desire
- Answer clarifying questions about who, context, frequency, impact

### Phase 2: Context Gathering
For each context item, choose to:
- Type directly
- Load from file/folder path
- Skip (optional items)

Context items:
- ICP / Target Audience
- Product Vision & Strategy
- Product Category & Description
- Primary Product Metric
- Constraints

### Phase 3: Evaluation Criteria
- Use default criteria or define custom ones
- Rate importance of each criterion (1-5)

### Phase 4: Competitive Analysis (Optional)
- Provide URLs to competitors/alternatives
- Add observations about each

### Phase 5: Example Ideas
- Provide 5 seed ideas
- These calibrate the AI's output style and detail level

### Phase 6: Idea Generation
- AI generates 7-10 ideas based on all inputs
- Each idea includes title, description, impact analysis, and implementation considerations

### Phase 7: Output & Saving
- Review all generated ideas
- See top 3 force-ranked ideas with reasoning
- Choose which ideas to save
- Ideas saved to `ideation_outputs/ideation_session_YYYYMMDD_HHMMSS.md`

## Example Workflow

```bash
$ python3 ideation_agent.py

============================================================
  IDEATION AGENT
  Generate innovative solutions for customer opportunities
============================================================

Let's start your ideation session!

============================================================
PHASE 1: OPPORTUNITY DISCOVERY
============================================================

What is the customer pain point, wish, or desire you want to solve? (required)
> Users struggle to find relevant features in our complex product interface

...

✓ Ideas saved to: ideation_outputs/ideation_session_20241121_143022.md
  (7 idea(s) saved)
```

## Output Format

Generated markdown files include:
- Opportunity summary
- Context overview
- Evaluation criteria
- Top 3 force-ranked ideas
- All generated ideas with scores

## Mock Mode

If no API key is configured, the agent runs in mock mode with sample ideas for testing the workflow.

## File Structure

```
ideation-agent/
├── ideation_agent.py      # Main entry point
├── session_manager.py     # Orchestrates workflow
├── config.py              # Configuration management
├── input_helpers.py       # CLI input utilities
├── phase1_opportunity.py  # Opportunity discovery
├── phase2_context.py      # Context gathering
├── phase3_criteria.py     # Criteria setup
├── phase4_competitive.py  # Competitive analysis
├── phase5_examples.py     # Example collection
├── phase6_generation.py   # AI idea generation
├── phase7_output.py       # Output formatting
├── requirements.txt       # Python dependencies
└── ideation_outputs/      # Generated output files
```

## Tips for Best Results

1. **Be Specific**: The more detail you provide about the opportunity, the better the ideas
2. **Provide Context**: Loading product docs or strategy files helps calibrate the AI
3. **Good Examples**: Your 5 example ideas should represent the quality and style you want
4. **Clear Criteria**: Well-defined evaluation criteria lead to better force-ranking
5. **Competitive Insights**: Adding competitor analysis can inspire unique angles

## Troubleshooting

**API Errors:**
- Verify your API key is set correctly
- Check you have credits/quota available
- The agent will fall back to mock mode if API fails

**File Loading Issues:**
- Use absolute paths or paths relative to current directory
- Supported formats: .txt, .md files
- For folders, all .txt and .md files will be concatenated

**Import Errors:**
- Make sure you've installed requirements: `pip3 install -r requirements.txt`
- Use Python 3.8 or higher

## Future Enhancements

Potential additions:
- Subagent mode (callable from other agents)
- Web scraping for competitive analysis
- Idea refinement/iteration mode
- Export to other formats (PDF, JSON)
- Integration with project management tools

## License

Internal use only.
