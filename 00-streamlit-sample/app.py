import streamlit as st
import fitz  # PyMuPDF
import time
import pandas as pd
import io

# --------------------------------------------------------------------------
# アプリの基本設定
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="配合計画書OCRアプリ (サンプル)",
    page_icon="📄",
    layout="wide"
)

st.title("📄 配合計画書OCRアプリ (サンプル)")
st.caption("PDFをアップロードし、OCR処理を実行するデモです。")


# --------------------------------------------------------------------------
# セッション状態の初期化
# --------------------------------------------------------------------------
# 拡大率や処理結果をページのリロード後も保持するために使用します。
if 'zoom_level' not in st.session_state:
    st.session_state.zoom_level = 1.0
if 'pdf_document' not in st.session_state:
    st.session_state.pdf_document = None
if 'ocr_result_df' not in st.session_state:
    st.session_state.ocr_result_df = None


# --------------------------------------------------------------------------
# サイドバー: ファイルアップロードと情報表示
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("1. ファイル選択")
    uploaded_file = st.file_uploader(
        "処理したいPDFファイルをアップロードしてください",
        type="pdf"
    )

    if uploaded_file:
        # アップロードされたらファイルをメモリに読み込み、セッションに保存
        # file_bytes = uploaded_file.getvalue()
        file_bytes = uploaded_file.read()
        st.session_state.pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        
        st.success(f"「{uploaded_file.name}」を読み込みました。")
        st.write(f"ページ数: {st.session_state.pdf_document.page_count} ページ")

        # --- サムネイル表示 ---
        st.subheader("サムネイル")
        first_page = st.session_state.pdf_document.load_page(0)
        pix = first_page.get_pixmap(dpi=50) # 低解像度でサムネイルを生成
        st.image(pix.tobytes("png"), use_container_width=True)

        # --- 処理実行ボタン ---
        st.header("2. 処理実行")
        if st.button("🤖 OCRと補正を実行", type="primary", use_container_width=True):
            with st.spinner("AI OCRとLLMによる補正を実行中です... (約5秒)"):
                # ここで本来のAPI呼び出し処理を行う
                time.sleep(5) 
                
                # サンプル用のダミーデータを作成
                dummy_data = {
                    '品目コード': ['A-001', 'B-102', 'C-234'],
                    '品目名': ['主成分X', '添加剤Y', '結合剤Z'],
                    '配合量(kg)': [150.5, 25.0, 10.2],
                    '備考': ['温度注意', '', '湿度管理']
                }
                st.session_state.ocr_result_df = pd.DataFrame(dummy_data)

            st.success("🎉 処理が完了しました！")
            st.toast("結果を画面右側で確認できます。")


# --------------------------------------------------------------------------
# メイン画面: PDFビューアと結果表示
# --------------------------------------------------------------------------
col1, col2 = st.columns(2)

# --- 左カラム: PDFビューア ---
with col1:
    st.subheader("PDFビューア")
    if st.session_state.pdf_document:
        # --- ページ選択 ---
        page_num = st.number_input(
            "ページ番号", 
            min_value=1, 
            max_value=st.session_state.pdf_document.page_count, 
            value=1
        )
        
        # --- 拡大・縮小コントロール ---
        zoom_col1, zoom_col2, zoom_col3 = st.columns([1, 1, 8])
        if zoom_col1.button("➖", use_container_width=True):
            st.session_state.zoom_level = max(0.5, st.session_state.zoom_level - 0.2)
        if zoom_col2.button("➕", use_container_width=True):
            st.session_state.zoom_level = min(5.0, st.session_state.zoom_level + 0.2)
        
        st.slider("拡大率", 0.5, 5.0, step=0.1, key="zoom_level")

        # --- PDFページを画像として表示 ---
        page_to_show = st.session_state.pdf_document.load_page(page_num - 1)
        mat = fitz.Matrix(st.session_state.zoom_level, st.session_state.zoom_level)
        pix_large = page_to_show.get_pixmap(matrix=mat)
        st.image(pix_large.tobytes("png"))
    else:
        st.info("サイドバーからPDFファイルをアップロードしてください。")

# --- 右カラム: 処理結果 ---
with col2:
    st.subheader("処理結果")
    if st.session_state.ocr_result_df is not None:
        st.dataframe(st.session_state.ocr_result_df, use_container_width=True)
        
        # --- 結果ダウンロードボタン ---
        # DataFrameをExcel形式にメモリ上で変換
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            st.session_state.ocr_result_df.to_excel(writer, index=False, sheet_name='Sheet1')
        excel_data = output.getvalue()

        st.download_button(
            label="✅ Excel形式でダウンロード",
            data=excel_data,
            file_name="配合計画書_OCR結果.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    else:
        st.info("処理を実行すると、ここに結果が表示されます。")