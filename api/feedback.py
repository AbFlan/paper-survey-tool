import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()
SLACK_URL = os.getenv("SLACK_URL")

def send_feedback_to_slack(feedback):
    
    if not feedback.strip():
        return "空欄です。"

    message = {
        "text": f'📨新しいフィードバックが届きました:\n {feedback}\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    }
    try:
        response = requests.post(SLACK_URL, json=message)
        if response.status_code == 200:
            return "成功"
        else:
            return f"Slack送信に失敗しています {response.status_code}"
    except Exception as e:
        return f"エラーが発生しました: {e}"
    
def send_user_using_tools(hits, issn, start_year, end_year):
    message = {
        "text": f'ツールが正常に使用されました:\n 検索ヒット件数: {hits}\n ISSN: {issn} \n開始年: {start_year} \n終了年: {end_year} \n検索時刻:{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    }
    try:
        response = send_feedback_to_slack(message)
    except Exception as e:
        print("エラー発生、ただしユーザに見せる必要のないエラーのため意図的に握り潰す:", e)