import os
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, String, DateTime, Text, Integer, JSON, Enum as SQLEnum
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./validation.db")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

# Create async session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentStage(str, Enum):
    RESEARCH = "research"
    ANALYSIS = "analysis"
    VALIDATION = "validation"
    REPORTING = "reporting"


class ValidationExecution(Base):
    __tablename__ = "validation_executions"
    
    execution_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    status: Mapped[ExecutionStatus] = mapped_column(SQLEnum(ExecutionStatus), default=ExecutionStatus.PENDING)
    user_context: Mapped[dict] = mapped_column(JSON)
    topic: Mapped[str] = mapped_column(String(500))
    webhook_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    final_report: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    final_report_markdown: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class AgentResult(Base):
    __tablename__ = "agent_results"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[str] = mapped_column(String(50))
    agent_name: Mapped[str] = mapped_column(String(100))
    status: Mapped[AgentStatus] = mapped_column(SQLEnum(AgentStatus), default=AgentStatus.PENDING)
    stage: Mapped[AgentStage] = mapped_column(SQLEnum(AgentStage))
    
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    result_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class ValidationMetrics(Base):
    __tablename__ = "validation_metrics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[str] = mapped_column(String(50))
    
    agents_count: Mapped[int] = mapped_column(Integer)
    total_tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    execution_duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    report_completeness_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Get database session"""
    async with async_session_maker() as session:
        yield session