import os
from flask import Flask, request
from telegram import Bot
import google.generativeai as genai

app = Flask(__name__)

# 환경변수에서 보안 정보를 가져옵니다 (절대 코드에 직접 입력하지 마세요)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# API 키가 설정되어 있는지 확인
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")

genai.configure(api_key=GEMINI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)

# 1. 서버 시작 시 사용 가능한 모델 목록을 로그로 출력
print("--- [디버깅] 사용 가능한 모델 목록 확인 시작 ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"사용 가능한 모델명: {m.name}")
except Exception as e:
    print(f"모델 목록 확인 중 오류 발생: {e}")
print("--- [디버깅] 모델 목록 확인 끝 ---")
    
def get_gemini_response(user_text):
    # 인지 동사 우선 원칙 적용
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
        
        reply = get_gemini_response(user_text)
        
        bot.send_message(chat_id=chat_id, text=reply)
        print("Processing message successfully...") 
        
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
