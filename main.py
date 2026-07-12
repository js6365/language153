# main.py 파일 내용
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    
""" import os
import logging
from flask import Flask, request # 웹 서버를 위해 Flask 추가
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

app = Flask(__name__) # 1. 웹 서버 앱 생성

# 설정
TELEGRAM_TOKEN = '8852406644:AAHwoncCUAT6yjvhiOeleO6Q837rDeqhBoU'
GEMINI_API_KEY = 'AIzaSyAAB_81wnm6Jx5TPB2bPJqnbI0YwK_yhdc'
genai.configure(api_key=GEMINI_API_KEY)

# Gemini 답변 생성 함수
async def get_gemini_response(user_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"당신은 학원 원장님입니다. 강의 문의에 친절하게 답변해주세요: {user_text}")
    return response.text

# 메시지 처리 핸들러
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = await get_gemini_response(user_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

# 2. Flask 웹 서버 경로 설정 (Cloud Run 호출 대응)
@app.route('/', methods=['POST'])
def index():
    return "Bot is running", 200

if __name__ == '__main__':
    # 텔레그램 봇 설정
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(msg_handler)
    
    # Cloud Run 포트 설정
    port = int(os.environ.get("PORT", 8080))
    
    # 3. Flask 서버 실행
    app.run(host="0.0.0.0", port=port)"""
