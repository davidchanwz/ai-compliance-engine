from sqlalchemy import Column, DateTime, String, Integer, func, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Transactions(Base):
    __tablename__ = 'Transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_hash = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    value = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Transaction(id={self.id}, hash={self.transaction_hash}, status={self.status}, timestamp={self.timestamp}, value={self.value})>"
    
class DatabaseChanges(Base):
    __tablename__ = 'database_changes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    action = Column(String, nullable=False)
    data = Column(String, nullable=False)  # Use JSON or JSONB based on your dialect
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<DatabaseChanges(id={self.id}, table_name={self.table_name}, action={self.action}, data={self.data}, created_at={self.created_at})>"
