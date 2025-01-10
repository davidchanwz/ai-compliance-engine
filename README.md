# ai-compliance-engine

## Directory Structure

```
📦 ai-compliance-engine
├── 📁 app
|   ├── __init__.py
|   ├── __pycache__
|   │   ├── __init__.cpython-311.pyc
|   │   ├── dependencies.cpython-311.pyc
|   │   └── main.cpython-311.pyc
|   ├── ai_models
|   │   ├── __pycache__
|   │   │   ├── interact_with_blockchain.cpython-311.pyc
|   │   │   └── interaction.cpython-311.pyc
|   │   ├── anomaly_detection.py
|   │   ├── fraud_model_v2.pkl
|   │   ├── interact_with_blockchain.py
|   │   ├── kyc_verification.py
|   │   ├── model_loader.py
|   │   └── risk_scoring.py
|   ├── api
|   │   ├── __pycache__
|   │   │   └── router.cpython-311.pyc
|   │   ├── endpoints
|   │   │   ├── __pycache__
|   │   │   │   ├── auth.cpython-311.pyc
|   │   │   │   ├── compliance.cpython-311.pyc
|   │   │   │   └── protected.cpython-311.pyc
|   │   │   ├── auth.py
|   │   │   ├── compliance.py
|   │   │   ├── health.py
|   │   │   ├── kyc.py
|   │   │   └── protected.py
|   │   └── router.py
|   ├── core
|   │   ├── __pycache__
|   │   │   ├── config.cpython-311.pyc
|   │   │   ├── jwt.cpython-311.pyc
|   │   │   └── security.cpython-311.pyc
|   │   ├── config.py
|   │   ├── jwt.py
|   │   ├── logging_config.py
|   │   └── security.py
|   ├── database
|   │   ├── __init__.py
|   │   ├── __pycache__
|   │   │   ├── __init__.cpython-311.pyc
|   │   │   ├── alembic_models.cpython-311.pyc
|   │   │   └── db_functions.cpython-311.pyc
|   │   ├── alembic_models.py
|   │   ├── db_functions.py
|   │   └── main.py
|   ├── dependencies.py
|   ├── main.py
|   ├── services
|   │   ├── __init__.py
|   │   ├── __pycache__
|   │   │   ├── __init__.cpython-311.pyc
|   │   │   ├── compliance_service.cpython-311.pyc
|   │   │   └── user_service.cpython-311.pyc
|   │   ├── audit_service.py
|   │   ├── compliance_service.py
|   │   ├── kyc_service.py
|   │   └── user_service.py
|   └── tests
|       ├── conftest.py
|       ├── integration
|       │   ├── test_auth.py
|       │   ├── test_database.py
|       │   └── test_endpoints.py
|       └── unit
|           ├── test_compliance.py
|           ├── test_jwt.py
|           └── test_kyc.py
│
├── 📁 scripts                       
|    ├── anomaly_detection.ipynb
|    ├── data_preprocessing.ipynb
|    ├── fraud_model_v1.ipynb
|    ├── fraud_model_v2.ipynb
|    ├── generate_password.py
|    ├── generate_test_data.py
|    └── test_verify_pwd.py
|
├── 📁 alembic                        
|   ├── env.py
|   ├── script.py.mako
|   └── versions
|       ├── 20b72c84164d_create_users_table.py
|       ├── 5bae64d09a9c_add_audit_trail_table.py
|       ├── 9c7182748d5c_add_checked_transactions_table.py
|       ├── 9e3777d73267_change_anomaly_rating_to_float.py
|   └── __pycache__
|       ├── 20b72c84164d_create_users_table.cpython-311.pyc
|       ├── 5bae64d09a9c_add_audit_trail_table.cpython-311.pyc
|       ├── 9c7182748d5c_add_checked_transactions_table.cpython-311.pyc
|       ├── 9e3777d73267_change_anomaly_rating_to_float.cpython-311.pyc
|       ├── b9c39b7c5a2b_setting_up_tables.cpython-311.pyc
|       └── b9c39b7c5a2b_setting_up_tables.py
├── 📁 UI
|    ├── ace.jpg
|    ├── index.html
|    └── styles.css
|
├── 📄 .env                          # Default environment variables
├── 📄 .gitignore                    # Git ignore file
├── 📄 requirements.txt              # Python dependencies
├── 📄 Dockerfile                    # Dockerfile for building the app image
├── 📄 docker-compose.yml            # Docker Compose for multi-container setup
├── 📄 README.md                     # Project documentation
└── 📄 pyproject.toml                # Python project configuration
```
