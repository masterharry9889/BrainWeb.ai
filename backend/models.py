from sqlalchemy import Column, String, DateTime, Integer, JSON, ForeignKey, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class UserSettings(Base):
    __tablename__ = "user_settings"
    
    user_id = Column(String, primary_key=True)
    provider = Column(String, primary_key=True, nullable=False)
    api_key_encrypted = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

class CustomAgent(Base):
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    system_prompt = Column(String, nullable=False)
    tools = Column(JSON, default=list)
    input_schema = Column(JSON, default=dict)
    output_schema = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=func.now())

class Node(Base):
    __tablename__ = "nodes"
    
    id = Column(String, primary_key=True)
    project_id = Column(String, nullable=False, default="default", index=True)
    label = Column(String, nullable=False)
    type = Column(String, nullable=False)
    embedding = Column(JSON, default=list)
    metadata_ = Column("metadata", JSON, default=dict)
    mention_count = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())

class Edge(Base):
    __tablename__ = "edges"
    
    id = Column(String, primary_key=True)
    project_id = Column(String, nullable=False, default="default", index=True)
    source_id = Column(String, ForeignKey("nodes.id"), nullable=False)
    target_id = Column(String, ForeignKey("nodes.id"), nullable=False)
    relation_type = Column(String, nullable=False)
    weight = Column(Float, default=1.0)
    created_by_agent = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
