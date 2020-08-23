
alfabeto = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "X", "Y", "Z"]
mensaje_codificado = input("Introduce mensaje:")
mensaje_codificado = mensaje_codificado.upper()
numero_operador = input("Introduce un numero:")
mensaje_decodificado = ""

for letra in mensaje_codificado:
    if letra ==  " ":
        mensaje_decodificado += " "
    else:
        valor_inicial_letra = alfabeto.index(letra) + 1
        valor_final_letra = valor_inicial_letra + int(numero_operador)
        if valor_final_letra >= 25:
            valor_final_letra -= 25
        if valor_final_letra <= 0:
            valor_final_letra += 25
        mensaje_decodificado += alfabeto[valor_final_letra-1]

print("Mensaje modificado: "+mensaje_decodificado)
    
