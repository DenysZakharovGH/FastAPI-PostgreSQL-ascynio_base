from core.models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class User(Base):
    username: Mapped[str] = mapped_column(unique=True)