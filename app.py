import streamlit as st
import google.generativeai as genai

# --- 1. PENGATURAN HALAMAN ---
st.set_page_config(page_title="Mr. Angiet Grammar Pro", page_icon="👨‍🏫")

# --- 2. CEK API KEY ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Kunci API belum dipasang di menu Secrets!")
    st.stop()

# --- 3. TAMPILAN ---
st.title("Let Mr. Angiet Check Your Grammar")
st.write("English Dept. Politeknik MBP")

# --- 4. DETEKSI OTOMATIS MODEL (SOLUSI PINTAR) ---
@st.cache_resource
def cari_model_yang_bisa():
    try:
        # Mencari model yang mendukung fitur 'generateContent'
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name # Mengambil model pertama yang ditemukan
    except Exception as e:
        return str(e)
    return None

nama_model_aktif = cari_model_yang_bisa()

# --- 5. INPUT & PROSES ---
input_teks = st.text_area("Masukkan teks bahasa Inggris:", placeholder="Contoh: She don't like apple.")

if st.button("Analisis Sekarang"):
    if not input_teks.strip():
        st.warning("Isi teksnya dulu ya.")
    elif "403" in str(nama_model_aktif) or "API_KEY_INVALID" in str(nama_model_aktif):
        st.error("Kunci API Bapak sepertinya salah atau belum aktif. Coba cek lagi di Google AI Studio.")
    elif nama_model_aktif:
        try:
            with st.spinner(f'Mencoba menggunakan model: {nama_model_aktif}...'):
                model = genai.GenerativeModel(nama_model_aktif)
                prompt = f'Analyze this English text for grammar: "{input_teks}". Provide: 1. Corrected Version. 2. Short Explanation in Bahasa Indonesia.'
                response = model.generate_content(prompt)
                st.success("Berhasil!")
                st.write(response.text)
        except Exception as e:
            st.error(f"Gagal memproses teks: {e}")
    else:
        st.error("Sistem tidak menemukan model yang aktif. Pastikan Billing/API Key sudah benar.")

# --- 6. INFO TEKNIS (Sembunyikan jika sudah lancar) ---
with st.expander("Klik untuk lihat info teknis"):
    st.write(f"Model yang terdeteksi di akun Bapak: `{nama_model_aktif}`")
