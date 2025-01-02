import tkinter as tk
import heapq
import networkx as nx

class Ambiente:
    def __init__(self, grade):
        self.grade = grade
        self.linhas = len(grade)
        self.colunas = len(grade[0])
        self.grafo = self.criar_grafo()

    def criar_grafo(self):
        grafo = nx.Graph()
        movimentos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if self.grade[linha][coluna] == 0:
                    for dx, dy in movimentos:
                        vizinho = (linha + dx, coluna + dy)
                        if 0 <= vizinho[0] < self.linhas and 0 <= vizinho[1] < self.colunas:
                            if self.grade[vizinho[0]][vizinho[1]] == 0:
                                grafo.add_edge((linha, coluna), vizinho)
        return grafo

class Agente:
    def __init__(self, ambiente, inicio, objetivo):
        self.ambiente = ambiente
        self.inicio = inicio
        self.objetivo = objetivo
        self.custos = {}

    def busca_a_estrela(self):
        def heuristica(posicao, objetivo):
            return abs(posicao[0] - objetivo[0]) + abs(posicao[1] - objetivo[1])

        conjunto_aberto = []
        heapq.heappush(conjunto_aberto, (0, self.inicio))
        veio_de = {}
        g_custo = {self.inicio: 0}

        while conjunto_aberto:
            _, atual = heapq.heappop(conjunto_aberto)

            if atual == self.objetivo:
                caminho = []
                while atual in veio_de:
                    caminho.append(atual)
                    atual = veio_de[atual]
                caminho.reverse()
                return caminho

            for vizinho in self.ambiente.grafo.neighbors(atual):
                g_custo_tentativo = g_custo[atual] + 1
                if g_custo_tentativo < g_custo.get(vizinho, float('inf')):
                    veio_de[vizinho] = atual
                    g_custo[vizinho] = g_custo_tentativo
                    f_custo = g_custo_tentativo + heuristica(vizinho, self.objetivo)
                    heapq.heappush(conjunto_aberto, (f_custo, vizinho))
                    self.custos[vizinho] = g_custo_tentativo

        return None

class JogoLabirinto:
    def __init__(self, raiz, ambiente, agente):
        self.raiz = raiz
        self.ambiente = ambiente
        self.agente = agente
        self.linhas = ambiente.linhas
        self.colunas = ambiente.colunas
        self.tamanho_celula = 30

        self.canvas = tk.Canvas(raiz, width=self.colunas * self.tamanho_celula, height=self.linhas * self.tamanho_celula)
        self.canvas.pack()

        self.desenhar_grade()

        self.botao_iniciar = tk.Button(raiz, text="Iniciar", command=self.executar_a_estrela)
        self.botao_iniciar.pack(side=tk.LEFT)

        self.botao_reiniciar = tk.Button(raiz, text="Reiniciar", command=self.reiniciar_labirinto)
        self.botao_reiniciar.pack(side=tk.RIGHT)

    def desenhar_grade(self):
        self.canvas.delete("all")
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                cor = "white" if self.ambiente.grade[linha][coluna] == 0 else "black"
                if (linha, coluna) == self.agente.inicio:
                    cor = "green"
                elif (linha, coluna) == self.agente.objetivo:
                    cor = "red"
                self.canvas.create_rectangle(
                    coluna * self.tamanho_celula, linha * self.tamanho_celula,
                    (coluna + 1) * self.tamanho_celula, (linha + 1) * self.tamanho_celula,
                    fill=cor, outline="gray"
                )

    def executar_a_estrela(self):
        caminho = self.agente.busca_a_estrela()
        if caminho:
            self.animar_caminho(caminho)
            self.exibir_custos()
        else:
            print("Nenhum caminho encontrado.")

    def animar_caminho(self, caminho):
        for posicao in caminho:
            linha, coluna = posicao
            self.canvas.create_rectangle(
                coluna * self.tamanho_celula, linha * self.tamanho_celula,
                (coluna + 1) * self.tamanho_celula, (linha + 1) * self.tamanho_celula,
                fill="blue", outline="gray"
            )
            self.raiz.update()
            self.raiz.after(100)

    def exibir_custos(self):
        for posicao, custo in self.agente.custos.items():
            linha, coluna = posicao
            x_centro = coluna * self.tamanho_celula + self.tamanho_celula // 2
            y_centro = linha * self.tamanho_celula + self.tamanho_celula // 2
            self.canvas.create_text(x_centro, y_centro, text=str(custo), fill="black")

    def reiniciar_labirinto(self):
        self.agente.custos = {}
        self.desenhar_grade()

if __name__ == "__main__":
    grade = [
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    ]
    inicio = (0, 0)
    objetivo = (9, 9)

    ambiente = Ambiente(grade)
    agente = Agente(ambiente, inicio, objetivo)

    raiz = tk.Tk()
    raiz.title("Jogo do Labirinto")
    jogo = JogoLabirinto(raiz, ambiente, agente)
    raiz.mainloop()