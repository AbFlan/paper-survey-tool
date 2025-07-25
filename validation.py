

from datetime import datetime
import re

from constants import *


def validation_inputs(query, issn, start_year, end_year, user_email):
    errors = []
    warnings = []
    this_year = datetime.now().year

    #年チェック
    if not (re.fullmatch(r"\d{4}", start_year) and re.fullmatch(r"\d{4}", end_year)):
        errors.append(INVALID_YEAR_FORMAT)
        sy, ey = start_year, end_year
    else:
        sy = int(start_year)
        ey = int(end_year)

        if sy > ey:
            errors.append(YEAR_ORDER_ERROR)
        if ey > this_year:
            warnings.append(f"{FUTURE_YEAR_WARNING} {this_year}年までのデータを取得します。")
            ey = this_year

    #ISSNチェック
    issn = issn.strip().upper()
    if not re.fullmatch(r"\d{4}-\d{3}[\dXx]", issn):
        errors.append(ISSN_FORMAT_ERROR)

    #メール形式
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", user_email):
        errors.append(EMAIL_FORMAT_ERROR)
    
    #クエリ
    if not query.strip():
        errors.append(EMPTY_QUERY_ERROR)

    return errors, warnings, str(sy), str(ey)