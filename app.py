import streamlit as st
import google.generativeai as genai

# --- 1. PENGATURAN HALAMAN & KEAMANAN ---
st.set_page_config(page_title="Mr. Angiet Grammar Pro", page_icon="👨‍🏫")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Kunci API belum dipasang di menu Secrets!")

# --- 2. TAMPILAN FOTO KECIL DAN JUDUL ---
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
        with st.spinner('Mr. Angiet sedang memeriksa... Mohon tunggu sebentar...'):
            try:
                # MENGGUNAKAN MODEL GEMINI-PRO (PALING STABIL)
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f'Analyze this English text for grammar: "{input_teks}". Provide: 1. Corrected Version. 2. Explanation in Bahasa Indonesia.'
                
                response = model.generate_content(prompt)
                
                # Simpan ke memori sementara
                st.session_state['hasil_copy'] = response.text
                
            except Exception as e:
                # Menangani kuota (429) dengan bahasa yang ramah
                if "429" in str(e):
                    st.error("⚠️ SISTEM ANTRE: Kuota gratis sedang penuh. Mohon tunggu 30-60 detik lalu klik tombol Analisis lagi.")
                else:
                    st.error(f"Terjadi kesalahan teknis: {e}")

# --- 5. TAMPILAN HASIL ---
if 'hasil_copy' in st.session_state:
    st.subheader("Hasil Analisis:")
    st.warning("💡 **TIPS SALIN:** Tekan lama pada teks di bawah ini, lalu pilih 'Salin' (Copy) untuk dipindahkan ke Word.")
    st.text_area("Hasil (Bisa di-copy):", value=st.session_state['hasil_copy'], height=300)
    st.success("Analisis Selesai!")

# --- 6. FOOTER ---
st.divider()
st.caption("English Dept. Politeknik MBP | 2026")
