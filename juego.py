import curses
import actores

from mapa import Mapa
import sys

class Juego(object):
    def __init__(self, nombre_mapa):
        """Carga el mapa del juego a partir del archivo mapas/<nombre_mapa>.map."""
        with open("mapas/{}.map".format(nombre_mapa)) as f:
            filas = [ linea.strip() for linea in f ]
        mapa, heroe = self.crear_mapa(filas)
        self.mapa = mapa
        self.heroe = heroe
        self.juego_terminado = False
        # El historial de mensajes es simplemente una lista de strings.
        self.mensajes = []

    def crear_mapa(self, filas):
        """Crea el Mapa a partir de la definicion provista por parametro (`filas`),
        y devuelve una tupla con el mapa y el actor que representa al heroe del juego.
        Si hay mas de un heroe en la definicion del mapa, o bien si no hay ningun
        heroe, la funcion lanza una excepcion.
        `filas` es una lista de strings, que corresponde con el contenido completo
        del archivo .map."""
        ####
        #### Modificar este codigo para que cargue el mapa dinamicamente
        #### a partir de `filas`
        ####
        ancho = len(filas[0])
        alto = len(filas)
        mapa = Mapa(ancho, alto)
        actores_dic = {".":"None","@":"Heroe","#":"Pared","g":"Goblin","o":"Orco","<":"Salida"}
        x = 0
        y = 0
        for fila in filas:
            x+= 1
            y = 0
            
            for caracter in fila:
                y+=1
                if caracter in actores_dic:
                    if actores_dic[caracter] == "None":
                        a = raw_input("Hasta aca todo bien, se agrego vacio")
                        celda_vacia = actores.Vacio()
                        mapa.agregar_actor(celda_vacia,x,y)
                    if actores_dic[caracter] == "Heroe":
                        a = raw_input("Hasta aca todo bien, se agrego heroe")
                        heroe = actores.Heroe()
                        mapa.agregar_actor(heroe,x,y)
                        
                    if actores_dic[caracter] == "Pared":
                        a = raw_input("Hasta aca todo bien, se agrego pared")
                        pared = actores.Pared()
                        mapa.agregar_actor(pared,x,y)
                    if actores_dic[caracter] == "Goblin":
                        a = raw_input("Hasta aca todo bien, se agrego goblin")
                        goblin = actores.Goblin()
                        
                        mapa.agregar_actor(goblin,x,y)
                    if actores_dic[caracter] == "Orco":
                        orco = actores.Orco()
                        a = raw_input("Hasta aca todo bien, se agrego orc")
                        mapa.agregar_actor(orco,x,y)
                    if actores_dic[caracter] == "Salida":
                        a = raw_input("Hasta aca todo bien, se agrego salida")
                        salida = actores.Salida()
                        mapa.agregar_actor(salida,x,y)
                
        
        
        return mapa, heroe

    def turno(self, evento):
        """Llama al metodo jugar_turno() del heroe. Si el heroe hizo algo,
        llama al metodo jugar_turno() para el resto de los actores"""
        if self.juego_terminado:
            return

        if not self.heroe.jugar_turno_heroe(evento, self):
            # El heroe no hizo nada
            return

        # El resto de los actores juegan su turno
        for actor in self.mapa.actores:
            if not actor.es_heroe():
                actor.jugar_turno(self)

        self.mapa.eliminar_actores_muertos()

    def terminar(self):
        """Marcar que el juego ha terminado."""
        self.juego_terminado = True

    def msg(self, *args):
        """Agregar un mensaje al historial."""
        self.mensajes.append(" ".join(args))

    def dibujar_mensajes(self, ventana, cantidad):
        """Dibujar los ultimos `cantidad` mensajes del historial en la ventana provista."""
        for y, mensaje in enumerate(self.mensajes[-cantidad:]):
            ventana.addstr(y, 0, mensaje)

    def main(self):
        """Bucle principal del juego."""
        try:
            pantalla = curses.initscr()

            # No imprimir la entrada del teclado:
            curses.noecho()

            # Cursor invisible:
            curses.curs_set(0)

            # Habilitar las flechas para moverse
            pantalla.keypad(1)

            self.msg("Has ingresado en el calabozo! Podras escapar?")
            self.msg("Flechas para moverse, Q para salir")
            while True:
                pantalla.clear()
                self.mapa.dibujar(pantalla.derwin(0, 0))
                self.dibujar_mensajes(pantalla.derwin(0, self.mapa.ancho() + 2), self.mapa.alto())

                evento = pantalla.getch()
                if evento == ord("q"):
                    break
                self.turno(evento)
        finally:
            # devolver el estado de la consola (por ejemplo la visibilidad del cursor)
            curses.endwin()


# Mapa por defecto:
nombre_mapa = 'nivel1'
if len(sys.argv) > 1:
    nombre_mapa = sys.argv[1]

Juego(nombre_mapa).main()
