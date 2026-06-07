import time
import random
import customtkinter as ctk
from funciones import esPar, resultadosATexto
from PIL import Image

#---pip install customtkinter---#

app = ctk.CTk()
app.title("Timba")
app.geometry("1200x800")


buttons = {}            #clave=numero, valor=boton, son los 36 numeros
botones_columna = []      #indice=columna, [indice]=boton, son los 3 de abajo

numero_actual = None     #ultimo numero que salió en la ruleta
ficha_actual = None      #ultimo ficha usada, (nombre, boton)
resultados = []       #numeros que salieron

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
                         "BLACK":none_2}              #ejemplo= diccionarioDeApuestas["36"] = (multiplicador, apuesta_actual sin multiplicador), todo str, las claves son el nombre del boton

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
    
def spin():                            #para hacer la tirada
    global numero_actual
    global resultados

    if(apuesta>saldo or saldo==0):           #falta apuesta==0
        print("flaco...")
        return 

    if(numero_actual!=None):
        resultados.append(numero_actual)

    numero_actual = random.randint(0, 36)
    time.sleep(3)
    button_numero.configure(text=str(numero_actual))
    if(len(resultados)<11):
        button_resultados.configure(text=resultadosATexto(resultados))
    else:
        button_resultados.configure(text=resultadosATexto(resultados[-10:]))

def elegir_ficha(boton, color_borde, nombre):

    global ficha_actual

    if(ficha_actual!=None):
        ficha_actual[1].configure(border_color="#8B4513")

    ficha_actual = (nombre, boton)
    boton.configure(border_color=color_borde)

def posicionar_ficha(boton, frame):            #---------ARREGLAR-------------
    
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
    boton_apuesta = diccionarioDeApuestas[texto_boton][1]     #plata puesto sobre la apuesta, None o algo anterior
    boton_ficha_texto = diccionarioDeFichas[ficha]    #texto de la ficha, es el numero

       
    nuevo_texto = str(int(boton_ficha_texto) + boton_apuesta)  #anterior + el nuevo
    diccionarioDeApuestas[texto_boton] = (diccionarioDeApuestas[texto_boton][0], int(nuevo_texto)) 

    boton_info = boton.grid_info()      #info del boton

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

#---------------------0-------------------------------#
button_0 = ctk.CTkButton(numeros_frame, 
                         text="0", 
                         text_color="white", 
                         fg_color="green", 
                         hover_color="green", 
                         border_width=2, 
                         border_color="black", font=("Arial", 20),
                         command=lambda: posicionar_ficha(button_0, numeros_frame))
button_0.grid(row=0, column=0, columnspan=3, sticky="nswe")

#--------numeros (sin el 0)---------------------#

fila_inicio = 1
columna_inicio = 0

for i in range(1, 37):
    color = esPar(i)
    button = ctk.CTkButton(numeros_frame, 
                           text=str(i), 
                           text_color="white", 
                           fg_color=color, 
                           hover_color=color, 
                           border_width=2, 
                           border_color="black",
                           font=("Arial", 20),
                           command=lambda b=i: posicionar_ficha(buttons[b], numeros_frame))
    button.grid(row=fila_inicio, column=columna_inicio,padx=0, pady=0, sticky="nswe")

    diccionarioDeApuestas[str(i)] = none_36

    buttons[i] = button

    columna_inicio+=1
    if(columna_inicio==3):
        columna_inicio=0
        fila_inicio+=1

#---------fila-2 to 1----------------------#

for i in range(3):
    button = ctk.CTkButton(numeros_frame, 
                           text="2 TO 1", 
                           text_color="white", 
                           fg_color="green", 
                           hover_color="green", 
                           border_width=2, 
                           border_color="black",
                           font=("Arial", 20),
                           command=lambda b=i: posicionar_ficha(botones_columna[b], numeros_frame))
    button.grid(row=13, column=i,padx=0, pady=0, sticky="nswe")
    diccionarioDeApuestas["2 TO 1"] = none_3
    botones_columna.append(button)


#----------fila-apuestas-----------------------------------------------------------------------------------------------------------------------------
button_1_18 = ctk.CTkButton(apuestas_frame, text="1\n\nT\nO\n\n18", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 17), command=lambda: posicionar_ficha(button_1_18, apuestas_frame))
button_1_18.grid(row=1, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

button_even = ctk.CTkButton(apuestas_frame, text="E\nV\nE\nN", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20), command=lambda: posicionar_ficha(button_even, apuestas_frame))
button_even.grid(row=3, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

button_red = ctk.CTkButton(apuestas_frame, text="RED", text_color="red", fg_color="red", hover_color="red", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20), command=lambda: posicionar_ficha(button_red, apuestas_frame))
button_red.grid(row=5, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

button_black = ctk.CTkButton(apuestas_frame, text="BLACK", text_color="black", fg_color="black", hover_color="black", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20), command=lambda: posicionar_ficha(button_black, apuestas_frame))
button_black.grid(row=7, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

button_odd = ctk.CTkButton(apuestas_frame, text="O\nD\nD", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20), command=lambda: posicionar_ficha(button_odd, apuestas_frame))
button_odd.grid(row=9, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

button_19_36 = ctk.CTkButton(apuestas_frame, text="19\n\nT\nO\n\n36", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 17), command=lambda: posicionar_ficha(button_19_36, apuestas_frame))
button_19_36.grid(row=11, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

#-----------fila-mitades--------------------------------------------------------------------------------------------------------------------------#
button_1st_12 = ctk.CTkButton(apuestas_frame, text="1\nS\nT\n\n12", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20), command=lambda: posicionar_ficha(button_1st_12, apuestas_frame))
button_1st_12.grid(row=1, column=1, rowspan=4, padx=0, pady=0, sticky="nsew")

button_2nd_12 = ctk.CTkButton(apuestas_frame, text="2\nN\nD\n\n12", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20), command=lambda: posicionar_ficha(button_2nd_12, apuestas_frame))
button_2nd_12.grid(row=5, column=1, rowspan=4, padx=0, pady=0, sticky="nsew")

button_3rd_12 = ctk.CTkButton(apuestas_frame, text="3\nR\nD\n\n12", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20), command=lambda: posicionar_ficha(button_3rd_12, apuestas_frame))
button_3rd_12.grid(row=9, column=1, rowspan=4, padx=0, pady=0, sticky="nsew")

#--------------------------------------------FRAME-OPCIONES---------------------------------------------------------------------------------------------------------------------------#

button_clear_last = ctk.CTkButton(opciones_frame, text="CLEAR", text_color="white", fg_color="black", width=190, command=lambda: clear_apuesta(True))
button_clear_last.place(relx=0.34, rely=0.85, anchor="center")

button_clear_all = ctk.CTkButton(opciones_frame, text="CLEAR ALL", text_color="white", fg_color="black", width=190, command=lambda: clear_apuesta(False))
button_clear_all.place(relx=0.34, rely=0.89, anchor="center")

button_apuesta_text = ctk.CTkButton(opciones_frame, text="BETS", text_color="white", fg_color="black",hover_color="black", width=20)
button_apuesta_text.place(relx=0.17, rely=0.93, anchor="center")

button_apuesta = ctk.CTkButton(opciones_frame, text="$ "+str(apuesta), text_color="white", fg_color="black", hover_color="black",border_width=1, border_color="black")
button_apuesta.place(relx=0.4, rely=0.93, anchor="center")

button_saldo_text = ctk.CTkButton(opciones_frame, text="PAID", text_color="white", fg_color="black",hover_color="black", width=20)
button_saldo_text.place(relx=0.17, rely=0.97, anchor="center")

button_saldo = ctk.CTkButton(opciones_frame, text="$ "+str(saldo), text_color="white", fg_color="black", hover_color="black",border_width=1, border_color="black")
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
entry_saldo.place(relx=0.6, rely=0.03)

button_entry_saldo = ctk.CTkButton(opciones_frame, 
                              text="Actualizar saldo", 
                              text_color="white", 
                              fg_color="black", 
                              border_width=1, 
                              border_color="grey",
                              width=140,
                              command=actualizar_saldo)
button_entry_saldo.place(relx=0.6, rely=0.07)

#---------------------------------------------------------FICHAS------------------------------------------------------------------------------#

ficha_celeste_png = ctk.CTkImage(light_image=Image.open("imagenes/celeste.png"), size=(70,70))
ficha_violeta_png = ctk.CTkImage(light_image=Image.open("imagenes/violeta.png"), size=(70,70))
ficha_roja_png = ctk.CTkImage(light_image=Image.open("imagenes/roja.png"), size=(70,70))
ficha_amarilla_png = ctk.CTkImage(light_image=Image.open("imagenes/amarilla.png"), size=(70,70))

button_celeste = ctk.CTkButton(opciones_frame, 
                              text="", 
                              text_color="white", 
                              fg_color="#8B4513",
                              hover_color="#8B4513", 
                              image=ficha_celeste_png,
                              border_width=1, 
                              border_color="#8B4513",
                              width=30,
                              command=lambda: elegir_ficha(button_celeste, "lightblue", "celeste"))
button_celeste.place(relx=0.55, rely=0.12)

button_violeta = ctk.CTkButton(opciones_frame, 
                              text="", 
                              text_color="white", 
                              fg_color="#8B4513",
                              hover_color="#8B4513", 
                              image=ficha_violeta_png,
                              border_width=1, 
                              border_color="#8B4513",
                              width=30,
                              command=lambda: elegir_ficha(button_violeta, "purple", "violeta"))
button_violeta.place(relx=0.76, rely=0.12)

button_roja = ctk.CTkButton(opciones_frame, 
                              text="", 
                              text_color="white", 
                              fg_color="#8B4513",
                              hover_color="#8B4513", 
                              image=ficha_roja_png,
                              border_width=1, 
                              border_color="#8B4513",
                              width=30,
                              command=lambda: elegir_ficha(button_roja, "red", "roja"))
button_roja.place(relx=0.55, rely=0.22)

button_amarilla = ctk.CTkButton(opciones_frame, 
                              text="", 
                              text_color="white", 
                              fg_color="#8B4513",
                              hover_color="#8B4513", 
                              image=ficha_amarilla_png,
                              border_width=1, 
                              border_color="#8B4513",
                              width=30,
                              command=lambda: elegir_ficha(button_amarilla, "yellow", "amarilla"))
button_amarilla.place(relx=0.76, rely=0.22)

app.mainloop()