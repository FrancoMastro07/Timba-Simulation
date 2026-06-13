import random
import pygame
import customtkinter as ctk
from funciones import rojoONegro, resultadosATexto
from PIL import Image

#---pip install customtkinter pillow pygame---#

app = ctk.CTk()
app.title("Timba")
app.geometry("1200x800")

pygame.mixer.init()
alarma = pygame.mixer.Sound("sonidos/alarma.wav")
bola = pygame.mixer.Sound("sonidos/bola.wav")
bola.set_volume(0.3)


buttons = {}            #clave=numero, valor=boton, son los 36 numeros
botones_columna = []      #indice=columna, [indice]=boton, son los 3 de abajo

numero_actual = None     #ultimo numero que salió en la ruleta
ficha_actual = None      #ultimo ficha usada, (nombre, boton)
ganaste = False

resultados = []       #numeros que salieron
black = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35] 
red = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]

ruleta_numeros = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26]

diccionarioRuleta = {}           #guarda por cada numero de la ruleta, la imagen si salio, y la de si no salio

for numero in ruleta_numeros:
    imagen1 = ctk.CTkImage(light_image=Image.open("imagenes/salio/"+str(numero)+".png"), size=(240,240))
    imagen2 = ctk.CTkImage(light_image=Image.open("imagenes/no_salio/"+str(numero)+".png"), size=(240,240))
    diccionarioRuleta[numero] = (imagen1, imagen2)

none_36 = (36, 0)
none_3 = (3, 0)
none_2 = (2, 0)

diccionarioDeApuestas = {"0":none_36,
                         "1\nS\nT\n\n12":none_3,
                         "2\nN\nD\n\n12":none_3,
                         "3\nR\nD\n\n12":none_3,
                         "1\n\nT\nO\n\n18":none_2,
                         "E\nV\nE\nN":none_2,
                         "O\nD\nD":none_2,
                         "19\n\nT\nO\n\n36":none_2,
                         "RED":none_2,
                         "BLACK":none_2}              #ejemplo= diccionarioDeApuestas["36"] = (multiplicador, apuesta_actual (x 10) sin multiplicador), todo str, las claves son el nombre del boton

diccionarioDeFichas = {"celeste":1,      #clave=color, valor=numero_base       todos se multiplican por diez despues para saber la apuesta
                       "violeta":2,      
                       "roja":5,
                       "amarilla":10}              

listaDeApuestasActuales = []          #ejemplo= listaDeApuestasActuales[i] = (nombreApuesta, apuesta, boton_apuesta), por si quiero tirar para atras una apuesta

apuesta = 0          #apuesta total actual
saldo = 0             #saldo actual

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

#-------------------------------------FUNCIONES------------------------------------------------------------#

def actualizar_saldo():           #actualiza el saldo del paid
    global saldo
    texto = entry_saldo.get()
    if(texto.isdigit()):
        saldo += int(texto)
        button_saldo.configure(text="$ "+str(saldo))

    else:
        print("Error")

def evaluar_apuesta(nombre_apuesta, numero):     #evalua el valor conseguido con el numero y la apuesta hecha, NO ME GUSTA COMO QUEDÓ

    global ganaste

    cantidad_apuesta = diccionarioDeApuestas[nombre_apuesta][1] * 10  #plata apostada x 10
    multiplicador = diccionarioDeApuestas[nombre_apuesta][0]     #multiplicador de la apuesta
    evaluacion = cantidad_apuesta * multiplicador

    if(nombre_apuesta=="1\n\nT\nO\n\n18"):    #apuesta 1 to 18
        if(numero>=1 and numero<=18):
            ganaste = True
            return evaluacion
        
    if(nombre_apuesta=="E\nV\nE\nN"):    #apuesta even
        if(numero%2==0 and numero!=0):
            ganaste = True
            return evaluacion

    if(nombre_apuesta=="RED"):     #apuesta red
        if(rojoONegro(numero, black, red)=="red"):
            ganaste = True
            return evaluacion
    
    if(nombre_apuesta=="BLACK"):         #apuesta black
        if(rojoONegro(numero, black, red)=="black"):
            ganaste = True
            return evaluacion
    
    if(nombre_apuesta=="O\nD\nD"):        #apuesta odd
        if(numero%2!=0 and numero!=0):
            ganaste = True
            return evaluacion

    if(nombre_apuesta=="19\n\nT\nO\n\n36"):   #apuesta 19 to 36
        if(numero>=19 and numero<=36):
            ganaste = True
            return evaluacion
    
    if(nombre_apuesta=="1\nS\nT\n\n12"):      #apuesta 1st 12
        if(numero>=1 and numero<=12):
            ganaste = True
            return evaluacion
        
    if(nombre_apuesta=="2\nN\nD\n\n12"):        #apuesta 2nd 12
        if(numero>=13 and numero<=24):
            ganaste = True
            return evaluacion

    if(nombre_apuesta=="3\nR\nD\n\n12"):      #apuesta 3rd 12
        if(numero>=25 and numero<=36):
            ganaste = True
            return evaluacion
    
    if(nombre_apuesta.isdigit()):          #apuesta del 0 al 36
        if(nombre_apuesta==str(numero)):
            ganaste = True
            return evaluacion

    if(nombre_apuesta=="2 TO 1 1"):      #apuesta columna 1
        if(numero in list(range(1, 37, 3))):
            ganaste = True
            return evaluacion

    if(nombre_apuesta=="2 TO 1 2"):      #apuesta columna 2
        if(numero in list(range(2, 37, 3))):
            ganaste = True
            return evaluacion

    if(nombre_apuesta=="2 TO 1 3"):      #apuesta columna 3
        if(numero in list(range(3, 37, 3))):
            ganaste = True
            return evaluacion

    return 0

def ruleta(i, espera):
    global saldo
    imagen = diccionarioRuleta[ruleta_numeros[i]][1]       #la imagen del numero si no salió
    button_ruleta.configure(image=imagen)      #actualizo

    bola.play()
    #winsound.PlaySound("sonidos/bola.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    if(i+1==len(ruleta_numeros)):
        espera+=1
        i=0
    else:
        i+=1
    if(espera<1 or numero_actual!=ruleta_numeros[i]):          #si la espera se pasó, y la imagen de la ruleta es igual al numero actual, entonces la pongo y sigo
        button_ruleta.after(100, lambda: ruleta(i, espera))
    else:                                                                         #si terminó la animacion de la ruleta termino con la funcion spin
        button_ruleta.configure(image=diccionarioRuleta[numero_actual][0])   
        button_numero.configure(text=str(numero_actual))
        
        #----------evaluar-apuesta------------------------------##

        for clave,valor in diccionarioDeApuestas.items():
            if (valor[1]>0):
                saldo += evaluar_apuesta(clave, numero_actual)
        
        if(ganaste):
            alarma.play(maxtime=5500)

        button_saldo.configure(text="$ "+str(saldo))
    
def spin():                            #para hacer la tirada
    global numero_actual
    global resultados
    global saldo
    global ganaste

    ganaste = False

    if(apuesta>saldo or saldo==0 or apuesta==0):          
        print("paga tio...")
        return 

    saldo -= apuesta                                 
    button_saldo.configure(text="$ "+str(saldo))

    #-------------sacar-numero--------------------------##
    if(numero_actual!=None):
        resultados.append(numero_actual)
    button_numero.configure(text="")

    numero_actual = random.randint(0, 36)

    if(len(resultados)<11):
        button_resultados.configure(text=resultadosATexto(resultados))
    else:
        button_resultados.configure(text=resultadosATexto(resultados[-10:]))
    #-------------------ruleta-------------------------#
    
    ruleta(0, 0)   #indice=0, espera=0

    

def elegir_ficha(boton, color_borde, nombre):

    global ficha_actual

    if(ficha_actual!=None):
        ficha_actual[1].configure(border_color="#8B4513")

    ficha_actual = (nombre, boton)
    boton.configure(border_color=color_borde)

def posicionar_ficha(boton, frame):            
    
    global ficha_actual
    global apuesta
    global saldo

    if(ficha_actual==None):    #si no elegiste ficha no jugas
        return
    
    ficha = ficha_actual[0]   #nombre de la ficha en string
    futura_apuesta = diccionarioDeFichas[ficha] * 10    #valor en pesos de la futura apuesta

    if(apuesta+futura_apuesta>saldo):        #si la apuesta actual mas la futura es mayor al saldo no podes seguir metiendo fichas
        return
    
    apuesta += futura_apuesta     #apuesto
    button_apuesta.configure(text="$ "+str(apuesta))   #recargo la apuesta

    texto_boton = boton.cget("text")     #nombre de la apuesta
    boton_info = boton.grid_info()      #info del boton

    if(texto_boton=="2 TO 1"):                #ARREGLO MONUMENTAL
        boton_columna = boton_info["column"]
        if(boton_columna==0):
            texto_boton = "2 TO 1 1"
        elif(boton_columna==1):
            texto_boton = "2 TO 1 2"
        else:
            texto_boton = "2 TO 1 3"

    boton_apuesta = diccionarioDeApuestas[texto_boton][1]     #plata puesto sobre la apuesta, None o algo anterior
    boton_ficha_texto = diccionarioDeFichas[ficha]    #texto de la ficha, es el numero

       
    nuevo_texto = str(int(boton_ficha_texto) + boton_apuesta)  #anterior + el nuevo
    diccionarioDeApuestas[texto_boton] = (diccionarioDeApuestas[texto_boton][0], int(nuevo_texto)) 

    boton_ficha = ctk.CTkButton(frame, 
                           text=nuevo_texto, 
                           text_color="white", 
                           fg_color="orange", 
                           hover_color="orange", 
                           border_width=2, 
                           border_color="black",
                           font=("Arial", 20),
                           width=30,
                           height=30)
    boton_ficha.grid(row=boton_info["row"], column=boton_info["column"])
    boton_ficha.lift()

    listaDeApuestasActuales.append((texto_boton, futura_apuesta, boton_ficha))
    
def clear_apuesta(decision):     #decision=True elimina el ultimo, decision=False elimina todas

    global apuesta
    global listaDeApuestasActuales
    global diccionarioDeApuestas

    if(len(listaDeApuestasActuales)==0):
        return
    
    i = len(listaDeApuestasActuales)-1
    while(i>=0):
        
        ultima_apuesta = listaDeApuestasActuales.pop()     #elimino la apuesta
        nombre_apuesta = ultima_apuesta[0]      #nombre de la apuesta
        apuesta -= ultima_apuesta[1]          #resto la ultima apuesta
        ultima_apuesta[2].destroy()          #elimino el boton
        button_apuesta.configure(text="$ "+str(apuesta))      #actualiza el grafico
        dict_apuesta = diccionarioDeApuestas[nombre_apuesta][1]      #ultimo valor guardado en la apuesta
        nuevo_valor = max(0, dict_apuesta-ultima_apuesta[1])    

        diccionarioDeApuestas[nombre_apuesta] = (diccionarioDeApuestas[nombre_apuesta][0], nuevo_valor)
        
        if(decision):
            return
        i -= 1

#..........................................................................FRAMES........................................................................................................................
timba_frame = ctk.CTkFrame(app, corner_radius=10, fg_color="green")
timba_frame.grid(row=0, column=0, sticky="nsew")

timba_frame.grid_rowconfigure(0, weight=1)
timba_frame.grid_columnconfigure(0, weight=1)
timba_frame.grid_columnconfigure(1, weight=1)


opciones_frame = ctk.CTkFrame(app, corner_radius=10, fg_color="#8B4513")
opciones_frame.grid(row=0, column=1, sticky="nsew")

#-----------------timba-subframes-------------------------------##

apuestas_frame = ctk.CTkFrame(timba_frame, fg_color="green")
apuestas_frame.grid(row=0, column=0, sticky="nsew")

numeros_frame = ctk.CTkFrame(timba_frame, fg_color="green")
numeros_frame.grid(row=0, column=1, sticky="nsew")


#--------------acomoda el tamaño de las filas y columnas-------#

for r in range(14):
    numeros_frame.grid_rowconfigure(r, weight=1)
    apuestas_frame.grid_rowconfigure(r, weight=1)
for c in range(3):
    numeros_frame.grid_columnconfigure(c, weight=1)

for c in range(2):
    apuestas_frame.grid_columnconfigure(c, weight=1)

#......................................................................BOTONES........................................................................................................#
#-----------------------------------------FRAME-TABLERO--------------------------------------------------#

def crear_botones_numeros(txt, fg, hv, comm_lamb, fila, columna, columna_extend):

    global buttons

    button = ctk.CTkButton(numeros_frame, 
                         text=txt, 
                         text_color="white", 
                         fg_color=fg, 
                         hover_color=hv, 
                         border_width=2, 
                         border_color="black", 
                         font=("Arial", 20),
                         command=comm_lamb)
    
    if(txt=="0"):
        button.configure(command=lambda: posicionar_ficha(button, numeros_frame))

    button.grid(row=fila, column=columna, columnspan=columna_extend, sticky="nswe")
    return button

#---------------------0-------------------------------#
button_0 = crear_botones_numeros("0", "green", "green", None, 0, 0, 3)

#--------numeros (sin el 0)---------------------#

fila_inicio = 1
columna_inicio = 0

for i in range(1, 37):
    color = rojoONegro(i, black, red)
    button = crear_botones_numeros(str(i), color, color, lambda b=i: posicionar_ficha(buttons[b], numeros_frame), fila_inicio, columna_inicio, 1)

    diccionarioDeApuestas[str(i)] = none_36

    buttons[i] = button

    columna_inicio+=1
    if(columna_inicio==3):
        columna_inicio=0
        fila_inicio+=1

#---------fila-2 to 1----------------------#

for i in range(3):
    button = crear_botones_numeros("2 TO 1", "green", "green", lambda b=i: posicionar_ficha(botones_columna[b], numeros_frame), 13, i, 1)
    diccionarioDeApuestas["2 TO 1 "+str(i+1)] = none_3    #2 TO 1 1 = columna 1
    botones_columna.append(button)                      #2 TO 1 2 = columna 2
                                                       #2 TO 1 3 = columna 3


#----------fila-apuestas-y-mitades---------------------------------------------------------------------------------------------------------------------------

def crear_boton_fila_apuestas(txt, txt_color, fg, hv, f, fila, columna, fila_extend):
    button = ctk.CTkButton(apuestas_frame,
                         text=txt,
                         text_color=txt_color,
                         fg_color=fg,
                         hover_color=hv,
                         width=50,
                         height=200,
                         border_width=1,
                         border_color="black",
                         font=("Arial", f))
    button.configure(command=lambda: posicionar_ficha(button, apuestas_frame))
    button.grid(row=fila, column=columna, rowspan=fila_extend, padx=0, pady=0, sticky="nsew")
    return button


button_1_18 = crear_boton_fila_apuestas("1\n\nT\nO\n\n18", "white", "green", "green", 17, 1, 0, 2)

button_even = crear_boton_fila_apuestas("E\nV\nE\nN", "white", "green", "green", 20, 3, 0, 2)

button_red = crear_boton_fila_apuestas("RED", "red", "red", "red", 20, 5, 0, 2)

button_black = crear_boton_fila_apuestas("BLACK", "black", "black", "black", 20, 7, 0, 2)

button_odd = crear_boton_fila_apuestas("O\nD\nD", "white", "green", "green", 20, 9, 0, 2)

button_19_36 = crear_boton_fila_apuestas("19\n\nT\nO\n\n36", "white", "green", "green", 17, 11, 0, 2)

button_1st_12 = crear_boton_fila_apuestas("1\nS\nT\n\n12", "white", "green", "green", 20, 1, 1, 4)

button_2nd_12 = crear_boton_fila_apuestas("2\nN\nD\n\n12", "white", "green", "green", 20, 5, 1, 4)

button_3rd_12 = crear_boton_fila_apuestas("3\nR\nD\n\n12", "white", "green", "green", 20, 9, 1, 4)

#--------------------------------------------FRAME-OPCIONES---------------------------------------------------------------------------------------------------------------------------#

button_clear_last = ctk.CTkButton(opciones_frame, text="CLEAR", text_color="white", fg_color="black", width=190, command=lambda: clear_apuesta(True))
button_clear_last.place(relx=0.34, rely=0.85, anchor="center")

button_clear_all = ctk.CTkButton(opciones_frame, text="CLEAR ALL", text_color="white", fg_color="black", width=190, command=lambda: clear_apuesta(False))
button_clear_all.place(relx=0.34, rely=0.89, anchor="center")

button_apuesta_text = ctk.CTkButton(opciones_frame, text="BETS", text_color="white", fg_color="black",hover_color="black", width=20)
button_apuesta_text.place(relx=0.17, rely=0.93, anchor="center")

button_apuesta = ctk.CTkButton(opciones_frame, text="$ "+str(apuesta), text_color="white", fg_color="black", hover_color="black", border_color="black")
button_apuesta.place(relx=0.4, rely=0.93, anchor="center")

button_saldo_text = ctk.CTkButton(opciones_frame, text="PAID", text_color="white", fg_color="black",hover_color="black", width=20)
button_saldo_text.place(relx=0.17, rely=0.97, anchor="center")

button_saldo = ctk.CTkButton(opciones_frame, text="$ "+str(saldo), text_color="white", fg_color="black", hover_color="black", border_color="black")
button_saldo.place(relx=0.4, rely=0.97, anchor="center")

button_spin = ctk.CTkButton(opciones_frame, 
                            text="SPIN", 
                            text_color="white", 
                            fg_color="grey", 
                            hover_color="grey",
                            border_width=1, 
                            border_color="black",
                            command=spin)
button_spin.place(relx=0.8, rely=0.97, anchor="center")

button_numero = ctk.CTkButton(opciones_frame, 
                              text="", 
                              text_color="white", 
                              fg_color="black", 
                              hover_color="black",
                              border_width=1, 
                              border_color="yellow",
                              width=60,
                              height=50,
                              font=("Arial", 20))
button_numero.place(relx=0.05, rely=0.03)

button_ruleta = ctk.CTkButton(opciones_frame, 
                              text="", 
                              text_color="#8B4513", 
                              fg_color="#8B4513", 
                              hover_color="#8B4513",
                              border_width=1, 
                              image=ctk.CTkImage(light_image=Image.open("imagenes/no_salio/0.png"), size=(240,240)),
                              border_color="#8B4513",
                              width=60,
                              height=50,
                              font=("Arial", 20))
button_ruleta.place(relx=0.29, rely=0.03)

button_resultados = ctk.CTkButton(opciones_frame, 
                              text="", 
                              text_color="white", 
                              fg_color="blue", 
                              hover_color="blue",
                              border_width=1, 
                              border_color="yellow",
                              width=60,
                              height=60,
                              font=("Arial", 20))
button_resultados.place(relx=0.05, rely=0.10)

entry_saldo = ctk.CTkEntry(opciones_frame, placeholder_text="Meté plata...")
entry_saldo.place(relx=0.6, rely=0.83)

button_entry_saldo = ctk.CTkButton(opciones_frame, 
                              text="Actualizar saldo", 
                              text_color="white", 
                              fg_color="black", 
                              border_width=1, 
                              border_color="grey",
                              width=140,
                              command=actualizar_saldo)
button_entry_saldo.place(relx=0.6, rely=0.87)

#---------------------------------------------------------FICHAS------------------------------------------------------------------------------#

def crear_ficha(dir, command_lambda, x, y):

    button = ctk.CTkButton(opciones_frame, 
                              text="", 
                              text_color="white", 
                              fg_color="#8B4513",
                              hover_color="#8B4513", 
                              image=ctk.CTkImage(light_image=Image.open(dir), size=(70,70)),
                              border_width=1, 
                              border_color="#8B4513",
                              width=30,
                              command=command_lambda)
    button.place(relx=x, rely=y)
    return button

button_celeste = crear_ficha("imagenes/fichas/celeste.png", lambda: elegir_ficha(button_celeste, "lightblue", "celeste"), 0.38, 0.35)

button_violeta = crear_ficha("imagenes/fichas/violeta.png", lambda: elegir_ficha(button_violeta, "purple", "violeta"), 0.60, 0.35)

button_roja = crear_ficha("imagenes/fichas/roja.png", lambda: elegir_ficha(button_roja, "red", "roja"), 0.38, 0.45)

button_amarilla = crear_ficha("imagenes/fichas/amarilla.png", lambda: elegir_ficha(button_amarilla, "yellow", "amarilla"), 0.60, 0.45)

app.mainloop()