import streamlit as st
import pandas as pd
import time
import io
from PyPDF2 import PdfReader # このライブラリの動作をテストします
import openpyxl

st.set_page_config(page_title="配合計画書OCRアプリ", layout="wide")
st.title("📄 配合計画書OCRアプリ (プロトタイプ)")

uploaded_file = st.file_uploader(
    "PDFファイルをアップロードしてください",
    type="pdf"
)

if uploaded_file is not None:
    st.success(f"✅ ファイル「{uploaded_file.name}」を認識しました。")
    process_button = st.button("処理実行", type="primary")

    # --- ここからが今回のテスト対象 ---
    if process_button:
        st.info("🔘 ボタンがクリックされました。PDFファイルの読み込みを開始します...")
        
        try:
            # PyPDF2でアップロードされたファイルを読み込むテスト
            pdf_reader = PdfReader(uploaded_file)
            
            # ページ数を取得するテスト
            num_pages = len(pdf_reader.pages)
            
            # 成功した場合
            st.success(f"✅ PDFの読み込みに成功しました！ 総ページ数: {num_pages}")
            st.balloons()

        except Exception as e:
            # エラーが発生した場合
            st.error(f"❌ PDFの読み込み中、またはページ数取得中にエラーが発生しました。")
            # エラーの詳細を画面に表示します
            st.exception(e)
            
else:
    st.info("☝️ PDFファイルをアップロードしてください。")