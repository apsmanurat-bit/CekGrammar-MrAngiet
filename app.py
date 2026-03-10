import streamlit as st
import google.generativeai as genai

# --- 1. PENGATURAN HALAMAN & KEAMANAN ---
st.set_page_config(page_title="Mr. Angiet Grammar Pro", page_icon="👨‍🏫")

# Mengambil kunci dari brankas Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Kunci API belum dipasang di menu Secrets!")

# --- 2. TAMPILAN FOTO KECIL DAN JUDUL (SATU BARIS) ---
col1, col2 = st.columns([0.15, 0.85]) 

with col1:
    try:
        st.image("Anggiat-Simamora.jpg", width=60)
    except:
        st.write("👨‍🏫")

with col2:
    st.title("Let Mr. Angiet Check Your Grammar")

st.write("Selamat datang! Masukkan teks bahasa Inggris Anda untuk diperiksa.")

# --- 3. INPUT TEKS ---
input_teks = st.text_area("Masukkan teks di sini:", height=150, placeholder="Contoh: She go to school yesterday.")

# --- 4. PROSES ANALISIS ---
if st.button("Analisis Sekarang"):
    if not input_teks.strip():
        st.warning("Silakan masukkan teksnya dulu, Pak Guru.")
    else:
        with st.spinner('Sedang menganalisis... Mohon tunggu...'):
            try:
                model = genai.GenerativeModel('gemini-flash-lite-latest')
                
                prompt = f"""
                Analyze this English text for grammar: "{input_teks}"
                Provide:
                1. Corrected Version
                2. Explanation in Bahasa Indonesia.
                """
                
                response = model.generate_content(prompt)
                hasil_ai = response.text
                
                st.subheader("Hasil Analisis:")
                st.info(hasil_ai)
                
                # FITUR BARU: TOMBOL COPY
                st.copy_config = True
                st.code(hasil_ai, language=None)
                st.caption("💡 Klik ikon dua kotak di pojok kanan atas kotak abu-abu di atas untuk menyalin teks, lalu paste ke Word.")
                
                st.success("Analisis Berhasil!")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")

# --- 5. FOOTER ---
st.divider()
st.caption("Aplikasi Pembelajaran Mr. Angiet | 2026")
