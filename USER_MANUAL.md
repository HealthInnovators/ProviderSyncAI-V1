# ProviderSyncAI - User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Installation & Setup](#installation--setup)
3. [Getting Started](#getting-started)
4. [Core Features](#core-features)
5. [Using the Web Interface](#using-the-web-interface)
6. [API Usage Guide](#api-usage-guide)
7. [Workflow Guides](#workflow-guides)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Introduction

ProviderSyncAI is an intelligent healthcare provider data validation and management system that automates provider directory maintenance through AI-powered agents. The system validates contact information, enriches provider data, detects discrepancies, and generates comprehensive reports.

### Key Capabilities

- **Automated Provider Search**: Search healthcare providers using NPPES registry
- **Contact Validation**: Validate provider contact information across multiple sources
- **Data Enrichment**: Automatically enrich provider profiles with additional information
- **PDF Processing**: Extract provider data from scanned PDFs and documents
- **Batch Processing**: Process 100-500 providers simultaneously
- **Quality Assurance**: Detect discrepancies and flag providers requiring review
- **Reporting**: Generate comprehensive validation reports and metrics

---

## Installation & Setup

### Prerequisites

- Python 3.11 or higher
- Node.js 18+ and npm
- Grok API key (xAI) for AI features
- 4GB+ RAM recommended

### Step 1: Clone the Repository

```bash
git clone git@github.com:HealthInnovators/ProviderSyncAI-V1.git
cd ProviderSyncAI-V1
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

Create a `.env` file in the `backend` directory:

```bash
# Required: Grok API Key
GROK_API_KEY=your_grok_api_key_here

# Optional: Database (defaults to SQLite)
DATABASE_URL=sqlite+aiosqlite:///./providersync.db

# External Services (defaults provided)
NPPES_BASE_URL=https://npiregistry.cms.hhs.gov/api
SEARXNG_URL=https://searxng.site

# Server Configuration
ENVIRONMENT=local
API_PREFIX=/api
REQUEST_TIMEOUT_SECONDS=10.0
HTTP_MAX_RETRIES=2
CACHE_TTL_SECONDS=300
RATE_LIMIT_PER_MINUTE=60
```

### Step 4: Frontend Setup

```bash
cd frontend
npm install
```

### Step 5: Start the Application

**Option A: Start Both Services**
```bash
./START_ALL.sh
```

**Option B: Start Separately**

Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### Step 6: Verify Installation

1. **Health Check**:
   ```bash
   curl http://127.0.0.1:8000/api/health
   ```
   Expected: `{"status":"ok"}`

2. **Access Points**:
   - Frontend: http://localhost:5173
   - Backend API: http://127.0.0.1:8000
   - API Docs: http://127.0.0.1:8000/docs

---

## Getting Started

### First Steps

1. **Access the Web Interface**
   - Open http://localhost:5173 in your browser
   - You'll see the ProviderSyncAI search interface

2. **Perform Your First Search**
   - Enter provider information (name, location, specialty)
   - Click "Search"
   - Results will display provider information with confidence scores

3. **Explore API Documentation**
   - Visit http://127.0.0.1:8000/docs
   - Interactive API documentation with "Try it out" functionality

---

## Core Features

### 1. Provider Search

Search for healthcare providers using the NPPES registry.

**Web Interface:**
1. Navigate to http://localhost:5173
2. Fill in search criteria:
   - First Name / Last Name
   - Organization Name
   - City / State / Postal Code
   - Taxonomy (Specialty)
3. Click "Search"
4. View results with provider details

**API Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/search/providers \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "city": "Boston",
    "state": "MA",
    "limit": 10
  }'
```

### 2. Contact Validation Workflow

Automatically validate provider contact information across multiple sources.

**Use Case**: Validate contact information for multiple providers

**API Endpoint**: `POST /api/workflows/contact-validation/batch`

**Request Example:**
```json
[
  {
    "npi": "1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "555-1234",
    "email": "john.doe@example.com",
    "address_line1": "123 Main St",
    "city": "Boston",
    "state": "MA",
    "postal_code": "02115"
  },
  {
    "npi": "0987654321",
    "first_name": "Jane",
    "last_name": "Smith",
    "phone": "555-5678",
    "address_line1": "456 Oak Ave",
    "city": "Cambridge",
    "state": "MA",
    "postal_code": "02142"
  }
]
```

**Response:**
```json
{
  "batch_id": "uuid-here",
  "status": "completed",
  "total_providers": 2,
  "processed_count": 2,
  "validated_count": 1,
  "discrepancy_count": 1,
  "requires_review_count": 1
}
```

**What Happens**:
1. Data Validation Agent verifies contact info via NPPES and web scraping
2. Confidence scores are calculated for each data element
3. Quality Assurance Agent detects discrepancies
4. Results are stored in database
5. Providers requiring review are flagged

### 3. Credential Verification

Verify and enrich provider credentials for new provider onboarding.

**API Endpoint**: `POST /api/workflows/credential-verification`

**Request Example:**
```json
{
  "npi": "1234567890",
  "first_name": "John",
  "last_name": "Doe",
  "city": "Boston",
  "state": "MA",
  "taxonomy": "Internal Medicine"
}
```

**Response:**
```json
{
  "npi": "1234567890",
  "validation_status": "validated",
  "overall_confidence": 0.85,
  "requires_manual_review": false
}
```

**What Happens**:
1. Information Enrichment Agent searches for credentials
2. License verification (if available)
3. Education and board certification lookup
4. Quality assurance check
5. Confidence scoring

### 4. Quality Assessment

Assess the quality of your provider directory.

**API Endpoint**: `POST /api/workflows/quality-assessment`

**Request Example:**
```json
["1234567890", "0987654321", "1122334455"]
```

**Response:**
```json
{
  "report_id": "uuid-here",
  "generated_at": "2025-11-03T12:00:00Z",
  "summary": {
    "total_providers": 3,
    "validated": 2,
    "discrepancies": 1,
    "requires_review": 1,
    "average_confidence": 0.78
  },
  "providers_validated": 2,
  "providers_with_discrepancies": 1,
  "providers_requiring_review": 1,
  "recommendations": [
    "High discrepancy rate detected - review data sources"
  ]
}
```

### 5. PDF Document Extraction

Extract provider information from PDF documents (including scanned PDFs).

**API Endpoint**: `POST /api/workflows/extract-pdf`

**Using cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/workflows/extract-pdf \
  -F "file=@/path/to/provider_document.pdf"
```

**Using Python:**
```python
import requests

url = "http://127.0.0.1:8000/api/workflows/extract-pdf"
files = {"file": open("provider_document.pdf", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

**Response:**
```json
{
  "extracted_data": {
    "first_name": "John",
    "last_name": "Doe",
    "phone": "555-1234",
    "email": "john.doe@example.com",
    "address": "123 Main St",
    "city": "Boston",
    "state": "MA",
    "postal_code": "02115",
    "license_number": "MD12345",
    "specialties": ["Internal Medicine"]
  }
}
```

**Supported Formats**:
- Scanned PDFs (using VLM extraction)
- Text-based PDFs (direct text extraction)
- Unstructured documents

### 6. Review Queue

View providers requiring manual review, prioritized by urgency.

**API Endpoint**: `GET /api/workflows/review-queue`

**Example:**
```bash
curl http://127.0.0.1:8000/api/workflows/review-queue?limit=50
```

**Response:**
```json
{
  "count": 50,
  "providers": [
    {
      "npi": "1234567890",
      "name": "John Doe",
      "priority": 8,
      "discrepancies": [
        "Phone number mismatch between sources",
        "Address confidence below threshold"
      ],
      "validation_status": "requires_review"
    }
  ]
}
```

**Priority Levels**:
- 1-3: Low priority
- 4-6: Medium priority
- 7-9: High priority
- 10: Critical (fraud suspected, validation failed)

### 7. Quality Metrics

Track and monitor data quality over time.

**API Endpoint**: `GET /api/metrics`

**Example:**
```bash
curl "http://127.0.0.1:8000/api/metrics?days=30"
```

**Response:**
```json
{
  "metrics": [
    {
      "metric_name": "directory_quality_score",
      "value": 0.82,
      "threshold": 0.8,
      "trend": "improving",
      "measured_at": "2025-11-03T12:00:00Z"
    },
    {
      "metric_name": "contact_accuracy_rate",
      "value": 0.87,
      "threshold": 0.85,
      "trend": "stable",
      "measured_at": "2025-11-03T12:00:00Z"
    }
  ]
}
```

**Directory Quality Score:**
```bash
curl http://127.0.0.1:8000/api/metrics/directory-quality
```

**Response:**
```json
{
  "directory_quality_score": 0.82,
  "threshold": 0.8,
  "status": "meeting_threshold"
}
```

---

## Using the Web Interface

### Search Page

The main search interface allows you to:

1. **Enter Search Criteria**
   - Use any combination of fields
   - Leave fields blank to search broadly

2. **View Results**
   - Provider cards show key information
   - Click on provider cards for details
   - Website links (if available) are clickable

3. **Filter Results**
   - Results are automatically limited (default: 10)
   - Adjust limit in API calls for more results

### Features Available in UI

- Real-time search with React Query caching
- Responsive design (mobile-friendly)
- Error handling with user-friendly messages
- Loading states for better UX

---

## API Usage Guide

### Authentication

Currently, the API uses IP-based rate limiting. No API keys required for basic usage.

**Rate Limits**:
- Default: 60 requests per minute per IP
- Configurable via `RATE_LIMIT_PER_MINUTE` in `.env`

### Base URL

- Local: `http://127.0.0.1:8000`
- Production: Your deployed URL

### API Endpoints Reference

#### Search Endpoints

**POST /api/search/providers**
- Search for providers
- Request body: `ProviderSearchRequest`
- Response: `ProviderSearchResponse`

**GET /api/health**
- Health check endpoint
- Response: `{"status": "ok"}`

#### Workflow Endpoints

**POST /api/workflows/contact-validation/batch**
- Batch contact validation
- Request: Array of `EnrichedProvider` objects
- Response: Batch job status

**POST /api/workflows/credential-verification**
- Credential verification for single provider
- Request: `EnrichedProvider` object
- Response: Verification result

**POST /api/workflows/quality-assessment**
- Quality assessment for multiple providers
- Request: Array of NPI strings
- Response: Validation report

**POST /api/workflows/extract-pdf**
- PDF extraction
- Request: Multipart form data with PDF file
- Response: Extracted data JSON

**GET /api/workflows/review-queue**
- Get providers requiring review
- Query params: `limit` (default: 50)
- Response: Review queue list

#### Metrics Endpoints

**GET /api/metrics**
- Get quality metrics
- Query params: `metric_name`, `days` (default: 30)
- Response: Metrics array

**GET /api/metrics/directory-quality**
- Get overall directory quality score
- Response: Quality score and status

### Error Handling

All endpoints return standard HTTP status codes:

- `200`: Success
- `400`: Bad Request (validation error)
- `429`: Rate Limit Exceeded
- `500`: Internal Server Error

Error responses include a `detail` field:
```json
{
  "detail": "Error message here"
}
```

---

## Workflow Guides

### Workflow 1: Daily Contact Validation

**Scenario**: Validate contact information for 200 providers daily

**Steps**:

1. **Prepare Provider Data**
   ```json
   [
     {
       "npi": "...",
       "phone": "...",
       "email": "...",
       "address_line1": "..."
     }
   ]
   ```

2. **Submit Batch Validation**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/workflows/contact-validation/batch \
     -H "Content-Type: application/json" \
     -d @providers.json
   ```

3. **Monitor Progress**
   - Check batch status via batch_id
   - Review completion notifications

4. **Get Review Queue**
   ```bash
   curl http://127.0.0.1:8000/api/workflows/review-queue
   ```

5. **Review Flagged Providers**
   - Providers with discrepancies appear in review queue
   - Priority indicates urgency
   - Manual verification required for flagged items

**Expected Results**:
- 80%+ validation accuracy
- Complete validation in under 5 minutes (vs hours manually)
- Prioritized review list for manual attention

### Workflow 2: New Provider Onboarding

**Scenario**: Verify credentials for 25 new providers

**Steps**:

1. **Extract Data from Application Forms** (if PDF)
   ```bash
   curl -X POST http://127.0.0.1:8000/api/workflows/extract-pdf \
     -F "file=@application.pdf"
   ```

2. **Verify Credentials**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/workflows/credential-verification \
     -H "Content-Type: application/json" \
     -d '{"npi": "...", ...}'
   ```

3. **Review Results**
   - Check validation_status
   - Review confidence scores
   - Investigate flagged providers

4. **Generate Credentialing Report**
   - Use quality assessment for batch review
   - Generate summary reports

**Expected Results**:
- Automated credential verification
- Enriched provider profiles
- Confidence scores for decision-making

### Workflow 3: Weekly Quality Assessment

**Scenario**: Assess quality of entire provider directory (500 providers)

**Steps**:

1. **Get Provider NPIs**
   ```bash
   # Extract NPIs from your database or directory
   # Example: ["1234567890", "0987654321", ...]
   ```

2. **Run Quality Assessment**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/workflows/quality-assessment \
     -H "Content-Type: application/json" \
     -d '["1234567890", "0987654321", ...]'
   ```

3. **Review Report**
   - Check quality metrics
   - Review recommendations
   - Prioritize action items

4. **Take Action**
   - Focus on providers requiring review
   - Update data based on recommendations
   - Track improvements over time

**Expected Results**:
- Comprehensive quality metrics
- Trend analysis (improving/declining/stable)
- Actionable recommendations
- Quality score tracking

---

## Advanced Features

### Confidence Scoring

The system calculates confidence scores for each data element:

**Score Ranges**:
- 0.8 - 1.0: High confidence (validated)
- 0.6 - 0.79: Moderate confidence (acceptable)
- 0.4 - 0.59: Low confidence (review recommended)
- 0.0 - 0.39: Very low confidence (review required)

**Factors Affecting Confidence**:
- Data source reliability (NPPES: 0.9, Web: 0.7, etc.)
- Cross-validation agreement
- Data completeness
- Discrepancy detection

### Batch Processing

**Best Practices**:
- Process in batches of 100-200 providers
- Monitor batch status
- Handle errors gracefully
- Use caching for repeated searches

**Performance Tips**:
- Batch processing is faster than individual calls
- Results are cached automatically
- Use async processing for large batches

### Email Generation

Generate emails for provider communication:

```python
from app.infrastructure.services.email_service import EmailService
from app.domain.enriched_entities import EnrichedProvider

service = EmailService()

# Generate validation request email
email = service.generate_validation_email(provider)
print(email.subject)
print(email.body)
```

### Custom Agent Configuration

Modify agent behavior by adjusting:

1. **Temperature** (in `grok_model.py`):
   ```python
   model = GrokModel(api_key=key, temperature=0.7)  # Lower = more focused
   ```

2. **Confidence Thresholds** (in `confidence_scoring.py`):
   ```python
   # Adjust source weights and thresholds
   ```

3. **Review Priority Logic** (in `quality_assurance_agent.py`):
   ```python
   # Customize priority scoring
   ```

---

## Troubleshooting

### Common Issues

#### Issue: Server Won't Start

**Symptoms**: `uvicorn` command fails or server crashes

**Solutions**:
1. Check virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Verify all dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

3. Check port availability:
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

4. Check for import errors:
   ```bash
   python -c "from main import app"
   ```

#### Issue: Database Errors

**Symptoms**: Database initialization fails or queries fail

**Solutions**:
1. Delete and recreate database:
   ```bash
   rm backend/providersync.db
   # Restart server - it will recreate
   ```

2. Check database URL in `.env`:
   ```
   DATABASE_URL=sqlite+aiosqlite:///./providersync.db
   ```

3. Verify SQLAlchemy version:
   ```bash
   pip install sqlalchemy==2.0.36
   ```

#### Issue: Grok API Errors

**Symptoms**: Agent workflows fail with API errors

**Solutions**:
1. Verify API key is set:
   ```bash
   echo $GROK_API_KEY  # Should not be empty
   ```

2. Check API key validity
3. Verify rate limits not exceeded
4. Check network connectivity

#### Issue: Rate Limiting from SearXNG

**Symptoms**: 429 errors in logs, web enrichment fails

**Solutions**:
- This is handled gracefully - searches still return NPPES data
- Web enrichment is optional
- Consider using a different SearXNG instance
- Reduce search frequency

#### Issue: PDF Extraction Returns Empty

**Symptoms**: PDF extraction returns no data or errors

**Solutions**:
1. Verify PDF is readable (not corrupted)
2. Check PDF format (text vs scanned)
3. For scanned PDFs, ensure Grok API key is configured
4. Try smaller PDFs first
5. Check logs for specific errors

#### Issue: Frontend Can't Connect to Backend

**Symptoms**: API calls fail in frontend, network errors

**Solutions**:
1. Verify backend is running on port 8000
2. Check CORS configuration in `main.py`
3. Verify proxy settings in `vite.config.ts`
4. Check browser console for errors
5. Test API directly with curl

### Debug Mode

Enable detailed logging:

```python
# In infrastructure/logging.py
# Change log level to DEBUG
wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG)
```

View logs:
```bash
# Backend logs appear in terminal
# Or check logs/backend.log if using START_ALL.sh
```

### Getting Help

1. **Check Logs**: Review application logs for error details
2. **API Documentation**: Use `/docs` endpoint for interactive testing
3. **Health Check**: Verify server status with `/api/health`
4. **Database**: Check database file exists and is readable

---

## Best Practices

### 1. Data Management

- **Regular Validation**: Run contact validation weekly
- **Batch Processing**: Process providers in batches for efficiency
- **Review Queue**: Regularly review flagged providers
- **Quality Metrics**: Monitor quality trends over time

### 2. API Usage

- **Rate Limiting**: Respect rate limits (60/min default)
- **Error Handling**: Implement retry logic for failed requests
- **Caching**: Take advantage of automatic caching
- **Batch Operations**: Use batch endpoints for multiple providers

### 3. Confidence Scores

- **High Confidence (≥0.8)**: Accept automatically
- **Moderate (0.6-0.79)**: Review for critical providers
- **Low (<0.6)**: Always review manually
- **Discrepancies**: Always investigate flagged items

### 4. Performance

- **Batch Size**: 100-200 providers per batch optimal
- **Processing Time**: Allow 5-10 minutes for 100 providers
- **Caching**: Results cached for 5 minutes (configurable)
- **Concurrent Requests**: System handles multiple requests efficiently

### 5. Security

- **API Keys**: Never commit API keys to repository
- **Environment Variables**: Use `.env` file for configuration
- **Rate Limiting**: Configure appropriate rate limits
- **Input Validation**: Always validate input data

### 6. Monitoring

- **Quality Metrics**: Track metrics weekly
- **Error Rates**: Monitor for increasing error rates
- **Processing Times**: Watch for performance degradation
- **Review Queue Size**: Monitor queue size and address promptly

---

## API Examples

### Python Client Example

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Search providers
response = requests.post(
    f"{BASE_URL}/api/search/providers",
    json={
        "first_name": "John",
        "last_name": "Smith",
        "state": "MA",
        "limit": 10
    }
)
providers = response.json()["providers"]

# Batch validation
response = requests.post(
    f"{BASE_URL}/api/workflows/contact-validation/batch",
    json=[{
        "npi": "1234567890",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "555-1234",
        "city": "Boston",
        "state": "MA"
    }]
)
batch_result = response.json()

# Get review queue
response = requests.get(
    f"{BASE_URL}/api/workflows/review-queue",
    params={"limit": 50}
)
review_queue = response.json()
```

### JavaScript/TypeScript Example

```typescript
const API_BASE = 'http://127.0.0.1:8000';

// Search providers
async function searchProviders(params: any) {
  const response = await fetch(`${API_BASE}/api/search/providers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  return response.json();
}

// Batch validation
async function batchValidate(providers: any[]) {
  const response = await fetch(`${API_BASE}/api/workflows/contact-validation/batch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(providers)
  });
  return response.json();
}

// Get review queue
async function getReviewQueue(limit = 50) {
  const response = await fetch(`${API_BASE}/api/workflows/review-queue?limit=${limit}`);
  return response.json();
}
```

---

## Glossary

- **NPPES**: National Plan and Provider Enumeration System
- **NPI**: National Provider Identifier
- **Confidence Score**: Measure of data reliability (0.0 to 1.0)
- **Cross-Validation**: Comparing data across multiple sources
- **Discrepancy**: Difference in data values across sources
- **Validation Status**: Current state of provider validation (pending/validated/discrepancy/requires_review)
- **Review Priority**: Urgency level for manual review (1-10)
- **Enrichment**: Adding additional data to provider profiles
- **Quality Metrics**: Measurements of directory data quality

---

## Support & Resources

- **API Documentation**: http://127.0.0.1:8000/docs
- **Repository**: https://github.com/HealthInnovators/ProviderSyncAI-V1
- **Implementation Summary**: See `IMPLEMENTATION_SUMMARY.md`
- **Quick Start Guide**: See `QUICK_START.md`

---

## Appendix: Complete API Reference

### Search Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/search/providers` | Search providers |

### Workflow Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/workflows/contact-validation/batch` | Batch contact validation |
| POST | `/api/workflows/credential-verification` | Credential verification |
| POST | `/api/workflows/quality-assessment` | Quality assessment |
| POST | `/api/workflows/extract-pdf` | PDF extraction |
| GET | `/api/workflows/review-queue` | Get review queue |

### Metrics Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/metrics` | Get quality metrics |
| GET | `/api/metrics/directory-quality` | Directory quality score |

---

**Version**: 1.0  
**Last Updated**: November 2025  
**Documentation Version**: Complete Implementation

