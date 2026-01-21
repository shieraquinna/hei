#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Sudoku untuk Pemula - 3 Level Kesulitan
Console-based Sudoku Game
"""

import random
import time
import os
import sys
from copy import deepcopy


class SudokuGame:
    def __init__(self):
        self.board = []
        self.original_board = []
        self.solution = []
        self.start_time = None
        self.difficulty = None
        self.hints_used = 0

    def generate_puzzle(self, difficulty):
        """Generate Sudoku puzzle berdasarkan difficulty level"""
        self.difficulty = difficulty
        
        # Generate solved board
        self.solution = self.generate_solved_board()
        
        # Copy solution
        self.board = [row[:] for row in self.solution]
        self.original_board = [row[:] for row in self.solution]
        
        # Remove numbers based on difficulty
        remove_counts = {
            'mudah': 64,      # Keep 17 clues
            'sedang': 73,     # Keep 8 clues
            'sulit': 82       # Keep 7 clues
        }
        
        target_remove = remove_counts.get(difficulty, 64)
        removed = 0
        
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for row, col in cells:
            if removed >= target_remove:
                break
            
            if self.board[row][col] != 0:
                backup = self.board[row][col]
                self.board[row][col] = 0
                
                # Check if puzzle still has unique solution
                if self.count_solutions(deepcopy(self.board)) == 1:
                    self.original_board[row][col] = 0
                    removed += 1
                else:
                    self.board[row][col] = backup

    def generate_solved_board(self):
        """Generate valid solved Sudoku board"""
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_board(board)
        return board

    def fill_board(self, board):
        """Fill board using backtracking algorithm"""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    
                    for num in numbers:
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            
                            if self.fill_board(board):
                                return True
                            
                            board[row][col] = 0
                    
                    return False
        
        return True

    def is_valid(self, board, row, col, num):
        """Check if number is valid at position"""
        # Check row
        if num in board[row]:
            return False
        
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        return True

    def count_solutions(self, board):
        """Count number of solutions (max 2 for performance)"""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    count = 0
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            count += self.count_solutions(board)
                            if count > 1:
                                board[row][col] = 0
                                return count
                            board[row][col] = 0
                    return count
        
        return 1

    def is_complete(self):
        """Check if board is completely filled"""
        for row in self.board:
            if 0 in row:
                return False
        return True

    def is_solved(self):
        """Check if board is correctly solved"""
        if not self.is_complete():
            return False
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != self.solution[i][j]:
                    return False
        
        return True

    def get_hint(self):
        """Get a hint by revealing a random empty cell"""
        empty_cells = []
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and self.original_board[i][j] == 0:
                    empty_cells.append({
                        'row': i,
                        'col': j,
                        'value': self.solution[i][j]
                    })
        
        if not empty_cells:
            return None
        
        hint = random.choice(empty_cells)
        self.board[hint['row']][hint['col']] = hint['value']
        self.hints_used += 1
        
        return hint

    def get_elapsed_time(self):
        """Get elapsed time in MM:SS format"""
        if self.start_time is None:
            return "00:00"
        
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        return f"{minutes:02d}:{seconds:02d}"


class SudokuUI:
    def __init__(self):
        self.game = SudokuGame()

    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print game header"""
        print("\n" + "=" * 50)
        print("🎮 SUDOKU GAME - UNTUK PEMULA 🎮".center(50))
        print("=" * 50 + "\n")

    def print_menu(self):
        """Print main menu"""
        self.clear_screen()
        self.print_header()
        
        print("Pilih Level Kesulitan:\n")
        print("1. ⭐ MUDAH (17 angka tersedia)")
        print("2. ⭐⭐ SEDANG (8 angka tersedia)")
        print("3. ⭐⭐⭐ SULIT (7 angka tersedia)")
        print("4. 📖 CARA BERMAIN")
        print("5. ❌ KELUAR\n")

    def print_rules(self):
        """Print game rules"""
        self.clear_screen()
        self.print_header()
        
        print("📋 CARA BERMAIN SUDOKU:\n")
        print("Tujuan:")
        print("  Isi semua kotak agar setiap baris, kolom, dan kotak")
        print("  3x3 berisi angka 1-9 tanpa pengulangan.\n")
        
        print("Aturan:")
        print("  1. Setiap baris harus berisi angka 1-9 tanpa duplikat")
        print("  2. Setiap kolom harus berisi angka 1-9 tanpa duplikat")
        print("  3. Setiap kotak 3x3 harus berisi angka 1-9 tanpa duplikat\n")
        
        print("Level Kesulitan:")
        print("  • Mudah: 17 angka tersedia (paling mudah)")
        print("  • Sedang: 8 angka tersedia (menengah)")
        print("  • Sulit: 7 angka tersedia (paling menantang)\n")
        
        print("Perintah Saat Bermain:")
        print("  • Ketik ROW COL NUM untuk mengisi (contoh: 0 0 5)")
        print("  • Ketik 'hint' untuk mendapat bantuan")
        print("  • Ketik 'clear' untuk menghapus semua input")
        print("  • Ketik 'check' untuk memeriksa jawaban")
        print("  • Ketik 'menu' untuk kembali ke menu\n")
        
        input("Tekan ENTER untuk melanjutkan...")

    def print_board(self):
        """Print the current board state"""
        print("\n" + "=" * 40)
        print(f"Level: {self.game.difficulty.upper()} | Waktu: {self.game.get_elapsed_time()} | Hints: {self.game.hints_used}".center(40))
        print("=" * 40 + "\n")
        
        print("    0 1 2   3 4 5   6 7 8")
        print("  +" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")
        
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("  +" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")
            
            row_str = f"{i} | "
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "| "
                
                val = self.game.board[i][j]
                
                # Check if original (given) or user input
                if self.game.original_board[i][j] != 0:
                    row_str += f"{val} "
                elif val != 0:
                    row_str += f"({val}) "
                else:
                    row_str += ". "
            
            row_str += "|"
            print(row_str)
        
        print("  +" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+\n")

    def get_user_input(self):
        """Get and process user input"""
        while True:
            try:
                user_input = input("Masukkan input (contoh: 0 0 5 atau 'hint'): ").strip().lower()
                
                if user_input == 'menu':
                    return 'menu'
                
                if user_input == 'hint':
                    hint = self.game.get_hint()
                    if hint:
                        print(f"\n💡 Hint: Baris {hint['row']}, Kolom {hint['col']} = {hint['value']}")
                    else:
                        print("\n⚠️ Tidak ada sel kosong untuk hint!")
                    return 'continue'
                
                if user_input == 'clear':
                    self.clear_user_inputs()
                    print("\n✓ Semua input telah dihapus")
                    return 'continue'
                
                if user_input == 'check':
                    return 'check'
                
                # Parse row, col, num
                parts = user_input.split()
                if len(parts) != 3:
                    print("❌ Format salah! Gunakan: ROW COL NUM (contoh: 0 0 5)")
                    continue
                
                row, col, num = int(parts[0]), int(parts[1]), int(parts[2])
                
                # Validate input
                if not (0 <= row < 9 and 0 <= col < 9):
                    print("❌ Posisi harus antara 0-8!")
                    continue
                
                if not (1 <= num <= 9):
                    print("❌ Angka harus antara 1-9!")
                    continue
                
                if self.game.original_board[row][col] != 0:
                    print("❌ Sel ini sudah terisi! Anda tidak bisa mengubahnya.")
                    continue
                
                # Check for duplicates
                if not self.game.is_valid(self.game.board, row, col, num):
                    print(f"❌ Angka {num} sudah ada di baris, kolom, atau kotak 3x3!")
                    return 'continue'
                
                self.game.board[row][col] = num
                print("✓ Input diterima")
                return 'continue'
            
            except ValueError:
                print("❌ Input tidak valid! Gunakan angka 0-8 untuk posisi dan 1-9 untuk nilai.")
            except Exception as e:
                print(f"❌ Error: {e}")

    def clear_user_inputs(self):
        """Clear all user inputs"""
        for i in range(9):
            for j in range(9):
                if self.game.original_board[i][j] == 0:
                    self.game.board[i][j] = 0

    def check_solution(self):
        """Check if solution is correct"""
        if not self.game.is_complete():
            print("\n⚠️ Silakan isi semua kotak terlebih dahulu!")
            return False
        
        if self.game.is_solved():
            return True
        else:
            print("\n❌ Ada yang salah! Periksa kembali jawaban Anda.")
            return False

    def play_game(self, difficulty):
        """Main game loop"""
        self.clear_screen()
        
        difficulty_names = {
            '1': 'mudah',
            '2': 'sedang',
            '3': 'sulit'
        }
        
        diff = difficulty_names.get(difficulty, 'mudah')
        self.game.generate_puzzle(diff)
        self.game.start_time = time.time()
        
        while True:
            self.clear_screen()
            self.print_header()
            self.print_board()
            
            print("Perintah: ROW COL NUM | hint | clear | check | menu\n")
            
            action = self.get_user_input()
            
            if action == 'menu':
                return
            
            if action == 'check':
                if self.check_solution():
                    elapsed_time = self.game.get_elapsed_time()
                    self.clear_screen()
                    self.print_header()
                    print("🎉 SELAMAT! ANDA BERHASIL! 🎉\n".center(50))
                    print(f"Waktu: {elapsed_time}".center(50))
                    print(f"Hints yang digunakan: {self.game.hints_used}".center(50))
                    print("\n")
                    
                    while True:
                        choice = input("Mainkan lagi? (y/n): ").strip().lower()
                        if choice in ['y', 'n']:
                            return choice == 'y'
                        print("Pilih y atau n")
                else:
                    input("\nTekan ENTER untuk melanjutkan...")

    def run(self):
        """Run the game"""
        while True:
            self.print_menu()
            choice = input("Pilih menu (1-5): ").strip()
            
            if choice == '1':
                play_again = self.play_game('1')
                if play_again:
                    continue
            
            elif choice == '2':
                play_again = self.play_game('2')
                if play_again:
                    continue
            
            elif choice == '3':
                play_again = self.play_game('3')
                if play_again:
                    continue
            
            elif choice == '4':
                self.print_rules()
            
            elif choice == '5':
                self.clear_screen()
                print("Terima kasih telah bermain Sudoku! 👋\n")
                sys.exit(0)
            
            else:
                print("❌ Pilihan tidak valid!")
                input("Tekan ENTER untuk melanjutkan...")


def main():
    """Entry point"""
    try:
        ui = SudokuUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n\nGame dihentikan oleh pengguna. Terima kasih! 👋\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
