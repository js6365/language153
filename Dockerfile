# 파이썬 3.10 버전의 가벼운 이미지를 사용합니다
FROM python:3.10-slim

# 컨테이너 내부의 작업 디렉토리를 설정합니다
WORKDIR /app

# 필요한 파이썬 라이브러리 설치를 위해 파일을 복사합니다
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트의 모든 코드를 컨테이너로 복사합니다
COPY . .

# 봇을 실행하는 명령어를 지정합니다 (main.py 대신 실제 실행 파일명을 쓰세요)
CMD ["python", "main.py"]

ENV PORT 8080

CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8080"]
