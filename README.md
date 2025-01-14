# Chatbot-AI-Hospital
Proyek **Chatbot AI Hospital** adalah aplikasi berbasis web yang dapat digunakan untuk:
1. Mencari jadwal dokter berdasarkan nama dokter atau spesialisasi.
2. Membooking janji temu dengan dokter.
3. Menggunakan chatbot berbasis AI **IndoGPT** untuk menjawab pertanyaan kesehatan.
4. Menampilkan tips kesehatan relevan melalui sistem RAG (Retrieval-Augmented Generation).
5. Menampilkan riwayat booking yang dilakukan oleh pengguna.

6. ## Fitur Utama
- **Pencarian Jadwal Dokter**: Menampilkan informasi jadwal dokter berdasarkan spesialisasi atau nama.
- **Booking Janji Temu**: Memungkinkan pengguna membuat janji temu dengan dokter.
- **Chatbot AI**: Menggunakan model **IndoGPT** untuk menjawab pertanyaan pengguna.
- **Tips Kesehatan**: Menggunakan sistem RAG untuk memberikan tips kesehatan berdasarkan query pengguna.
- **Riwayat Booking**: Menampilkan daftar semua janji temu yang telah dibuat.

---

## 1. **Setup Proyek**

### **1.1 Prasyarat**
Pastikan Anda sudah memiliki:
- Python 3.8 atau lebih baru
- `pip` package manager
- Virtual environment (opsional tetapi disarankan)

### **1.2 Langkah Instalasi**
1. **Clone Repository**
   git clone https://github.com/username/Chatbot-AI-Hospital.git
   cd Chatbot-AI-Hospital
2. Install Dependencies Install semua dependensi menggunakan file **requirements.txt**:
   pip install -r requirements.txt
3. Jalankan Aplikasi Jalankan aplikasi Flask:
   python main.py
4. Akses di **Browser** Buka aplikasi di browser:
   http://127.0.0.1:5000

## 2. **Penggunaan**
### **2.1 Fitur-fitur**
- Pencarian Jadwal Dokter: Masukkan nama dokter atau spesialisasi pada formulir di halaman utama untuk melihat jadwal dokter yang tersedia.
- Booking Janji Temu: Isi formulir booking dengan nama dokter, tanggal, waktu, dan nama pasien. Konfirmasi booking akan ditampilkan setelah pengiriman berhasil.
- Riwayat Booking: Semua janji temu yang telah dibuat akan ditampilkan di tabel "Riwayat Booking".
- Chatbot AI: Tanyakan pertanyaan terkait kesehatan kepada chatbot, dan chatbot akan memberikan respons.
- Tips Kesehatan: Cari tips kesehatan berdasarkan topik seperti "olahraga" atau "diet sehat". Tiga tips paling relevan akan ditampilkan.

### **2.2 Error Handling**
Jika terjadi kesalahan, aplikasi akan menampilkan pesan error yang sesuai. Pastikan semua file data dan dependensi terpasang dengan benar.

## 3. **Notes**
### **3.1 Struktur Direktori**
- app/: Berisi file main.py (aplikasi utama menggunakan Flask), rag_generate.py (membuat dataset rag), trainer.py (fine-tuning indogpt untuk medical dataset).
- data/: Berisi data jadwal dokter dan tips kesehatan.
- templates/: Berisi file HTML.
- static/: Berisi file CSS dan JavaScript.
- requirements.txt: Daftar dependensi proyek.
### **3.2 Model yang Digunakan**
- Model AI: IndoGPT (w11wo/indo-gpt2-small)
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Dataset fine-tuning: ruslanmv/ai-medical-chatbot
