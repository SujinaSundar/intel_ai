"""
Database models.

Defines all database tables
used by the Trading
Research Agent.
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
    UniqueConstraint,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
)

Base = declarative_base()


# -----------------------------------------------------
# Company
# -----------------------------------------------------


class Company(Base):
    """
    Company master table.
    """

    __tablename__ = "companies"

    id = Column(
        Integer,
        primary_key=True,
    )

    company_name = Column(
        String(200),
        nullable=False,
        index=True,
    )

    ticker = Column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )

    sector = Column(
        String(100),
        nullable=False,
        index=True,
    )

    stock_prices = relationship(
        "StockPrice",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    news = relationship(
        "NewsMetadata",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    sentiments = relationship(
        "SentimentScore",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    research_reports = relationship(
        "ResearchReport",
        back_populates="company",
        cascade="all, delete-orphan",
    )


# -----------------------------------------------------
# Stock Price
# -----------------------------------------------------


class StockPrice(Base):
    """
    Historical stock prices.
    """

    __tablename__ = "stock_prices"

    id = Column(
        Integer,
        primary_key=True,
    )

    company_id = Column(
        Integer,
        ForeignKey(
            "companies.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    trade_date = Column(
        Date,
        nullable=False,
        index=True,
    )

    open_price = Column(
        Float,
        nullable=False,
    )

    high_price = Column(
        Float,
        nullable=False,
    )

    low_price = Column(
        Float,
        nullable=False,
    )

    close_price = Column(
        Float,
        nullable=False,
    )

    volume = Column(
        BigInteger,
        nullable=False,
    )

    company = relationship(
        "Company",
        back_populates="stock_prices",
    )


# -----------------------------------------------------
# News Metadata
# -----------------------------------------------------


class NewsMetadata(Base):
    """
    Stores news article metadata.
    """

    __tablename__ = "news_metadata"

    id = Column(
        Integer,
        primary_key=True,
    )

    company_id = Column(
        Integer,
        ForeignKey(
            "companies.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title = Column(
        Text,
        nullable=False,
    )

    source = Column(
        String(255),
        nullable=False,
    )

    url = Column(
        Text,
        unique=True,
        nullable=False,
    )

    published_date = Column(
        DateTime,
        nullable=False,
        index=True,
    )

    is_processed = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    company = relationship(
        "Company",
        back_populates="news",
    )

    sentiment = relationship(
        "SentimentScore",
        back_populates="news",
        uselist=False,
        cascade="all, delete-orphan",
    )
# -----------------------------------------------------
# Sentiment Score
# -----------------------------------------------------


class SentimentScore(Base):
    """
    Stores sentiment generated
    from news articles.

    One news article has
    one sentiment score.
    """

    __tablename__ = "sentiment_scores"

    id = Column(
        Integer,
        primary_key=True,
    )

    news_id = Column(
        Integer,
        ForeignKey(
            "news_metadata.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    company_id = Column(
        Integer,
        ForeignKey(
            "companies.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    sentiment_label = Column(
        String(50),
        nullable=False,
    )

    confidence_score = Column(
        Float,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    company = relationship(
        "Company",
        back_populates="sentiments",
    )

    news = relationship(
        "NewsMetadata",
        back_populates="sentiment",
    )


# -----------------------------------------------------
# Research Report
# -----------------------------------------------------


class ResearchReport(Base):
    """
    Stores research reports
    such as annual reports,
    quarterly reports and
    other company documents.
    """

    __tablename__ = "research_reports"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "report_type",
            "year",
            "quarter",
            name="uq_report",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
    )

    company_id = Column(
        Integer,
        ForeignKey(
            "companies.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    report_type = Column(
        String(50),
        nullable=False,
    )

    year = Column(
        Integer,
        nullable=False,
        index=True,
    )

    quarter = Column(
        String(10),
        nullable=True,
    )

    pdf_path = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    company = relationship(
        "Company",
        back_populates="research_reports",
    )

    document_chunks = relationship(
        "DocumentChunk",
        back_populates="report",
        cascade="all, delete-orphan",
    )


# -----------------------------------------------------
# Document Chunk
# -----------------------------------------------------


class DocumentChunk(Base):
    """
    Stores chunked text
    extracted from research
    reports.
    """

    __tablename__ = "document_chunks"

    id = Column(
        Integer,
        primary_key=True,
    )

    report_id = Column(
        Integer,
        ForeignKey(
            "research_reports.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    chunk_number = Column(
        Integer,
        nullable=False,
    )

    chunk_text = Column(
        Text,
        nullable=False,
    )

    is_embedded = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    report = relationship(
        "ResearchReport",
        back_populates="document_chunks",
    )


# -----------------------------------------------------
# Users
# -----------------------------------------------------


class User(Base):
    """
    Stores application users.
    """

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )