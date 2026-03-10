import streamlit as st
import google.generativeai as genai

# --- 1. PENGATURAN HALAMAN & KEAMANAN ---
st.set_page_config(page_title="Mr. Angiet Grammar Pro", page_icon="👨‍🏫")

# Mengambil kunci dari brankas Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Kunci API belum dipasang di menu Secrets!")

# --- 2. TAMPILAN FOTO DAN JUDUL ---
# Menampilkan foto Bapak (Anggiat-Simamora.jpg) yang sudah ada di GitHub
try:
    st.image("Anggiat-Simamora.jpg", width=200)
except:
    st.info("Sedang memproses tampilan foto...")

st.title("👨‍🏫 Let Mr. Angiet Check Your Grammar")
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
                # Menggunakan model Gemini Flash Lite
                model = genai.GenerativeModel('gemini-flash-lite-latest')
                
                prompt = f"""
                Analyze this English text for grammar: "{input_teks}"
                Provide:
                1. Corrected Version
                2. Explanation in Bahasa Indonesia.
                """
                
                response = model.generate_content(prompt)
                
                st.subheader("Hasil Analisis:")
                st.info(response.text)
                st.success("Analisis Berhasil!")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")

# --- 5. FOOTER ---
st.divider()
st.caption("Aplikasi Pembelajaran Mr. Angiet | 2026")
