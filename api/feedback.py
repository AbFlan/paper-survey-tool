import requests
from datetime import datetime
from dotenv import load_dotenv
import os

from constants import JST


load_dotenv()
SLACK_URL = os.getenv("SLACK_URL")

def post_to_slack(message: str):
    try:
        response = requests.post(SLACK_URL, json={"text": message})
        if response.status_code == 200:
            return "成功"
        else:
            return f"Slack送信に失敗しています {response.status_code}"
    except Exception as e:
        return f"エラーが発生しました: {e}"


def send_feedback_to_slack(feedback):
    if not feedback.strip():
        return "空欄です。"
    timestamp = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    message = f'📨新しいフィードバックが届きました:\n {feedback}\n {timestamp}'
    response = post_to_slack(message=message)
    return response
    
    
def send_user_using_tools(hits, issn, start_year, end_year):
    timestamp = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    message = f'ツールが正常に使用されました:\n 検索ヒット件数: {hits}\n ISSN: {issn} \n開始年: {start_year} \n終了年: {end_year} \n検索時刻:{timestamp}'

    response = post_to_slack(message)
    if "エラーが発生しました" in response or "Slack送信に失敗しています" in response:
        print(f"Slack送信エラー（握り潰し）: {response}")