from shapely.geometry import Point, Polygon, LineString

def ponto_dentro_poligono(p, poligono):
    return Polygon(poligono).covers(Point(p))

def intersecao(p1, q1, p2, q2):
    return LineString([p1, q1]).intersects(LineString([p2, q2]))

def linha_livre(p1, p2, obstaculos):
    linha = LineString([p1, p2])
    for obst in obstaculos:
        poligono = Polygon(obst)
        if poligono.is_empty:
            continue
        if linha.intersects(poligono) and not linha.touches(poligono):
            return False
    return True
