from db_functions import delete_entry, add_entry, engine
from sqlalchemy import Column, Integer, String, DateTime, Float, func
import sqlalchemy as sa


# Code for populating the Transactions table
# dummy_transactions = [
#         {
#             "transaction_hash": "0xabc123",
#             "status": "pending",
#             "timestamp": "2025-01-01T12:00:00Z",  # Current UTC timestamp
#             "value": 45.50
#         },
#         {
#             "transaction_hash": "0xdef456",
#             "status": "failed",
#             "timestamp": "2025-01-01T13:30:00Z",  # Another UTC timestamp
#             "value": 75.00
#         },
#         {
#             "transaction_hash": "0xghi789",
#             "status": "success",
#             "timestamp": "2025-01-01T14:45:00Z",  # UTC timestamp for the third entry
#             "value": 120.25
#         }
#     ]
# add_entry("Transactions", dummy_transactions)

def main():

    Transactions = sa.Table(
        'Transactions', sa.MetaData(), 
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('transaction_hash', String, unique=True, nullable=False),
        Column('status', String, nullable=False),
        Column('timestamp', DateTime(timezone=True), default=func.now()),
        Column('value', Float, nullable=False)
    )
    
    # Query for all pending transactions
    stmt = sa.select([Transactions]).where(Transactions.c.status == 'pending')
    result = sa.session.execute(stmt)
    transactions = result.fetchall()
    
    return transactions
    

    #delete_entry("Transactions", {"transaction_hash" : "0x123abc"})

if __name__ == "__main__":
    output = main()
    for i in output:
        print(i)
