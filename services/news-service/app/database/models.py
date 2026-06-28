"""
Database models for the Financial Research Agent.

This module defines all PostgreSQL tables used by the application:
- Companies
- Stock Prices
- News Metadata
- Sentiment Scores
- Research Scores
- Risk Scores
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Float,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
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


class ResearchReport(Base):
    """
    Stores metadata about annual and quarterly reports.

    Prevents duplicate reports for the same company,
    report type, year and quarter.
    """

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
    """
    Stores chunks extracted from reports.
    """

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


class NewsMetadata(Base):
    """
    Stores news article metadata.
    """

    __tablename__ = "news_metadata"

    id = Column(
        Integer,
        primary_key=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id")
    )

    title = Column(
        Text
    )

    source = Column(
        String
    )

    url = Column(
        Text,
        unique=True
    )

    published_date = Column(
        DateTime
    )

    is_processed = Column(
        Boolean,
        default=False
    )


class SentimentScore(Base):
    """
    Stores sentiment generated from news.
    One news article corresponds to one sentiment row.
    """

    __tablename__ = "sentiment_scores"

    id = Column(
        Integer,
        primary_key=True
    )

    news_id = Column(
        Integer,
        ForeignKey("news_metadata.id"),
        unique=True,
        nullable=False
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