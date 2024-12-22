"""Utility functions for data validation"""
from typing import List, Dict
from datetime import datetime, timedelta

def validate_expiration_date(expires_in_days: int) -> datetime:
    """Validate and calculate expiration date"""
    if expires_in_days < 1:
        raise ValueError("Expiration days must be greater than 0")
    return datetime.utcnow() + timedelta(days=expires_in_days)

def validate_account_ids(account_ids: List[int], available_accounts: List[Dict]) -> bool:
    """Validate that all account IDs exist in available accounts"""
    available_ids = {acc['id'] for acc in available_accounts}
    return all(acc_id in available_ids for acc_id in account_ids)