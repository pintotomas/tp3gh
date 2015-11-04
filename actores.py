#coding=utf-8
import curses

import random
class Actor(object):
    """Clase base para todas las entidades capaces de ocupar una posicion en el mapa."""

    def __init__(self):
        """Inicializa el Actor."""
        
        self.x = 0
        self.y = 0
        self.vivo = True
        
    def dibujar(self):
        """Devuelve el caracter que representa al Actor."""
        
        return '?'
       

    def jugar_turno(self, juego):
        """Jugar un turno. `juego` es la instancia del `Juego`."""
        
        pass
        
    def interactuar_con_heroe(self, juego):
        """Realiza la accion correspondiente a la interaccion con el heroe (es
        decir, cuando el heroe intenta moverse a la posicion ocupada por este actor).
        Devuelve True si el heroe realizo alguna accion, False en caso contrario."""
        
        return False
             
    def esta_vivo(self):
        """Devuelve True en caso de estar vivo, False en caso contrario.
        Cuando un actor informa que no esta vivo, es eliminado del mapa
        automaticamente."""
        
        return self.vivo
        
    def es_heroe(self):
        """Devuelve True si es el heroe del juego (es decir, si es controlado
        por la entrada del usuario)."""
        
        return False
        
class Heroe(Actor):
    """Representa al Heroe del juego."""

    direcciones = {
            curses.KEY_UP: (0, -1),
            curses.KEY_LEFT: (-1, 0),
            curses.KEY_DOWN: (0, 1),
            curses.KEY_RIGHT: (1, 0),
    }

    def __init__(self):
        """Crea al Heroe."""
        self.monedas = 0
        Actor.__init__(self)
        
    def es_heroe(self):
        """Devuelve True si es el heroe del juego (es decir, si es controlado
        por la entrada del usuario)."""
        
        return True
       
    def dibujar(self):
        """Devuelve el caracter que representa al Heroe."""
        
        return '@'
        
    def accion(self, dx, dy, juego):
        """Intenta realizar una accion con la celda que esta en la direccion (dx, dy).
        Devuelve True si se realizo alguna accion, False en caso contrario."""
        
        mapa = juego.mapa
        x = max(0, min(mapa.ancho() - 1, self.x + dx))
        y = max(0, min(mapa.alto() - 1, self.y + dy))
        if not mapa.posicion_valida(x, y):
            return False

        actor = mapa.get_celda(x, y)
        if actor:
            return actor.interactuar_con_heroe(juego)
        mapa.mover_actor(self, x, y)
        return True

    def jugar_turno_heroe(self, evento, juego):
        """Jugar un turno. `evento` es un evento de la libreria `curses` que permite
        reaccionar ante la entrada del usuario. `juego` es una instancia `Juego`.
        Devuelve True si se hizo alguna accion, False en caso contrario."""
        
        if evento in Heroe.direcciones:
            dx, dy = Heroe.direcciones[evento]
            return self.accion(dx, dy, juego)
        return False
class Enemigo(Actor):
	"""Representa a los enemigos del juego"""
	def __init__(self):
		"Crea a un enemigo"
		Actor.__init__(self)
		self.tiene_monedas = random.randint(0,1)
	
	def interactuar_con_heroe(self,juego):
		mapa = juego.mapa
		self.vivo = False
		mapa.eliminar_actores_muertos()
		juego.msg("has matado a un enemigo")
		if self.tiene_monedas == 1:
			mapa = juego.mapa
			moneda = Moneda()
			mapa.agregar_actor(moneda,self.x,self.y)
    		
class Goblin(Enemigo):
    """Representa al enemigo Goblin"""
    def dibujar(self):
        """Devuelve el caracter que representa al goblin."""
        return 'g'
class Orco(Enemigo):
    """Representa al enemigo Orco"""
    		
    def dibujar(self):
        """Devuelve el caracter que presenta al orco"""
        return 'o'
    
class Moneda(Actor):
    def dibujar(self):
        """Devuelve el caracter que representa una moneda"""
        return '$'
	def interactuar_con_heroe(self,juego):
		mapa = juego.mapa
		self.vivo = False
		mapa.eliminar_actores_muertos()
		juego.heroe.monedas+=1
		juego.msg("has obtenido una moneda, total de monedas:{}".format(juego.heroe.monedas))
		##Ver por que no pasa nada con esto##
class Pared(Actor):
    """Representa a las paredes del juego"""
    def dibujar(self):
        """Devuelve el caracter que representa una pared"""
        return "#"
class Salida(Actor):
    """Representa a la salida del calabozo"""
    def dibujar(self):
        """Devuelve el caracter que representa la salida"""
        return "<"
###
### Agregar las clases Enemigo (g = goblin, o = orco), Moneda ($), Pared (#) y Salida (<)
###
