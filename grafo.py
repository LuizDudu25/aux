import math
import itertools
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

from geometria import linha_livre

try:
    from shapely.geometry import LineString, Polygon, Point
    HAS_SHAPELY = True
except Exception:
    HAS_SHAPELY = False

def _linha_livre_shapely(p1, p2, obstaculos):
    line = LineString([p1, p2])
    for obst in obstaculos:
        poly = Polygon(obst)
        # Se a linha intersecta o polígono e não apenas toca a borda -> não livre
        if poly.is_empty:
            continue
        if line.intersects(poly):
            # Se a linha toca apenas a borda/contorno (touches), considerar livre
            if line.touches(poly):
                continue
            return False
    return True

def grafo_visibilidade(q_start, q_goal, obstaculos, max_distancia=None, debug=False):
    # Coletar todos os vértices
    vertices = [q_start, q_goal]
    for obst in obstaculos:
        vertices.extend(obst)
    
    # Inicializar o grafo
    G = {v: [] for v in vertices}
    
    # Testar visibilidade entre todos os pares de vértices
    total_pares = 0
    conexoes = 0
    
    for v1, v2 in itertools.combinations(vertices, 2):
        total_pares += 1
        distancia = math.dist(v1, v2)
        
        # Otimização: ignorar conexões muito distantes (se especificado)
        if max_distancia and distancia > max_distancia:
            continue
        
        # Verificar se a linha entre v1 e v2 está livre
        livre = False
        if HAS_SHAPELY:
            try:
                livre = _linha_livre_shapely(v1, v2, obstaculos)
            except Exception as e:
                # Em caso de erro com shapely, cair para o fallback
                if debug:
                    print("shapely check failed:", e)
                livre = linha_livre(v1, v2, obstaculos)
        else:
            livre = linha_livre(v1, v2, obstaculos)
        
        if livre:
            G[v1].append((v2, distancia))
            G[v2].append((v1, distancia))
            conexoes += 1
        else:
            if debug:
                # Log leve para entender porque nenhuma aresta existe
                print(f"bloqueado: {v1} <-> {v2} (dist={distancia:.2f})")
    
    if debug:
        print(f"Grafo criado: {len(vertices)} vértices, {conexoes} arestas")
        print(f"Testados {total_pares} pares de vértices")
        # graus
        graus = {v: len(adj) for v, adj in G.items()}
        degs = sorted(graus.items(), key=lambda x: -x[1])
        print("Top graus (vértice: grau):", degs[:6])
    
    return G

def plotar_grafo(grafo, obstaculos, q_start=None, q_goal=None):
    """
    Plota o grafo de visibilidade com obstáculos e pontos especiais.
    Linhas mais grossas, cores distintas e legenda fora da área principal.
    """

    fig, ax = plt.subplots(figsize=(8, 8))

    # Obstáculos
    for obst in obstaculos:
        pol = Polygon(obst)
        x, y = pol.exterior.xy
        ax.fill(x, y, color="lightgray", alpha=0.8, zorder=1)
        ax.plot(x, y, color="black", linewidth=2.0, zorder=5, label="_contorno")

    # Arestas
    for v in grafo:
        for viz, _ in grafo[v]:
            # garante que v e viz sejam iteráveis com 2 valores (x, y)
            if isinstance(v, (tuple, list)) and isinstance(viz, (tuple, list)) and len(v) == 2 and len(viz) == 2:
                ax.plot(
                    [v[0], viz[0]], [v[1], viz[1]],
                    color='steelblue', linewidth=1.8, alpha=0.7, zorder=1
                )

    # Vértices
    try:
        xs, ys = zip(*[v for v in grafo.keys() if isinstance(v, (tuple, list)) and len(v) == 2])
        ax.scatter(xs, ys, s=20, color='navy', label='Vértices do grafo', zorder=2)
    except ValueError:
        # Grafo pode estar vazio — apenas ignora
        pass

    # Ponto inicial e final
    if q_start and isinstance(q_start, (tuple, list)) and len(q_start) == 2:
        ax.scatter(*q_start, s=80, color='green', marker='o', edgecolors='black',
                   label='Ponto inicial (q_start)', zorder=3)
    if q_goal and isinstance(q_goal, (tuple, list)) and len(q_goal) == 2:
        ax.scatter(*q_goal, s=80, color='red', marker='X', edgecolors='black',
                   label='Ponto final (q_goal)', zorder=3)

    # Aparência geral
    ax.set_title("Grafo de Visibilidade", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, linestyle="--", alpha=0.3)

    # Legenda
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])  # espaço para legenda
    ax.legend(
        loc='center left',
        bbox_to_anchor=(1.02, 0.5),
        frameon=True,
        shadow=True
    )

    # Aspecto e exibição
    ax.set_aspect('equal', 'box')
    plt.tight_layout()
    plt.show()

