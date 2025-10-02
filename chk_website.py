#!/usr/bin/env bash

# 설정 부분 — 당신의 봇 토큰과 chat_id로 변경하세요
BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID=os.getenv("TELEGRAM_CHAT_ID")
URL=os.getenv("CHK_WEBSITE")
CHECK_TIMEOUT=10     # curl 연결/응답 타임아웃 (초)

send_telegram() {
    local message="$1"
    local api="https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"
    # JSON 방식으로 보내기
    curl -s -X POST "${api}" \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\":\"${CHAT_ID}\",\"text\":\"${message}\"}" \
        >/dev/null
}

check_server() {
    # HTTP 상태코드만 확인
    local status
    status=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout ${CHECK_TIMEOUT} "${URL}")
    echo "$status"
}

main() {
    local status
    status=$(check_server)
    # 상태코드 200이 아닌 경우 또는 비응답인 경우 처리
    if [[ "$status" != "200" ]]; then
        local msg="⚠️ 서버 점검 알림\nURL: ${URL}\n상태 코드: ${status}"
        send_telegram "$msg"
    fi
}

main
