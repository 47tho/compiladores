import matplotlib.pyplot as plt

# Listas de operadores y símbolos reconocidos
operadores_logicos = ['and', 'or', 'not']
operadores_aritmeticos = ['+', '-', '*', '/', '%']
operadores_relacionales = ['<', '>', '!']
operadores_asignacion = ['=']

# Palabras clave y funciones comunes de Python
palabras_clave = [
    'if', 'else', 'while', 'for', 'return', 'def', 'class', 'break', 'continue', 
    'in', 'is', 'lambda', 'print', 'input', 'len', 'range', 'import', 'from', 
    'as', 'with', 'try', 'except', 'finally', 'raise', 'yield', 'del', 'pass', 
    'global', 'nonlocal', 'assert', 'async', 'await'
]

# Signos de puntuación
puntuacion = ['{', '}', '(', ')', '[', ']', ',', '.', ';', ':']

# Captura el código fuente del usuario
def capturar_codigo():
    print("Ingrese su código. Presione Enter dos veces para finalizar.")
    lineas = []
    contador_enter = 0

    while True:
        linea = input()
        if linea == "":
            contador_enter += 1
            if contador_enter == 2:
                break
        else:
            contador_enter = 0
            lineas.append(linea)

    return "\n".join(lineas)

# Clasificación de tokens
def clasificar_token(token):
    if token in operadores_logicos:
        return 'OPERADOR_LOGICO'
    elif token in operadores_aritmeticos:
        return 'OPERADOR_ARITMETICO'
    elif token in operadores_relacionales:
        return 'OPERADOR_RELACIONAL'
    elif token in operadores_asignacion:
        return 'OPERADOR_ASIGNACION'
    elif token in palabras_clave:
        return 'PALABRA_CLAVE'
    elif token.isdigit() or (token.replace('.', '', 1).isdigit() and token.count('.') < 2):
        return 'NUMERO'
    elif (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'")):
        return 'CADENA'
    elif token in puntuacion:
        return 'PUNTUACION'
    elif token.isidentifier():
        return 'IDENTIFICADOR'
    else:
        return 'DESCONOCIDO'

# Analizador léxico
def analizador_lexico(codigo):
    tokens = []
    token_actual = ''
    cadena_abierta = False

    for caracter in codigo:
        if caracter in ['"', "'"]:
            if cadena_abierta:
                token_actual += caracter
                tokens.append(token_actual)
                token_actual = ''
                cadena_abierta = False
            else:
                if token_actual:
                    tokens.append(token_actual)
                token_actual = caracter
                cadena_abierta = True
        elif cadena_abierta:
            token_actual += caracter
        elif caracter.isspace() or caracter in puntuacion + operadores_aritmeticos + operadores_relacionales + operadores_asignacion:
            if token_actual:
                tokens.append(token_actual)
                token_actual = ''
            if caracter in puntuacion + operadores_aritmeticos + operadores_relacionales + operadores_asignacion:
                tokens.append(caracter)
        else:
            token_actual += caracter

    if token_actual:
        tokens.append(token_actual)

    return tokens

# Estructura de un nodo del árbol sintáctico
class NodoArbol:
    def __init__(self, valor, hijos=None):
        self.valor = valor
        self.hijos = hijos if hijos else []

# Función para dibujar el árbol sintáctico utilizando matplotlib
def dibujar_arbol_grafico(nodo, posiciones=None, nivel=0, x=0.5, dx=0.25, ax=None):
    if posiciones is None:
        posiciones = {}

    posiciones[nodo] = (x, 1 - nivel * 0.1)

    for i, hijo in enumerate(nodo.hijos):
        x_hijo = x - dx / 2 + i * dx
        dibujar_arbol_grafico(hijo, posiciones, nivel + 1, x_hijo, dx / 2, ax)
        ax.plot([posiciones[nodo][0], posiciones[hijo][0]], [posiciones[nodo][1], posiciones[hijo][1]], color="black", lw=2)

    ax.text(posiciones[nodo][0], posiciones[nodo][1], str(nodo.valor), fontsize=16, ha='center', va='center', bbox=dict(boxstyle="circle", facecolor="white", edgecolor="black"))

def crear_arbol_grafico(raiz):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    dibujar_arbol_grafico(raiz, ax=ax)
    plt.show()

# Analizador sintáctico que genera el árbol
def analizador_sintactico(tokens):
    indice = 0
    longitud = len(tokens)

    def siguiente_token():
        nonlocal indice
        if indice < longitud:
            token = tokens[indice]
            indice += 1
            return token
        return None

    def peek_token():
        if indice < longitud:
            return tokens[indice]
        return None

    def es_factor():
        token = siguiente_token()
        if clasificar_token(token) == 'NUMERO':
            return NodoArbol(token)
        elif token == '(':
            nodo_expresion = es_expresion()
            if siguiente_token() == ')':
                return nodo_expresion
        return None

    def es_termino():
        nodo_factor = es_factor()
        if nodo_factor is None:
            return None

        while peek_token() in ['*', '/']:
            operador = siguiente_token()
            nodo_derecha = es_factor()
            if nodo_derecha is None:
                return None
            nodo_factor = NodoArbol(operador, [nodo_factor, nodo_derecha])
        return nodo_factor

    def es_expresion():
        nodo_termino = es_termino()
        if nodo_termino is None:
            return None

        while peek_token() in ['+', '-']:
            operador = siguiente_token()
            nodo_derecha = es_termino()
            if nodo_derecha is None:
                return None
            nodo_termino = NodoArbol(operador, [nodo_termino, nodo_derecha])
        return nodo_termino

    arbol_sintactico = es_expresion()

    if arbol_sintactico is None or siguiente_token() is not None:
        return "Error sintáctico en la expresión.", None

    return "Análisis sintáctico completado sin errores.", arbol_sintactico

# Bucle principal para el analizador léxico y sintáctico
while True:
    codigo_usuario = capturar_codigo()

    # Realiza el análisis léxico
    tokens = analizador_lexico(codigo_usuario)

    # Clasificar y mostrar tokens
    diccionario_tokens = {
        'OPERADOR_LOGICO': [], 'OPERADOR_ARITMETICO': [], 'OPERADOR_RELACIONAL': [],
        'OPERADOR_ASIGNACION': [], 'PALABRA_CLAVE': [], 'IDENTIFICADOR': [],
        'NUMERO': [], 'CADENA': [], 'PUNTUACION': [], 'DESCONOCIDO': []
    }

    for token in tokens:
        tipo_token = clasificar_token(token)
        diccionario_tokens[tipo_token].append(token)

    for tipo_token, valores in diccionario_tokens.items():
        if valores:
            print(f"{tipo_token}: {', '.join(valores)}")

    # Realiza el análisis sintáctico
    resultado_sintactico, arbol_sintactico = analizador_sintactico(tokens)
    print(resultado_sintactico)

    # Imprimir y dibujar el árbol si no hubo errores
    if arbol_sintactico:
        crear_arbol_grafico(arbol_sintactico)

    # Preguntar si el usuario desea salir
    salir = input("¿Desea salir? (s/n): ")
    if salir.lower() == 's':
        break
