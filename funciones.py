def esPar(n):
    if(n % 2 == 0):
        return "black"
    else: 
        return "red"
    
def resultadosATexto(lista):
    res = ""
    for elem in lista:
        res += str(elem)+"\n"
    return res
