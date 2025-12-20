from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.kit.db.models import RecordModel


class Items(RecordModel):
    __tablename__ = "items"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )
    count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
