def rojoONegro(n, black, red):
    if(n in black):
        return "black"
    if(n in red):
        return "red"
    return "green"
    
def resultadosATexto(lista):
    res = ""
    for elem in lista:
        res += str(elem)+"\n"
    return res


