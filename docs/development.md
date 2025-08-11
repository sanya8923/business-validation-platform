# Development Guide

## Project Structure

```
business-validation-platform/
├── backend/              # Django web application
│   ├── ideas/           # Main Django app
│   ├── project/         # Django settings
│   ├── webapp/          # Web UI templates
│   └── manage.py
├── ai-engine/           # CrewAI service
│   ├── src/validity_crew/
│   ├── config/          # Agent configurations
│   └── Dockerfile
├── docker-compose.yml   # Production setup
├── .env.example         # Environment template
└── docs/                # Documentation
```

## Development Workflow

### 1. Initial Setup

```bash
# Clone and setup
git clone https://github.com/sanya8923/business-validation-platform.git
cd business-validation-platform
cp .env.example .env
# Edit .env with your API keys
```

### 2. Start Development Environment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web
docker-compose logs -f ai-engine
```

### 3. Development Commands

```bash
# Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# AI Engine commands
docker-compose exec ai-engine uv run python src/validity_crew/main.py serve
```

## Architecture Details

### Django Backend (`backend/`)

- **ideas/**: Main app handling business ideas and validation sessions
- **webapp/**: Web UI with templates and views
- **agent_client.py**: Adapter between Django and CrewAI API

### CrewAI AI Engine (`ai-engine/`)

- **11 specialized agents** for business validation
- **FastAPI server** with REST endpoints
- **Async processing** with database persistence

### Integration Flow

```
1. User submits idea → Django creates Session
2. Django calls CrewAI /api/v1/validate
3. CrewAI starts 11 agents, returns execution_id
4. Django polls CrewAI for progress updates
5. CrewAI completes → Django stores final report
```

## Configuration

### Required Environment Variables

```bash
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgres://user:pass@db:5432/dbname
DJANGO_SECRET_KEY=your_django_secret
AGENT_CALLBACK_SECRET=callback_secret
```

### Optional Settings

```bash
DEBUG=1                    # Enable Django debug mode
CELERY_BROKER_URL=redis://redis:6379/0
AGENTS_BASE_URL=http://ai-engine:8000
```

## Testing

### Django Tests
```bash
docker-compose exec web python manage.py test
```

### AI Engine Tests  
```bash
docker-compose exec ai-engine uv run pytest
```

### Integration Tests
```bash
# Test full workflow
curl -X POST http://localhost:8000/api/ideas/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Idea", "description": "AI-powered pet food delivery"}'
```

## Debugging

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f ai-engine
```

### Connect to Services
```bash
# Django shell
docker-compose exec web python manage.py shell

# Database
docker-compose exec db psql -U bizuser -d business_validation

# AI Engine logs
docker-compose exec ai-engine tail -f /app/logs/validation.log
```

### Common Issues

1. **CrewAI not responding**: Check OPENAI_API_KEY is set
2. **Database connection**: Ensure DB is healthy before starting web
3. **Port conflicts**: Change ports in docker-compose.yml if needed

## API Documentation

### Django REST API

- **GET /api/ideas/**: List user ideas
- **POST /api/ideas/**: Create new idea (starts validation)
- **GET /api/messages/?session=X**: Get validation messages

### CrewAI API

- **POST /api/v1/validate**: Start validation
- **GET /api/v1/status/{id}**: Check status
- **GET /api/v1/result/{id}**: Get results

## Deployment

For production deployment:

1. Set `DEBUG=0` in environment
2. Configure proper `ALLOWED_HOSTS` 
3. Use production database credentials
4. Set secure `DJANGO_SECRET_KEY`
5. Configure SSL/HTTPS
6. Set up monitoring and logging