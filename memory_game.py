#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Number Game - Temukan Pasangan Angka
Console-based Memory Game
"""

import random
import time
import os
import sys


class MemoryGame:
    def __init__(self):
        self.board = []
        self.revealed = []
        self.found_pairs = []
        self.attempts = 0
        self.start_time = None
        self.first_card = None
        self.second_card = None

    def initialize_board(self):
        """Initialize the game board with numbers 1-6 appearing twice"""
        numbers = list(range(1, 7)) * 2  # [1,2,3,4,5,6,1,2,3,4,5,6]
        random.shuffle(numbers)
        
        # Create 3x4 board (3 rows, 4 columns)
        self.board = [numbers[i*4:(i+1)*4] for i in range(3)]
        
        # Initialize revealed state (False = hidden, True = revealed)
        self.revealed = [[False for _ in range(4)] for _ in range(3)]
        
        self.found_pairs = []
        self.attempts = 0
        self.start_time = time.time()

    def get_elapsed_time(self):
        """Get elapsed time in MM:SS format"""
        if self.start_time is None:
            return "00:00"
        
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        return f"{minutes:02d}:{seconds:02d}"

    def is_game_complete(self):
        """Check if all pairs have been found"""
        return len(self.found_pairs) == 6


class MemoryUI:
    def __init__(self):
        self.game = MemoryGame()

    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print game header"""
        print("\n" + "=" * 50)
        print("🎮 MEMORY NUMBER GAME 🎮".center(50))
        print("=" * 50 + "\n")

    def print_menu(self):
        """Print main menu"""
        self.clear_screen()
        self.print_header()
        
        print("Selamat datang di Memory Number Game!\n")
        print("Pilihan:\n")
        print("1. ▶️  MULAI GAME")
        print("2. 📖 CARA BERMAIN")
        print("3. ❌ KELUAR\n")

    def print_rules(self):
        """Print game rules"""
        self.clear_screen()
        self.print_header()
        
        print("📋 CARA BERMAIN MEMORY NUMBER:\n")
        print("Tujuan:")
        print("  Temukan semua pasangan angka yang sama.\n")
        
        print("Cara Bermain:")
        print("  1. Board akan menampilkan semua angka selama 3 detik")
        print("  2. Angka akan tersembunyi")
        print("  3. Ketik posisi untuk membuka kotak (contoh: 0 0)")
        print("  4. Ketik posisi kedua untuk mencari pasangan")
        print("  5. Jika cocok, pair akan tetap terbuka")
        print("  6. Jika tidak cocok, keduanya akan tersembunyi lagi")
        print("  7. Ulangi hingga semua pasangan ketemu\n")
        
        print("Format Posisi:")
        print("  • Baris: 0, 1, 2 (dari atas ke bawah)")
        print("  • Kolom: 0, 1, 2, 3 (dari kiri ke kanan)")
        print("  • Contoh: 1 2 (baris 1, kolom 2)\n")
        
        print("Board Layout:")
        print("     0 1 2 3")
        print("  0  ? ? ? ?")
        print("  1  ? ? ? ?")
        print("  2  ? ? ? ?\n")
        
        input("Tekan ENTER untuk kembali ke menu...")

    def print_board(self, show_all=False):
        """Print the current board state"""
        print("\n" + "=" * 50)
        print(f"Waktu: {self.game.get_elapsed_time()} | Pasangan Ditemukan: {len(self.game.found_pairs)}/6 | Percobaan: {self.game.attempts}".center(50))
        print("=" * 50 + "\n")
        
        print("     0 1 2 3")
        print("  +" + "-" * 13 + "+")
        
        for i in range(3):
            row_str = f"{i} | "
            for j in range(4):
                if show_all:
                    # Show all numbers during memorization phase
                    row_str += f"{self.game.board[i][j]} "
                elif self.game.revealed[i][j]:
                    # Show revealed cards
                    row_str += f"{self.game.board[i][j]} "
                else:
                    # Show hidden cards
                    row_str += "? "
            
            row_str += "|"
            print(row_str)
        
        print("  +" + "-" * 13 + "+\n")

    def memorization_phase(self):
        """Show all cards for memorization"""
        self.clear_screen()
        self.print_header()
        print("📌 HAFAL POSISI ANGKA-ANGKA INI!\n")
        self.print_board(show_all=True)
        
        for i in range(20, 0, -1):
            print(f"Angka akan tersembunyi dalam {i} detik...".center(50))
            time.sleep(1)
        
        self.clear_screen()
        self.print_header()
        print("🔒 SEMUA ANGKA SUDAH TERSEMBUNYI. MULAI BERMAIN!\n")
        self.print_board(show_all=False)
        time.sleep(1)

    def get_card_input(self, card_number=1):
        """Get card position input from user"""
        while True:
            try:
                user_input = input(f"Pilih kartu ke-{card_number} (ROW COL atau 'menu'): ").strip().lower()
                
                if user_input == 'menu':
                    return None
                
                parts = user_input.split()
                if len(parts) != 2:
                    print("❌ Format salah! Gunakan: ROW COL (contoh: 0 0)")
                    continue
                
                row, col = int(parts[0]), int(parts[1])
                
                if not (0 <= row < 3 and 0 <= col < 4):
                    print("❌ Posisi harus valid! Baris: 0-2, Kolom: 0-3")
                    continue
                
                return (row, col)
            
            except ValueError:
                print("❌ Input tidak valid! Gunakan angka.")
            except Exception as e:
                print(f"❌ Error: {e}")

    def check_pair(self, pos1, pos2):
        """Check if two cards form a pair"""
        row1, col1 = pos1
        row2, col2 = pos2
        
        # Prevent selecting same card twice
        if pos1 == pos2:
            print("❌ Anda harus memilih 2 kartu yang berbeda!")
            return False
        
        # Prevent selecting already revealed cards
        if self.game.revealed[row1][col1] or self.game.revealed[row2][col2]:
            print("❌ Salah satu atau kedua kartu sudah terbuka!")
            return False
        
        # Check if cards match
        value1 = self.game.board[row1][col1]
        value2 = self.game.board[row2][col2]
        
        self.game.revealed[row1][col1] = True
        self.game.revealed[row2][col2] = True
        self.game.attempts += 1
        
        self.clear_screen()
        self.print_header()
        self.print_board(show_all=False)
        
        print(f"Kartu 1: ({row1}, {col1}) = {value1}")
        print(f"Kartu 2: ({row2}, {col2}) = {value2}\n")
        
        if value1 == value2:
            print("✅ BENAR! Pasangan ditemukan!\n")
            self.game.found_pairs.append((value1, value2))
            time.sleep(2)
            return True
        else:
            print("❌ SALAH! Kartu tidak cocok.\n")
            # Hide the cards again
            self.game.revealed[row1][col1] = False
            self.game.revealed[row2][col2] = False
            time.sleep(2)
            return False

    def play_game(self):
        """Main game loop"""
        self.game.initialize_board()
        self.memorization_phase()
        
        while not self.game.is_game_complete():
            self.clear_screen()
            self.print_header()
            self.print_board(show_all=False)
            
            # Get first card
            pos1 = self.get_card_input(1)
            if pos1 is None:
                return
            
            # Reveal first card
            row1, col1 = pos1
            self.game.revealed[row1][col1] = True
            
            self.clear_screen()
            self.print_header()
            self.print_board(show_all=False)
            print(f"Kartu 1: ({row1}, {col1}) = {self.game.board[row1][col1]}\n")
            
            # Get second card
            pos2 = self.get_card_input(2)
            if pos2 is None:
                self.game.revealed[row1][col1] = False
                return
            
            # Check the pair
            self.check_pair(pos1, pos2)
        
        # Game complete
        self.show_win_screen()

    def show_win_screen(self):
        """Show win screen with stats"""
        elapsed_time = self.game.get_elapsed_time()
        
        self.clear_screen()
        self.print_header()
        
        print("🎉 SELAMAT! ANDA MENANG! 🎉\n".center(50))
        print("=" * 50)
        print(f"Waktu: {elapsed_time}".center(50))
        print(f"Total Percobaan: {self.game.attempts}".center(50))
        print(f"Pasangan Ditemukan: {len(self.game.found_pairs)}/6".center(50))
        print("=" * 50 + "\n")
        
        input("Tekan ENTER untuk kembali ke menu...")

    def run(self):
        """Run the game"""
        while True:
            self.print_menu()
            choice = input("Pilih menu (1-3): ").strip()
            
            if choice == '1':
                self.play_game()
            
            elif choice == '2':
                self.print_rules()
            
            elif choice == '3':
                self.clear_screen()
                print("Terima kasih telah bermain Memory Number Game! 👋\n")
                sys.exit(0)
            
            else:
                print("❌ Pilihan tidak valid!")
                input("Tekan ENTER untuk melanjutkan...")


def main():
    """Entry point"""
    try:
        ui = MemoryUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n\nGame dihentikan oleh pengguna. Terima kasih! 👋\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
