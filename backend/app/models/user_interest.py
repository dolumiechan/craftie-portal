from sqlalchemy import Column, Integer, ForeignKey, Table
from app.core.database import Base

user_interests = Table(
    "user_interests",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "category_id",
        Integer,
        ForeignKey("interest_categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
