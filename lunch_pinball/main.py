from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json

app = FastAPI()
#
# 1. 정적 파일 디렉토리 마운트 (index.html, game.js 등 제공)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Jinja2 템플릿 설정 (index.html 렌더링용)
templates = Jinja2Templates(directory="static")

# 현재 연결된 클라이언트 리스트
active_connections: list[WebSocket] = []

## 🌐 라우트 정의

# 루트 페이지 (index.html을 제공)
@app.get("/")
async def get_home(request: Request):
    """HTML 메인 페이지 렌더링"""
    # templates.TemplateResponse는 static/index.html 파일을 찾아서 클라이언트에게 보냅니다.
    return templates.TemplateResponse("index.html", {"request": request})

## 🔌 WebSocket 엔드포인트

@app.websocket("/ws/pinball")
async def websocket_endpoint(websocket: WebSocket):
    """핀볼 게임의 실시간 통신을 위한 WebSocket 연결"""
    await websocket.accept()
    active_connections.append(websocket)
    print(f"새로운 클라이언트 연결됨: {websocket.client}")

    try:
        while True:
            # 클라이언트로부터 메시지 수신 (예: 플리퍼 작동 입력, 공 발사)
            data = await websocket.receive_text()
            print(f"클라이언트로부터 메시지 수신: {data}")

            # 예시: 받은 메시지를 모든 클라이언트에게 브로드캐스트 (게임 상태 업데이트)
            # 실제 핀볼 게임에서는 서버가 물리 시뮬레이션을 하거나
            # 클라이언트의 입력을 다른 클라이언트(멀티플레이) 또는 상태로 전달합니다.
            
            # 여기서 게임 로직 (점수 계산, 충돌 처리 등)을 실행할 수 있습니다.
            
            message_to_send = json.dumps({"type": "status_update", "data": data})
            await broadcast(message_to_send)
            
    except Exception as e:
        print(f"연결 종료 또는 오류 발생: {e}")
    finally:
        active_connections.remove(websocket)
        print("클라이언트 연결 해제됨")

async def broadcast(message: str):
    """모든 활성 WebSocket 연결에 메시지를 보냅니다."""
    for connection in active_connections:
        await connection.send_text(message)

# 서버 실행 (이 파일 자체를 실행할 때만)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)