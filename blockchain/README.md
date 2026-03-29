# MediFlow Ledger | Smart Contracts

This directory contains the Ethereum-based accountability layer for the MediFlow TB Diagnostic system.

## Tech Stack

- Solidity (^0.8.19)
- Foundry (Forge, Cast, Anvil)

## Quick Start

### 1) Install Foundry

Follow the official guide: https://book.getfoundry.sh/getting-started/installation

### 2) Install dependencies

```bash
forge install
```

### 3) Build & test

```bash
forge build
forge test
```

### 4) Local deployment (Anvil)

```bash
anvil
```

In a new terminal:

```bash
forge create src/MediFlow.sol:MediFlow --rpc-url http://127.0.0.1:8545 --interactive
```

After deployment, copy the deployed address and set `CONTRACT_ADDRESS` in the root `.env` so the backend can write to the ledger.

## Helpful commands

```bash
forge fmt
forge snapshot
cast --help
forge --help
anvil --help
```
