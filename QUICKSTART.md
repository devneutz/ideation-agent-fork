# Quick Start Guide

## Installation (One-time setup)

1. **Navigate to the directory:**
   ```bash
   cd "subagents/ideation-agent"
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set your API key** (choose one method):

   **Option A: Using .env file (Recommended)**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your actual API key
   # Change: MY_API_KEY=your-anthropic-api-key-here
   # To:     MY_API_KEY=sk-ant-api03-...
   ```

   **Option B: Environment variable (temporary)**
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

   **Option C: Shell profile (permanent)**
   ```bash
   echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
   source ~/.zshrc
   ```

## Running the Agent

**Method 1: Using the launcher script**
```bash
./run.sh
```

**Method 2: Direct Python execution**
```bash
python3 ideation_agent.py
```

## What to Expect

The agent will guide you through 7 phases:

1. **Opportunity Discovery** (~3-5 min)
   - Describe the problem/opportunity
   - Answer clarifying questions

2. **Context Gathering** (~5-10 min)
   - Provide product context
   - Option to load from files or type directly

3. **Evaluation Criteria** (~2-3 min)
   - Choose criteria for evaluating ideas
   - Rate their importance

4. **Competitive Analysis** (~3-5 min, optional)
   - Add competitor URLs and observations
   - Can skip if not needed

5. **Example Ideas** (~5-7 min)
   - Provide 5 seed ideas
   - Calibrates the AI's output

6. **Idea Generation** (~30-60 sec)
   - AI generates 7-10 ideas
   - Automatic scoring and ranking

7. **Review & Save** (~2-5 min)
   - Review all ideas
   - See top 3 ranked ideas
   - Save selected ideas to markdown

**Total time: ~20-35 minutes**

## Tips for Your First Session

1. **Start Simple**: Don't worry about perfection on your first run
2. **Skip Optional Parts**: You can skip competitive analysis to save time
3. **Use Mock Mode**: If you don't have an API key yet, the agent still works with sample ideas
4. **Save Everything**: You can always edit the markdown file later

## Example Output Location

Ideas are saved to:
```
ideation_outputs/ideation_session_YYYYMMDD_HHMMSS.md
```

## Troubleshooting

**"No module named 'anthropic'"**
- Run: `pip3 install -r requirements.txt`

**"No API key found"**
- Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`
- Agent will run in mock mode without API key

**Permission denied on run.sh**
- Run: `chmod +x run.sh`

## Need Help?

See [README.md](README.md) for full documentation.
