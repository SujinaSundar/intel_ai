"""
Database models for the Financial Research Agent.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass


class Company(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)

    company_name = Column(
        String,
        nullable=False
    )

    ticker = Column(
        String,
        nullable=False
    )

    sector = Column(
        String,
        nullable=False
    )


class StockPrice(Base):

    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id")
    )

    trade_date = Column(Date)

    open_price = Column(Float)

    high_price = Column(Float)

    low_price = Column(Float)

    close_price = Column(Float)

    volume = Column(BigInteger)


class NewsMetadata(Base):

    __tablename__ = "news_metadata"

    id = Column(
        Integer,
        primary_key=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id")
    )

    title = Column(Text)

    source = Column(String)

    url = Column(
        Text,
        unique=True
    )

    published_date = Column(DateTime)

    is_processed = Column(
        Boolean,
        default=False
    )


class SentimentScore(Base):
    """
    One sentiment row per news article.
    """

    __tablename__ = "sentiment_scores"

    id = Column(
        Integer,
        primary_key=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id")
    )

    sentiment_label = Column(
        String,
        nullable=False
    )

    confidence_score = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class ResearchScore(Base):

    __tablename__ = "research_scores"

    id = Column(
        Integer,
        primary_key=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id")
    )

    research_score = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class RiskScore(Base):

    __tablename__ = "risk_scores"

    id = Column(
        Integer,
        primary_key=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id")
    )

    risk_score = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class ResearchReport(Base):

    __tablename__ = "research_reports"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "report_type",
            "year",
            "quarter",
            name="uq_report"
        ),
    )

    id = Column(
        Integer,
        primary_key=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    report_type = Column(
        String,
        nullable=False
    )

    year = Column(
        Integer,
        nullable=False
    )

    quarter = Column(
        String,
        nullable=True
    )

    pdf_path = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class DocumentChunk(Base):

    __tablename__ = "document_chunks"

    id = Column(
        Integer,
        primary_key=True
    )

    report_id = Column(
        Integer,
        ForeignKey("research_reports.id"),
        nullable=False
    )

    chunk_number = Column(
        Integer,
        nullable=False
    )

    chunk_text = Column(
        Text,
        nullable=False
    )

    is_embedded = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )