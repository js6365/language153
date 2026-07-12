import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# 웹 서버 초기화
app = Flask(__name__)

# 설정
TELEGRAM_TOKEN = '8852406644:AAHwoncCUAT6yjvhiOeleO6Q837rDeqhBoU'
GEMINI_API_KEY = 'AIzaSyAAB_81wnm6Jx5TPB2bPJqnbI0YwK_yhdc'
genai.configure(api_key=GEMINI_API_KEY)

# 텔레그램 봇 애플리케이션 빌드
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

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

# 핸들러 등록
msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
application.add_handler(msg_handler)

# 1. 웹 서버 경로: 텔레그램이 메시지를 보내는 곳
@app.route(f"/{TELEGRAM_TOKEN}", methods=['POST'])
async def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok", 200

# 2. 상태 확인용
@app.route('/', methods=['GET'])
def index():
    return "Bot is running", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    app.run(host="0.0.0.0", port=port)"""
