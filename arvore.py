import heapq
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

def verticeMaisProximo(ponto, arvore, retornar_distancia=False):
    # Validações
    if not arvore:
        print("Árvore vazia fornecida")
        return None if not retornar_distancia else (None, float('inf'))
    
    if ponto is None or len(ponto) != 2:
        print("Ponto inválido fornecido")
        return None if not retornar_distancia else (None, float('inf'))
    
    # Extrair todos os vértices únicos da árvore
    vertices = extrair_vertices_arvore(arvore)
    
    if not vertices:
        print("Nenhum vértice encontrado na árvore")
        return None if not retornar_distancia else (None, float('inf'))
    
    # Encontrar o vértice mais próximo usando distância euclidiana
    mais_proximo = None
    menor_distancia = float('inf')
    
    for vertice in vertices:
        distancia = math.dist(ponto, vertice)
        if distancia < menor_distancia:
            menor_distancia = distancia
            mais_proximo = vertice
    
    if retornar_distancia:
        return mais_proximo, menor_distancia
    return mais_proximo

def plotar_mst(q_start, q_goal, obstaculos, mst, mostrar_pesos=False):
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_aspect('equal')

    # Plotar obstáculos
    for obst in obstaculos:
        ax.add_patch(patches.Polygon(obst, closed=True, 
                                    facecolor='gray', 
                                    edgecolor='black',
                                    alpha=0.7,
                                    linewidth=2))

    # Plotar arestas da MST com gradiente de cores
    if mst:
        pesos = [peso for (_, _, peso) in mst]
        peso_min, peso_max = min(pesos), max(pesos)
        
        for (u, v, peso) in mst:
            # Gradiente: azul (leve) -> vermelho (pesado)
            if peso_max > peso_min:
                intensidade = (peso - peso_min) / (peso_max - peso_min)
            else:
                intensidade = 0.5
            
            # RGB: azul escuro -> roxo -> vermelho
            cor = (0.8 * intensidade, 0.2, 1 - 0.8 * intensidade)
            
            plt.plot([u[0], v[0]], [u[1], v[1]], 
                    color=cor, linewidth=2.5, alpha=0.9, zorder=2)
            
            # Opcional: mostrar peso da aresta
            if mostrar_pesos:
                meio_x = (u[0] + v[0]) / 2
                meio_y = (u[1] + v[1]) / 2
                ax.text(meio_x, meio_y, f'{peso:.1f}', 
                       fontsize=7, ha='center', 
                       bbox=dict(boxstyle='round,pad=0.3', 
                                facecolor='white', alpha=0.7))

    # Plotar vértices dos obstáculos
    for obst in obstaculos:
        xs, ys = zip(*obst)
        plt.plot(xs, ys, 'ko', markersize=6, zorder=3, alpha=0.6)

    # Plotar pontos inicial e final (destaque)
    ax.plot(q_start[0], q_start[1], 'go', markersize=16, 
            label='Início (q_start)', zorder=5, 
            markeredgecolor='darkgreen', markeredgewidth=2.5)
    ax.plot(q_goal[0], q_goal[1], 'ro', markersize=16, 
            label='Objetivo (q_goal)', zorder=5, 
            markeredgecolor='darkred', markeredgewidth=2.5)

    # Informações da MST
    stats = estatisticas_mst(mst)
    info_text = f"Arestas: {stats['num_arestas']} | Peso Total: {stats['peso_total']:.2f}"
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.legend(loc='upper right', fontsize=11, framealpha=0.9)
    plt.title("Árvore Geradora Mínima (MST) - Algoritmo de Prim", 
             fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("X", fontsize=11)
    plt.ylabel("Y", fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()

def plotar_vertice_mais_proximo(q_start, q_goal, obstaculos, mst, ponto, vertice=None):
    # Calcular vértice mais próximo se não fornecido
    if vertice is None:
        vertice, distancia = verticeMaisProximo(ponto, mst, retornar_distancia=True)
        if vertice is None:
            print("Não foi possível encontrar vértice mais próximo")
            return
    else:
        distancia = math.dist(ponto, vertice)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_aspect('equal')
    
    # Plotar obstáculos
    for obst in obstaculos:
        ax.add_patch(patches.Polygon(obst, closed=True, 
                                    facecolor='gray', 
                                    edgecolor='black',
                                    alpha=0.7,
                                    linewidth=2))
    
    # Plotar arestas da árvore
    for (u, v, _) in mst:
        plt.plot([u[0], v[0]], [u[1], v[1]], 
                color='lightblue', linewidth=2, alpha=0.6, zorder=2)
    
    # Plotar todos os vértices da árvore
    vertices = extrair_vertices_arvore(mst)
    for v in vertices:
        plt.plot(v[0], v[1], 'o', color='lightgray', 
                markersize=6, zorder=3, alpha=0.5)
    
    # Linha de conexão entre ponto e vértice mais próximo
    plt.plot([ponto[0], vertice[0]], [ponto[1], vertice[1]], 
            'y--', linewidth=2.5, alpha=0.8, zorder=4, 
            label=f'Distância: {distancia:.2f}')
    
    # Pontos principais
    ax.plot(q_start[0], q_start[1], 'go', markersize=14, 
            label='Início (q_start)', zorder=5,
            markeredgecolor='darkgreen', markeredgewidth=2)
    ax.plot(q_goal[0], q_goal[1], 'ro', markersize=14, 
            label='Objetivo (q_goal)', zorder=5,
            markeredgecolor='darkred', markeredgewidth=2)
    
    # Ponto de consulta e vértice mais próximo (DESTAQUE)
    ax.plot(ponto[0], ponto[1], 'o', color='gold', markersize=16, 
            label='Ponto de consulta', zorder=6,
            markeredgecolor='orange', markeredgewidth=3)
    ax.plot(vertice[0], vertice[1], 'o', color='magenta', markersize=16, 
            label='Vértice mais próximo', zorder=6,
            markeredgecolor='purple', markeredgewidth=3)
    
    # Anotações com as coordenadas
    offset_ponto = 0.5
    offset_vertice = 0.5
    ax.annotate(f'P: {ponto}', xy=ponto, 
               xytext=(ponto[0] + offset_ponto, ponto[1] + offset_ponto),
               fontsize=9, bbox=dict(boxstyle='round,pad=0.5', 
                                    facecolor='yellow', alpha=0.7),
               arrowprops=dict(arrowstyle='->', color='orange', lw=1.5))
    ax.annotate(f'V: {vertice}', xy=vertice, 
               xytext=(vertice[0] + offset_vertice, vertice[1] - offset_vertice),
               fontsize=9, bbox=dict(boxstyle='round,pad=0.5', 
                                    facecolor='magenta', alpha=0.7),
               arrowprops=dict(arrowstyle='->', color='purple', lw=1.5))
    
    plt.legend(loc='best', fontsize=10, framealpha=0.95)
    plt.title("Busca do Vértice Mais Próximo na Árvore", 
             fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("X", fontsize=11)
    plt.ylabel("Y", fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()