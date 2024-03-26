import FichExterno

# a = FichExterno.CartaBase(9)
# print(a.ind)
# print(a.valor)

class Carta(FichExterno.CartaBase):
    def __init__(self, ind):
        print("Carta con id: " + ind)



def main():
    numBarajas = 2
    Estrategia = FichExterno.Estrategia(numBarajas)
    print("BLACKJACK - PARADIGMAS DE PROGRAMACION 2023/2024")
    ModoJuego = preguntaVariasOpciones("¿Modo de ejecucion? [J]uego [A]nalisis: ", "J", "A", "", "")
    repartoInicial()
    
    
def repartoInicial():
    print("Haciendo reparto inicial")


def preguntaVariasOpciones(Pregunta, OpcionA, OpcionB, OpcionC, OpcionD):
    Respuesta = "Null"
    while (((Respuesta != OpcionA) & (Respuesta != OpcionB) & (Respuesta != OpcionC) & (Respuesta != OpcionD)) | (Respuesta == "")):
        print(Pregunta, end="")
        Respuesta = input().upper()
        if Respuesta == "":
            print("Respuesta no válida")
        elif Respuesta == OpcionA:
            elegido = "A"
        elif Respuesta == OpcionB:
            elegido = "B"
        elif Respuesta == OpcionC:
            elegido = "C"
        elif Respuesta == OpcionD:
            elegido = "D"
        else:
            print("Respuesta no válida")
    return elegido
        
main()

