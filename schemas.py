# schemas.py

from pydantic import BaseModel
from typing import Optional # Python 3.9 이하 사용 시

# (DB에 저장할 때) 클라이언트가 FastAPI로 보낼 데이터 형식
class RestaurantCreate(BaseModel):
    name: str
    category: str
    location_url: Optional[str] = None # Optional[str] 대신 str | None (3.10 이상)도 가능

# (DB에서 읽어서) 클라이언트에게 FastAPI가 응답할 데이터 형식
class Restaurant(BaseModel):
    id: int # DB에서 생성된 ID 포함
    name: str
    category: str
    location_url: Optional[str] = None

    class Config:
        # SQLAlchemy 모델과 Pydantic 모델 간의 매핑을 위해 필요
        orm_mode = True