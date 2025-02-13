FROM python:3.11

WORKDIR /app

# 필요한 Python 패키지 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# 포트 설정
EXPOSE 8000 