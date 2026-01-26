import getpass
import importlib
import subprocess
import sys
import requests

# Daftar modul eksternal yang dibutuhkan
REQUIRED_MODULES = [
    "requests",
    "pdfplumber",
    "pyautogui",
    "pyperclip"
]

def ensure_module(module_name):
    """Cek apakah modul sudah terinstall, kalau belum install otomatis."""
    try:
        importlib.import_module(module_name)
    except ImportError:
        print(f"Module {module_name} belum ada, menginstall...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

def main():
    # Password check
    password = getpass.getpass("Masukkan password: ")
    if password != "asdasd":
        print("Password salah!")
        return

    # Pastikan semua dependency terinstall
    for module in REQUIRED_MODULES:
        ensure_module(module)

    # URL raw file dari GitHub public repo
    url = "https://raw.githubusercontent.com/basprogr/emr/main/emr.py"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengakses GitHub: {e}")
        return

    if response.status_code != 200:
        print(f"Gagal mengambil script dari GitHub. Status: {response.status_code}")
        return

    script_code = response.text

    # Validasi isi: jangan eksekusi kalau ternyata HTML
    if script_code.strip().startswith("<"):
        print("Isi yang diunduh bukan Python, kemungkinan salah URL.")
        print("Isi awal respons:\n", script_code[:200])
        return

    # Jalankan script langsung dari memori
    exec(script_code, globals())

if __name__ == "__main__":
    main()
