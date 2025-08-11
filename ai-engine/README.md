# CrewAI Business Validation Engine

Powerful multi-agent AI system for comprehensive business idea validation using CrewAI framework.

## Features

- **11 Specialized AI Agents** for different aspects of business validation
- **FastAPI REST API** for integration with external systems  
- **Comprehensive Analysis** covering market, competition, finances, and risks
- **Real-time Progress Tracking** with detailed status updates
- **Database Integration** for persistent storage of validation results

## Architecture

### AI Agents

1. **Requirements Analyst** - Analyzes business requirements and assumptions
2. **Market Research Agent** - Investigates target market and demand
3. **Competition Analyst** - Evaluates competitive landscape
4. **Financial Projector** - Creates financial models and projections
5. **Risk Assessment Agent** - Identifies potential risks and mitigation strategies
6. **Product Validator** - Validates product-market fit
7. **Operations Analyst** - Evaluates operational requirements
8. **Marketing Strategist** - Develops marketing approach
9. **Technology Assessor** - Reviews technical feasibility
10. **Legal Advisor** - Identifies legal and regulatory considerations
11. **Report Generator** - Synthesizes all findings into comprehensive report

### API Endpoints

- `POST /api/v1/validate` - Start new validation process
- `GET /api/v1/status/{execution_id}` - Check validation status
- `GET /api/v1/result/{execution_id}` - Get validation results
- `GET /api/v1/health` - Service health check

## Quick Start

### Using Docker

```bash
# Build and run
docker build -t business-validation-ai .
docker run -p 8001:8000 -e OPENAI_API_KEY=your_key business-validation-ai
```

### Local Development

```bash
# Install dependencies
uv sync

# Start server
uv run python src/validity_crew/main.py serve
```

## Configuration

### Required Environment Variables

- `OPENAI_API_KEY` - OpenAI API key for AI agents
- `DATABASE_URL` - PostgreSQL connection string (optional)

### Optional Settings

- `PYTHONPATH` - Python module path (default: /app/src)
- `PYTHONUNBUFFERED` - Python output buffering (default: 1)

## Usage Example

```python
import requests

# Start validation
response = requests.post('http://localhost:8001/api/v1/validate', json={
    'topic': 'AI-powered pet food delivery service',
    'user_context': {
        'business_idea': 'On-demand pet food delivery with AI nutrition recommendations',
        'target_market': 'Urban pet owners',
        'budget': 50000,
        'timeline': '6 months'
    }
})

execution_id = response.json()['execution_id']

# Check status
status_response = requests.get(f'http://localhost:8001/api/v1/status/{execution_id}')
print(status_response.json())

# Get results (when completed)
result_response = requests.get(f'http://localhost:8001/api/v1/result/{execution_id}')
print(result_response.json())
```

## Development

### Project Structure

```
ai-engine/
├── src/validity_crew/
│   ├── api.py              # FastAPI application
│   ├── crew.py             # CrewAI crew definition
│   ├── models.py           # Pydantic models
│   ├── database.py         # Database operations
│   ├── main.py             # Entry point
│   └── config/
│       ├── agents.yaml     # Agent definitions
│       └── tasks.yaml      # Task definitions
├── pyproject.toml          # Project configuration
└── Dockerfile              # Container configuration
```

### Running Tests

```bash
uv run pytest
```

### API Documentation

Once running, visit http://localhost:8001/docs for interactive Swagger documentation.

## Integration

This AI engine is designed to work with the Django web platform in the parent project. The Django backend calls this service via REST API for business validation.

## License

MIT License - see LICENSE file for details.