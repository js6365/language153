import os
import asyncio
from flask import Flask, request
from telegram import Bot
import google.generativeai as genai

app = Flask(__name__)

# 설정
TELEGRAM_TOKEN = '8852406644:AAHwoncCUAT6yjvhiOeleO6Q837rDeqhBoU'
GEMINI_API_KEY = 'AIzaSyAAB_81wnm6Jx5TPB2bPJqnbI0YwK_yhdc'

genai.configure(api_key=GEMINI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)

# Gemini 답변 생성 함수 (인지 동사 우선 원칙 적용)
def get_gemini_response(user_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"당신은 학원 원장님입니다. 강의 문의에 친절하게 답변해주세요: {user_text}")
    return response.text

# 1. 루트 경로 (서버 상태 확인용)
@app.route('/', methods=['GET'])
def index():
    return "Bot is active", 200

# 2. 텔레그램 웹훅 경로
@app.route(f"/{TELEGRAM_TOKEN}", methods=['POST'])
def telegram_webhook():
    update = request.get_json(force=True)
    
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        user_text = update["message"]["text"]
        
        # 답변 생성
        reply = get_gemini_response(user_text)
        
        # 텔레그램으로 전송
        asyncio.run(bot.send_message(chat_id=chat_id, text=reply))
        
    return "ok", 200

# Gunicorn이 실행할 app 객체
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
