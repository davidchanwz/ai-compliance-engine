# ai-compliance-engine

## Directory Structure

```
📦 ai-compliance-engine
├── 📁 app
│   ├── 📁 api
│   │   ├── 📁 endpoints
│   │   │   ├── 📄 auth.py           # Endpoints for user authentication (login, register)
│   │   │   ├── 📄 compliance.py     # Endpoints for compliance checks (transaction checks, audit logs)
│   │   │   ├── 📄 kyc.py            # Endpoints for KYC and AML processes
│   │   │   └── 📄 health.py         # Health check endpoint
│   │   └── 📄 router.py             # Main router to include all endpoints
│   │
│   ├── 📁 core
│   │   ├── 📄 config.py             # Global configurations (environment variables, settings)
│   │   ├── 📄 security.py           # JWT token logic, password hashing
│   │   └── 📄 logging_config.py     # Logger setup for structured logs
│   │
│   ├── 📁 services
│   │   ├── 📄 compliance_service.py # Business logic for compliance checks, risk scoring
│   │   ├── 📄 kyc_service.py        # KYC processing (AI model calls, validation)
│   │   ├── 📄 audit_service.py      # Audit logging service for recording compliance events
│   │   └── 📄 auth_service.py       # User authentication, registration, and JWT handling
│   │
│   ├── 📁 ai_models
│   │   ├── 📄 anomaly_detection.py  # Anomaly detection model (Isolation Forest, etc.)
│   │   ├── 📄 risk_scoring.py       # Risk scoring model (Logistic Regression, etc.)
│   │   ├── 📄 kyc_verification.py   # KYC biometric verification (FaceNet, etc.)
│   │   └── 📄 model_loader.py       # Model loader for all AI/ML models
│   │
│   ├── 📁 tests
│   │   ├── 📁 unit
│   │   │   ├── 📄 test_auth.py      # Unit tests for authentication logic
│   │   │   ├── 📄 test_compliance.py # Unit tests for compliance logic
│   │   │   └── 📄 test_kyc.py       # Unit tests for KYC logic
│   │   ├── 📁 integration
│   │   │   ├── 📄 test_endpoints.py # End-to-end tests for API endpoints
│   │   │   └── 📄 test_database.py  # Integration tests for the database connection
│   │   └── 📄 conftest.py           # Pytest fixtures (database, test clients, mock models)
│   │
│   ├── 📄 main.py                   # Main entry point for FastAPI app
│   └── 📄 dependencies.py           # Shared dependencies for FastAPI routes (e.g., JWT tokens, DB session)
│
├── 📁 scripts                       # Utility scripts for local development, model training, etc.
│   └── 📄 anomaly_detection.ipynb
│   └── 📄 data_preprocessing.ipynb
│
├── 📁 models                        # Trained AI/ML models directory (for loading models)
│   └── (empty)
│
├── 📄 .env                          # Default environment variables
├── 📄 .gitignore                    # Git ignore file
├── 📄 requirements.txt              # Python dependencies
├── 📄 Dockerfile                 # Dockerfile for building the app image
├── 📄 docker-compose.yml            # Docker Compose for multi-container setup
├── 📄 README.md                     # Project documentation
└── 📄 pyproject.toml                # Python project configuration
```