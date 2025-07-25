Berikut adalah **isi lengkap `README.md`** versi lucu, nyeleneh, tapi tetap informatif—siap kamu copy-paste langsung ke GitHub:

---

````markdown
# 🐫 SPHINX101 - Alat Pemburu Shell & Celah Web

**SPHINX101** adalah alat sakti mandraguna berbasis Python untuk mengendus keberadaan shell backdoor, RCE, file backup, dan berbagai kerentanan web **secepat kamu ngedeteksi mantan stalking IG kamu**.

> 🚨 Gunakan hanya di domain milik sendiri atau atas izin. Jangan jadi script kiddie yang viral di berita kriminal.

---

## 🦾 Fitur Andalan (Auto Nyusup)

- 🔍 **Random Shell Finder (RSF)**  
  Nyari file `shell.php`, `r57.php`, sampe `b374k.php` kayak mantan nyari kehangatan lama.

- 🔥 **PHPUnit RCE Scanner**  
  Tes endpoint `eval-stdin.php` buat ngecek apakah bisa dieksploitasi.

- 🧩 **WordPress Install Detector**  
  Cari situs WP yang belum di-install... siapa tau bisa "bantuin" installin. 😏

- 🗂️ **Roxy File Manager Scanner**  
  Cek apakah ada file manager terbuka buat upload "oleh-oleh".

- 🔐 **SFTP/SSH Port Checker**  
  Ngecek port 22 terbuka. Siapa tau ada lubang buat masuk lewat pintu belakang.

- 🧾 **Laravel RCE & Ignition Debug Check**  
  Intip file `.env`, `laravel.log`, sampe endpoint debug yang bisa dijadikan tempat main-main shell.

- 🧳 **Archives Finder**  
  Nyari file `backup.zip`, `database.tar.gz`, `site.7z`, dan temen-temennya. Gak usah jadi hacker, tinggal download aja 😆

- ⚡ **Multithreaded & Auto Save**  
  Cepat dan otomatis nyimpen hasil di folder `results/`.

---

## ⚙️ Cara Pakai (Gampang banget kok)

1. **Install dependensi dulu:**

```bash
pip install -r requirements.txt
````

2. **Bikin file `list.txt`** berisi daftar domain. Satu domain per baris.

3. **Jalankan:**

```bash
python sphinx101.py
```

4. Pilih menu sesuai keinginan. Hasil akan otomatis disimpan.

---

## 💾 Struktur Folder

```
sphinx101/
├── sphinx101.py            # Script utama
├── payloads/shell.php      # Shell PHP default
└── results/                # Tempat hasil hasil cuan audit
```

---

## 🧪 Contoh Output

```
[SHELL UPLOADED] http://example.com/shell.php
[FOUND] Laravel .env exposed at http://target.com/.env
[FOUND] SFTP/SSH open on target.com:22
```

---

## 📜 Disclaimer

Ini tools **untuk edukasi, pembelajaran keamanan siber, dan audit sistem milik sendiri**.
❌ Jangan digunakan untuk menyerang, deface, atau upload shell ke sistem orang lain tanpa izin.

**Ingat:**

> *Nyari bug boleh, nyolong enggak. Jangan malu-maluin komunitas.*

---

## 👑 Quotes Pembuat

> "IF YOU'RE STILL POOR, WHAT DO YOU HAVE TO FEAR?"
> — SPHINX101.GOV.ID

---

## 📃 Lisensi

MIT License. Gunakan dengan tanggung jawab.
Kalau kamu pakai alat ini dan dapat bug bounty...
**Jangan lupa traktir kopi 😎☕**

---

## ✨ Credits

Made with 💀 by **sphinx101.gov.id** team
Untuk dunia pentest yang lebih terbuka dan lucu

```
