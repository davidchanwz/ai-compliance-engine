from db_functions import delete_entry, add_entry, engine
from sqlalchemy import Column, Integer, String, DateTime, Float, func
import sqlalchemy as sa


def main():

    dummy_transactions = [
        {
            "transaction_hash": "0xabc123",
            "status": "pending",
            "timestamp": "2025-01-01T12:00:00Z",  # Current UTC timestamp
            "value": 45.50
        },
        {
            "transaction_hash": "0xdef456",
            "status": "failed",
            "timestamp": "2025-01-01T13:30:00Z",  # Another UTC timestamp
            "value": 75.00
        },
        {
            "transaction_hash": "0xghi789",
            "status": "success",
            "timestamp": "2025-01-01T14:45:00Z",  # UTC timestamp for the third entry
            "value": 120.25
        }
    ]

    add_entry("Transactions", dummy_transactions)
if __name__ == "__main__":
    main()
