import FichExterno

a = FichExterno.CartaBase(9)
print(a.ind)
print(a.valor)


def main():
    print("BLACKJACK - PARADIGMAS DE PROGRAMACION 2023/2024")
    respuesta = "Null"
    print(respuesta)
    while ((respuesta != "J") & (respuesta != "A")):
        print("¿Modo de ejecución? [J]uego [A]nálisis: ", end="")
        respuesta = input().upper()
        if respuesta == "J":
            Analisis = False
        elif respuesta == "A":
            Analisis = True
        else:
            print("Respuesta no válida")
        
main()

