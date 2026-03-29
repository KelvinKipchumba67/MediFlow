import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from web3 import Web3
from eth_account import Account
import logging

logger = logging.getLogger("mediflow")

class MediFlowBlockchain:
    def __init__(self, provider_url: str = None, contract_address: str = None, private_key: str = None):
        self.w3 = None
        self.contract = None
        self.account = None
        self.is_connected = False
        self.mock_mode = True
        self.chain: List[Dict] = []  # Mock ledger events (predictions + validations)

        if not provider_url or not contract_address:
            logger.warning("Blockchain configuration incomplete. Running in mock mode.")
            return

        try:
            self.w3 = Web3(Web3.HTTPProvider(provider_url))
            if not self.w3.is_connected():
                logger.warning("Blockchain provider not reachable. Running in mock mode.")
                return

            abi_path = "blockchain/out/MediFlow.sol/MediFlow.json"
            if not os.path.exists(abi_path):
                logger.warning(f"ABI file not found at {abi_path}. Running in mock mode.")
                return

            with open(abi_path, "r") as f:
                contract_json = json.load(f)
                self.contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(contract_address),
                    abi=contract_json["abi"],
                )

            if not private_key:
                logger.warning("PRIVATE_KEY not set. Running in read-only mock mode.")
                return

            self.account = Account.from_key(private_key)
            self.is_connected = True
            self.mock_mode = False
            logger.info(f"Connected to blockchain at {provider_url}")
        except Exception as e:
            logger.error(f"Blockchain init error: {e}. Falling back to mock mode.")

    def _get_patient_id_hash(self, patient_id: str) -> bytes:
        return hashlib.sha256(patient_id.encode()).digest()

    def record_ai_prediction(self, prediction_id: str, patient_id: str, prediction_hash: str) -> Dict:
        patient_id_hash = self._get_patient_id_hash(patient_id)

        if self.mock_mode:
            logger.info(f"[Mock] Recording AI prediction {prediction_id}")
            tx = {
                "transaction_hash": f"mock_tx_ai_{prediction_id[:8]}",
                "prediction_id": prediction_id,
                "patient_id_hash": patient_id_hash.hex(),
                "prediction_hash": prediction_hash,
                "timestamp": datetime.now().isoformat(),
                "block_number": len(self.chain) + 1,
                "status": "success",
                "network": "mock",
            }
            self.chain.append({"type": "prediction", **tx})
            return tx

        if not self.is_connected:
            return {"status": "error", "message": "Blockchain not connected."}

        pred_hash_bytes = bytes.fromhex(prediction_hash)

        try:
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            tx_data = self.contract.functions.recordAIPrediction(
                prediction_id,
                pred_hash_bytes,
                patient_id_hash
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx_data, private_key=self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                "transaction_hash": tx_hash.hex(),
                "block_number": receipt.blockNumber,
                "status": "success",
                "network": "live",
            }
        except Exception as e:
            logger.error(f"On-chain AI record failed: {e}")
            return {"status": "error", "message": str(e)}

    def record_doctor_validation(self, validation_id: str, prediction_id: str, doctor_id: str, decision: str, signature: str) -> Dict:
        if self.mock_mode:
            logger.info(f"[Mock] Recording Doctor validation for {prediction_id}")
            tx = {
                "transaction_hash": f"mock_tx_val_{validation_id[:8]}",
                "validation_id": validation_id,
                "prediction_id": prediction_id,
                "doctor_id": doctor_id,
                "decision": decision,
                "signature": signature,
                "timestamp": datetime.now().isoformat(),
                "block_number": len(self.chain) + 1,
                "status": "success",
                "network": "mock",
            }
            self.chain.append({"type": "validation", **tx})
            return tx

        if not self.is_connected:
            return {"status": "error", "message": "Blockchain not connected."}

        try:
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            tx_data = self.contract.functions.recordDoctorValidation(
                validation_id,
                prediction_id,
                doctor_id,
                decision,
                signature
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx_data, private_key=self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                "transaction_hash": tx_hash.hex(),
                "block_number": receipt.blockNumber,
                "status": "success",
                "network": "live",
            }
        except Exception as e:
            logger.error(f"On-chain validation record failed: {e}")
            return {"status": "error", "message": str(e)}

    def get_audit_trail(self, patient_id: str) -> List[Dict]:
        patient_id_hash = self._get_patient_id_hash(patient_id)

        if self.mock_mode:
            predictions: Dict[str, Dict] = {}
            validations: Dict[str, Dict] = {}
            for event in self.chain:
                if event.get("type") == "prediction" and event.get("patient_id_hash") == patient_id_hash.hex():
                    predictions[event["prediction_id"]] = event
                elif event.get("type") == "validation":
                    validations[event.get("prediction_id")] = event

            trail: List[Dict] = []
            for prediction_id, pred in predictions.items():
                val = validations.get(prediction_id)
                trail.append(
                    {
                        "prediction": {
                            "id": prediction_id,
                            "hash": pred.get("prediction_hash"),
                            "timestamp": pred.get("timestamp"),
                            "recorded_by": "mock",
                        },
                        "validation": {
                            "id": val.get("validation_id"),
                            "decision": val.get("decision"),
                            "signature": val.get("signature"),
                            "timestamp": val.get("timestamp"),
                            "doctor_address": val.get("doctor_id"),
                        }
                        if val
                        else None,
                    }
                )
            return trail

        if not self.is_connected:
            return []
        try:
            prediction_ids = self.contract.functions.getPatientPredictions(patient_id_hash).call()
            trail = []
            for pid in prediction_ids:
                pred = self.contract.functions.predictions(pid).call()
                valid = self.contract.functions.validations(pid).call()
                trail.append({
                    "prediction": {
                        "id": pred[0],
                        "hash": pred[1].hex(),
                        "timestamp": pred[3],
                        "recorded_by": pred[4]
                    },
                    "validation": {
                        "id": valid[0],
                        "decision": valid[3],
                        "signature": valid[4],
                        "timestamp": valid[5],
                        "doctor_address": valid[6]
                    } if valid[0] else None
                })
            return trail
        except Exception as e:
            logger.error(f"Failed to fetch audit trail: {e}")
            return []
