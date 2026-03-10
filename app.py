import streamlit as st
import google.generativeai as genai

# API Key Bapak
genai.configure(api_key="AIzaSyD-x6HjDBwkwuWO-Zt__QqSWOYt1_cv1wk")

st.set_page_config(page_title="Mr. Angiet Grammar Lite", page_icon="👨‍🏫")
st.title("👨‍🏫 Let Mr. Angiet Check Your Grammar")
st.write("Menggunakan Jalur 'Lite' (Lebih Cepat & Hemat Kuota)")

input_teks = st.text_area("Masukkan teks di sini:", height=150)

if st.button("Analisis Sekarang"):
    if not input_teks.strip():
        st.warning("Masukkan teksnya dulu, Pak Guru.")
    else:
        with st.spinner('Sedang menganalisis...'):
            try:
                # Menggunakan model 'Lite' yang biasanya kuotanya lebih besar/tersedia
                model = genai.GenerativeModel('gemini-flash-lite-latest')
                
                prompt = f"""
                Analyze this English text for grammar: "{input_teks}"
                1. Corrected Version
                2. Explanation in Bahasa Indonesia.
                """
                
                response = model.generate_content(prompt)
                st.subheader("Hasil Analisis:")
                st.info(response.text)
                st.success("Berhasil! Jalur Lite akhirnya terbuka.")
                
            except Exception as e:
                st.error(f"Sistem Google masih membatasi akses: {e}")
                st.info("Pak Guru, jika ini tetap gagal, ada kemungkinan Bapak perlu membuat API Key baru di Google AI Studio karena Key yang ini sedang 'dihukum' sementara oleh Google.")

st.divider()
st.caption("Mr. Angiet Assistant | Jalur Hemat")