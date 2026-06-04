import time
import random
import customtkinter as ctk
from funciones import esPar, resultadosATexto

#---pip install customtkinter---#

app = ctk.CTk()
app.title("Timba")
app.geometry("1200x800")


buttons = {}            #clave=numero, valor=boton, son los 36 numeros
botones_columna = []      #indice=columna, [indice] = boton, son los 3 de abajo

numero_actual = None     #ultimo numero que salió en la ruleta
resultados = []       #numeros que salieron

diccionarioDeApuestas = {}              #ejemplo= diccionarioDeApuestas["36"] = multiplicador, todo str, las claves son el nombre del boton
listaDeApuestasActuales = []          #ejemplo= listaDeApuestasActuales[i] = (nombreApuesta, apuesta)
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

    if(numero_actual!=None):
        resultados.append(numero_actual)

    numero_actual = random.randint(0, 36)
    time.sleep(3)
    button_numero.configure(text=str(numero_actual))
    if(len(resultados)<11):
        button_resultados.configure(text=resultadosATexto(resultados))
    else:
        button_resultados.configure(text=resultadosATexto(resultados[-10:]))


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
                         border_color="black", font=("Arial", 20))
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
                           font=("Arial", 20))
    button.grid(row=fila_inicio, column=columna_inicio,padx=0, pady=0, sticky="nswe")

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
                           font=("Arial", 20))
    button.grid(row=13, column=i,padx=0, pady=0, sticky="nswe")
    botones_columna.append(button)


#----------fila-apuestas-----------------------------------------------------------------------------------------------------------------------------
button_1_18 = ctk.CTkButton(apuestas_frame, text="1\n\nT\nO\n\n18", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 17))
button_1_18.grid(row=1, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

button_even = ctk.CTkButton(apuestas_frame, text="E\nV\nE\nN", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20))
button_even.grid(row=3, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

button_red = ctk.CTkButton(apuestas_frame, text="", text_color="white", fg_color="red", hover_color="red", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20))
button_red.grid(row=5, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

button_black = ctk.CTkButton(apuestas_frame, text="", text_color="white", fg_color="black", hover_color="black", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20))
button_black.grid(row=7, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

button_odd = ctk.CTkButton(apuestas_frame, text="O\nD\nD", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20))
button_odd.grid(row=9, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

button_19_36 = ctk.CTkButton(apuestas_frame, text="19\n\nT\nO\n\n36", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 17))
button_19_36.grid(row=11, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")

#-----------fila-mitades--------------------------------------------------------------------------------------------------------------------------#
button_1st_12 = ctk.CTkButton(apuestas_frame, text="1\nS\nT\n\n12", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20))
button_1st_12.grid(row=1, column=1, rowspan=4, padx=0, pady=0, sticky="nsew")

button_2nd_12 = ctk.CTkButton(apuestas_frame, text="2\nN\nD\n\n12", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20))
button_2nd_12.grid(row=5, column=1, rowspan=4, padx=0, pady=0, sticky="nsew")

button_3rd_12 = ctk.CTkButton(apuestas_frame, text="3\nR\nD\n\n12", text_color="white", fg_color="green", hover_color="green", width=50, height=200, border_width=1, border_color="black", font=("Arial", 20))
button_3rd_12.grid(row=9, column=1, rowspan=4, padx=0, pady=0, sticky="nsew")

#--------------------------------------------FRAME-OPCIONES---------------------------------------------------------------------------------------------------------------------------#

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

app.mainloop()