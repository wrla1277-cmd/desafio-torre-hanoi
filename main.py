import tkinter as tk
from tkinter import messagebox

class TorreHanoi:
    def __init__(self, root):
        self.root = root
        self.root.title("Torre de Hanói: O Desafio Clássico")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # --- Cores e Estilos ---
        self.cores_discos = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3", "#A52A2A"]
        self.bg_cor = "#f0f0f0"
        self.root.configure(bg=self.bg_cor)

        # --- Variáveis do Jogo ---
        self.pinos = []
        self.selecionado = None
        self.movimentos = 0
        self.minimo_movimentos = 0  # Meta a ser batida
        
        self.num_discos = 4
        self.num_pinos = 3 # FIXO: Sempre 3 pinos agora

        # --- Interface Gráfica (Layout) ---
        
        # 1. Painel Superior (Placar e Título)
        self.frame_top = tk.Frame(root, bg=self.bg_cor, pady=20)
        self.frame_top.pack(fill="x")
        
        tk.Label(self.frame_top, text="Torre de Hanói - Desafio", font=("Arial", 24, "bold"), bg=self.bg_cor, fg="#333").pack()
        
        # Label de Status (Mostra o Desafio)
        self.lbl_status = tk.Label(
            self.frame_top, 
            text="Movimentos: 0 | Meta: 0", 
            font=("Arial", 16), 
            bg=self.bg_cor, fg="#555"
        )
        self.lbl_status.pack(pady=10)

        # 2. Área do Jogo (Canvas)
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=40, pady=10)
        self.canvas.bind("<Button-1>", self.clique_canvas)

        # 3. Painel Inferior (Controles)
        self.frame_controles = tk.Frame(root, bg="#ddd", pady=20, padx=20)
        self.frame_controles.pack(fill="x", side="bottom")

        # Container para centralizar os botões
        frame_botoes = tk.Frame(self.frame_controles, bg="#ddd")
        frame_botoes.pack()

        # Controle de Discos
        tk.Label(frame_botoes, text="Número de Discos (3-8):", bg="#ddd", font=("Arial", 12)).pack(side="left", padx=(0, 10))
        self.spin_discos = tk.Spinbox(frame_botoes, from_=3, to=8, width=5, font=("Arial", 12), justify="center")
        self.spin_discos.delete(0, "end")
        self.spin_discos.insert(0, 4) # Valor padrão
        self.spin_discos.pack(side="left", padx=(0, 20))

        # Botão Reiniciar
        self.btn_reset = tk.Button(
            frame_botoes, 
            text="🔄 Reiniciar Desafio", 
            command=self.reiniciar_jogo,
            bg="#2196F3", fg="white", font=("Arial", 11, "bold"), padx=20, pady=5, borderwidth=0, cursor="hand2"
        )
        self.btn_reset.pack(side="left")

        # Inicializa o primeiro jogo
        self.reiniciar_jogo()

    def calcular_minimo_teorico(self, n):
        """
        Para 3 pinos, a fórmula é sempre 2^n - 1.
        """
        return (2 ** n) - 1

    def reiniciar_jogo(self):
        try:
            d_val = int(self.spin_discos.get())
            self.num_discos = max(3, min(8, d_val))
        except ValueError:
            pass

        # Reseta estado
        self.movimentos = 0
        self.selecionado = None
        self.num_pinos = 3 # Garante que seja sempre 3
        
        # CALCULA A META
        self.minimo_movimentos = self.calcular_minimo_teorico(self.num_discos)
        
        self.lbl_status.config(text=f"Movimentos: 0  |  🏆 Meta Perfeita: {self.minimo_movimentos}", fg="#555")

        # Configura os pinos: [[discos...], [], []]
        self.pinos = [[] for _ in range(self.num_pinos)]
        self.pinos[0] = list(range(self.num_discos, 0, -1))

        self.desenhar()

    def desenhar(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100: w = 800
        if h < 100: h = 600

        largura_coluna = w / self.num_pinos
        base_y = h - 40
        altura_disco = 30

        for i, pilha in enumerate(self.pinos):
            centro_x = largura_coluna * i + (largura_coluna / 2)
            
            # Estilos
            cor_haste = "#555"
            largura_haste = 10
            
            # Destaque de Seleção
            if self.selecionado == i:
                self.canvas.create_rectangle(
                    centro_x - (largura_coluna/2) + 10, 20, 
                    centro_x + (largura_coluna/2) - 10, base_y + 10, 
                    fill="#e3f2fd", outline="#bbdefb", width=2
                )
                cor_haste = "#FF5722" # Laranja
            
            # Base do pino
            self.canvas.create_line(centro_x - 100, base_y, centro_x + 100, base_y, width=6, fill="#555", capstyle="round")
            # Haste vertical
            self.canvas.create_line(centro_x, 150, centro_x, base_y, width=largura_haste, fill=cor_haste, capstyle="round")

            # Discos
            for j, tamanho_disco in enumerate(pilha):
                largura_max = 200 # Largura fixa máxima para ficar bonito em 3 pinos
                largura_atual = (tamanho_disco / self.num_discos) * (largura_max - 40) + 40
                
                x1 = centro_x - (largura_atual / 2)
                x2 = centro_x + (largura_atual / 2)
                y1 = base_y - (j * altura_disco) - altura_disco
                y2 = base_y - (j * altura_disco)
                
                cor = self.cores_discos[(tamanho_disco - 1) % len(self.cores_discos)]
                
                # Efeito 3D simples (borda)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="#333", width=1)

    def clique_canvas(self, event):
        w = self.canvas.winfo_width()
        largura_coluna = w / self.num_pinos
        pino_clicado = int(event.x // largura_coluna)
        if pino_clicado >= self.num_pinos: return

        if self.selecionado is None:
            if self.pinos[pino_clicado]:
                self.selecionado = pino_clicado
                self.desenhar()
        else:
            origem = self.selecionado
            destino = pino_clicado
            
            if origem == destino:
                self.selecionado = None
                self.desenhar()
            else:
                if self.validar_movimento(origem, destino):
                    disco = self.pinos[origem].pop()
                    self.pinos[destino].append(disco)
                    self.movimentos += 1
                    
                    # Atualiza placar
                    cor_status = "#555"
                    if self.movimentos > self.minimo_movimentos:
                        cor_status = "red"
                        
                    self.lbl_status.config(
                        text=f"Movimentos: {self.movimentos}  |  🏆 Meta Perfeita: {self.minimo_movimentos}",
                        fg=cor_status
                    )
                    
                    self.selecionado = None
                    self.desenhar()
                    self.root.update_idletasks() # Força desenho antes da mensagem
                    self.verificar_vitoria()
                else:
                    self.selecionado = None
                    self.desenhar()

    def validar_movimento(self, origem, destino):
        pilha_origem = self.pinos[origem]
        pilha_destino = self.pinos[destino]
        if not pilha_origem: return False
        if not pilha_destino: return True 
        return pilha_origem[-1] < pilha_destino[-1]

    def verificar_vitoria(self):
        # Ganha se o pino C (índice 2) ou B (índice 1) tiver todos os discos
        for i in range(1, self.num_pinos):
            if len(self.pinos[i]) == self.num_discos:
                self.root.after(200) 
                
                if self.movimentos == self.minimo_movimentos:
                    # Vitória Perfeita
                    messagebox.showinfo(
                        "🎉 PERFEITO! 🎉", 
                        f"Você atingiu a perfeição matemática!\n\n"
                        f"Discos: {self.num_discos}\n"
                        f"Movimentos: {self.movimentos}\n"
                        f"Resultado: Impecável."
                    )
                else:
                    # Vitória Imperfeita
                    diferenca = self.movimentos - self.minimo_movimentos
                    resposta = messagebox.askretrycancel(
                        "👍 Você ganhou, mas...", 
                        f"Que pena! O número mínimo possível era {self.minimo_movimentos}.\n"
                        f"Você fez em {self.movimentos} movimentos ({diferenca} a mais).\n\n"
                        f"Deseja reiniciar para tentar a pontuação perfeita?"
                    )
                    if resposta:
                        self.reiniciar_jogo()
                return

if __name__ == "__main__":
    root = tk.Tk()
    app = TorreHanoi(root)
    root.mainloop()