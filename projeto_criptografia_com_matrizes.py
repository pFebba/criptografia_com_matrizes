from datetime import datetime
import pytz


def mostrardatahorasp():
    # Obtém o fuso horário de São Paulo
    fusosp = pytz.timezone('America/Sao_Paulo')
    # Obtém a data e hora atual no fuso horário de São Paulo
    datahorasp = datetime.now(fusosp)
    # Formata a data e hora
    formatada = datahorasp.strftime("%d-%m-%Y %H:%M")
    print("Data e hora atual em São Paulo:", formatada)


# Chama a função para mostrar a data e hora atual em São Paulo
mostrardatahorasp()


def cdeterminante(matriz):
    # calcular o determinante de uma matriz 2x2.
    return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]


def inversa(matriz):
    # calcular a inversa de uma matriz 2x2.
    det = cdeterminante(matriz)
    if det == 0:
        raise ValueError("A matriz não é invertível")
    return [[matriz[1][1] / det, -matriz[0][1] / det], [-matriz[1][0] / det, matriz[0][0] / det]]


def mmatriz(matriz1, matriz2):
    # multiplicar duas matrizes 2x2.
    resultado = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                resultado[i][j] += matriz1[i][k] * matriz2[k][j]
    return resultado


def numeropletra(numero):
    # Função que converte um número em uma letra usando a tabela ASCII Windows-1252. 97 é convertido para 'a', 98 para 'b', e assim por diante.
    # Qualquer número <32(espaço na tabela ascii) é um caractere não imprimível por isso limita a ser no mínimo 32, 255 é o valor final e max da tabela
    return chr(numero % 223+32)


def letrapnumero(letra):
    # Função que converte uma letra em um número usando a tabela ASCII Windows-1252.
    return ord(letra)-32


def criarmatriz2x2(numeros):
    # Função que cria uma matriz 2x2 e preenche com os números fornecidos. completando com zeros se necessário.
    matriz = []
    # Completa a lista de números com zeros se tiver menos de 4 elementos
    while len(numeros) < 4:
        numeros.append(0)
    # Cria a matriz 2x2 e preenche com os números
    matriz = [numeros[:2], numeros[2:]]
    return matriz


def gerarchavecriptografica(cpf):
    # Função que gera uma chave de criptografia em forma de matriz de ordem 2 utilizando os números de um CPF como base, garantindo que o determinante seja diferente de zero.
    # Extrai os números do CPF e transforma em uma lista de inteiros
    numeroscpf = [int(digito) for digito in cpf if digito.isdigit()]
    if len(numeroscpf) < 11:
        raise ValueError("CPF inválido: deve conter pelo menos 11 dígitos.")
    # Garante que a lista de números do CPF tenha pelo menos 4 elementos
    while len(numeroscpf) < 4:
        numeroscpf.append(0)
    # Gera a chave utilizando os números do CPF
    chave = [
        [numeroscpf[0], numeroscpf[4]],
        [numeroscpf[5], numeroscpf[10]]
    ]
    # Calcula o determinante da matriz chave
    det = chave[0][0] * chave[1][1] - chave[0][1] * chave[1][0]
    # Se o determinante for igual a zero, ajusta a chave para garantir que seja diferente de zero
    if det == 0:
        chave[1][1] += 1
        chave[1][0] += 1
        chave[0][0] += 1
        chave[0][1] += 1
    return chave


def gerarchavecriptograficacep(cep):
    numeroscep = [int(digito) for digito in cep if digito.isdigit()]
    if len(numeroscep) < 8:
        raise ValueError(
            "CEP inválido: deve conter pelo menos 8 dígitos numéricos.")
    while len(numeroscep) < 4:
        numeroscep.append(0)
    chave = [
        [numeroscep[0], numeroscep[4]],
        [numeroscep[5], numeroscep[7]]  # Corrigido o índice do segundo número
    ]
    det = chave[0][0] * chave[1][1] - chave[0][1] * chave[1][0]
    if det == 0:
        chave[1][1] += 1
        chave[1][0] += 1
        chave[0][0] += 1
        chave[0][1] += 1
    return chave


def main():
    mostrardatahorasp()
    minuto_atual = datetime.now().minute

    if minuto_atual % 2 == 0:
        cpf = input("Digite o CPF da pessoa: ")
        while not cpf.isdigit() or len(cpf) < 11:
            print('Digite um CPF válido! Ele precisa ter 11 dígitos numéricos')
            cpf = str(input('Digite o CPF da pessoa: '))
        texto = input("Digite uma palavra ou frase: ")
        tamantexto = len(texto)
        print("Tabela utilizada: Tabela ASCII de acordo com Windows-1252")

        print("\nMatrizes da palavra:")
        matrizes_palavra = []
        for i in range(0, len(texto), 4):
            parte = texto[i:i+4]
            numeros = [letrapnumero(letra) for letra in parte]
            matriz = criarmatriz2x2(numeros)
            matrizes_palavra.append(matriz)
            print(f"Matriz {i//4 + 1}:")
            for linha in matriz:
                print(linha)

        print("\nChave de criptografia:")
        for linha in gerarchavecriptograficacep(cpf):
            print(linha)

        print("\nMultiplicação da chave pelas matrizes da palavra:")
        resultados = []
        for i, matriz in enumerate(matrizes_palavra):
            resultado = mmatriz(gerarchavecriptograficacep(cpf), matriz)
            resultados.append(resultado)
            print(f"Matriz {i+1}:")
            for linha in resultado:
                print(linha)

            print("\nResultado final em linha única:")
            resultado_linha_unica = []
        for resultado in resultados:
            for linha in resultado:
                for numero in linha:
                    resultado_linha_unica.append(numero)
            for numero in resultado_linha_unica:
                print(numeropletra(round(numero)), end="")
            print()

        print("\nDescriptografando o resultado final:")
        inversa_chave = inversa(gerarchavecriptograficacep(cpf))
        resultado_final = []
        for i in range(0, len(resultado_linha_unica), 4):
            parte = resultado_linha_unica[i:i + 4]
            matriz = criarmatriz2x2(parte)
            print("\nMatriz criptografada:")
            for linha in matriz:
                print(linha)
            print("Matriz descriptografada:")
            matriz_descriptografada = mmatriz(inversa_chave, matriz)
            for linha in matriz_descriptografada:
                print(linha)
            for linha in matriz_descriptografada:
                for numero in linha:
                    resultado_final.append(numero)
        print("Resultado final (números):", resultado_final)

        print("\nResultado final descriptografado:")
        for numero in resultado_final:
            print(numeropletra(round(numero)), end="")
        print()

    else:
        cep = input("Digite o CEP da pessoa: ")
        while not cep.isdigit() or len(cep) < 8:
            print('Digite um CEP válido! Ele precisa ter 8 dígitos numéricos')
            cep = str(input('Digite o CEP da pessoa: '))
        texto = input("Digite uma palavra ou frase: ")
        tamantexto = len(texto)
        print("Tabela utilizada: Tabela ASCII de acordo com Windows-1252")
        chave_criptografica = gerarchavecriptograficacep(cep)  # Corrigido aqui

        print("\nMatrizes da palavra:")
        matrizes_palavra = []
        for i in range(0, len(texto), 4):
            parte = texto[i:i+4]
            numeros = [letrapnumero(letra) for letra in parte]
            matriz = criarmatriz2x2(numeros)
            matrizes_palavra.append(matriz)
            print(f"Matriz {i//4 + 1}:")
            for linha in matriz:
                print(linha)

        print("\nChave de criptografia:")
        for linha in gerarchavecriptograficacep(cep):
            print(linha)

        print("\nMultiplicação da chave pelas matrizes da palavra:")
        resultados = []
        for i, matriz in enumerate(matrizes_palavra):
            resultado = mmatriz(chave_criptografica, matriz)
            resultados.append(resultado)
            print(f"Matriz {i+1}:")
            for linha in resultado:
                print(linha)

        print("\nResultado final em linha única:")
        resultado_linha_unica = []
        for resultado in resultados:
            for linha in resultado:
                for numero in linha:
                    resultado_linha_unica.append(numero)
        for numero in resultado_linha_unica:
            print(numeropletra(round(numero)), end="")
        print()

        print("\nDescriptografando o resultado final:")
        inversa_chave = inversa(chave_criptografica)
        resultado_final = []
        for i in range(0, len(resultado_linha_unica), 4):
            parte = resultado_linha_unica[i:i + 4]
            matriz = criarmatriz2x2(parte)
            print("\nMatriz criptografada:")
            for linha in matriz:
                print(linha)
            print("Matriz descriptografada:")
            matriz_descriptografada = mmatriz(inversa_chave, matriz)
            for linha in matriz_descriptografada:
                print(linha)
            for linha in matriz_descriptografada:
                for numero in linha:
                    resultado_final.append(numero)
        print("Resultado final (números):", resultado_final)

        print("\nResultado final descriptografado:")
        for numero in resultado_final:
            print(numeropletra(round(numero)), end="")
        print()


main()
