from sqlalchemy import UniqueConstraint

from core.models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int]
    email: Mapped[str]

    # cant be second user with same email
    __table_args__ = (
        UniqueConstraint("email"),
    )
