# -*- coding: cp1252 -*-
import curses
import actores
import errores
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
        
    def agregar_goblin(self,mapa,x,y):
        "Agrega un goblin al mapa"
        goblin = actores.Goblin()
        mapa.agregar_actor(goblin,x,y)
        
    def agregar_orco(self,mapa,x,y):
        "Agrega un orco al mapa"
        orco = actores.Orco()
        mapa.agregar_actor(orco,x,y)
        
    def agregar_pared(self,mapa,x,y):
        "Agrega una pared al mapa"
        pared = actores.Pared()
        mapa.agregar_actor(pared,x,y)
        
    def agregar_salida(self,mapa,x,y):
        "Agrega una salida al mapa"
        salida = actores.Salida()
        mapa.agregar_actor(salida,x,y)

    
        
    def crear_mapa(self, filas):
        """Crea el Mapa a partir de la definicion provista por parametro (`filas`),
        y devuelve una tupla con el mapa y el actor que representa al heroe del juego.
        Si hay mas de un heroe en la definicion del mapa, o bien si no hay ningun
        heroe, la funcion lanza una excepcion. Se presupone que en el mapa se
        proporciona una salida para poder finalizar el juego.
        `filas` es una lista de strings, que corresponde con el contenido completo
        del archivo .map."""
        dic_funciones = {"#":Juego.agregar_pared,
                         "o":Juego.agregar_orco,
                         "g":Juego.agregar_goblin,
                         "<":Juego.agregar_salida
                         }
        ALTO = len(filas)
        ANCHO = len(filas[0])
        if ANCHO == 0: raise IndexError
        mapa = Mapa(ANCHO,ALTO)
        x = 0
        y = -1
        heroe = None
        cantidad_heroes = 0
        for fila in filas:
            if len(fila) != ANCHO: raise errores.MapaIncorrectoError\
           ("la linea",fila,\
           "no contiene la misma cantidad de caracteres que la primer linea del archivo")
            x = 0
            y+= 1
            for caracter in fila:
                if caracter == "@":
                    # Lo necesitamos ya que, debemos definir heroe para poder devolverlo
                    heroe = actores.Heroe()
                    mapa.agregar_actor(heroe,x,y)
                    cantidad_heroes+=1
                    if cantidad_heroes > 1:
                        raise errores.DemasiadosHeroesError("Se esta añadiendo",cantidad_heroes-1,"heroes de mas")
                elif caracter in dic_funciones:
                    dic_funciones[caracter](self,mapa,x,y)
                elif caracter != ".":
                   raise errores.PersonajeInexistenteError\
                   ("El caracter",caracter,"no hace referencia a ningun personaje en el juego")
            	x+=1
            
        if heroe == None:
            raise errores.NoHayHeroeError("No hay ningun heroe(@) en el mapa")
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
try:
    Juego(nombre_mapa).main()

except errores.NoHayHeroeError:
    print "Debe haber un heroe representado por '@' para que juege el usuario."
except errores.PersonajeInexistenteError:
    print "El mapa provisto incluye personajes que no son del juego!."
except errores.MapaIncorrectoError:
    print "Formato del mapa incorrecto, debe ser rectangular"
except errores.DemasiadosHeroesError:
    print "Se estan añadiendo heroes de mas, solo puede haber uno"
except IOError:
    print "Archivo del mapa o directorio inexistentes, o no se tienen los permisos necesarios."
except IndexError:
    print "Mapa vacio, o no esta alineado en la izquierda superior del archivo"
