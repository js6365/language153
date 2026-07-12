import os
from flask import Flask, request
from telegram import Bot
import google.generativeai as genai
import threading

app = Flask(__name__)

# 설정
TELEGRAM_TOKEN = '8852406644:AAHwoncCUAT6yjvhiOeleO6Q837rDeqhBoU'
GEMINI_API_KEY = 'AIzaSyAAB_81wnm6Jx5TPB2bPJqnbI0YwK_yhdc'
genai.configure(api_key=GEMINI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)

# 사용 가능한 모델 목록을 로그로 출력하여 확인합니다.
for m in genai.list_models():
    print(f"사용 가능한 모델명: {m.name}")
    
def get_gemini_response(user_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"당신은 학원 원장님입니다. 강의 문의에 친절하게 답변해주세요: {user_text}")
    return response.text

@app.route('/', methods=['GET'])
def index():
    return "Bot is running", 200

@app.route(f"/{TELEGRAM_TOKEN}", methods=['POST'])
def telegram_webhook():
    update = request.get_json(force=True)
    print(f"Received update: {update}") # 로그에 메시지 내용이 찍힘
    
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        user_text = update["message"]["text"]
        reply = get_gemini_response(user_text)
        bot.send_message(chat_id=chat_id, text=reply) # 동기식 호출로 변경하여 충돌 방지
        print("Processing message...") # 처리 중인지 로그 확인
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
