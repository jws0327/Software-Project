// WebSocket 연결 설정
const socket = new WebSocket("ws://localhost:8000/ws/pinball");

const statusDiv = document.getElementById('status');
const messagesDiv = document.getElementById('messages');
const canvas = document.getElementById('pinballCanvas');
const ctx = canvas.getContext('2d');

// 1. 연결이 열렸을 때
socket.onopen = (event) => {
    statusDiv.textContent = "✅ WebSocket 연결 성공!";
    console.log("WebSocket 연결 성공", event);
};

// 2. 서버로부터 메시지를 수신했을 때
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    // 게임 상태 업데이트 처리 (예: 공 위치 업데이트)
    if (data.type === 'status_update') {
        const p = document.createElement('p');
        p.textContent = `서버로부터 상태 업데이트: ${data.data}`;
        messagesDiv.appendChild(p);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    // 이 부분에서 수신한 데이터를 바탕으로 캔버스에 공의 위치를 다시 그립니다.
    // drawGame(data.game_state);
};

// 3. 연결이 닫혔을 때
socket.onclose = (event) => {
    statusDiv.textContent = "❌ WebSocket 연결 끊김.";
    console.log("WebSocket 연결 끊김", event);
};

// 4. 에러 발생 시
socket.onerror = (error) => {
    console.error("WebSocket 오류 발생:", error);
    statusDiv.textContent = "⚠️ 오류 발생! 콘솔 확인.";
};

// 서버로 메시지를 보내는 함수 (예: 플리퍼 입력)
function sendMessage(action) {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ action: action }));
        console.log(`메시지 전송: ${action}`);
    } else {
        console.log("WebSocket 연결이 준비되지 않았습니다.");
    }
}


// 여기에 핀볼 **물리 시뮬레이션** 및 **렌더링** 코드를 작성합니다.
function drawGame(gameState) {
    // 캔버스 초기화
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 공 그리기 (예시)
    ctx.beginPath();
    ctx.arc(300, 400, 10, 0, Math.PI * 2); // 임의의 위치
    ctx.fillStyle = "blue";
    ctx.fill();
    ctx.closePath();
    
    // 플리퍼, 범퍼 등 그리기...
}

// 초기 렌더링 호출
drawGame(null);