import streamlit as st
import pandas as pd
import time
import io
from PyPDF2 import PdfReader
import openpyxl

# --- ダミー関数 (AI OCRやLLMの処理を模倣) ---
def dummy_page_type_check(page_text):
    """ページの種別を簡易判定するダミー関数"""
    time.sleep(0.1)  # 判定処理を模倣
    if "配合計画書" in page_text:
        return "配合計画書"
    elif "材料リスト" in page_text:
        return "材料リスト"
    else:
        return "その他"

def dummy_ocr_and_llm(page_text):
    """OCRとLLMでの解析を模倣するダミー関数"""
    time.sleep(1.0)  # 重い処理を模倣
    data = {
        "製品名": [f"製品サンプル-{int(time.time()) % 1000}"],
        "材料A(kg)": [round(100 + time.time() % 50, 1)],
        "材料B(kg)": [round(200 + time.time() % 30, 1)],
        "合計(kg)": [round(300 + time.time() % 80, 1)]
    }
    return pd.DataFrame(data)


# --- Streamlit アプリケーション本体 ---
st.set_page_config(page_title="配合計画書OCRアプリ", layout="wide")
st.title("📄 配合計画書OCRアプリ (プロトタイプ)")

uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type="pdf")

if uploaded_file is not None:
    st.success(f"✅ ファイル「{uploaded_file.name}」を認識しました。")
    process_button = st.button("処理実行", type="primary")

    if process_button:
        try:
            pdf_reader = PdfReader(uploaded_file)
            num_pages = len(pdf_reader.pages)
            
            st.markdown("---")
            st.info("処理を開始します...")

            # UIコンポーネントを初期化
            progress_bar = st.progress(0, text="処理待機中...")
            all_results = []
            
            # --- フェーズ1: ページ種別判定 (st.status なし) ---
            st.subheader("📖 フェーズ1: ページ種別判定")
            page_types = {}
            for i in range(num_pages):
                # 実際のコードではここで簡易OCRを実行します
                page_text = f"これは{i+1}ページ目のダミーテキストです。"
                if i in [4, 15, 30, 55, 70]: # 配合計画書のダミーページを増やす
                    page_text += "配合計画書"

                page_type = dummy_page_type_check(page_text)
                page_types[i] = page_type
                progress_bar.progress((i + 1) / num_pages, text=f"ページ種別判定中... {i + 1}/{num_pages}")

            haigou_pages = [p for p, t in page_types.items() if t == "配合計画書"]
            st.write(f"✅ ページ種別判定完了。 **{len(haigou_pages)}** 件の配合計画書が見つかりました。")

            # --- フェーズ2: 配合計画書のOCRとLLM解析 (st.status なし) ---
            if haigou_pages:
                st.subheader(f"📑 フェーズ2: 配合計画書のOCR & LLM解析")
                for idx, page_num in enumerate(haigou_pages):
                    # 各ページの処理状況をテキストで表示
                    st.text(f"  - 配合計画書を処理中 ({idx + 1}/{len(haigou_pages)}) ... [該当ページ: {page_num + 1}]")
                    page_text_full = f"これは{page_num+1}ページ目の配合計画書の詳細なダミーテキストです。"
                    
                    result_df = dummy_ocr_and_llm(page_text_full)
                    result_df["抽出元ページ"] = page_num + 1
                    all_results.append(result_df)
            
            st.markdown("---")

            # --- 3. 結果表示とダウンロード ---
            if all_results:
                final_df = pd.concat(all_results, ignore_index=True)
                st.success("🎉 全ての処理が完了しました！")
                st.header("抽出結果")
                st.dataframe(final_df)

                # Excelファイルへの変換
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    final_df.to_excel(writer, index=False, sheet_name='配合計画書データ')
                excel_data = output.getvalue()

                st.download_button(
                    label="📥 Excelファイルをダウンロード",
                    data=excel_data,
                    file_name="haigou_keikakusho_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("配合計画書が見つかりませんでした。")

        except Exception as e:
            st.error("❌ 処理中にエラーが発生しました。")
            st.exception(e)

else:
    st.info("☝️ PDFファイルをアップロードしてください。")