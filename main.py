import chess
import chess.engine

# --- KONFIGURASI ---
path_engine = r"C:\Users\ACER\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
waktu_mikir = 0.5  
kedalaman = 12     

def main():
    board = chess.Board()
    try:
        engine = chess.engine.SimpleEngine.popen_uci(path_engine)
        engine.configure({"Threads": 2, "Hash": 512})
        print(f"✅ Engine Aktif: {engine.id['name']}\n")
    except Exception as e:
        print(f"Error: Path Stockfish salah! {e}")
        return

    # --- PILIH WARNA ---
    while True:
        warna = input("Lu main sebagai Putih atau Hitam? (W/B): ").strip().lower()
        if warna in ['w', 'b']:
            break
        print("Input gak valid! Ketik 'W' untuk Putih atau 'B' untuk Hitam.")

    print("\n--- KONTROL ---")
    print("1 -> UNDO (Mundur 2 langkah)")
    print("2 -> KELUAR GAME")
    print("----------------\n")

    while not board.is_game_over():
        giliran_lu = (warna == 'w' and board.turn) or (warna == 'b' and not board.turn)

        if giliran_lu:
            # 1. GILIRAN LU (BOT JALAN OTOMATIS)
            print("\n🤖 Bot lagi mikir langkah buat Lu...")
            info = engine.analyse(board, chess.engine.Limit(time=waktu_mikir, depth=kedalaman), multipv=1)
            
            # PERBAIKAN: Akses indeks list [0] terlebih dahulu sebelum mengambil key dictionary
            langkah_terbaik = info[0]["pv"][0]
            
            notasi_san = board.san(langkah_terbaik)
            score = info[0]["score"].relative.score(mate_score=10000) / 100
            print(f"👉 Langkah Lu (Otomatis): {notasi_san} (Skor: {score:+})")
            
            board.push(langkah_terbaik)
        
        else:
            # 2. GILIRAN MUSUH (LU INPUT MANUAL)
            while True:
                langkah_musuh = input("\n♟️ Masukkan langkah Musuh: ").strip()
                
                if langkah_musuh == '2': 
                    engine.quit()
                    return
                
                if langkah_musuh == '1':
                    if len(board.move_stack) >= 2:
                        board.pop() 
                        board.pop() 
                        print("<<< Mundur 2 langkah.")
                        break
                    else:
                        print(">>> Gak bisa undo.")
                        continue
                
                try:
                    board.push_san(langkah_musuh)
                    break
                except ValueError:
                    print(">>> Langkah musuh gak valid (Contoh: e5, Nf6, dll). Coba lagi!")

    print(f"\nGAME SELESAI! Hasil: {board.result()}")
    engine.quit()

if __name__ == "__main__":
    main()
