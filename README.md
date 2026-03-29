# MediFlow TB Diagnostic & Accountability System

<<<<<<< HEAD
MediFlow is an AI-powered Tuberculosis (TB) diagnostic platform that uses Machine Learning for triage and blockchain-backed cryptographic proofs for accountability and an immutable audit trail.

## Overview

Healthcare systems increasingly rely on AI, but many deployments suffer from an “AI black box” problem and weak auditability. MediFlow closes the accountability gap by hashing and recording decision artifacts so that predictions and validations can be verified later without exposing sensitive patient data.

## Core Mechanisms

- Hashing (SHA-256): Creates tamper-evident fingerprints of predictions, model versions, and related metadata.
- Digital signatures (HMAC / asymmetric signatures): Allows actors (system/clinician) to sign validations so actions are attributable and non-repudiable.
- Blockchain / distributed ledger: Stores the audit trail as append-only records (Solidity/EVM in this repo).

## Project Structure

```text
app/
  api/                 # FastAPI endpoints
  core/                # Configuration
  models/              # Pydantic schemas
  resources/           # ML model weights
  services/            # Business logic (diagnosis & blockchain)
  utils/               # Hashing & security helpers
  main.py              # FastAPI app entrypoint

blockchain/            # Foundry (Solidity) project
scripts/               # Utility scripts (data generation, training)
Frontend/              # Vite/React frontend
```

## Getting Started
=======
MediFlow is an AI-powered Tuberculosis (TB) diagnostic platform that leverages Machine Learning for triage and Blockchain for accountability and an immutable audit trail.

## 🚀 Project Overview

- **AI Triage:** Uses a hybrid engine (Rule-Based + Random Forest) to assess TB risk based on clinical symptoms.
- **Blockchain Accountability:** Records every AI prediction and doctor validation on an immutable ledger (Solidity/Ethereum).
- **Privacy First:** Only non-reversible hashes of patient data are stored on-chain, ensuring patient privacy while maintaining a complete audit trail.
- **Modular Architecture:** Cleanly separated into API, Services, and Blockchain layers.

## 📂 Project Structure

```text
ai-backend/
├── app/
│   ├── api/                 # FastAPI Endpoints
│   ├── core/                # Configuration
│   ├── models/              # Pydantic Schemas
│   ├── services/            # Business Logic (Diagnosis & Blockchain)
│   ├── utils/               # Hashing & Security
│   └── resources/           # ML Model weights
├── blockchain/              # Foundry (Solidity) project
│   ├── src/                 # Smart Contracts
│   └── forge build/         # Compiled artifacts
├── scripts/                 # Utility scripts (Data gen, Training)
├── tests/                   # Test suite
└── README.md
```

## 🛠️ Getting Started
>>>>>>> a1b6ff2f6a05662b15fe7db073692ef0643c0b24

### Prerequisites

- Python 3.10+
<<<<<<< HEAD
- Foundry (optional, for Solidity): https://book.getfoundry.sh/getting-started/installation

### Backend

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
=======
- [Foundry](https://book.getfoundry.sh/getting-started/installation) (for Solidity)

### Backend Setup

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn joblib pandas numpy web3 pydantic
>>>>>>> a1b6ff2f6a05662b15fe7db073692ef0643c0b24
   ```

2. Run the API:
   ```bash
   python -m app.main
   ```

<<<<<<< HEAD
### Blockchain (optional)

1. Compile contracts:

=======
### Blockchain Setup

1. Compile the contracts:
>>>>>>> a1b6ff2f6a05662b15fe7db073692ef0643c0b24
   ```bash
   cd blockchain
   forge build
   ```

<<<<<<< HEAD
2. (Optional) Deploy locally with Anvil:
   ```bash
   anvil
   ```

## AI Engine

The triage engine is hybrid:

1. Rule-based guardrails (WHO-style red flags)
2. Random Forest model for probabilistic risk classification

## Accountability Flow

1. AI generates a prediction.
2. A SHA-256 hash is computed for the decision payload.
3. The hash (and an anonymized patient identifier hash) is recorded on-chain.
4. A clinician validates/overrides the decision and the validation is linked to the original record.

## Team

- Ombati Benson — Machine Learning Engineer
- Kelvin Kipchumba — Full Stack Developer
- Denzel William — Blockchain Engineer
- Kihiu James — Machine Learning Engineer
- David Oyugi — Digital Solutions Analyst
- Ian Kariuki — Healthcare Systems Lead
=======
2. (Optional) Deploy to a local node (Anvil):
   ```bash
   # In a separate terminal
   anvil
   
   # Deploy
   forge create --rpc-url http://localhost:8545 --private-key <YOUR_PRIVATE_KEY> src/MediFlow.sol:MediFlow
   ```

## 🧪 AI Engine

The hybrid diagnostic engine combines:
1. **Rule-Based Tier:** Implements WHO clinical guidelines for immediate red-flag detection (e.g., Hemoptysis).
2. **ML Tier:** A Random Forest model trained on synthetic/real TB data to identify complex symptom patterns.

## 🔒 Security & Accountability

Every diagnostic decision follows this flow:
1. AI generates a prediction.
2. A unique SHA256 hash of the prediction is created.
3. The hash and an anonymized patient ID hash are recorded on the blockchain.
4. A doctor reviews the case and signs their decision using an HMAC-based digital signature.
5. The doctor's validation is linked to the original AI prediction on-chain.
>>>>>>> a1b6ff2f6a05662b15fe7db073692ef0643c0b24
