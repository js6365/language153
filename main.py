import os
from flask import Flask, request
from telegram import Bot
import google.generativeai as genai

app = Flask(__name__)

# 설정
TELEGRAM_TOKEN = '8852406644:AAHwoncCUAT6yjvhiOeleO6Q837rDeqhBoU'
GEMINI_API_KEY = 'AIzaSyAAB_81wnm6Jx5TPB2bPJqnbI0YwK_yhdc'
genai.configure(api_key=GEMINI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)

# 1. 서버 시작 시 사용 가능한 모델 목록을 로그로 출력 (디버깅용)
print("--- [디버깅] 사용 가능한 모델 목록 확인 시작 ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"사용 가능한 모델명: {m.name}")
print("--- [디버깅] 모델 목록 확인 끝 ---")
    
def get_gemini_response(user_text):
    # 2. 모델 설정: 로그에서 확인된 이름을 아래 'gemini-1.5-flash' 대신 넣으세요.
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"당신은 학원 원장님입니다. 강의 문의에 친절하게 답변해주세요: {user_text}")
    return response.text

@app.route('/', methods=['GET'])
def index():
    return "Bot is running", 200

@app.route(f"/{TELEGRAM_TOKEN}", methods=['POST'])
def telegram_webhook():
    update = request.get_json(force=True)
    print(f"Received update: {update}") 
    
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        user_text = update["message"]["text"]
        
        # 인지 동사 우선 원칙 적용 및 응답 생성
        reply = get_gemini_response(user_text)
        
        # 봇 메시지 전송
        bot.send_message(chat_id=chat_id, text=reply)
        print("Processing message successfully...") 
        
    return "ok", 200

if __name__ == "__main__":
    # 포트 설정
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
