# 🚀 Business Validation Platform

**AI-powered platform for validating business ideas using CrewAI multi-agent system**

[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://djangoproject.com/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Agents-purple.svg)](https://www.crewai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- 🎯 **Multi-agent AI validation** - 11 specialized AI agents analyze your business idea
- 📊 **Comprehensive reports** - Market analysis, competition, financials, and recommendations  
- 🔐 **User management** - Authentication, subscriptions, and validation history
- 📈 **Real-time progress** - Live updates during AI analysis process
- 🌐 **Web interface** - Clean Django-based UI for easy interaction
- 🐳 **Docker ready** - One-command deployment with docker-compose

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │   AI Engine     │    │   Database      │
│   (Django)      │◄──►│   (CrewAI)      │    │   (PostgreSQL)  │
│   Port 8000     │    │   Port 8001     │    │   Port 5432     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Redis       │
                    │  (Task Queue)   │
                    │   Port 6379     │
                    └─────────────────┘
```

### Components

- **Backend**: Django web platform with REST API
- **AI Engine**: CrewAI-based business validation service  
- **Database**: PostgreSQL with user management and session tracking
- **Queue**: Redis for async task processing
- **Frontend**: Django templates with modern UI

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/sanya8923/business-validation-platform.git
cd business-validation-platform
```

2. **Set up environment**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. **Start the platform**
```bash
docker-compose up -d
```

4. **Access the application**
- **Web Platform**: http://localhost:8000
- **AI Engine API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

### First Run

1. Create a superuser account:
```bash
docker-compose exec web python manage.py createsuperuser
```

2. Visit http://localhost:8000 and register/login
3. Submit your business idea for AI validation
4. Watch real-time progress as 11 AI agents analyze your idea

## 📖 Usage

### For End Users

1. **Register/Login** at http://localhost:8000
2. **Submit Business Idea** - Describe your business concept
3. **Watch AI Analysis** - 11 specialized agents work on your idea:
   - Market Research Agent
   - Competition Analyst  
   - Financial Projector
   - Risk Assessor
   - And 7 more specialized agents
4. **Get Comprehensive Report** - Detailed analysis with recommendations

### For Developers

#### Backend API (Django)
- `GET /api/ideas/` - List user's ideas
- `POST /api/ideas/` - Submit new idea for validation
- `GET /api/messages/` - Get validation messages/progress
- `POST /api/messages/` - Send message to AI agents

#### AI Engine API (CrewAI)
- `POST /api/v1/validate` - Start validation process
- `GET /api/v1/status/{execution_id}` - Check validation status  
- `GET /api/v1/result/{execution_id}` - Get validation results
- `GET /api/v1/health` - Health check

## 🛠️ Development

### Local Development Setup

1. **Backend (Django)**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

2. **AI Engine (CrewAI)**
```bash
cd ai-engine
uv sync
uv run python src/validity_crew/main.py serve
```

### Environment Variables

Key environment variables (see `.env.example`):

- `OPENAI_API_KEY` - Required for AI agents
- `DATABASE_URL` - PostgreSQL connection string
- `DJANGO_SECRET_KEY` - Django security key
- `AGENT_CALLBACK_SECRET` - Security token for AI↔Django communication

## 🧪 Testing

Run tests for both components:

```bash
# Django backend tests
docker-compose exec web python manage.py test

# AI engine tests  
docker-compose exec ai-engine uv run pytest
```

## 📚 Documentation

- [Development Guide](docs/development.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Contributing](docs/contributing.md)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📋 Roadmap

- [ ] **Enhanced AI Agents** - More specialized validation agents
- [ ] **Real-time Chat** - Direct chat with AI agents during validation
- [ ] **Export Options** - PDF/Word report generation
- [ ] **Integration APIs** - Webhooks and third-party integrations
- [ ] **Mobile App** - React Native mobile application
- [ ] **Multi-language** - Support for multiple languages

## 🐛 Issues & Support

- [Report Bug](https://github.com/sanya8923/business-validation-platform/issues)
- [Request Feature](https://github.com/sanya8923/business-validation-platform/issues)
- [Documentation](docs/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://www.crewai.com/) - Multi-agent AI framework
- [Django](https://djangoproject.com/) - Web framework
- [OpenAI](https://openai.com/) - AI models
- [PostgreSQL](https://postgresql.org/) - Database
- [Redis](https://redis.io/) - Task queue

---

**Made with ❤️ for entrepreneurs and innovators**