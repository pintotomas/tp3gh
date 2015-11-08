dic_funciones = {"#":mapa.agregar_actor,
                 "o":mapa.agregar_actor,
                 "g":mapa.agregar_actor,
                 "<":mapa.agregar_actor
                 }

for caracter in fila:
    if caracter == "#":
        dic_funciones[caracter](actores.Pared(),x,y)
    if caracter == "o":
        dic_funciones[caracter](actores.Orco(),x,y)
    if caracter == "g":
        dic_funciones[caracter](actores.Goblin(),x,y)
    if caracter == "<":
        dic_funciones[caracter](actores.Salida(),x,y)
