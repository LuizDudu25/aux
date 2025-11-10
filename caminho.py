import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def construir_adjacencia(arvore):
    adj = {}
    for (u, v, peso) in arvore:
        adj.setdefault(u, []).append((v, peso))
        adj.setdefault(v, []).append((u, peso))
    return adj


def buscarCaminho(v_inicio, v_fim, arvore):
    # Validações
    if not arvore:
        print("Árvore vazia fornecida")
        return None, 0
    
    # Construir adjacência com pesos
    adj = construir_adjacencia(arvore)
    
    # Verificar se os vértices existem
    if v_inicio not in adj:
        print(f"Vértice inicial {v_inicio} não está na árvore")
        return None, 0
    if v_fim not in adj:
        print(f"Vértice final {v_fim} não está na árvore")
        return None, 0
    
    # DFS com backtracking para encontrar o caminho
    visitados = set()
    caminho = []
    distancia_total = [0]  # Lista para poder modificar em função aninhada
    
    def dfs(atual, dist_acumulada):
        """Busca em profundidade recursiva."""
        visitados.add(atual)
        caminho.append(atual)
        
        # Se encontrou o destino
        if atual == v_fim:
            distancia_total[0] = dist_acumulada
            return True
        
        # Explorar vizinhos
        for (viz, peso) in adj.get(atual, []):
            if viz not in visitados:
                if dfs(viz, dist_acumulada + peso):
                    return True
        
        # Backtracking: remover vértice se não levou ao destino
        caminho.pop()
        return False
    
    # Executar busca
    if dfs(v_inicio, 0):
        return caminho, distancia_total[0]
    else:
        return None, 0


def estatisticas_caminho(caminho, distancia):
    if not caminho or len(caminho) < 2:
        return {
            'num_vertices': 0 if not caminho else len(caminho),
            'num_arestas': 0,
            'distancia_total': 0,
            'distancia_media_aresta': 0,
            'distancia_euclidiana_direta': 0,
            'razao_caminho': 0
        }
    
    num_vertices = len(caminho)
    num_arestas = num_vertices - 1
    distancia_media = distancia / num_arestas if num_arestas > 0 else 0
    
    # Distância euclidiana direta
    import math
    dist_direta = math.dist(caminho[0], caminho[-1])
    
    # Razão entre caminho na árvore e linha reta
    razao = distancia / dist_direta if dist_direta > 0 else float('inf')
    
    return {
        'num_vertices': num_vertices,
        'num_arestas': num_arestas,
        'distancia_total': distancia,
        'distancia_media_aresta': distancia_media,
        'distancia_euclidiana_direta': dist_direta,
        'razao_caminho': razao
    }


def plotarCaminho(q_start, q_goal, obstaculos, arvore, caminho, mostrar_arvore=True, destacar_vertices=True):

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_aspect('equal')
    
    # Plotar obstáculos
    for obst in obstaculos:
        ax.add_patch(patches.Polygon(obst, closed=True, 
                                    facecolor='gray', 
                                    edgecolor='black',
                                    alpha=0.7,
                                    linewidth=2))
    
    # Plotar árvore completa (opcional, em segundo plano)
    if mostrar_arvore:
        for (u, v, _) in arvore:
            plt.plot([u[0], v[0]], [u[1], v[1]], 
                    color='lightblue', linewidth=1.5, 
                    alpha=0.4, zorder=1)
    
    # Plotar caminho encontrado (DESTAQUE)
    if caminho and len(caminho) > 1:
        # Segmentos do caminho com cores variadas
        for i in range(len(caminho) - 1):
            u, v = caminho[i], caminho[i + 1]
            
            # Gradiente de cor: verde (início) -> vermelho (fim)
            intensidade = i / (len(caminho) - 2) if len(caminho) > 2 else 0.5
            cor = (0.2 + 0.8 * intensidade, 0.8 - 0.6 * intensidade, 0.2)
            
            plt.plot([u[0], v[0]], [u[1], v[1]], 
                    color=cor, linewidth=4, alpha=0.9, zorder=3,
                    solid_capstyle='round')
        
        # Vértices intermediários do caminho
        if destacar_vertices and len(caminho) > 2:
            vertices_intermediarios = caminho[1:-1]
            xs, ys = zip(*vertices_intermediarios)
            plt.plot(xs, ys, 'o', color='orange', markersize=10, 
                    zorder=4, markeredgecolor='darkorange', 
                    markeredgewidth=2, label='Vértices do caminho')
        
        # Seta indicando direção
        if len(caminho) > 2:
            # Seta no meio do caminho
            meio_idx = len(caminho) // 2
            u, v = caminho[meio_idx], caminho[meio_idx + 1]
            meio_x = (u[0] + v[0]) / 2
            meio_y = (u[1] + v[1]) / 2
            dx = v[0] - u[0]
            dy = v[1] - u[1]
            
            plt.arrow(meio_x - dx * 0.1, meio_y - dy * 0.1, 
                     dx * 0.2, dy * 0.2,
                     head_width=0.3, head_length=0.2, 
                     fc='yellow', ec='orange', zorder=5, linewidth=2)
    
    # Plotar vértices dos obstáculos
    for obst in obstaculos:
        xs, ys = zip(*obst)
        plt.plot(xs, ys, 'ko', markersize=5, zorder=2, alpha=0.5)
    
    # Pontos inicial e final (DESTAQUE MÁXIMO)
    ax.plot(q_start[0], q_start[1], 'go', markersize=18, 
            label='Início (q_start)', zorder=6, 
            markeredgecolor='darkgreen', markeredgewidth=3)
    ax.plot(q_goal[0], q_goal[1], 'ro', markersize=18, 
            label='Objetivo (q_goal)', zorder=6, 
            markeredgecolor='darkred', markeredgewidth=3)
    
    # Linha direta (referência)
    plt.plot([q_start[0], q_goal[0]], [q_start[1], q_goal[1]], 
            'k--', linewidth=1, alpha=0.3, zorder=0, 
            label='Linha direta')
    
    # Calcular e mostrar estatísticas
    if caminho and len(caminho) > 1:
        # Calcular distância do caminho
        distancia_caminho = 0
        for i in range(len(caminho) - 1):
            u, v = caminho[i], caminho[i + 1]
            # Encontrar peso da aresta na árvore
            for (a, b, peso) in arvore:
                if (a == u and b == v) or (a == v and b == u):
                    distancia_caminho += peso
                    break
        
        stats = estatisticas_caminho(caminho, distancia_caminho)
        
        # Caixa de informações
        info_text = (
            f"Vértices: {stats['num_vertices']}\n"
            f"Arestas: {stats['num_arestas']}\n"
            f"Dist. Caminho: {stats['distancia_total']:.2f}\n"
            f"Dist. Direta: {stats['distancia_euclidiana_direta']:.2f}\n"
            f"Razão: {stats['razao_caminho']:.2f}x"
        )
        
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightyellow', 
                         alpha=0.9, edgecolor='orange', linewidth=2),
                family='monospace')
    
    plt.legend(loc='upper right', fontsize=11, framealpha=0.95)
    plt.title("Caminho Encontrado na Árvore de Visibilidade", 
             fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("X", fontsize=11)
    plt.ylabel("Y", fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()