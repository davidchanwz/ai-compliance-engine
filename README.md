# ai-compliance-engine

## Testing the ACE API

DISCLAIMER:
Our API is deployed on a free-tier Render server, which includes an automatic spin-down feature when the server is idle. As a result, the first request after a period of inactivity may experience a delay as the server “spins up” again. Subsequent requests should proceed without delay. We recommend allowing a few moments for the initial response if the server has been idle.

Follow these steps to test the ACE API using the live demo:

1. **Access the Demo Interface**  
   Go to https://ai-compliance-engine.onrender.com/ui/index.html

2. **Login**  
   - Select `Login` from the **Select a function** dropdown menu.  
   - Input the following credentials:  
     - **Email:** `test-87239689-46f0-4605-94de-1c6235d745eb@example.com`  
     - **Password:** `password`  
   - Click `Run`.

3. **Transaction Check**  
   - Select `Transaction Check` from the **Select a function** dropdown menu.  
   - Obtain a `Transaction_Hash` from https://etherscan.io/txs 
   - Input the `Transaction_Hash` in the provided field.  
   - Click `Run`.

4. **Audit Trail**  
   - Select `Audit Trail` from the **Select a function** dropdown menu.  
   - Click `Run` to view the audit logs.

## Documentations
[Detailed documentation](https://docs.google.com/document/d/1h5OhWD8RSjyE05rEagEvz6LnUuQ4sgvLDffz2l2PrI0/edit?usp=sharing)

[Youtube Video](https://youtu.be/onFCQf1fKVQ)

## Members
[Lionel See](https://github.com/lionsee77)

[David Chan](https://github.com/davidchanwz)


## Directory Structure

```
📦 ai-compliance-engine
├── 📁 app
|   ├── __init__.py
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
|   │   ├── endpoints
|   │   │   ├── auth.py
|   │   │   ├── compliance.py
|   │   │   ├── health.py
|   │   │   ├── kyc.py
|   │   │   └── protected.py
|   │   └── router.py
|   ├── core
|   │   ├── config.py
|   │   ├── jwt.py
|   │   ├── logging_config.py
|   │   └── security.py
|   ├── database
|   │   ├── __init__.py
|   │   ├── alembic_models.py
|   │   ├── db_functions.py
|   │   └── main.py
|   ├── dependencies.py
|   ├── main.py
|   ├── services
|   │   ├── __init__.py
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
