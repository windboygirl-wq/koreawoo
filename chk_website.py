#!/usr/bin/env python3
import os
import requests

# 환경 변수에서 불러오기
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = os.getenv("CHK_WEBSITE")
CHECK_TIMEOUT = 10  # 초

def send_telegram(message: str):
    """텔레그램 메시지 전송"""
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(api_url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram send failed: {e}")

def check_server() -> str:
    """서버 상태 확인 (HTTP status code 반환)"""
    try:
        response = requests.get(URL, timeout=CHECK_TIMEOUT)
        return str(response.status_code)
    except requests.RequestException:
        return "NO RESPONSE"

def main():
    status = check_server()
    if status != "200":
        message = f"⚠️ 서버 점검 알림\nURL: {URL}\n상태 코드: {status}"
        send_telegram(message)

if __name__ == "__main__":
    main()
