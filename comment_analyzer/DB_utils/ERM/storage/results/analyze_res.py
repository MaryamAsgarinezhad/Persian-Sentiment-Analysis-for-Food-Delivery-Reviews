from sqlalchemy import Column, Integer, String, VARCHAR, BOOLEAN, FLOAT, ARRAY, ForeignKey, DateTime, func
from ....ERM.config.db import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import text


class AnalyzerResult(Base):
    __tablename__ = 'analyzer_result'

    comment_id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer)
    comment_text = Column(VARCHAR)
    vendor_code = Column(String)
    qualities = Column(ARRAY(JSONB))
    services = Column(ARRAY(JSONB))
    foods = Column(ARRAY(JSONB))
    overall = Column(FLOAT)
    created_at = Column(DateTime(timezone=True), server_default=text("timezone('Asia/Tehran', CURRENT_TIMESTAMP)"),
                        nullable=False)
