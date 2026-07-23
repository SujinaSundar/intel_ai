from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    Text,
    ForeignKey,
    BigInteger,
    Boolean,
    UniqueConstraint
)
from datetime import datetime

from sqlalchemy.orm import declarative_base

Base = declarative_base()


# --------------------
# Company
# --------------------

class Company(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)

    company_name = Column(String, nullable=False)

    ticker = Column(String, nullable=False)

    sector = Column(String, nullable=False)


# --------------------
# Stock Price
# --------------------

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


# --------------------
# News Metadata
# --------------------

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
# --------------------
# Users
# --------------------

class User(Base):
    """
    Stores application users.
    """

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )