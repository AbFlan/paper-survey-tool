from unittest.mock import MagicMock, patch
from api.feedback import send_feedback_to_slack



def test_send_feedback_empty():
    result = send_feedback_to_slack(" ")
    assert "空欄です。" in result

@patch("api.feedback.requests.post")
def test_send_feedback_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    result = send_feedback_to_slack("テストフィードバック")
    assert result == "成功"
    mock_post.assert_called_once()

@patch("api.feedback.requests.post")
def test_send_feedback_fail_status_code(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_post.return_value = mock_response

    result = send_feedback_to_slack("テストフィードバック")
    assert "Slack送信に失敗しています" in result
    mock_post.assert_called_once()

@patch("api.feedback.requests.post")
def test_send_feedback_exception(mock_post):
    mock_post.side_effect = Exception("ネットワークエラー")

    result = send_feedback_to_slack("テストフィードバック")
    assert "エラーが発生しました" in result
    mock_post.assert_called_once()

