# ProviderSyncAI

A production-ready full-stack application for searching and enriching healthcare provider information using the NPPES NPI Registry API and web search capabilities.

## Architecture

- **Frontend**: React + Vite + TypeScript + Tailwind CSS
- **Backend**: Python FastAPI with Hugging Face Smolagents framework
- **Clean Architecture**: Modular design with separation of concerns

## Features

- Search healthcare providers using NPPES NPI Registry
- Web enrichment via SearXNG for additional provider information
- Caching for improved performance
- Rate limiting for API protection
- Structured logging
- Modern, responsive UI

## Setup

### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory (or root) with your configuration:
```bash
cp ../.env.example .env
# Edit .env with your API keys
```

5. Run the backend server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Configuration

Key environment variables:

- `OPENAI_API_KEY` or `HF_TOKEN`: Required for Smolagents LLM functionality
- `SEARXNG_URL`: SearXNG instance URL (default: https://searxng.site)
- `NPPES_BASE_URL`: NPPES API base URL (default: https://npiregistry.cms.hhs.gov/api)
- `CACHE_TTL_SECONDS`: Cache TTL in seconds (default: 300)
- `RATE_LIMIT_PER_MINUTE`: Rate limit per IP (default: 60)

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/search/providers` - Search for providers

### Search Providers Request

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "city": "New York",
  "state": "NY",
  "taxonomy": "Internal Medicine",
  "limit": 10
}
```

## Project Structure

```
backend/
  app/
    domain/           # Domain entities
    application/       # Use cases
    infrastructure/    # External adapters (NPPES, SearXNG, cache, http)
    interfaces/        # API routes and schemas
    agents/            # Smolagents tools and coordinator
  main.py             # FastAPI application entry point

frontend/
  src/
    components/       # Reusable UI components
    features/         # Feature-based pages
    api/              # API client
    types/            # TypeScript type definitions
```

## Testing

Backend tests (to be implemented):
```bash
cd backend
pytest
```

## Development

- Backend uses structured logging via `structlog`
- Frontend uses React Query for data fetching and caching
- Both frontend and backend support hot reload in development mode

## License

MIT

