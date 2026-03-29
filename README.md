# MediFlow TB Diagnostic & Accountability System

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

### Prerequisites

- Python 3.10+
- Foundry (optional, for Solidity): https://book.getfoundry.sh/getting-started/installation

### Backend

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the API:
   ```bash
   python -m app.main
   ```

### Blockchain (optional)

1. Compile contracts:

   ```bash
   cd blockchain
   forge build
   ```

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
