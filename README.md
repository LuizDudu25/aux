---

### 3. Geração da Árvore Geradora Mínima (`arvore.py`)

Com o grafo de visibilidade construído, o próximo passo é reduzi-lo a uma estrutura mínima de conexões.  
Isso é feito aplicando um algoritmo de Árvore Geradora Mínima (MST), que conecta todos os vértices do grafo com o menor custo total possível.

Essa árvore representa a estrutura mínima de navegação do robô, preservando a conectividade entre os vértices relevantes sem criar ciclos desnecessários.

---

### Lógica geral

O algoritmo percorre o grafo escolhendo arestas de menor peso que não formam ciclos, até conectar todos os vértices.

---

### Implementação

O projeto implementa o algoritmo de Prim, por ser eficiente e fácil de adaptar para grafos representados por dicionários de adjacência.

```python
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
```

### Visualização
A função `plotar_mst()` (em `plots.py`) exibe a árvore gerada, destacando as arestas que conectam os vértices escolhidos pelo algoritmo.
Com o exemplo de mapa de `mapa.txt` temos a seguinte visualização:

<p align="center">
  <img src="imagens/Grafo_MST.png" alt="Grafo de Visibilidade" width="600"/>
</p>

Essa visualização ajuda a confirmar que a árvore cobre todas as regiões navegáveis do mapa, conectando os vértices visíveis sem redundância.
