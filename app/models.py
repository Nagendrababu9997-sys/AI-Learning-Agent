from sqlalchemy import Column, Integer, String, Text, DateTime

from datetime import datetime

from .database import Base


class LearningContent(Base):

    __tablename__ = "learning_content"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    topic = Column(

        String(200),

        nullable=False

    )


    level = Column(

        String(50),

        nullable=False

    )


    learning_goal = Column(

        String(100),

        nullable=False

    )


    content_type = Column(

        String(50),

        nullable=False

    )


    lesson = Column(

        Text,

        nullable=True

    )


    quiz = Column(

        Text,

        nullable=True

    )


    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )