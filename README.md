# SCP-001: 변칙 개체 관리 시뮬레이션

이 프로젝트는 SCP 재단을 모티브로 한 Discord 봇으로, 사용자가 자신만의 변칙 개체 연구소를 운영하는 경험을 제공합니다. 직원을 고용하고, 탐사를 보내고, 변칙 개체를 격리하며 연구소를 성장시키세요.

## 주요 기능

*   **탐사 (Advanture):** 직원을 탐사 보내 새로운 변칙 개체나 재료를 획득할 수 있습니다.
*   **격리 (Containment):** 발견한 변칙 개체를 격리하고 관리합니다.
*   **직원 (Employee):** 다양한 등급과 특성을 가진 직원을 고용하고 관리합니다.
*   **상점 (Shop):** 탐사나 격리에 필요한 아이템을 구매할 수 있습니다.
*   **기록 (History):** 연구소에서 일어난 모든 활동과 이벤트가 기록됩니다.

## 요구 사항

*   Python 3.8 이상
*   Discord Bot Token
*   Google Gemini API Key

## 설치 및 실행 방법

1.  **저장소 복제:**
    ```bash
    git clone https://github.com/carbo-ifari/SCP-AI-Discord-Bot.git
    cd SCP-001
    ```

2.  **의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **.env 파일 설정:**
    ```bash
    DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
    GEMINI_API_KEY=YOUR_GEMINI_BOT_TOKEN
    ```

4.  **봇 실행:**
    ```bash
    python main.py
    ```

이제 당신의 Discord 서버에서 봇을 사용할수 있습니다.
