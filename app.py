import streamlit as st
import yt_dlp

st.set_page_config(page_title="YouTube Streaming Linker", page_icon="🎥", layout="centered")

st.title("🎥 YouTube 視聴リンク生成器")
st.write("RenderサーバーのIP制限を回避し、安全に再生・保存できるリンクを生成します。")

url = st.text_input("YouTubeの動画URLを入力してください:", placeholder="https://youtube.com...")

if st.button("リンクを生成する"):
    if not url:
        st.warning("URLを入力してください。")
    else:
        with st.spinner("視聴用URLを解析中..."):
            try:
                # サーバー側ではダウンロードせず、URLの解析(extract_info)のみ行う
                ydl_opts = {
                    'format': 'best[ext=mp4]/best',
                    'skip_download': True, # ← ここがポイント（ダウンロードしない）
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['mweb', 'web_embedded']
                        }
                    }
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # download=False にして情報だけを高速取得
                    info = ydl.extract_info(url, download=False)
                    
                    # 実際の動画ファイルが置かれている直リンク（Direct URL）を取得
                    video_url = info.get('url')
                    video_title = info.get('title', 'video')

                if video_url:
                    st.success("🎉 視聴・保存用の直接リンクの抽出に成功しました！")
                    st.write(f"**タイトル:** {video_title}")
                    
                    # 1. Streamlit上でそのまま再生できるようにする
                    st.video(video_url)
                    
                    # 2. Safariで開いて保存・視聴できるリンクを設置
                    st.markdown(f'👉 [ここを右クリック（または長押し）して「リンク先ファイルをダウンロード」を選択]({video_url})')
                else:
                    st.error("リンクの抽出に失敗しました。")

            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
                st.info("この方法でもエラーが出る場合、RenderのIPがYouTubeに完全に拒否されています。対策2をお試しください。")
