import enum
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Text, Enum, DateTime, JSON, Boolean, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class AssetStatus(str, enum.Enum):
    NEW = "NEW"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SCHEDULED = "SCHEDULED"
    PUBLISHED = "PUBLISHED"

class ContentCategory(str, enum.Enum):
    LOVE = "Love"
    HEARTBREAK = "Heartbreak"
    RELATIONSHIPS = "Relationships"
    EMOTIONAL = "Emotional"
    DEEP_THOUGHTS = "Deep Thoughts"
    QUOTES = "Quotes"
    MOVIES = "Movies"
    CINEMA = "Cinema"
    STORYTELLING = "Storytelling"
    FUNNY = "Funny"
    MEMES = "Memes"
    RELATABLE = "Relatable"
    NOSTALGIA = "Nostalgia"
    OTHER = "Other"

class Asset(Base):
    __tablename__ = "assets"

    id = Column(String(36), primary_key=True)  # UUID
    original_filename = Column(String(255), nullable=False)
    original_file_path = Column(Text, nullable=False)
    file_hash_sha256 = Column(String(64), unique=True, index=True, nullable=False)
    perceptual_hash = Column(String(64), index=True, nullable=True)
    
    # Media specifications
    file_size_bytes = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    aspect_ratio = Column(String(20), nullable=True) # e.g. "4:5", "1:1", "9:16", "custom"
    format = Column(String(20), nullable=True) # PNG, JPEG, WEBP
    
    # AI & Intelligence Extraction
    extracted_text = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    primary_category = Column(Enum(ContentCategory), default=ContentCategory.OTHER, nullable=False)
    tags = Column(JSON, default=list) # List[str]
    quality_score = Column(Float, default=0.0) # 0.0 to 10.0
    brand_fit_score = Column(Float, default=0.0) # 0.0 to 10.0
    is_duplicate = Column(Boolean, default=False)
    duplicate_of_id = Column(String(36), nullable=True)
    
    # Publishing Strategy Suggestions
    recommended_modifications = Column(Text, nullable=True)
    suggested_caption = Column(Text, nullable=True)
    suggested_hashtags = Column(JSON, default=list)
    publishing_suitability = Column(String(50), default="NEEDS_REVIEW")
    
    status = Column(Enum(AssetStatus), default=AssetStatus.NEW, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
