

from datetime import datetime
import re

from constants import *


def validation_inputs(query, issn, start_year, end_year, user_email):
    errors = []
    warnings = []
    this_year = datetime.now().year

    #年チェック
    if not (start_year.isdigit() and end_year.isdigit()):
        errors.append(INVALID_YEAR_FORMAT)
    else:
        sy = int(start_year)
        ey = int(end_year)

        if sy > ey:
            errors.append(YEAR_ORDER_ERROR)
        if ey > this_year:
            warnings.append(f"{FUTURE_YEAR_WARNING} {this_year}年までのデータを取得します。")
            end_year = str(this_year)

    #ISSNチェック
    issn = issn.strip().upper()
    if not re.match(r"^\d{4}-\d{3}[\dXx]$", issn):
        errors.append(ISSN_FORMAT_ERROR)

    #メール形式
    if "@"not in user_email or "." not in user_email:
        errors.append(EMAIL_FORMAT_ERROR)
    
    #クエリ
    if not query.strip():
        errors.append(EMPTY_QUERY_ERROR)

    return errors, warnings, start_year, end_year