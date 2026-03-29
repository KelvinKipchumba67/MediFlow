from fastapi import APIRouter, Depends, HTTPException
import json
import os

from app.models.schemas import AuditTrailResponse
from app.api.deps import get_blockchain_service


router = APIRouter()

AUDIT_STORE = "data/secure_audit_store.json"


@router.get("/{patient_id}", response_model=AuditTrailResponse)
async def get_audit_trail(
    patient_id: str,
    blockchain=Depends(get_blockchain_service),
):
    try:
        blockchain_trail = blockchain.get_audit_trail(patient_id)

        local_records = []
        if os.path.exists(AUDIT_STORE):
            with open(AUDIT_STORE, "r") as f:
                try:
                    all_records = json.load(f)
                except Exception:
                    all_records = []
            local_records = [r for r in all_records if r.get("patient_id") == patient_id]

        transactions = []
        bc_map = {}
        for item in blockchain_trail:
            try:
                bc_map[item["prediction"]["id"]] = item
            except Exception:
                continue

        for local in local_records:
            pid = local.get("prediction_id")
            if not pid:
                continue

            bc_data = bc_map.get(pid)
            local_validation = local.get("validation")

            transactions.append(
                {
                    "prediction_id": pid,
                    "timestamp": (local.get("raw_data") or {}).get("timestamp"),
                    "ai_hash": local.get("ai_hash"),
                    "risk_level": (local.get("ai_result") or {}).get("risk_level"),
                    "confidence": (local.get("ai_result") or {}).get("confidence"),
                    "raw_features": (local.get("raw_data") or {}).get("input_features"),
                    "blockchain_verified": bc_data is not None,
                    "blockchain": {
                        "transaction_hash": local.get("blockchain_tx"),
                    },
                    "validation": (bc_data.get("validation") if bc_data else None) or local_validation,
                }
            )

        if not transactions:
            transactions = blockchain_trail

        ai_predictions = len(transactions)
        doctor_validations = 0
        for item in transactions:
            if isinstance(item, dict) and item.get("validation"):
                doctor_validations += 1

        return AuditTrailResponse(
            patient_id=patient_id,
            total_transactions=ai_predictions + doctor_validations,
            ai_predictions=ai_predictions,
            doctor_validations=doctor_validations,
            transactions=transactions,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
