import streamlit as st
import pandas as pd
import time
import io
from PyPDF2 import PdfReader
import openpyxl

st.set_page_config(page_title="配合計画書OCRアプリ", layout="wide")
st.title("📄 配合計画書OCRアプリ (プロトタイプ)")

uploaded_file = st.file_uploader(
    "PDFファイルをアップロードしてください",
    type="pdf"
)

# --- ここからが今回のテスト対象 ---

if uploaded_file is not None:
    # ファイルがアップロードされた後に、これらのUI要素が表示されるかを確認します
    st.success(f"✅ ファイル「{uploaded_file.name}」を認識しました。")
    
    st.write("この下に「処理実行」ボタンは表示されますか？")
    
    # ボタンを表示するテスト
    process_button = st.button("処理実行", type="primary")

    if process_button:
        st.info("ボタンがクリックされました！")
    else:
        st.info("☝️ ここまで表示されれば、ボタンの配置までは正常です。")

else:
    # ファイルがアップロードされる前の表示
    st.info("☝️ PDFファイルをアップロードしてください。")