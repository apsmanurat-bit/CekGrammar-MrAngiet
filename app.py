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

# --- 4. PROSES ANALISIS DENGAN AUTO-RETRY ---
if st.button("Analisis Sekarang"):
    if not input_teks.strip():
        st.warning("Silakan masukkan teksnya dulu.")
    else:
        hasil_didapat = False
        max_percobaan = 3
        
        with st.spinner('Mr. Angiet sedang memeriksa... (Jika antre, sistem akan mencoba otomatis)'):
            for i in range(max_percobaan):
                try:
                    # Menggunakan model Flash yang punya kuota gratis lebih longgar
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f'Analyze this English text for grammar: "{input_teks}". Provide: 1. Corrected Version. 2. Short Explanation in Bahasa Indonesia.'
                    
                    response = model.generate_content(prompt)
                    st.session_state['hasil_copy'] = response.text
                    hasil_didapat = True
                    break # Berhasil, keluar dari perulangan
                
                except Exception as e:
                    if "429" in str(e) and i < max_percobaan - 1:
                        time.sleep(2) # Tunggu 2 detik sebelum coba lagi
                        continue
                    else:
                        st.error(f"Sistem sedang sangat sibuk. Mohon tunggu 1 menit lalu coba lagi ya. (Error: {e})")
                        break
        
        if hasil_didapat:
            st.balloons() # Efek perayaan kecil jika berhasil

# --- 5. TAMPILAN HASIL ---
if 'hasil_copy' in st.session_state:
    st.subheader("Hasil Analisis:")
    st.info("💡 **INFO UNTUK MAHASISWA:** Tekan lama pada teks di bawah ini untuk Copy ke Word.")
    st.text_area("Hasil (Tekan lama untuk Copy):", value=st.session_state['hasil_copy'], height=250)
    st.success("Analisis Selesai!")

# --- 6. FOOTER ---
st.divider()
st.caption("English Dept. Politeknik MBP | 2026")
