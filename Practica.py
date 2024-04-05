import externo

"""a = FichExterno.CartaBase(9)
    print(a.ind)
    print(a.valor)
    Ejemplo de como crear un objeto y enseñar los valores del objeto llamado a"""

class Carta(externo.CartaBase):
    def __init__(self, ind):
        self.ind = ind
        
    def representarRank(self):
        if self.Rank == "10":
            print("│ " + self.Rank + "│ ", end="")
        else:
            print("│  " + self.Rank + "│ ", end="")
    
    def representarPalo(self):
        print("│" + self.Palo +"  │ ", end="")
    
    def info(self):
        print("Rank: " + self.Rank + "  Ind: " + str(self.ind) + "  Value: " + str(self.valor))
    
    @property
    def PaloNum(self):
        return (self.ind // 13)

    @property
    def Palo(self):
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
    Estrategia = externo.Estrategia(externo.Mazo.NUM_BARAJAS)
    Mazo = externo.Mazo(Carta, Estrategia)
    print("BLACKJACK - PARADIGMAS DE PROGRAMACION 2023/2024")
    ModoJuego = preguntaVariasOpciones("¿Modo de ejecucion? [J]uego [A]nalisis: ", "J", "A", "", "")
    while (SeguirJugando == "A"):
        print("")
        print("--- INICIO DE LA PARTIDA #" + str(NumPartida) + "--- BALANCE = " + str(Balance) + " €")
        Apuesta = preguntaVariasOpciones("¿Apuesta? [2] [10] [50]: ", "2", "10", "50", "")
        if Apuesta == "A":
            Apuesta = 2
        elif Apuesta == "B":
            Apuesta = 10
        elif Apuesta == "C":
            Apuesta = 50
        print("")
        Balance += partida(Mazo, Apuesta)
        SeguirJugando = preguntaVariasOpciones("¿Otra partida? [S/N]: ", "S", "N", "", "")
        NumPartida += 1
    
    
def repartoInicial(Mazo: externo.Mazo):
    print("REPARTO INICIAL")
    ManoJugador = []
    ManoCroupier = []
    EsBlackjack = False
    i = 0
    while i != 2:
        ManoJugador.append(Mazo.reparte())
        i += 1
    ManoCroupier.append(Mazo.reparte())
    if ((ManoJugador[0].valor + ManoJugador[1].valor) == 11 and (ManoJugador[0].valor == 1 or ManoJugador[1].valor == 1)):
        EsBlackjack = True
    return [EsBlackjack, ManoCroupier, ManoJugador]

    
def partida(Mazo: externo.Mazo, ApuestaInic):
    EstadoManos = ["ABIERTA"]
    ApuestaManos = [ApuestaInic]
    AlgunaManoAbierta = True
    ListaManos = []
    NombresManos = ["Mano"]
    DatosRepartoinicial = repartoInicial(Mazo)
    EsBlackjack = DatosRepartoinicial[0]
    ManoCroupier = DatosRepartoinicial[1]
    ManoInic = DatosRepartoinicial[2]
    representacionManos([ManoCroupier], ["Croupier"], [], [])
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
            for Mano in ListaManos:
                if sePuedePasarMano(Mano) == True:
                    Respuesta = preguntaVariasOpciones("¿Jugada para " + NombresManos[i] +"? [P]edir [D]oblar [C]errar [S]eparar: ", "P", "D", "C", "S")
                else:
                    Respuesta = preguntaVariasOpciones("¿Jugada para " + NombresManos[i] + "? [P]edir [D]oblar [C]errar: ", "P", "D", "C", "")
            
                if Respuesta == "A" or Respuesta == "B":
                    Mano.append(Mazo.reparte())
                    if Respuesta == "B":
                        ApuestaManos[i] += ApuestaManos[i]
                    if valorMano(Mano) > 21:
                        EstadoManos[i] = "PASADA"
                
                if Respuesta == "C":
                    EstadoManos[i] = "CERRADA"
                
                i += 1
                representacionManos([ManoCroupier], ["Croupier"], [], [])
                representacionManos(ListaManos, NombresManos, EstadoManos, ApuestaManos)
            
            AlgunaManoAbierta = False
            for Estado in EstadoManos:
                if Estado == "ABIERTA":
                    AlgunaManoAbierta = True
            
                
        DineroGanado = -ApuestaInic                                     #CAMBIAR POR LA SUMA DE TODOS LOS NUMEROS DENTRO DE ApuestaManos: list
        print("¡Has perdido " + str(int(-DineroGanado)) + "€!")
    return int(DineroGanado)
        

def valorMano(Mano: list):
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



def sePuedePasarMano(Mano: list):
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
    #Primera linea de la representacion con la siguiente forma: ManoX   ╭───╮ ╭───╮ ╭───╮  │ ManoX ╭───╮ ╭───╮ ╭───╮ │
    print("")
    i = 0
    Margen = 13
    for Mano in ListaManos:
        print(NombresManos[i].ljust(Margen), end="")
        for Carta in Mano:
            print("╭───╮ ", end="")
        print(" │ ", end="")
        i += 1
    print("")
    

    #Segunda linea de la representacion con la siguiente forma:   (x) │   Y│  │   Y│ │   Y│  │    (x) │   Y│ │   Y│ │   Y│ │
    for Mano in ListaManos:
        Num = 0
        for Carta in Mano:
            Num =+ Carta.valor
        Numrepresentar = "(" + str(valorMano(Mano)) + ") "
        print(Numrepresentar.rjust(Margen), end="")

        for Carta in Mano:
            Carta.representarRank()
        print(" │ ", end="")
    print("")
    
    
    #Tercera linea de la representacion con la siguiente forma:   X€ │Y   │  │Y   │ │Y   │  │    X€ │Y   │ │Y   │ │Y   │ │
    i = 0
    for Mano in ListaManos:
        if NombresManos[0] != "Croupier":
            print(str(ApuestaManos[i]).rjust(Margen - 1), end="")
            print("€", end="")
        else:
            print("".rjust(Margen), end="")
        for Carta in Mano:
            Carta.representarPalo()
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
        print(" │ ", end="")
        i += 1
    print("")
    print("")
main()