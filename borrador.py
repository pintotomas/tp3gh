#faltaria una manera de ver la dimension del mapa para Mapa(x,y), una seria recorrer el archivo del mapa 2 veces.
#Para la dimension, le pregunte la longitud de filas(que vendria a ser el largo) y de filas[0](que vendria a ser el ancho)
#Esto de la dimension ya lo pongo en el codigo original porque creo que es la mejor manera de obtener la dimension
#Para hacer que quede mejor la asignacion 
mapa = Mapa(x,y)
x = 0
y = 0
representacion_actores = {"@":"Heroe"
with open(nombre_mapa) as m:
	for linea in m:
		x = 0
		y += 1
		for caracter in linea:
			x += 1
			if caracter == actores.Pared.dibujo:
				pared = actores.Pared
				mapa.agregar_actor(pared, x, y)
			elif caracter == actores.Goblin.dibujo:
				goblin = actores.Goblin
				mapa.agregar_actor(goblin, x, y)
			elif caracter == actores.Orco.dibujo:
				orco = actores.Orco
				mapa.agregar_actor(orco, x, y)
			...
			#debe de haber otra manera mas optimizada para ver que clase le corresponde al caracter
