# Program Simulasi Lampu Lalu Lintas 4-Arah dengan Mobil
# Program ini mensimulasikan sistem lalu lintas dengan 4 arah jalan (Utara, Timur, Selatan, Barat)

import tkinter as tk
import random
import time
import threading

# Konstanta warna untuk elemen-elemen dalam simulasi
CLR_BG   = "#2e3f4f"  # Warna latar belakang
CLR_ROAD = "#404040"  # Warna jalan
CLR_CAR  = ["#070f7e", "#db349e", "#8318B1", "#f1c40f", "#9b59b6", "#9f032a"]  # Warna mobil

# Durasi waktu lampu lalu lintas (dalam detik)
PHASES   = {"green": 10, "yellow": 2, "red": 12}
LANE_WIDTH = 120          # lebar satu jalur arah
INTERP_STEPS = 0          # turning is eliminated

class TrafficLightGUI:
    def __init__(self, root):
        """
        Inisialisasi GUI Simulasi Lampu Lalu Lintas
        Fungsi ini membuat tampilan antarmuka pengguna termasuk tombol kontrol, 
        canvas untuk menggambar jalan dan mobil, serta posisi lampu lalu lintas
        """
        self.root = root
        root.title("Simulasi Lampu Lalu Lintas")
        root.configure(bg=CLR_BG)
        self.canvas_w = 700
        self.canvas_h = 700
        self.center_x = self.canvas_w // 2
        self.center_y = self.canvas_h // 2

        # --- Frame Kontrol untuk tombol-tombol ---
        ctrl = tk.Frame(root, bg=CLR_BG)
        ctrl.pack(pady=10)

        # Tombol-tombol kontrol simulasi
        tk.Button(ctrl, text="Start",  width=8, command=self.start).grid(row=0, column=0, padx=5)
        tk.Button(ctrl, text="Stop",   width=8, command=self.stop).grid(row=0, column=1, padx=5)
        tk.Button(ctrl, text="Reset",  width=8, command=self.reset).grid(row=0, column=2, padx=5)

        # Slider kecepatan mobil
        tk.Label(ctrl, text="Kecepatan:", fg="white", bg=CLR_BG).grid(row=1, column=0, pady=5)
        self.speed_var = tk.DoubleVar(value=2.0)
        tk.Scale(ctrl, from_=0.5, to=5, resolution=0.5, orient="horizontal",
                 variable=self.speed_var, bg=CLR_BG, fg="white",
                 troughcolor="#555").grid(row=1, column=1, columnspan=3, sticky="ew", padx=5)

        # --- Canvas tempat menggambar jalan dan mobil ---
        self.canvas = tk.Canvas(root, width=self.canvas_w, height=self.canvas_h,
                                bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack()
        self.draw_road()

        # Menentukan posisi lampu lalu lintas di keempat arah
        offset = 80
        self.light_pos = {
            "Utara": (self.center_x, offset),
            "Timur": (self.canvas_w - offset, self.center_y),
            "Selatan": (self.center_x, self.canvas_h - offset),
            "Barat": (offset, self.center_y)
        }
        
        # Membuat elemen-elemen lampu lalu lintas
        self.lights = {}
        for name, (x, y) in self.light_pos.items():
            self.lights[name] = {
                "circle": self.canvas.create_oval(x-25, y-25, x+25, y+25, fill="black"),
                "label":  self.canvas.create_text(x, y+35, text=name, fill="white", font=("Arial", 10)),
                "timer":  self.canvas.create_text(x, y+50, text="", fill="white", font=("Arial", 9))
            }

        # Daftar arah jalan
        self.dirs = ["Utara", "Timur", "Selatan", "Barat"]
        self.lights_state = {}
        self.current_green = "Utara"
        self.sequence_index = 0
        self.reset_lights()

        # Timer untuk perubahan lampu dan spawn mobil
        self.next_light_change = time.monotonic() + 1.0
        self.spawn_timer = time.monotonic()

        self.cars = []
        self.running = False

    # ---------- Fungsi untuk menggambar jalan ----------
    def draw_road(self):
        """
        Fungsi untuk menggambar jalan silang di tengah canvas
        Menggambar jalan horizontal dan vertikal dengan garis pembatas
        """
        r = 120
        # horizontal
        self.canvas.create_rectangle(0, self.center_y - r,
                                     self.canvas_w, self.center_y + r,
                                     fill=CLR_ROAD, outline="")
        # vertical
        self.canvas.create_rectangle(self.center_x - r, 0,
                                     self.center_x + r, self.canvas_h,
                                     fill=CLR_ROAD, outline="")
        # garis pembatas dua arah
        self.canvas.create_line(0, self.center_y,
                                self.center_x - r, self.center_y,
                                fill="white", width=2)
        self.canvas.create_line(self.center_x + r, self.center_y,
                                self.canvas_w, self.center_y,
                                fill="white", width=2)
        self.canvas.create_line(self.center_x, 0,
                                self.center_x, self.center_y - r,
                                fill="white", width=2)
        self.canvas.create_line(self.center_x, self.center_y + r,
                                self.center_x, self.canvas_h,
                                fill="white", width=2)

    # ---------- Fungsi-fungsi untuk mengatur lampu lalu lintas ----------
    def reset_lights(self):
        """
        Mengatur ulang status semua lampu lalu lintas ke kondisi awal
        Arah Utara pertama kali mendapat lampu hijau, yang lainnya merah
        """
        for d in self.dirs:
            if d == self.current_green:
                self.lights_state[d] = {"color": "green", "remain": PHASES["green"]}
            else:
                self.lights_state[d] = {"color": "red", "remain": PHASES["red"]}
        self.update_lights_display()

    def update_lights_display(self):
        """
        Memperbarui tampilan warna dan timer pada lampu lalu lintas
        Fungsi ini mengubah warna dan angka pada lampu di canvas
        """
        for d, data in self.lights_state.items():
            self.canvas.itemconfig(self.lights[d]["circle"], fill=data["color"])
            self.canvas.itemconfig(self.lights[d]["timer"], text=str(data["remain"]))

    def update_lights(self):
        """
        Memperbarui status lampu lalu lintas secara otomatis
        Mengatur perubahan warna lampu sesuai siklus: hijau -> kuning -> merah
        """
        now = time.monotonic()
        if now < self.next_light_change:
            return
        self.next_light_change = now + 1.0

        for d, data in self.lights_state.items():
            if data["remain"] > 0:
                data["remain"] -= 1
                continue
            if data["color"] == "green":
                data.update({"color": "yellow", "remain": PHASES["yellow"]})
            elif data["color"] == "yellow":
                data.update({"color": "red", "remain": PHASES["red"]})
                self.sequence_index = (self.sequence_index + 1) % len(self.dirs)
                self.current_green = self.dirs[self.sequence_index]
                self.lights_state[self.current_green].update(
                    {"color": "green", "remain": PHASES["green"]})
        self.update_lights_display()

    # ---------- Fungsi-fungsi untuk mengatur mobil ----------
    def spawn_car(self):
        """
        Fungsi untuk membuat mobil baru di ujung jalan secara acak
        Mobil dipilih dari arah acak dan akan bergerak lurus
        """
        now = time.monotonic()
        if now - self.spawn_timer < 2.5 or len(self.cars) >= 16:
            return
        self.spawn_timer = now

        src = random.choice(self.dirs)
        color = random.choice(CLR_CAR)
        speed = self.speed_var.get() * random.uniform(0.8, 1.2)

        # Only go straight
        idx = self.dirs.index(src)
        tgt = self.dirs[(idx + 2) % 4]  # Go straight (opposite direction)

        lane_offset = -60 if src in ("Utara", "Timur") else 60
        if src == "Utara":
            y_spawn, x_lane = (-20, self.center_x + lane_offset)
            car = {"x": float(x_lane), "y": float(y_spawn), "dx": 0, "dy": 1, "dir": src, "target_dir": tgt,
                   "color": color, "speed": speed, "state": "straight", "step": 0}
        elif src == "Timur":
            x_spawn, y_lane = (self.canvas_w + 20, self.center_y + lane_offset)
            car = {"x": float(x_spawn), "y": float(y_lane), "dx": -1, "dy": 0, "dir": src, "target_dir": tgt,
                   "color": color, "speed": speed, "state": "straight", "step": 0}
        elif src == "Selatan":
            y_spawn, x_lane = (self.canvas_h + 20, self.center_x + lane_offset)
            car = {"x": float(x_lane), "y": float(y_spawn), "dx": 0, "dy": -1, "dir": src, "target_dir": tgt,
                   "color": color, "speed": speed, "state": "straight", "step": 0}
        else:  # Barat
            x_spawn, y_lane = (-20, self.center_y + lane_offset)
            car = {"x": float(x_spawn), "y": float(y_lane), "dx": 1, "dy": 0, "dir": src, "target_dir": tgt,
                   "color": color, "speed": speed, "state": "straight", "step": 0}

        car["item"] = self.canvas.create_rectangle(
            car["x"] - 15, car["y"] - 15,
            car["x"] + 15, car["y"] + 15,
            fill=car["color"], outline="")
        self.cars.append(car)

    def should_stop(self, car):
        """
        Memeriksa apakah mobil harus berhenti karena lampu merah atau kuning
        Mengembalikan True jika mobil harus berhenti, False jika tidak
        """
        light = self.lights_state[car["dir"]]
        if light["color"] == "green":
            return False
        stop_dist = 180
        cx, cy = self.center_x, self.center_y
        if car["dir"] == "Utara" and cy - stop_dist <= car["y"] <= cy - stop_dist + 20:
            return True
        if car["dir"] == "Timur" and cx + stop_dist - 40 <= car["x"] <= cx + stop_dist:
            return True
        if car["dir"] == "Selatan" and cy + stop_dist - 20 <= car["y"] <= cy + stop_dist:
            return True
        if car["dir"] == "Barat" and cx - stop_dist <= car["x"] <= cx - stop_dist + 20:
            return True
        return False

    def car_ahead(self, car):
        """
        Memeriksa apakah ada mobil lain di depan mobil saat ini
        Mengembalikan True jika ada mobil di depan, False jika tidak
        """
        for other in self.cars:
            if other is car or other["dir"] != car["dir"] or other["state"] == "turning":
                continue
            dx = other["x"] - car["x"]
            dy = other["y"] - car["y"]
            dist = dx * car["dx"] + dy * car["dy"]
            if 0 < dist < 50:
                return True
        return False

    def move_cars(self):
        """
        Memindahkan semua mobil sesuai dengan arah dan kecepatannya
        Sekarang hanya mendukung pergerakan lurus
        """
        for car in self.cars[:]:
            # Turn behavior is removed - only straight movement is supported
            if self.should_stop(car) or self.car_ahead(car):
                continue

            car["x"] += car["dx"] * car["speed"]
            car["y"] += car["dy"] * car["speed"]
            self.canvas.coords(car["item"],
                               car["x"] - 15, car["y"] - 15,
                               car["x"] + 15, car["y"] + 15)

           

    # ---------- Fungsi-fungsi kontrol simulasi ----------
    def start(self):
        """
        Memulai simulasi dengan membuat thread baru
        Thread ini akan menjalankan fungsi loop secara terus-menerus
        """
        if not self.running:
            self.running = True
            threading.Thread(target=self.loop, daemon=True).start()

    def stop(self):
        """
        Menghentikan simulasi dengan mengubah status running menjadi False
        Thread simulasi akan berhenti saat kondisi running menjadi False
        """
        self.running = False

    def reset(self):
        """
        Mengatur ulang simulasi ke kondisi awal
        Menghapus semua mobil, mengatur ulang lampu lalu lintas
        """
        self.stop()
        for c in self.cars:
            self.canvas.delete(c["item"])
        self.cars.clear()
        self.current_green = "Utara"
        self.sequence_index = 0
        self.reset_lights()
        self.next_light_change = time.monotonic() + 1.0

    # ---------- Thread utama simulasi ----------
    def loop(self):
        """
        Loop utama yang dijalankan secara terus-menerus dalam thread
        Fungsi ini mengatur sinkronisasi antara update lampu, gerakan mobil,
        dan spawn mobil baru
        """
        while self.running:
            self.update_lights()
            self.move_cars()
            self.spawn_car()
            time.sleep(0.016)  # ~60 FPS for smoother animation

if __name__ == "__main__":
    # Jalankan program simulasi lampu lalu lintas
    root = tk.Tk()
    TrafficLightGUI(root)
    root.mainloop()
