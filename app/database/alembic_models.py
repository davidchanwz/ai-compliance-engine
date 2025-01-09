import uuid
from sqlalchemy import JSON, Column, DateTime, String, Integer, func, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone


Base = declarative_base()
metadata = Base.metadata

class Transactions(Base):
    __tablename__ = 'Transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_hash = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=True)
    value = Column(Float, nullable=False)
    
class DatabaseChanges(Base):
    __tablename__ = 'database_changes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String, nullable=False)
    action = Column(String, nullable=False)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<DatabaseChanges(id={self.id}, table_name={self.table_name}, action={self.action}, data={self.data}, created_at={self.created_at})>"

class CheckedTransactions(Base):
    __tablename__ = 'Checked_transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_hash = Column(String(80), nullable=False, unique=True)
    anomaly_rating = Column(Float, nullable=False)
    anomaly = Column(Integer, nullable=False)
    checked_at = Column(DateTime, nullable=False, server_default=func.now())
 
class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Updated here