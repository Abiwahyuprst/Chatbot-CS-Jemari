import os
import streamlit as st
from datetime import datetime
from groq import Groq

# 1. Konfigurasi Halaman & Tema
st.set_page_config(
    page_title="CS Virtual Cafe Jemari",
    page_icon="☕",
    layout="wide"
)

# 2. Custom CSS Sempurna (Pembersihan Total Kotak Hitam Bawah & Kontras Teks)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background Utama Aplikasi (Krem Hangat) */
    .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FAF7F2 !important;
        color: #1A1A1A !important;
    }

    /* Header Utama */
    h1 {
        color: #A64B35 !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        letter-spacing: -0.5px;
    }

    /* Styling Sidebar Keseluruhan */
    [data-testid="stSidebar"] {
        background-color: #F3ECE4 !important;
        border-right: 1px solid #E5D7C7;
        padding-top: 1rem;
    }
    
    [data-testid="stSidebar"] * {
        color: #1A1A1A !important;
    }

    /* Styling Tombol "MAU TANYA APA?" dengan Animasi Smooth & Warna Serasi */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #FAF7F2 !important;
        color: #A64B35 !important;
        border: 1.5px solid #A64B35 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 2px 5px rgba(166, 75, 53, 0.05);
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #A64B35 !important;
        color: #FFFFFF !important;
        border-color: #A64B35 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(166, 75, 53, 0.25);
    }

    /* --- BUBBLE CHAT ASSISTANT (KIRI - PUTIH BERSIH & TEKS HITAM TAJAM) --- */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #E5D7C7;
        border-radius: 16px 16px 16px 4px;
        padding: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-right: auto;
        max-width: 80%;
    }
    
    [data-testid="stChatMessage"]:nth-child(odd) *, 
    [data-testid="stChatMessage"]:nth-child(odd) p, 
    [data-testid="stChatMessage"]:nth-child(odd) span, 
    [data-testid="stChatMessage"]:nth-child(odd) td, 
    [data-testid="stChatMessage"]:nth-child(odd) th,
    [data-testid="stChatMessage"]:nth-child(odd) li,
    [data-testid="stChatMessage"]:nth-child(odd) strong {
        color: #1A1A1A !important;
    }

    /* --- BUBBLE CHAT USER (KANAN - MERAH MAROON & TEKS PUTIH) --- */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #A64B35 !important;
        color: #FFFFFF !important;
        border-radius: 16px 16px 4px 16px;
        padding: 14px;
        box-shadow: 0 4px 12px rgba(166, 75, 53, 0.15);
        margin-left: auto;
        max-width: 80%;
    }
    
    [data-testid="stChatMessage"]:nth-child(even) *, 
    [data-testid="stChatMessage"]:nth-child(even) p, 
    [data-testid="stChatMessage"]:nth-child(even) span {
        color: #FFFFFF !important;
    }

    /* --- PEMBERSIHAN TOTAL KOTAK GELAP DI AREA BAWAH --- */
    [data-testid="stBottomBlockContainer"], 
    [data-testid="stChatInputContainer"],
    [data-testid="stBottom"],
    .stBottom, 
    footer {
        background-color: #FFFFFF !important;
    }

    /* Memaksa pembungkus input chat menjadi krem tanpa kotak hitam */
    div[data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border-radius: 24px !important;
    }
    
    div[data-testid="stChatInput"] > div {
        border-radius: 24px !important;
    }

    /* Area teks saat diketik pengguna agar hitam pekat dan jelas */
    .stChatInput textarea {
        color: #FFFFFF !important;
        font-size: 15px !important;
    }
    
    .stChatInput textarea::placeholder {
        color: #FFFFFF !important;
    }

    /* Spasi dan Jarak Halaman */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 5rem;
        max-width: 1000px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Inisialisasi API Key Groq 
# PERHATIAN: Ganti string di bawah ini dengan API Key Groq terbaru milikmu yang aktif!
GROQ_KEY = os.environ.get("GROQ_API_KEY", "masukkan_api_key_disini") 
client = Groq(api_key=GROQ_KEY)

# 4. System Instruction & Knowledge Base Cafe Jemari
SYSTEM_INSTRUCTION = """
Kamu adalah CS Virtual pintar, ramah, dan komunikatif dari "Cafe Jemari" yang berlokasi di Desa Penjalin, Kecamatan Brangsong, Kabupaten Kendal.

Gaya Bahasa & Kepribadian:
- Gunakan bahasa Indonesia yang santai, ramah, sopan, dan hangat (khas anak muda/tempat nongkrong).
- Sering gunakan emoji yang relevan seperti ☕, 🍰, ✨, 🪑.

Pengetahuan Domain (Cafe Jemari):
- Lokasi: Penjalin, Brangsong, Kendal.
- Jam Operasional: Setiap hari pukul 10.00 - 22.00 WIB.
- Fasilitas: Wi-Fi cepat, area outdoor & indoor, colokan listrik di tiap meja (cocok buat nugas/kerja), tempat parkir luas, mushola, toilet.
- Menu Populer & Harga:
  * Kopi: Es Kopi Susu Jemari (Rp 15.000), Americano (Rp 12.000), Cafe Latte (Rp 18.000).
  * Non-Kopi: Matcha Latte (Rp 18.000), Chocolate Ice (Rp 16.000), Red Velvet (Rp 16.000).
  * Makanan/Cemilan: Mix Platter (Rp 20.000), Kentang Goreng (Rp 12.000), Roti Bakar Cokelat Keju (Rp 14.000), Mie Goreng Special (Rp 15.000).

Tugas Utama:
1. Membantu menjawab pertanyaan jam buka, lokasi, dan fasilitas.
2. Memberikan rekomendasi menu jika pengunjung bingung ingin memesan apa.
3. Menjawab pertanyaan dengan singkat, jelas, dan menarik.
"""

# 5. Sidebar Sesuai Desain Figma
with st.sidebar:
    if os.path.exists("Logo Jemari.jpg"):
        st.image("Logo Jemari.jpg", width=210)
    else:
        st.markdown("### **JE** MARI")
    
    st.markdown("<p style='font-size: 18px; color: #A64B35; font-weight: 600; margin-top: -8px; margin-bottom: 12px;'>SELAMAT DATANG DI JEMARI</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 15px; color: #666666; font-weight: 600; margin-top: -8px; margin-bottom: 12px;'>Kamis, 15 Oktober 2026 📅</p>", unsafe_allow_html=True)
    st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("#### Fasilitas ✨")
    st.markdown("💻 Wi-Fi Cepat")
    st.markdown("🔌 Stopkontak")
    st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("#### **MAU TANYA APA?**")
    if st.button("↗ Menu & rekomendasi", use_container_width=True):
        st.session_state.pending_prompt = "Apa saja menu dan rekomendasi populer di Cafe Jemari?"
    if st.button("↗ Suasana & fasilitas", use_container_width=True):
        st.session_state.pending_prompt = "Bagaimana suasana dan fasilitas yang ada di Cafe Jemari?"
    if st.button("↗ Informasi kunjungan", use_container_width=True):
        st.session_state.pending_prompt = "Di mana lokasi dan jam operasional Cafe Jemari?"
        
    st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background-color: #FFFFFF; padding: 10px; border-radius: 10px; border: 1px solid #E5D7C7;">
            <p style="color: #A64B35; font-weight: 700; margin-bottom: 2px; font-size: 20px;">☕ Singgah, cerita, senyum.</p>
            <p style="font-size: 15px; color: #555555; margin: 0;">Dari pilihan minuman sampai teman nugas, mulai saja dari sini.</p>
        </div>
    """, unsafe_allow_html=True)

# 6. Header Utama Aplikasi
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.title("CS Cafe Jemari")

st.caption("Silahkan Jika Bingung Di Tanyakan Kakak 👇")

# 7. Pengelolaan Riwayat Percakapan (Chat History)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Halo, selamat datang di Cafe Jemari! 👋 Mau cari teman ngopi, tempat nugas, atau rekomendasi sesuai seleramu?", "time": "10:24"}
    ]

current_input = None
if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    current_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.markdown(f"<div style='text-align: right; font-size: 10px; color: #888888; margin-top: 2px;'>{message.get('time', '10:25')}</div>", unsafe_allow_html=True)

# 8. Input Chat Pengguna
chat_input_val = st.chat_input("Tanyakan menu, lokasi, atau rekomendasi Cafe Jemari...")
user_input = current_input if current_input else chat_input_val

if user_input:
    current_time = datetime.now().strftime("%H:%M")
    
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input, "time": current_time})

    messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for msg in st.session_state.chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        bot_response = completion.choices[0].message.content
    except Exception as e:
        bot_response = f"Maaf, terjadi kendala koneksi: {str(e)}"

    bot_time = datetime.now().strftime("%H:%M")
    with st.chat_message("assistant"):
        st.markdown(bot_response)
        st.markdown(f"<div style='text-align: right; font-size: 10px; color: #888888; margin-top: 2px;'>{bot_time}</div>", unsafe_allow_html=True)
        
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response, "time": bot_time})