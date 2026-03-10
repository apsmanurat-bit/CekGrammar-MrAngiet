import streamlit as st
import google.generativeai as genai
import time

# --- 1. PENGATURAN HALAMAN & KEAMANAN ---
st.set_page_config(page_title="Mr. Angiet Grammar Pro", page_icon="👨‍🏫")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Kunci API belum dipasang di menu Secrets!")
    st.stop()

# --- 2. FUNGSI DETEKSI MODEL (OTOMATIS) ---
@st.cache_resource
def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
    except:
        return "gemini-1.5-flash" # fallback
    return "gemini-1.5-flash"

working_model = get_working_model()

# --- 3. TAMPILAN HEADER ---
col1, col2 = st.columns([0.15, 0.85]) 
with col1:
    try:
        st.image("Anggiat-Simamora.jpg", width=60)
    except:
        st.write("👨‍🏫")
with col2:
    st.title("Let Mr. Angiet Check Your Grammar")
    st.caption("English Dept. Politeknik MBP")

# --- 4. LAMPU INDIKATOR STATUS ---
st.divider()
status_col1, status_col2 = st.columns([0.7, 0.3])
with status_col2:
    st.success("● System Ready") # Indikator Hijau

# --- 5. INPUT TEKS ---
input_teks = st.text_area("Masukkan teks bahasa Inggris Anda:", height=150, placeholder="Example: She don't know where he go.")

# --- 6. PROSES DENGAN PENGATURAN ANTREAN ---
if st.button("Analisis Sekarang"):
    if not input_teks.strip():
        st.warning("Silakan masukkan teksnya terlebih dahulu.")
    else:
        with st.spinner('Mr. Angiet sedang menganalisis... Mohon tidak menekan tombol berkali-kali.'):
            try:
                model = genai.GenerativeModel(working_model)
                prompt = f"""
                You are Mr. Angiet, a professional English Lecturer. 
                Analyze this text: "{input_teks}"
                Provide:
                1. Corrected Version.
                2. Grammar Explanation in Bahasa Indonesia.
                """
                response = model.generate_content(prompt)
                st.session_state['hasil_copy'] = response.text
                st.balloons()
            
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ **SISTEM SEDANG ANTRE (QUOTA FULL)**")
                    st.info("Batas gratis tercapai karena banyak mahasiswa yang akses bersamaan. Mohon tunggu sebentar.")
                    # Fitur Countdown (Lampu Kuning)
                    for i in range(15, 0, -1):
                        st.write(f"Silakan coba lagi dalam {i} detik...")
                        time.sleep(1)
                    st.success("Silakan klik kembali tombol 'Analisis Sekarang'!")
                else:
                    st.error(f"Terjadi kendala teknis: {e}")

# --- 7. TAMPILAN HASIL ---
if 'hasil_copy' in st.session_state:
    st.subheader("Hasil Analisis:")
    st.info("💡 **TIPS:** Tekan lama pada kotak di bawah untuk menyalin (copy) hasil ke Word.")
    st.text_area("Hasil Analisis Mr. Angiet:", value=st.session_state['hasil_copy'], height=300)
    st.success("Selesai! Silakan pelajari penjelasannya.")

# --- 8. FOOTER ---
st.divider()
st.caption("© 2026 English Dept. Politeknik MBP - Medan")
