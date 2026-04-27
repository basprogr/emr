import tkinter as tk
from tkinter import messagebox
import pyautogui
import time

def jalankan_automasi():
    # 1. Ambil semua data dari Text widget
    raw_data = text_area.get("1.0", tk.END).strip()
    
    if not raw_data:
        messagebox.showwarning("Peringatan", "Data kosong!")
        return

    # 2. Pisahkan per baris
    daftar_baris = raw_data.split('\n')

    # Memberi waktu user untuk pindah ke window browser (3 detik)
    messagebox.showinfo("Siap-siap", "Klik OK, lalu segera fokuskan kursor ke input field pertama di browser.\nAutomasi dimulai dalam 3 detik.")
    time.sleep(3)

    for baris in daftar_baris:
        if not baris.strip(): continue # Skip jika ada baris kosong
        
        # 3. Parsing data (pecah berdasarkan '-')
        # Susunan: tanggal-ruang-sistole-diastole-nadi-suhu-rr-spo2
        data = baris.split('-')
        
        if len(data) < 7:
            print(f"Format baris salah: {baris}")
            continue

        # Kita asumsikan kursor sudah ada di field pertama
        # Urutan input sesuai keinginanmu:
        # Sistole (index 2), Diastole (index 3), Nadi (4), Suhu (5), RR (6), SpO2 (7)
        
        # Contoh alur pengisian:
        pyautogui.write(data[2]) # Sistole
        pyautogui.press('tab')
        
        pyautogui.write(data[3]) # Diastole
        pyautogui.press('tab')
        
        pyautogui.write(data[4]) # Nadi
        pyautogui.press('tab')
        
        pyautogui.write(data[5]) # Suhu
        pyautogui.press('tab')
        
        pyautogui.write(data[6]) # RR
        pyautogui.press('tab')
        
        pyautogui.write(data[7]) # SpO2
        
        # 4. Berhenti sejenak dan minta konfirmasi untuk baris berikutnya
        # Ini berfungsi sebagai "Pause" agar tidak bablas
        msg = f"Baris selesai: {baris}\nLanjut ke baris berikutnya?"
        if not messagebox.askyesno("Konfirmasi", msg):
            break 
        
        # Beri jeda kecil agar user punya waktu klik field awal lagi jika perlu
        time.sleep(1)

# --- Setup GUI Sederhana ---
root = tk.Tk()
root.title("Automasi Input Medis")

text_area = tk.Text(root, height=10, width=50)
text_area.pack(pady=10)

# Contoh data awal
text_area.insert(tk.END, "20260401-301a-120-80-69-36,9-20-98\n20260401-302b-110-75-60-37.2-18-97")

btn_start = tk.Button(root, text="Mulai Input Otomatis", command=jalankan_automasi)
btn_start.pack(pady=10)

root.mainloop()