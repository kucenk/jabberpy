# Bot Jabber/XMPP Python

Bot XMPP/Jabber yang dibuat dengan Python menggunakan pustaka slixmpp. Bot ini memiliki fitur lengkap untuk conference chat dengan greeting otomatis dan pengumuman waktu setiap jam.

## Fitur Utama ✨

### 1. **Greeting Otomatis** 
Bot akan menyapa pengguna baru yang join ke ruang conference:
- Mendeteksi ketika seseorang masuk ke ruang
- Mengirim pesan sambutan personal
- Pesan dapat dikustomisasi di file konfigurasi

### 2. **Pengumuman Waktu Setiap Jam**
Bot mengirim update waktu setiap jam ke semua ruang yang terhubung:
- Menampilkan waktu saat ini dengan zona waktu
- Pesan khusus untuk waktu-waktu tertentu (pagi, siang, malam)
- Dapat diaktifkan/dinonaktifkan sesuai kebutuhan

### 3. **Sistem Perintah**
Bot merespons perintah yang dimulai dengan `!`:

#### Perintah yang Tersedia:
- `!help` - Menampilkan daftar perintah
- `!ping` - Cek apakah bot aktif
- `!time` - Tampilkan waktu saat ini
- `!status` - Status bot dan statistik
- `!rooms` - Daftar ruang conference yang terhubung
- `!users [ruang]` - Daftar pengguna di ruang
- `!about` - Informasi tentang bot

#### Contoh Penggunaan:
```
Pengguna: !time
Bot: Waktu saat ini: Sabtu, 10 Agustus 2025 pukul 14:30:15 UTC

Pengguna: !status
Bot: Status Bot:
• Terhubung: ✅ Ya
• Nama: JabberBot
• Ruang tergabung: 2
• Total pengguna terlacak: 8
• Zona waktu: UTC
```

## Cara Penggunaan 🚀

### 1. Persiapan
```bash
# Install dependensi yang diperlukan
pip install slixmpp configparser pytz
```

### 2. Konfigurasi
Salin dan edit file `config_example.ini` menjadi `config.ini`:

```ini
[bot]
# Ganti dengan kredensial XMPP Anda
jid = bot_saya@server.com
password = password_saya
nickname = BotSaya

# Zona waktu (gunakan nama timezone pytz)
timezone = Asia/Jakarta

# Ruang conference yang akan dimasuki otomatis
auto_join_rooms = room1@conference.server.com,room2@conference.server.com

[messages]
# Pesan sambutan dapat disesuaikan
greeting = Halo {nick}! Selamat datang di ruang ini! 👋

[scheduler]
# Aktifkan pengumuman waktu setiap jam
hourly_announcements = true
```

### 3. Menjalankan Bot
```bash
# Dengan mode debug
python main.py --debug

# Dengan file konfigurasi kustom
python main.py --config konfigurasi_saya.ini

# Melihat bantuan
python main.py --help
```

### 4. Menggunakan Environment Variables (Opsional)
```bash
export XMPP_JID="bot_saya@server.com"
export XMPP_PASSWORD="password_saya"
python main.py
```

## Contoh Interaksi 💬

Setelah bot aktif di ruang conference, Anda bisa berinteraksi:

```
# Cek apakah bot berfungsi
!ping
Bot: Pong! 🏓

# Lihat waktu saat ini
!time
Bot: Waktu saat ini: Sabtu, 10 Agustus 2025 pukul 21:30:15 WIB

# Lihat status bot
!status
Bot: Status Bot:
• Terhubung: ✅ Ya
• Nama: BotSaya
• Ruang tergabung: 2
• Total pengguna terlacak: 5
• Zona waktu: Asia/Jakarta

# Lihat pengguna di ruang saat ini
!users
Bot: Pengguna di room@conference.server.com:
• Alice
• Bob
• Charlie
• BotSaya
```

## Fitur Greeting 👋

Ketika pengguna baru masuk ke ruang conference:

```
* Alice bergabung dengan ruang
Bot: Halo Alice! Selamat datang di conference! 👋

* Bob bergabung dengan ruang  
Bot: Halo Bob! Selamat datang di conference! 👋
```

## Pengumuman Waktu ⏰

Setiap jam tepat, bot akan mengirim pengumuman:

```
Bot: 🕐 14:00 pada Sabtu - Selamat siang! ☀️
Bot: 🕐 18:00 pada Sabtu - Selamat sore! 🌅
Bot: 🕐 00:00 pada Minggu - Tengah malam! 🌙
```

## Struktur File 📁

```
jabberbot/
├── main.py              # Entry point utama
├── jabberbot.py         # Kelas utama bot
├── commands.py          # Handler perintah
├── conference.py        # Manajemen ruang conference
├── scheduler.py         # Penjadwalan tugas
├── config.ini           # Konfigurasi bot
├── config_example.ini   # Contoh konfigurasi
├── README.md           # Dokumentasi lengkap (Inggris)
├── PANDUAN.md          # Panduan bahasa Indonesia
└── jabberbot.log       # File log
```

## Log dan Debugging 🐛

Bot menyediakan logging yang komprehensif:
- Log file: `jabberbot.log`
- Output console untuk monitoring real-time
- Mode debug untuk troubleshooting
- Format log terstruktur dengan timestamp

Untuk debugging, jalankan dengan flag `--debug`:
```bash
python main.py --debug
```

## Kustomisasi 🎨

### Mengubah Pesan Greeting
Edit di `config.ini`:
```ini
[messages]
greeting = Selamat datang {nick}! Semoga betah di sini! 🎉
```

### Mengatur Zona Waktu
```ini
[bot]
timezone = Asia/Jakarta    # Untuk WIB
timezone = Asia/Makassar   # Untuk WITA  
timezone = Asia/Jayapura   # Untuk WIT
```

### Menonaktifkan Pengumuman Jam
```ini
[scheduler]
hourly_announcements = false
```

## Troubleshooting 🔧

### Bot Tidak Terhubung
1. Periksa kredensial JID dan password
2. Pastikan server XMPP dapat diakses
3. Cek log untuk pesan error spesifik

### Bot Tidak Merespons Perintah
1. Pastikan perintah dimulai dengan `!`
2. Cek apakah bot sudah berhasil join ke ruang
3. Lihat log untuk error handling perintah

### Pengumuman Waktu Tidak Muncul
1. Periksa setting `hourly_announcements = true`
2. Pastikan bot terhubung ke ruang conference
3. Tunggu hingga pergantian jam berikutnya

## Keamanan 🔒

- Jangan commit file `config.ini` yang berisi password ke repository
- Gunakan environment variables untuk produksi
- Pastikan menggunakan koneksi TLS/SSL ke server XMPP
- Batasi akses bot hanya ke ruang yang diperlukan

## Lisensi 📄

Proyek ini tersedia untuk digunakan dan dimodifikasi sesuai kebutuhan.

---

Dibuat dengan ❤️ menggunakan Python dan slixmpp