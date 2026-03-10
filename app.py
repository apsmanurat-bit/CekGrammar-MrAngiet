import streamlit as st
import google.generativeai as genai
import time

# --- 1. PENGATURAN HALAMAN & KEAMANAN ---
st.set_page_config(page_title="Mr. Angiet Grammar Pro", page_icon="👨‍🏫")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Kunci API belum dipasang di menu Secrets!")

# --- 2. TAMPILAN FOTO DAN JUDUL ---
col1, col2 = st.columns([0.15, 0.85]) 
with col1:
    try:
        st.image("Anggiat-Simamora.jpg", width=60)
    except:
        st.write("👨‍🏫")
with col2:
    st.title("Let Mr. Angiet Check Your Grammar")

st.write("Selamat datang mahasiswa **English Dept. Politeknik MBP**! Silakan periksa grammar Anda di sini.")

# --- 3. INPUT TEKS ---
input_teks = st.text_area("Masukkan teks bahasa Inggris:", height=150, placeholder="Contoh: I has a dream.")

# --- 4. PROSES ANALISIS ---
if st.button("Analisis Sekarang"):
    if not input_teks.strip():
        st.warning("Silakan masukkan teksnya dulu.")
    else:
        hasil_didapat = False
        
        with st.spinner('Mr. Angiet sedang memeriksa...'):
            # Kita coba daftar nama model yang paling mungkin tersedia
            # Mulai dari yang terbaru sampai yang standar
            model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            
            for name in model_names:
                try:
                    model = genai.GenerativeModel(name)
                    prompt = f'Analyze this English text for grammar: "{input_teks}". Provide: 1. Corrected Version. 2. Short Explanation in Bahasa Indonesia.'
                    response = model.generate_content(prompt)
                    
                    st.session_state['hasil_copy'] = response.text
                    hasil_didapat = True
                    break # Jika berhasil satu, langsung berhenti
                except Exception as e:
                    if "404" in str(e):
                        continue # Jika 404, coba nama model berikutnya di daftar
                    else:
                        st.error(f"Terjadi kendala: {e}")
                        break
        
        if hasil_didapat:
            st.balloons()
        else:
            st.error("Maaf Pak, sistem Google tidak merespon nama model. Mohon pastikan API Key di Secrets sudah benar.")

# --- 5. TAMPILAN HASIL ---
if 'hasil_copy' in st.session_state:
    st.subheader("Hasil Analisis:")
    st.info("💡 **INFO:** Tekan lama pada teks di bawah ini untuk Copy ke Word.")
    st.text_area("Hasil:", value=st.session_state['hasil_copy'], height=250)
    st.success("Analisis Selesai!")

# --- 6. FOOTER ---
st.divider()
st.caption("English Dept. Politeknik MBP | 2026")
