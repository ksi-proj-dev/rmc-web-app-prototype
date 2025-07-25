import streamlit as st
import pandas as pd
import time
import io
from PyPDF2 import PdfReader
import openpyxl

# ページ設定
st.set_page_config(page_title="配合計画書OCRアプリ", layout="wide")

# タイトル
st.title("📄 配合計画書OCRアプリ (プロトタイプ)")

# ファイルアップローダー
uploaded_file = st.file_uploader(
    "PDFファイルをアップロードしてください",
    type="pdf"
)

if uploaded_file is None:
    st.info("☝️ ここまで表示されれば、ファイル処理前のUI描画は正常です。")