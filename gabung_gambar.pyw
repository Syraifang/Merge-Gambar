import os
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image

def natural_sort_key(text):
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

class ImageMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Penggabung & Pemotong Gambar")
        self.root.geometry("460x380")
        self.root.resizable(False, False)

        # Variabel Input
        self.input_dir = tk.StringVar(value=os.path.abspath("input_gambar"))
        self.output_dir = tk.StringVar(value=os.path.abspath("hasil_gabungan"))
        self.target_width = tk.StringVar(value="800")
        self.max_height = tk.StringVar(value="8000")
        self.format_output = tk.StringVar(value="WEBP")
        self.quality = tk.IntVar(value=99)

        self.build_ui()

    def build_ui(self):
        pad = {'padx': 12, 'pady': 6}
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Folder Input
        ttk.Label(frame, text="Folder Input:").grid(row=0, column=0, sticky="w", **pad)
        ttk.Entry(frame, textvariable=self.input_dir, width=32).grid(row=0, column=1, **pad)
        ttk.Button(frame, text="Pilih...", command=self.browse_input).grid(row=0, column=2, **pad)

        # Folder Output
        ttk.Label(frame, text="Folder Output:").grid(row=1, column=0, sticky="w", **pad)
        ttk.Entry(frame, textvariable=self.output_dir, width=32).grid(row=1, column=1, **pad)
        ttk.Button(frame, text="Pilih...", command=self.browse_output).grid(row=1, column=2, **pad)

        # Target Width
        ttk.Label(frame, text="Lebar Hasil (px):").grid(row=2, column=0, sticky="w", **pad)
        ttk.Entry(frame, textvariable=self.target_width, width=15).grid(row=2, column=1, sticky="w", **pad)

        # Max Height
        ttk.Label(frame, text="Maks. Tinggi (px):").grid(row=3, column=0, sticky="w", **pad)
        ttk.Entry(frame, textvariable=self.max_height, width=15).grid(row=3, column=1, sticky="w", **pad)

        # Format Output
        ttk.Label(frame, text="Format Output:").grid(row=4, column=0, sticky="w", **pad)
        combo = ttk.Combobox(frame, textvariable=self.format_output, values=["WEBP", "JPEG", "PNG"], state="readonly", width=12)
        combo.grid(row=4, column=1, sticky="w", **pad)

        # Kualitas
        ttk.Label(frame, text="Kualitas (1-100):").grid(row=5, column=0, sticky="w", **pad)
        q_frame = ttk.Frame(frame)
        q_frame.grid(row=5, column=1, columnspan=2, sticky="w", **pad)
        ttk.Scale(q_frame, from_=1, to=100, variable=self.quality, orient="horizontal", length=160,
                  command=lambda v: self.q_label.config(text=f"{int(float(v))}%")).pack(side="left")
        self.q_label = ttk.Label(q_frame, text=f"{self.quality.get()}%")
        self.q_label.pack(side="left", padx=8)

        # Tombol Proses & Status
        self.btn_start = ttk.Button(frame, text="Mulai Gabungkan Gambar", command=self.start_process)
        self.btn_start.grid(row=6, column=0, columnspan=3, pady=15, ipadx=20, ipady=5)

        self.status_label = ttk.Label(frame, text="Siap memproses.", foreground="gray")
        self.status_label.grid(row=7, column=0, columnspan=3)

    def browse_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_dir.set(folder)

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir.set(folder)

    def start_process(self):
        try:
            width = int(self.target_width.get())
            height = int(self.max_height.get())
            if width <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Lebar dan Tinggi harus berupa angka lebih dari 0.")
            return

        self.btn_start.config(state="disabled")
        self.status_label.config(text="Sedang memproses gambar...", foreground="blue")
        
        
        threading.Thread(target=self.process_images, args=(width, height), daemon=True).start()

    def process_images(self, target_width, max_height):
        in_dir = self.input_dir.get()
        out_dir = self.output_dir.get()
        fmt = self.format_output.get()
        qual = self.quality.get()

        try:
            os.makedirs(in_dir, exist_ok=True)
            os.makedirs(out_dir, exist_ok=True)

            ekstensi_valid = ('.jpg', '.jpeg', '.webp', '.png')
            files = [f for f in os.listdir(in_dir) if f.lower().endswith(ekstensi_valid)]
            files.sort(key=natural_sort_key)

            if not files:
                self.finish_ui("Tidak ada gambar ditemukan di folder input.", "red")
                return

            resized_images = []
            for idx, f in enumerate(files, start=1):
                self.root.after(0, lambda i=idx, t=len(files): self.status_label.config(text=f"Mengubah ukuran gambar {i}/{t}..."))
                path = os.path.join(in_dir, f)
                with Image.open(path) as img:
                    if img.mode in ("RGBA", "P") and fmt == "JPEG":
                        bg = Image.new("RGB", img.size, (255, 255, 255))
                        bg.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
                        img = bg
                    elif img.mode != "RGB" and fmt != "PNG":
                        img = img.convert("RGB")

                    ratio = target_width / float(img.width)
                    new_height = int(float(img.height) * ratio)
                    resized_images.append(img.resize((target_width, new_height), Image.Resampling.LANCZOS))

            batches = []
            current_batch, current_height = [], 0
            for img in resized_images:
                if current_height + img.height > max_height and current_batch:
                    batches.append((current_batch, current_height))
                    current_batch = [img]
                    current_height = img.height
                else:
                    current_batch.append(img)
                    current_height += img.height
            if current_batch:
                batches.append((current_batch, current_height))

            ext_file = fmt.lower() if fmt != "JPEG" else "jpg"
            for idx, (batch, total_h) in enumerate(batches, start=1):
                self.root.after(0, lambda i=idx, t=len(batches): self.status_label.config(text=f"Menyimpan hasil {i}/{t}..."))
                mode_kanvas = "RGBA" if fmt == "PNG" else "RGB"
                kanvas = Image.new(mode_kanvas, (target_width, total_h))

                y_offset = 0
                for img in batch:
                    kanvas.paste(img, (0, y_offset))
                    y_offset += img.height

                nama_output = f"gabungan_{idx:03d}.{ext_file}"
                kanvas.save(os.path.join(out_dir, nama_output), format=fmt, quality=qual)

            self.finish_ui(f"Selesai! Berhasil membuat {len(batches)} file.", "green")
            self.root.after(0, lambda: messagebox.showinfo("Selesai", f"Berhasil menggabungkan {len(files)} gambar menjadi {len(batches)} file di folder output!"))

        except Exception as e:
            self.finish_ui(f"Terjadi kesalahan: {str(e)}", "red")

    def finish_ui(self, msg, color):
        self.root.after(0, lambda: self.status_label.config(text=msg, foreground=color))
        self.root.after(0, lambda: self.btn_start.config(state="normal"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageMergerApp(root)
    root.mainloop()