#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

# Definición de la clase Carta
class Carta:
    def __init__(self, pinta, valor):
        self.pinta = pinta
        self.valor = valor

    def __str__(self):
        return f"{self.valor} de {self.pinta}"

    def obtener_valor(self):
        if self.valor in ['J', 'Q', 'K']:
            return 10
        elif self.valor == 'A':
            return 11  # Valor por defecto, puede cambiar a 1 si es necesario
        else:
            return int(self.valor)

# Definición de la clase Baraja
class Baraja:
    def __init__(self):
        self.cartas = [Carta(pinta, valor) for pinta in ['CORAZÓN', 'TRÉBOL', 'DIAMANTE', 'ESPADA']
                                            for valor in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']]
        random.shuffle(self.cartas)

    def repartir_carta(self):
        return self.cartas.pop()

# Definición de la clase Mano
class Mano:
    def __init__(self):
        self.cartas = []

    def agregar_carta(self, carta):
        self.cartas.append(carta)

    def valor_total(self):
        valor = sum(carta.obtener_valor() for carta in self.cartas)
        num_as = sum(1 for carta in self.cartas if carta.valor == 'A')
        while valor > 21 and num_as:
            valor -= 10
            num_as -= 1
        return valor

    def mostrar(self, ocultar_primera=False):
        if ocultar_primera:
            return f"[Carta Oculta, {self.cartas[1]}]"
        return ', '.join(str(carta) for carta in self.cartas)

# Definición de la clase Jugador
class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.fichas = 100
        self.mano = Mano()

    def pedir_carta(self, baraja):
        self.mano.agregar_carta(baraja.repartir_carta())

    def decidir_accion(self, baraja):
        while True:
            decision = input(f"{self.nombre}, ¿Quieres pedir otra carta (p) o detenerte (d)? ").lower()
            if decision == 'p':
                self.pedir_carta(baraja)
                print(f"Tu mano: {self.mano.mostrar()}")
                if self.mano.valor_total() > 21:
                    print("¡Te has pasado de 21! Pierdes.")
                    return False
            elif decision == 'd':
                return True

# Definición de la clase JuegoBlackjack
class JuegoBlackjack:
    def __init__(self):
        self.baraja = Baraja()
        self.jugador = None
        self.casa = Mano()

    def iniciar_juego(self):
        nombre = input("Introduce tu nombre: ")
        self.jugador = Jugador(nombre)
        self.jugador.pedir_carta(self.baraja)
        self.jugador.pedir_carta(self.baraja)
        self.casa.agregar_carta(self.baraja.repartir_carta())
        self.casa.agregar_carta(self.baraja.repartir_carta())

    def mostrar_manos(self):
        print(f"Mano del jugador: {self.jugador.mano.mostrar()}")
        print(f"Mano de la casa: {self.casa.mostrar(ocultar_primera=True)}")

    def jugar(self):
        self.iniciar_juego()
        self.mostrar_manos()

        if self.jugador.mano.valor_total() == 21:
            print("¡Has hecho Blackjack! Ganaste.")
            return

        if not self.jugador.decidir_accion(self.baraja):
            self.ajustar_fichas(-self.apuesta)
            return

        self.casa.agregar_carta(self.baraja.repartir_carta())
        while self.casa.valor_total() <= 16:
            self.casa.agregar_carta(self.baraja.repartir_carta())
        
        self.mostrar_resultado()

    def mostrar_resultado(self):
        valor_jugador = self.jugador.mano.valor_total()
        valor_casa = self.casa.valor_total()
        print(f"Valor de la mano del jugador: {valor_jugador}")
        print(f"Valor de la mano de la casa: {valor_casa}")

        if valor_casa > 21 or valor_jugador > valor_casa:
            print("¡Ganaste!")
            self.ajustar_fichas(self.apuesta)
        elif valor_jugador < valor_casa:
            print("Perdiste.")
            self.ajustar_fichas(-self.apuesta)
        else:
            print("Empate.")
            self.ajustar_fichas(0)

    def ajustar_fichas(self, cantidad):
        self.jugador.fichas += cantidad
        print(f"Fichas del jugador: {self.jugador.fichas}")

# Código principal para ejecutar el juego
if __name__ == "__main__":
    juego = JuegoBlackjack()
    juego.jugar()


# In[ ]:




