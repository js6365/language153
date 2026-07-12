# 파이썬 3.10 버전의 가벼운 이미지를 사용합니다
FROM python:3.10-slim

# 컨테이너 내부의 작업 디렉토리를 설정합니다
WORKDIR /app

# 필요한 파이썬 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트의 모든 코드를 복사
COPY . .

# 포트 번호를 환경 변수로 지정
ENV PORT 8080

# 봇(Flask 서버)을 실행하는 명령어
CMD ["python", "main.py"]

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
