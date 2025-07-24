import streamlit as st
import pandas as pd
from datetime import datetime
from constants import CROSSREF_ROWS
from validation import validation_inputs
from api.paper_fetch import fetch_total_results ,paper_fetch_batch
from api.feedback import send_feedback_to_slack, send_user_using_tools



st.title("論文調査支援ツール（クローズドα版）")


query = st.text_input("検索キーワードを入力してください（例：synthesis natural product）:")
issn = st.text_input("ジャーナルのISSNを入力してください（例：0002-7863）:")
start_year = st.text_input("開始年を入力してください（例：2015）: ")
end_year = st.text_input("終了年を入力してください（例：2025）: ")
user_email = st.text_input("連絡用メールアドレスを入力してください（例：your_email@example.com）: ")
st.caption("※これはAPI提供元（論文検索サービス）へのマナーとして、リクエストに連絡先を含める必要があるための入力です。")
st.caption("※入力いただいたメールアドレスを、開発者や第三者が保存・使用することは一切ありません。")

now = datetime.now()



if st.button("検索"):   

    # ← 検索ボタンが押されたら古いソート結果などを初期化
    for key in ["result_row_datas", "sorted_result_df", "success_message"]:
        if key in st.session_state:
            del st.session_state[key]
    
    errors, warnings, start_year, end_year = validation_inputs(query, issn, start_year, end_year, user_email)
    
    if errors:
        for err in errors:
            st.error(err)
    else:
        for warn in warnings:
            st.warning(warn)

        with st.spinner("検索中..."):

            params = {
                "query": query,
                "rows": 1,
                "filter": f"issn: {issn},from-pub-date:{start_year}-01-01,until-pub-date:{end_year}-12-31,type:journal-article"
            }

            headers = {
                "User-Agent": f"MyApp/1.0 (mailto:{user_email})"
            }

            st.info(f"{start_year}-01-01から{end_year}-12-31の範囲で検索しています。")

            loop_count, err = fetch_total_results(params=params, headers=headers)
            if err != None:
                st.warning(err)
            st.text(f"約{loop_count * CROSSREF_ROWS}件の論文がヒットしました。")
            
            result_df = pd.DataFrame()

            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(loop_count):

                stock_df, err = paper_fetch_batch(params=params, headers=headers, i=i)
                if err != None:
                    st.warning(err)
                else:
                    result_df = pd.concat([result_df, stock_df], ignore_index=True)
               
                # 処理に失敗していても進行度は進ませる。
                progress_bar.progress(int((i + 1) / loop_count * 100))
                status_text.text(f"ただいま処理中です...バッチ {i + 1} / {loop_count}")
      
            st.session_state["result_row_datas"] = result_df

            if len(result_df) == 0:
                if "result_row_datas" in st.session_state:
                    del st.session_state["result_row_datas"]
                st.warning("検索は実行されましたが、結果は見つかりませんでした。")

                
            else:
                st.session_state["success_message"] = f"{len(result_df)}件の結果が見つかりました。" + now.strftime("%Y-%m-%d %H:%M:%S")

            #Slackに使用されたことを送るよう
            send_user_using_tools(len(result_df), issn, start_year, end_year)


if "success_message"in st.session_state:
    st.success(st.session_state["success_message"])

if "sort_expander_open" not in st.session_state:
    st.session_state["sort_expander_open"] = False

if "result_row_datas" in st.session_state:
    with st.expander("▼ ソートオプションを開く", expanded=st.session_state["sort_expander_open"]):

        sort_options = {"出版年": "pub_year", "タイトル": "title"}
        sort_label = st.selectbox("ソートしたい項目を選んでください", options=list(sort_options.keys()))
        sort_column = sort_options[sort_label]

        sort_order = st.radio("並び順を選んでください", options=["昇順", "降順"])
        ascending = sort_order == "昇順"
        st.session_state["sort_expander_open"] = True
        
        if st.button("ソート実行"):
            st.session_state["sorted_result_df"] = st.session_state["result_row_datas"].sort_values(by=sort_column, ascending=ascending)
            st.success("ソート完了")

if "sorted_result_df" in st.session_state or "result_row_datas" in st.session_state:
    if "result_row_datas" in st.session_state and "sorted_result_df" not in st.session_state:
        csv = st.session_state["result_row_datas"].to_csv(index=False, encoding='utf-8-sig')
    elif "sorted_result_df" in st.session_state:
        csv = st.session_state["sorted_result_df"].to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="CSVファイルをダウンロード",
        data=csv,
        file_name=now.strftime("%Y-%m-%d %H-%M")+ ("_sorted" if "sorted_result_df" in st.session_state else "") +"_results.csv",
        mime="text/csv"
    )



with st.expander("▼要望・フィードバックを送る"):
    feedback = st.text_area("ご意見・ご要望などがあればご記入ください。")
    send_button = st.button("送信")

    if send_button:

        response = send_feedback_to_slack(feedback)
        if response == "成功":
            st.success("ご意見ありがとうございました！Slackに送信されました。開発に取り込めるよう努力します。")
        elif "空欄" in response:
            st.warning("入力欄が空欄です、何か記入してください。")
        else:
            st.error(response)
