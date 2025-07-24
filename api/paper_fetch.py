import streamlit as st
import time
import requests
import math
import pandas as pd
from constants import *


def fetch_total_results(params: dict, headers: dict) -> tuple[int, str|None]:
    
    try:
        resp = requests.get(CROSSREF_URL, params=params, headers=headers)
        data = resp.json()
    except Exception as e:            
        return None, f"HTTPエラーを検出しました。もう一度検索をかけてください。 : {e}"
    #total-resultsには範囲内の日付に何件の論文があったかを示している。
    #すべてのデータをとるためにAPI最大1000回分で割って切り上げた数分回す
    
    roop_count = math.ceil(data["message"]["total-results"] / 1000)
    return roop_count, None

def paper_fetch_batch(params: dict, headers: dict, i: int) -> tuple[pd.DataFrame, str|None]:
    
    results = []
    params_with_offset = params.copy()
    params_with_offset["rows"] = CROSSREF_ROWS
    params_with_offset["offset"] = i * CROSSREF_ROWS
    try:
        resp = requests.get(CROSSREF_URL, params=params_with_offset, headers=headers)
        data = resp.json()

        for _, item in enumerate(data["message"]["items"], start=1):
            title = item.get("title", [""])[0]
            doi = item.get("DOI", "")
            pub_year = item.get("issued", {}).get("date-parts", [[None]])[0][0]
            article_url = item.get("URL", "")

            result = {"title": title, "doi": doi, "pub_year": pub_year, "url": article_url}
            results.append(result)
        
    except Exception as e:
        return pd.DataFrame(), f"{params_with_offset['offset']}番目のオフセットでエラーが発生しました : {e}"
       
    df = pd.DataFrame(results)
    return df, None