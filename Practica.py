#Desarrollado por Javier De Castro

import FichExterno

class Carta(FichExterno.CartaBase):
    """Clase que hereda de CartaBase, tiene funciones para representar sus propiedades
    """
    def __init__(self, ind):
        """Crea carta con indice ind

        Args:
            ind (int): Indice de la carta
        """
        self.ind = ind
        
    def representarRank(self):
        """Representa el valor(rank) de una carta (A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2) Ej. │  8│ 
        """
        if self.Rank == "10":
            print("│ " + self.Rank + "│ ", end="")
        else:
            print("│  " + self.Rank + "│ ", end="")
    
    def representarPalo(self):
        """Representa el palo de una carta (♠,♣,♥,♦) Ej. │♠  │ con el color correspondiente, rojo o negro
        """
        Negro = '\033[30m'
        Rojo = '\033[31m'
        Blanco = '\033[97m'

        if (self.PaloNum == 0 or self.PaloNum == 1):
            print("│" + Negro + self.Palo + Blanco + "  │ ", end="")
        else:
            print("│" + Rojo + self.Palo + Blanco + "  │ ", end="")
    
    def info(self):
        """Da la información sobre las propiedades de la carta, su indice, rank y valor
        """
        print("Rank: " + self.Rank + "  Ind: " + str(self.ind) + "  Value: " + str(self.valor))
    
    @property
    def PaloNum(self):
        """Representa en un numero el palo de la carta, los 13 primeros indices son el palo 0, los 13 siguientes el palo 1...

        Returns:
            (int): Entero que representa uno de los 4 palos de la baraja, sabiendo que solo hay 52 cartas por baraja
        """
        return (self.ind // 13)

    @property
    def Palo(self):
        """Es un simbolo a los numeros 0-3, siendo cada uno de ellos un palo distinto de la baraja(♠,♣,♥,♦)

        Returns:
            (string): Texto que contiene el simbolo del palo al que pertenece la carta 
        """
        if self.PaloNum == 0:
            Simbolo = "♠"
        elif self.PaloNum == 1:
            Simbolo = "♣"
        elif self.PaloNum == 2:
            Simbolo = "♥"
        elif self.PaloNum == 3:
            Simbolo = "♦"
        return Simbolo
    
    @property
    def Rank(self):
        """Es el valor(rank), no confundir con el valor al contar, de una carta (A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2)

        Returns:
            (string): Devuelve el valor en un string
        """
        if (self.ind % 13 == 0):
            Rank = "A"
        elif (self.ind % 13 == 10):
            Rank = "J"
        elif (self.ind % 13 == 11):
            Rank = "Q"
        elif (self.ind % 13 == 12):
            Rank = "K"
        else:
            Rank = (str((self.ind % 13) + 1))
        return Rank


def main():
    NumPartida = 1
    SeguirJugando = "A"
    Balance = 0
    PartidasParaAnalisis = 0
    Estrategia = FichExterno.Estrategia(FichExterno.Mazo.NUM_BARAJAS)
    Mazo = FichExterno.Mazo(Carta, Estrategia)
    print("BLACKJACK - PARADIGMAS DE PROGRAMACION 2023/2024")
    ModoAnalisis = preguntaVariasOpciones("¿Modo de ejecucion? [J]uego [A]nalisis: ", "J", "A", "", "")
    if ModoAnalisis == "B":
        ModoAnalisis = True
        while PartidasParaAnalisis < 1:
            print("¿Número de partidas?: ", end="")
            Respuesta = input()
            try:
                PartidasParaAnalisis = int(Respuesta)
            except ValueError:
                print("La respuesta no es un numero válido")
    else:
        ModoAnalisis = False
    
    while (SeguirJugando == "A"):
        print("")
        print("--- INICIO DE LA PARTIDA #" + str(NumPartida) + "--- BALANCE = " + str(Balance) + " €")
        if ModoAnalisis == True:
            print("¿Apuesta? [2] [10] [50]: ", end="")
            Apuesta = Estrategia.apuesta(2,10,50)
            print (str(Apuesta))
        else:
            Apuesta = preguntaVariasOpciones("¿Apuesta? [2] [10] [50]: ", "2", "10", "50", "")
            if Apuesta == "A":
                Apuesta = 2
            elif Apuesta == "B":
                Apuesta = 10
            elif Apuesta == "C":
                Apuesta = 50
        print("")
        Balance += partida(Mazo, Apuesta, ModoAnalisis, Estrategia)
        
        NumPartida += 1
        if ModoAnalisis == True:
            print("¿Otra partida? [S/N]: ", end="")
            if NumPartida > PartidasParaAnalisis:
                SeguirJugando = "B"
                print("N")
            else:
                print("S")
        else:
            SeguirJugando = preguntaVariasOpciones("¿Otra partida? [S/N]: ", "S", "N", "", "")
    print("BALANCE FINAL: " + str(Balance) + "€")
    
    
def repartoInicial(Mazo: FichExterno.Mazo):
    """Da el primer reparto de una partida
    Args:
        Mazo (FichExterno.Mazo): El objeto mazo del que sacar las cartas

    Returns:
        (list): Contiene varios datos, un bool con valor True en caso de blackjack, la mano del croupier y la mano del jugador
    """
    print("REPARTO INICIAL")
    ManoJugador = []
    ManoCroupier = []
    EsBlackjack = False
    i = 0
    ManoCroupier.append(Mazo.reparte())
    while i != 2:
        ManoJugador.append(Mazo.reparte())
        i += 1
    if ((ManoJugador[0].valor + ManoJugador[1].valor) == 11 and (ManoJugador[0].valor == 1 or ManoJugador[1].valor == 1)):
        EsBlackjack = True
    return [EsBlackjack, ManoCroupier, ManoJugador]

    
def partida(Mazo: FichExterno.Mazo, ApuestaInic: int, Analisis: bool, Estrategia: FichExterno.Estrategia):
    """Simula una partida de blackjacky sus apuetas correspondientes

    Args:
        Mazo (FichExterno.Mazo): Mazo del que se sacan las cartas
        ApuestaInic (int): Apuesta inicial de la partida
        Analisis (bool): Indica si el modo analisis esta activado o no
        Estrategia (FichExterno.Estrategia): La estrategia a utilizar en caso de que el modo analisis este activado

    Returns:
        (int): El dinero ganado en esta partida
    """
    EstadoManos = ["ABIERTA"]
    EstadoCroupier = ["ABIERTA"]
    ApuestaManos = [ApuestaInic]
    AlgunaManoAbierta = True
    CroupierTermino = False
    ListaManos = []
    NombresManos = ["Mano"]
    DatosRepartoinicial = repartoInicial(Mazo)
    EsBlackjack: bool = DatosRepartoinicial[0]
    ManoCroupier: list = DatosRepartoinicial[1]
    ManoInic: list = DatosRepartoinicial[2]
    representacionManos([ManoCroupier], ["Croupier"], EstadoCroupier, [])
    representacionManos([ManoInic], NombresManos, EstadoManos, ApuestaManos)
    if EsBlackjack == True:
        print("*****************")
        print("*** BLACKJACK ***")
        print("*****************")
        DineroGanado = ApuestaInic * 1.5
        print("¡Has ganado " + str(int(DineroGanado)) + "€!")
    else:
        ListaManos.append(ManoInic)
        print("TURNO DEL JUGADOR")
        while AlgunaManoAbierta == True:
            
            i= 0
            ListaTemp = []
            for Mano in ListaManos:
                if EstadoManos[i] == "ABIERTA":
                    if Analisis == True:
                        if sePuedeSepararMano(Mano) == True:
                            print("¿Jugada para " + NombresManos[i] +"? [P]edir [D]oblar [C]errar [S]eparar: ", end="")
                        else:
                            print("¿Jugada para " + NombresManos[i] +"? [P]edir [D]oblar [C]errar: ", end="")
                        Respuesta = Estrategia.jugada(ManoCroupier[0], Mano)
                        print(Respuesta)
                        if Respuesta == "P":
                            Respuesta = "A"
                        elif Respuesta == "D":
                            Respuesta = "B"
                        elif Respuesta == "S":
                            Respuesta = "D"
                    else:
                        if sePuedeSepararMano(Mano) == True:
                            Respuesta = preguntaVariasOpciones("¿Jugada para " + NombresManos[i] +"? [P]edir [D]oblar [C]errar [S]eparar: ", "P", "D", "C", "S")
                        else:
                            Respuesta = preguntaVariasOpciones("¿Jugada para " + NombresManos[i] + "? [P]edir [D]oblar [C]errar: ", "P", "D", "C", "")
                
                    if Respuesta == "A" or Respuesta == "B":
                        Mano.append(Mazo.reparte())
                        if Respuesta == "B":
                            ApuestaManos[i] += ApuestaManos[i]
                            EstadoManos[i] = "CERRADA"
                        if valorMano(Mano) > 21:
                            EstadoManos[i] = "PASADA"
                    
                    elif Respuesta == "C":
                        EstadoManos[i] = "CERRADA"
                    
                    elif Respuesta == "D":
                        NuevaMano = [Mano.pop(1)]
                        ListaTemp.append(NuevaMano)
                        EstadoManos.append("ABIERTA")
                        ApuestaManos.append(ApuestaManos[i])
                        NombresManos.append(NombresManos[i] + "B")
                        NombresManos[i] = NombresManos[i] + "A"  
                i += 1
            for Mano in ListaTemp:
                ListaManos.append(Mano)
            
            AlgunaManoAbierta = False
            AlgunaManoCerrada = False
            for Estado in EstadoManos:
                if Estado == "ABIERTA":
                    AlgunaManoAbierta = True
                elif Estado == "CERRADA":
                    AlgunaManoCerrada = True
            representacionManos(ListaManos, NombresManos, EstadoManos, ApuestaManos)
        if AlgunaManoCerrada == True:
            print("TURNO DEL CROUPIER")
            representacionManos([ManoCroupier], ["Croupier"], EstadoCroupier,[])
            while CroupierTermino == False:
                ManoCroupier.append(Mazo.reparte())
                if valorMano(ManoCroupier) > 16 and valorMano(ManoCroupier) < 22:
                    CroupierTermino = True
                    EstadoCroupier = ["CERRADA"]
                elif valorMano(ManoCroupier) > 21:
                    CroupierTermino = True
                    EstadoCroupier = ["PASADA"]                     
                representacionManos([ManoCroupier], ["Croupier"], EstadoCroupier,[])
        
        print("FIN DE LA PARTIDA")
        representacionManos([ManoCroupier], ["Croupier"], EstadoCroupier,[])
        representacionManos(ListaManos, NombresManos, EstadoManos, ApuestaManos)
        
        DineroGanado = 0
        i = 0
        print("")
        print("CONTABILIZACIÓN DE RESULTADOS")
        for Mano in ListaManos:
            DineroMano = 0

            if (valorMano(Mano) == valorMano(ManoCroupier)) or ((EstadoManos[i] == "PASADA") and (valorMano(ManoCroupier) > 21)):     #Ambas manos tienen el mismo valor o estan ambas pasadas
                DineroMano = 0
            
            elif (valorMano(Mano) > valorMano(ManoCroupier) and EstadoManos[i] == "CERRADA") or (valorMano(ManoCroupier) > 21):       #La mano jugada es mayor que la del croupier y esta cerrada o la mano del croupier esta pasada
                DineroMano = ApuestaManos[i]
            
            elif (valorMano(Mano) < valorMano(ManoCroupier)) or (EstadoManos[i] == "PASADA"):
                DineroMano = -ApuestaManos[i]
            
            if DineroMano >= 0:
                print("* Croupier: " + str(valorMano(ManoCroupier)) + ", " + NombresManos[i] + ": " + str(valorMano(Mano)) + " -> +" + str(DineroMano) +"")
            else:
                print("* Croupier: " + str(valorMano(ManoCroupier)) + ", " + NombresManos[i] + ": " + str(valorMano(Mano)) + " -> " + str(DineroMano) +"")
            DineroGanado += DineroMano
            i += 1
        print("Resultado de la partida: " + str(int(DineroGanado)) + "€")
    return int(DineroGanado)
        

def valorMano(Mano: list):
    """Dada una mano indica el valor de la mano teniendo en cuenta que los ases son 1 u 11 dependiendo del resto de valores

    Args:
        Mano (list): Mano a valorar

    Returns:
        (int): Valor de la mano
    """
    Valor = 0
    NumAsesAltos = 0
    for Carta in Mano:
        Valor += Carta.valor
        if Carta.valor == 1:
            Valor += 10
            NumAsesAltos += 1
        if Valor > 21 and NumAsesAltos > 0:
            Valor -= 10
            NumAsesAltos -= 1
    return Valor



def sePuedeSepararMano(Mano: list):
    """Indica si una mano dada es elegible para poder separarse

    Args:
        Mano (list): Mano a valorar

    Returns:
        (bool): Tiene el valor True si se puede separar la mano
    """
    Pasable = False
    if len(Mano) == 2:
        if Mano[0].valor == Mano[1].valor:
            Pasable = True
    return Pasable



def preguntaVariasOpciones(Pregunta, OpcionA, OpcionB, OpcionC, OpcionD):
    """ Metodo que dada una pregunta y 4 opciones devuelve "A"-"D" en un string dependiendo de la opcion seleccionada
        En caso de querer 2 o 3 opciones se puede dejar en el campo de las opciones el string "" en cuyo caso lo cogera como respuesta incorrecta
        Es independiente en la respuesta del usuario las mayusculas

    Args:
        Pregunta (String): String que contiene la pregunta a realizar
        OpcionA (String): String con la respuesta que debe dar el usuario para recibir "A"
        OpcionB (String): String con la respuesta que debe dar el usuario para recibir "B"
        OpcionC (String): String con la respuesta que debe dar el usuario para recibir "C"
        OpcionD (String): String con la respuesta que debe dar el usuario para recibir "D"

    Returns:
        String: String con una letra "A"-"D" dependiendo de la opcion seleccionada
    """
    Respuesta = "Null"
    while (((Respuesta != OpcionA) & (Respuesta != OpcionB) & (Respuesta != OpcionC) & (Respuesta != OpcionD)) | (Respuesta == "")):
        print(Pregunta, end="")
        Respuesta = input().upper()
        if Respuesta == "":
            print("Respuesta no válida")
        elif Respuesta == OpcionA:
            Elegido = "A"
        elif Respuesta == OpcionB:
            Elegido = "B"
        elif Respuesta == OpcionC:
            Elegido = "C"
        elif Respuesta == OpcionD:
            Elegido = "D"
        else:
            print("Respuesta no válida")
    return Elegido

def representacionManos(ListaManos: list, NombresManos: list, EstadoManos: list, ApuestaManos: list):
    """Representa una mano en consola 

    Args:
        ListaManos (list): Lista de manos a representar, lista con un unico objeto en caso de una mano
        NombresManos (list): Lista con los nombres asociados a cada mano en el mismo orden que en la lista de manos 
        EstadoManos (list): Lista con los estados asociados a cada mano en el mismo orden que en la lista de manos
        ApuestaManos (list): Lista con las apuestas asociadas a cada mano en el mismo orden que en la lista de manos 
    """
    #Primera linea de la representacion con la siguiente forma: ManoX   ╭───╮ ╭───╮ ╭───╮  │ ManoX ╭───╮ ╭───╮ ╭───╮ │
    print("")
    i = 0
    Margen = 13
    for Mano in ListaManos:
        print(NombresManos[i].ljust(Margen), end="")
        for Carta in Mano:
            print("╭───╮ ", end="")
        if i != len(ListaManos) - 1:
            print(" │ ", end="")
        i += 1
    print("")
    

    #Segunda linea de la representacion con la siguiente forma:   (x) │   Y│  │   Y│ │   Y│  │    (x) │   Y│ │   Y│ │   Y│ │
    i = 0
    for Mano in ListaManos:
        Num = 0
        for Carta in Mano:
            Num =+ Carta.valor
        Numrepresentar = "(" + str(valorMano(Mano)) + ") "
        print(Numrepresentar.rjust(Margen), end="")

        for Carta in Mano:
            Carta.representarRank()
        if i != len(ListaManos) - 1:
            print(" │ ", end="")
        i += 1
    print("")
    
    
    #Tercera linea de la representacion con la siguiente forma:   X€ │Y   │  │Y   │ │Y   │  │    X€ │Y   │ │Y   │ │Y   │ │
    i = 0
    for Mano in ListaManos:
        if NombresManos[0] != "Croupier":
            print(str(ApuestaManos[i]).rjust(Margen - 1), end="")
            print("€", end="")
        else:
            print(EstadoManos[i].rjust(Margen), end="")
        for Carta in Mano:
            Carta.representarPalo()
        if i != len(ListaManos) - 1:
            print(" │ ", end="")
        i += 1
    print("")
    
    
    #Cuarta linea de la representacion con la siguiente forma: XXXXX   ╰───╯ ╰───╯ ╰───╯  │ XXXXX ╰───╯ ╰───╯ ╰───╯  │
    i= 0
    for Mano in ListaManos:
        if NombresManos[0] != "Croupier":
            print(EstadoManos[i].rjust(Margen), end="")
        else:
            print("".rjust(Margen), end="")
        for Carta in Mano:
            print
            print("╰───╯ ", end="")
        if i != len(ListaManos) - 1:
            print(" │ ", end="")
        i += 1
    print("")
    print("")
main()