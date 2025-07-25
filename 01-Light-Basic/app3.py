import streamlit as st
import pandas as pd
import time
import io
# PyPDF2のインポートで問題が起きるケースがあるため確認します
from PyPDF2 import PdfReader
import openpyxl

st.title("ライブラリインポート テスト")
st.success("✅ この画面が表示されれば、ライブラリのインポートはすべて成功しています。")