import heapq
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon

def prim(grafo, inicio):
    visitado = set()
    mst = []
    pq = []  # fila de prioridade (peso, origem, destino)
    total_peso = 0.0

    def adicionar_arestas(v):
        visitado.add(v)
        for (viz, peso) in grafo.get(v, []):
            if viz not in visitado:
                heapq.heappush(pq, (peso, v, viz))

    # Iniciar do vértice fornecido
    adicionar_arestas(inicio)

    # Construir a MST
    while pq:
        peso, u, v = heapq.heappop(pq)
        if v not in visitado:
            mst.append((u, v, peso))
            total_peso += peso
            adicionar_arestas(v)

    return mst, total_peso, visitado


def validar_mst(grafo, mst, vertices_alcancados):
    total_vertices = len(grafo)
    vertices_na_mst = len(vertices_alcancados)
    arestas_esperadas = vertices_na_mst - 1 if vertices_na_mst > 0 else 0
    
    resultado = {
        'valida': len(mst) == arestas_esperadas and vertices_na_mst > 0,
        'total_vertices': total_vertices,
        'vertices_alcancados': vertices_na_mst,
        'arestas_na_mst': len(mst),
        'arestas_esperadas': arestas_esperadas,
        'grafo_conexo': vertices_na_mst == total_vertices,
        'componentes_desconexos': total_vertices - vertices_na_mst
    }
    
    return resultado


def estatisticas_mst(mst):
    if not mst:
        return {
            'peso_total': 0,
            'peso_medio': 0,
            'peso_min': 0,
            'peso_max': 0,
            'num_arestas': 0
        }
    
    pesos = [peso for (_, _, peso) in mst]
    
    return {
        'peso_total': sum(pesos),
        'peso_medio': sum(pesos) / len(pesos),
        'peso_min': min(pesos),
        'peso_max': max(pesos),
        'num_arestas': len(mst)
    }

def extrair_vertices_arvore(arvore):
    vertices = set()
    for (u, v, _) in arvore:
        vertices.add(u)
        vertices.add(v)
    return vertices

import math

def verticeMaisProximo(ponto, arvore):
    # validar ponto
    if not (isinstance(ponto, (tuple, list)) and len(ponto) == 2):
        raise ValueError("Ponto deve ser tupla/lista de 2 floats")

    # extrair vértices
    if isinstance(arvore, dict):
        vertices = list(arvore.keys())
    else:
        vertices = set()
        for u, v, _ in arvore:
            vertices.add(u)
            vertices.add(v)
        vertices = list(vertices)

    if len(vertices) == 0:
        raise ValueError("Árvore está vazia — nenhum vértice para examinar")

    # calcular mais próximo
    menor_dist = float('inf')
    mais_prox = None
    for v in vertices:
        d = math.dist(ponto, v)
        if d < menor_dist:
            menor_dist = d
            mais_prox = v

    return mais_prox

def plotar_mst(arestas, obstaculos, q_start=None, q_goal=None):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Obstáculos
    for obst in obstaculos:
        pol = Polygon(obst)
        x, y = pol.exterior.xy
        ax.fill(x, y, color="gainsboro", alpha=0.6, zorder=1)
        ax.plot(x, y, color="gray", linewidth=1.0, alpha=0.7, zorder=2, label="_contorno")

    # Arestas da MST
    for u, v, _ in arestas:
        if isinstance(u, (tuple, list)) and isinstance(v, (tuple, list)) and len(u) == 2 and len(v) == 2:
            ax.plot(
                [u[0], v[0]], [u[1], v[1]],
                color='forestgreen', linewidth=2.5, alpha=0.9, zorder=4
            )

    # Vértices
    vertices = set()
    for u, v, _ in arestas:
        vertices.add(u)
        vertices.add(v)

    if vertices:
        xs, ys = zip(*vertices)
        ax.scatter(xs, ys, s=25, color='darkgreen', label='Vértices da MST', zorder=3)

    # Ponto inicial e final
    if q_start:
        ax.scatter(*q_start, s=100, color='green', marker='o', edgecolors='black',
                   label='Ponto inicial (q_start)', zorder=6)
    if q_goal:
        ax.scatter(*q_goal, s=100, color='red', marker='X', edgecolors='black',
                   label='Ponto final (q_goal)', zorder=6)

    # Aparência geral
    ax.set_title("Árvore Geradora Mínima (MST)", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, linestyle="--", alpha=0.3)

    # Legenda fora do gráfico
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(
        loc='center left',
        bbox_to_anchor=(1.02, 0.5),
        frameon=True,
        shadow=True
    )

    # Ajustes finais
    ax.set_aspect('equal', 'box')
    plt.tight_layout()
    plt.show()
