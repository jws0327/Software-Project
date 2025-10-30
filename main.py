# main.py

import random
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas # models.py, schemas.py 임포트
from .models import SessionLocal, engine, Restaurant

# DB 테이블 생성 (DB 파일이 없으면 생성하고, 테이블이 없으면 생성)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 1. DB 세션 관리 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2. (관리자용) 식당 추가 API
@app.post("/restaurants", response_model=schemas.Restaurant)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    db_restaurant = Restaurant(
        name=restaurant.name, 
        category=restaurant.category,
        location_url=restaurant.location_url
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

# 3. 룰렛 API (핵심 기능)
@app.get("/roulette", response_model=schemas.Restaurant)
def get_random_restaurant(category: str = None, db: Session = Depends(get_db)):
    
    query = db.query(Restaurant)
    
    # 쿼리 파라미터(category)가 있으면 필터링
    if category:
        query = query.filter(Restaurant.category == category)
        
    restaurants = query.all()
    
    if not restaurants:
        # 조건에 맞는 식당이 없으면 404 에러 반환
        raise HTTPException(status_code=404, detail="No restaurants found matching the criteria")

    # 랜덤으로 하나 선택
    random_restaurant = random.choice(restaurants)
    return random_restaurant