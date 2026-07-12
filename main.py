import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# 1. 설정 (보안을 위해 환경변수 사용 권장)
TELEGRAM_TOKEN = '8852406644:AAHwoncCUAT6yjvhiOeleO6Q837rDeqhBoU'
GEMINI_API_KEY = 'AIzaSyAAB_81wnm6Jx5TPB2bPJqnbI0YwK_yhdc'

genai.configure(api_key=GEMINI_API_KEY)

# 2. Gemini 답변 생성 함수
async def get_gemini_response(user_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"당신은 학원 원장님입니다. 강의 문의에 친절하게 답변해주세요: {user_text}")
    return response.text

# 3. 메시지 핸들러 (메시지 수신 시 작동)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # 인지 동사 우선 원칙: 질문의 의도를 파악하고 Gemini 호출
    reply = await get_gemini_response(user_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

if __name__ == '__main__':
    # 봇 애플리케이션 시작
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # 메시지 처리기 등록
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(msg_handler)
    
    application.run_polling()
