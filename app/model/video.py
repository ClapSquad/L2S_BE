from sqlalchemy import Column, Integer, String
from app.db.base import Base  # assuming you have a Base declarative class

class VideoModel(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    youtube_url = Column(String, nullable=False)
    file_path = Column(String, nullable=True)  # path where video is downloaded
