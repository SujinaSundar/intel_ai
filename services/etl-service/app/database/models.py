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
    Boolean
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