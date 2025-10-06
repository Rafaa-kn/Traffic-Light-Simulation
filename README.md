# 🚦 Program Simulasi Lampu Lalu Lintas 4-Arah (Straight-Only)

Program ini mensimulasikan **sistem lampu lalu lintas 4 arah (Utara, Timur, Selatan, Barat)** menggunakan Python dan **Tkinter**.  
Pada versi ini, semua mobil hanya bergerak **lurus** melewati persimpangan, sehingga simulasi lebih sederhana dan fokus pada manajemen lampu lalu lintas.

---

## 🧩 Fitur Utama
- Empat arah lalu lintas: **Utara, Timur, Selatan, Barat**
- Siklus lampu otomatis: hijau → kuning → merah
- Mobil muncul secara acak dan bergerak lurus tanpa belokan
- Pengaturan **kecepatan mobil** melalui slider
- Tombol kontrol: **Start**, **Stop**, dan **Reset**
- Loop animasi berjalan **~60 FPS** untuk visual yang halus

---

## 🖼️ Tampilan Program
Tampilan utama berisi:
- Area simulasi (jalan silang 4 arah)
- Lampu lalu lintas di setiap sisi
- Mobil berwarna-warni bergerak lurus
- Panel kontrol di bagian atas untuk mengatur simulasi

---

## ⚙️ Instalasi dan Cara Menjalankan

### 1. Clone repositori
```bash
git clone https://github.com/username/nama-repo.git
cd nama-repo


### 2. Pastikan Python sudah terinstal

Program ini menggunakan **Python 3.x** dan modul bawaan **Tkinter**.

Cek versi Python:

```bash
python --version
```

Jika Tkinter belum ada (biasanya sudah otomatis diinstal bersama Python), tambahkan dengan:

* **Linux (Debian/Ubuntu):**

  ```bash
  sudo apt install python3-tk
  ```

### 3. Jalankan program

```bash
python lampu_lalu_lintas_straight.py
```

---

## 🧠 Konsep dan Logika Program

* Setiap arah memiliki lampu lalu lintas dengan tiga fase:

  * 🟢 **Hijau** — mobil boleh berjalan.
  * 🟡 **Kuning** — tanda berhati-hati.
  * 🔴 **Merah** — mobil harus berhenti.
* Siklus berganti secara otomatis sesuai durasi:

  * Hijau: 10 detik
  * Kuning: 2 detik
  * Merah: 12 detik
* Mobil muncul secara acak di setiap arah dan bergerak lurus ke arah berlawanan.
* **Belokan dihilangkan**, sehingga semua mobil mengikuti lintasan lurus melewati persimpangan.

---

## 🧰 Teknologi yang Digunakan

* **Python 3**
* **Tkinter** — untuk GUI (Graphical User Interface)
* **Threading** — agar simulasi berjalan mulus tanpa hang
* **Random & Time** — untuk pengacakan dan pengaturan durasi

---

## 🧑‍💻 Struktur Kode

| Bagian                         | Deskripsi                                         |
| ------------------------------ | ------------------------------------------------- |
| `TrafficLightGUI`              | Kelas utama yang mengatur GUI dan logika simulasi |
| `draw_road()`                  | Menggambar jalan dan marka                        |
| `update_lights()`              | Mengatur perubahan warna lampu                    |
| `spawn_car()`                  | Membuat mobil baru di arah acak (lurus saja)      |
| `move_cars()`                  | Menggerakkan mobil secara lurus                   |
| `start()`, `stop()`, `reset()` | Fungsi kontrol simulasi                           |
| `loop()`                       | Thread utama untuk animasi dan update mobil/lampu |

---

## 🖱️ Kontrol Pengguna

| Tombol / Kontrol     | Fungsi                              |
| -------------------- | ----------------------------------- |
| **Start**            | Memulai simulasi                    |
| **Stop**             | Menghentikan simulasi sementara     |
| **Reset**            | Mengatur ulang ke kondisi awal      |
| **Slider Kecepatan** | Mengubah kecepatan pergerakan mobil |

---

## 📜 Lisensi

Proyek ini bersifat **open-source** dan dapat digunakan untuk keperluan belajar atau pengembangan lebih lanjut.

---

## ✨ Kontributor

Dibuat oleh **[Nama Kamu]**
Sebagai proyek simulasi lalu lintas berbasis Python dengan mobil bergerak lurus.

```

---

Kalau mau, aku bisa buatkan **versi README “perbandingan versi”** yang menjelaskan tiga versi:  
1. Mobil belok normal  
2. Mobil belok halus (Bezier)  
3. Mobil hanya lurus  

Ini akan sangat berguna untuk repositori agar pengunjung cepat memahami evolusi simulasi.  

Apakah mau aku buatkan versi itu juga?
```
