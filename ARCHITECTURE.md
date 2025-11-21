# Ideation Agent - Architecture Documentation

## Overview

The Ideation Agent is a modular Python CLI application that guides users through a structured ideation process. It uses AI (Claude or GPT-4) to generate innovative solution ideas based on comprehensive context gathering.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ideation_agent.py                        │
│                    (Main Entry Point)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  session_manager.py                         │
│              (Orchestrates 7 Phases)                        │
└──┬──────┬──────┬──────┬──────┬──────┬──────┬──────────────┘
   │      │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼      ▼
┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
│ P1 │ │ P2 │ │ P3 │ │ P4 │ │ P5 │ │ P6 │ │ P7 │
└────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘

P1: Opportunity Discovery
P2: Context Gathering
P3: Criteria Setup
P4: Competitive Analysis
P5: Example Collection
P6: Idea Generation (AI)
P7: Output Generation
```

## Module Descriptions

### Core Modules

#### `ideation_agent.py`
- **Purpose**: Main entry point
- **Responsibilities**:
  - Initialize configuration
  - Create session manager
  - Handle top-level error handling
  - Provide welcome/goodbye messages

#### `session_manager.py`
- **Purpose**: Orchestrate the complete workflow
- **Responsibilities**:
  - Execute all 7 phases in sequence
  - Maintain session state
  - Pass data between phases
  - Handle phase transitions

#### `config.py`
- **Purpose**: Configuration management
- **Responsibilities**:
  - Load API keys from environment
  - Define default settings
  - Manage output directory
  - Provide configuration to all modules

### Supporting Modules

#### `input_helpers.py`
- **Purpose**: CLI input utilities
- **Functions**:
  - `get_user_input()`: Get text input with validation
  - `confirm()`: Yes/no confirmations
  - `get_choice()`: Multiple choice selection
  - `get_rating()`: Numeric ratings (1-5)
  - `read_file_content()`: Load content from files/folders
  - `get_input_with_file_option()`: Combined text/file input

### Phase Modules

#### `phase1_opportunity.py` - Opportunity Discovery
- **Purpose**: Understand the customer opportunity
- **Process**:
  1. Get main opportunity description
  2. Ask clarifying questions (who, context, frequency, impact)
  3. Display summary
  4. Confirm before proceeding
- **Output**: Dictionary with opportunity details

#### `phase2_context.py` - Context Gathering
- **Purpose**: Collect product and business context
- **Process**:
  1. For each context item (ICP, vision, product, metric, constraints):
     - Offer: type directly, load from file, or skip
     - Validate and store
  2. Display summary of collected context
- **Output**: Dictionary with context items

#### `phase3_criteria.py` - Evaluation Criteria Setup
- **Purpose**: Define how ideas should be evaluated
- **Process**:
  1. Present default criteria or allow custom
  2. Get importance ratings (1-5) for each
  3. Display weighted summary
- **Output**: Dictionary with criteria and weights

#### `phase4_competitive.py` - Competitive Analysis
- **Purpose**: Gather competitive insights (optional)
- **Process**:
  1. Ask if user wants competitive analysis
  2. If yes, collect URLs
  3. Gather manual observations for each
  4. Display summary
- **Output**: List of competitor insights

#### `phase5_examples.py` - Example Collection
- **Purpose**: Collect seed ideas for calibration
- **Process**:
  1. Collect 5 example ideas from user
  2. Analyze patterns (length, detail level)
  3. Display summary and patterns
- **Output**: List of example ideas + pattern analysis

#### `phase6_generation.py` - AI Idea Generation
- **Purpose**: Generate ideas using AI
- **Process**:
  1. Build comprehensive prompt from all gathered data
  2. Call Anthropic or OpenAI API
  3. Parse response into structured ideas
  4. Calculate scores and rankings
  5. Fall back to mock data if API unavailable
- **Output**: List of 7-10 generated ideas

#### `phase7_output.py` - Output Generation
- **Purpose**: Display and save results
- **Process**:
  1. Display all generated ideas
  2. Show top 3 force-ranked ideas
  3. Allow user to select ideas to save
  4. Generate markdown file
- **Output**: Markdown file in `ideation_outputs/`

## Data Flow

```
User Input → Opportunity Data
              ↓
User Input → Context Data
              ↓
User Input → Criteria Data
              ↓
User Input → Competitive Insights (optional)
              ↓
User Input → Example Ideas
              ↓
              └─→ All Data → AI Prompt Builder
                             ↓
                    API (Claude/GPT-4)
                             ↓
                    Generated Ideas
                             ↓
                    Scoring & Ranking
                             ↓
                    User Selection
                             ↓
                    Markdown Output File
```

## Session State Structure

```python
{
    "opportunity": {
        "description": str,
        "who": str,
        "context": str,
        "frequency": str,
        "impact": str,
        "current_solutions": str,
        "additional_notes": str
    },
    "context": {
        "icp": str,
        "vision": str,
        "product_description": str,
        "primary_metric": str,
        "constraints": str
    },
    "criteria": {
        "criteria_list": List[str],
        "weights": Dict[str, int]  # criterion -> importance (1-5)
    },
    "competitive_insights": [
        {
            "url": str,
            "notes": str
        }
    ],
    "example_ideas": [
        {
            "id": int,
            "description": str,
            "word_count": int,
            "char_count": int
        }
    ],
    "generated_ideas": [
        {
            "title": str,
            "content": str,
            "score": float,
            "rank": Optional[int]  # 1-3 for top ideas
        }
    ]
}
```

## AI Integration

### Prompt Construction

The AI prompt includes:
1. **Opportunity Context**: Problem statement, who, context, impact
2. **Product Context**: ICP, vision, product description, metrics, constraints
3. **Competitive Insights**: URLs and observations
4. **Example Ideas**: User-provided seed ideas for calibration
5. **Evaluation Criteria**: Weighted criteria for optimization
6. **Instructions**: Detailed formatting requirements

### Response Parsing

The system parses AI responses to extract:
- Idea titles
- Detailed descriptions
- Implementation considerations
- Impact analysis
- Force rankings with reasoning

### Fallback Strategy

If AI generation fails:
1. Try alternate provider (Claude → OpenAI or vice versa)
2. Fall back to mock data generation
3. Continue session without interruption

## File I/O

### Input
- **Supported formats**: .txt, .md
- **File handling**: Single files or entire folders
- **Path resolution**: Supports absolute and relative paths, tilde expansion

### Output
- **Format**: Markdown (.md)
- **Naming**: `ideation_session_YYYYMMDD_HHMMSS.md`
- **Location**: `ideation_outputs/` directory
- **Structure**:
  - Session metadata
  - Opportunity summary
  - Context overview
  - Evaluation criteria
  - Top 3 ranked ideas
  - All generated ideas

## Error Handling

### Input Validation
- Required fields checked before proceeding
- File paths validated before reading
- Numeric inputs validated (ratings, choices)

### API Errors
- Graceful degradation to mock mode
- Clear error messages
- Session continues without data loss

### File I/O Errors
- User-friendly error messages
- Option to retry failed operations
- No data loss on save failure

## Extensibility Points

### Adding New Phases
1. Create `phaseN_name.py` module
2. Implement `execute()` method
3. Add to `session_manager.py` workflow
4. Update state structure if needed

### Supporting New AI Providers
1. Add API key to `config.py`
2. Implement `_generate_with_provider()` in `phase6_generation.py`
3. Add provider detection logic
4. Update documentation

### Custom Output Formats
1. Add export method to `phase7_output.py`
2. Implement format-specific builder
3. Offer as option in save menu

## Dependencies

### Required
- `anthropic>=0.18.0`: Claude API client
- `openai>=1.12.0`: OpenAI API client

### Built-in
- `os`: File operations
- `json`: Data serialization (future use)
- `datetime`: Timestamps
- `typing`: Type hints

## Future Enhancement Areas

1. **Subagent Mode**: Accept structured input from other agents
2. **Web Scraping**: Automated competitive analysis
3. **Iterative Refinement**: Multi-round idea improvement
4. **Export Formats**: PDF, JSON, CSV exports
5. **Idea Clustering**: Group similar ideas automatically
6. **Collaborative Features**: Multi-user sessions
7. **Integration APIs**: Connect to project management tools
8. **Template System**: Pre-built prompts for common scenarios
9. **Analytics**: Track idea success metrics over time
10. **Version Control**: Track idea evolution

## Testing Strategy

### Unit Tests (Future)
- Each phase module tested independently
- Input validation tested
- File I/O tested with mock files

### Integration Tests (Future)
- Full session flow tested
- API mocking for consistent tests
- Output validation

### Manual Testing Checklist
- ✓ All modules import successfully
- ✓ Mock mode runs without API keys
- ✓ File loading works (single file, folder)
- ✓ All phases execute in sequence
- ✓ Output file generated correctly
- □ API generation with real keys (requires setup)

## Performance Considerations

- **Session Duration**: ~20-35 minutes total
- **API Latency**: 30-60 seconds for generation phase
- **Memory**: Minimal (<50MB typical)
- **Disk**: Output files ~5-50KB depending on detail

## Security Considerations

- API keys loaded from environment (not hardcoded)
- No sensitive data stored in output files
- File paths sanitized before access
- .gitignore configured to prevent key commits
