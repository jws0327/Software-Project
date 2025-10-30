# models.py

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite DB 파일 경로 설정 (프로젝트 폴더에 restaurants.db 파일 생성)
DATABASE_URL = "sqlite:///./restaurants.db" 

# DB 엔진 생성. connect_args는 SQLite의 동시성 문제 방지용
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 세션 생성 (DB 연결 관리)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Restaurant 테이블 구조 정의
class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True) # 예: 한식, 중식, 일식
    location_url = Column(String, nullable=True) # 지도 URL (선택 사항)