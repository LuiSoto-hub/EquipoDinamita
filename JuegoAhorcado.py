import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Ahorcado")
        self.root.geometry("600x400")
        
        # Lista de palabras
        self.words = ["python", "programacion", "computadora", "desarrollo", 
                     "tecnologia", "videojuego", "aplicacion", "software"]
        
        # Estados del juego
        self.word = ""
        self.hidden_word = []
        self.tries = 6
        self.used_letters = []
        
        # Componentes gráficos
        self.canvas = tk.Canvas(root, width=200, height=250)
        self.canvas.pack(side=tk.LEFT, padx=20)
        
        # Frame para los controles del juego
        self.game_frame = tk.Frame(root)
        self.game_frame.pack(side=tk.LEFT, padx=20)
        
        # Etiquetas y entrada
        self.word_label = tk.Label(self.game_frame, text="", font=('Arial', 24))
        self.word_label.pack(pady=20)
        
        self.tries_label = tk.Label(self.game_frame, text="Intentos restantes: 6", font=('Arial', 12))
        self.tries_label.pack()
        
        self.used_letters_label = tk.Label(self.game_frame, text="Letras usadas: ", font=('Arial', 12))
        self.used_letters_label.pack(pady=10)
        
        self.entry = tk.Entry(self.game_frame, font=('Arial', 18), width=5)
        self.entry.pack(pady=10)
        
        self.submit_button = tk.Button(self.game_frame, text="Adivinar", command=self.guess_letter)
        self.submit_button.pack(pady=5)
        
        self.new_game_button = tk.Button(self.game_frame, text="Nuevo Juego", command=self.start_new_game)
        self.new_game_button.pack(pady=10)
        
        # Iniciar juego
        self.start_new_game()
        
        # Bind de tecla Enter
        self.entry.bind('<Return>', lambda event: self.guess_letter())
        
    def draw_hangman(self):
        self.canvas.delete("all")
        # Base
        self.canvas.create_line(40, 220, 160, 220, width=3)
        # Poste vertical
        self.canvas.create_line(100, 220, 100, 40, width=3)
        # Poste horizontal
        self.canvas.create_line(100, 40, 140, 40, width=3)
        # Cuerda
        self.canvas.create_line(140, 40, 140, 60, width=3)
        
        if self.tries < 6:  # Cabeza
            self.canvas.create_oval(130, 60, 150, 80, width=3)
            
        if self.tries < 5:  # Cuerpo
            self.canvas.create_line(140, 80, 140, 120, width=3)
            
        if self.tries < 4:  # Brazo izquierdo
            self.canvas.create_line(140, 90, 120, 100, width=3)
            
        if self.tries < 3:  # Brazo derecho
            self.canvas.create_line(140, 90, 160, 100, width=3)
            
        if self.tries < 2:  # Pierna izquierda
            self.canvas.create_line(140, 120, 120, 140, width=3)
            
        if self.tries < 1:  # Pierna derecha
            self.canvas.create_line(140, 120, 160, 140, width=3)

    def start_new_game(self):
        self.word = random.choice(self.words).upper()
        self.hidden_word = ['_' for _ in self.word]
        self.tries = 6
        self.used_letters = []
        self.update_display()
        self.draw_hangman()
        self.entry.focus()

    def update_display(self):
        self.word_label.config(text=' '.join(self.hidden_word))
        self.tries_label.config(text=f"Intentos restantes: {self.tries}")
        self.used_letters_label.config(text=f"Letras usadas: {' '.join(sorted(self.used_letters))}")

    def guess_letter(self):
        letter = self.entry.get().upper()
        self.entry.delete(0, tk.END)
        
        if not letter or len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("Error", "Por favor ingresa una letra válida")
            return
            
        if letter in self.used_letters:
            messagebox.showinfo("Aviso", "Ya usaste esa letra")
            return
            
        self.used_letters.append(letter)
        
        if letter in self.word:
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.hidden_word[i] = letter
        else:
            self.tries -= 1
            self.draw_hangman()
            
        self.update_display()
        
        if '_' not in self.hidden_word:
            messagebox.showinfo("¡Felicitaciones!", "¡Ganaste! La palabra era " + self.word)
            self.start_new_game()
        elif self.tries == 0:
            messagebox.showinfo("Game Over", "¡Perdiste! La palabra era " + self.word)
            self.start_new_game()

# Crear y ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()