from datetime import timedelta, timezone

INVALID_YEAR_FORMAT = "開始年と終了年は数字(西暦4桁)で入力してください。"
YEAR_ORDER_ERROR = "開始年は終了年以下にしてください。"
FUTURE_YEAR_WARNING = "終了年が未来になっています。"
ISSN_FORMAT_ERROR = "ISSNは[1234-5678]の形式で入力してください。"
EMAIL_FORMAT_ERROR = "正しいメールアドレスを入力してください。"
EMPTY_QUERY_ERROR = "検索キーワードを入力してください。"
CROSSREF_URL = "https://api.crossref.org/works"
CROSSREF_ROWS = 1000
JST = timezone(timedelta(hours=9))