import serial
import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from time import strftime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

ser = serial.Serial('COM4', 9600)
# Conexion
client = MongoClient("mongodb://Jeison:root2023@localhost:27017/?authMechanism=DEFAULT")
db = client["Arduino"]
collection = db["TemperaturayHumedad"]

# Función para Recibir e imprimir los datos desde el Arduino
def actualizar_etiqueta():
    data = ser.readline().decode('utf-8').rstrip()
    etiqueta.config(text="Dato recibido: " + data)
    root.after(1000, actualizar_etiqueta)

# Función para imprimir la fecha y hora en tiempo real
def actualizar_hora():
    string_hora = strftime('%H:%M:%S %p')
    etiqueta_hora.config(text=string_hora)
    string_fecha = strftime('%d/%m/%Y')
    etiqueta_fecha.config(text=string_fecha)
    root.after(1000, actualizar_hora)

# Función para graficar los datos
def graficar_datos(i):
    resultados.delete(0, tk.END)
    datos_x, datos_y = [], []
    for doc in collection.find():
        datos_x.append(doc['Hora'])
        datos_y.append(float(doc['Datos']))

    ax.clear()
    ax.plot(datos_x, datos_y, label='Temperatura', marker='o', color='blue')
    ax.set_xlabel('Hora')
    ax.set_ylabel('Temperatura (°C)')
    ax.legend()

    # Retornar el objeto FigureCanvasTkAgg para evitar errores
    return FigureCanvasTkAgg(fig, master=root)

# Diseño de Ventana
root = tk.Tk()
root.title("Datos desde Arduino")
root.geometry("800x600")

# Elementos de la GUI
# -----------------------------------------Hora-----------------------------------------------------
etiqueta_hora = tk.Label(root, font=('calibri', 50, 'bold'), background='black', foreground='white')
etiqueta_hora.pack(anchor='center')
# -----------------------------------------Fecha------------------------------------------------------
etiqueta_fecha = tk.Label(root, font=('calibri', 50, 'bold'), background='red', foreground='black')
etiqueta_fecha.pack(anchor='center')
# ----------------------------------------------Arduino-------------------------------------------------------------------
etiqueta = tk.Label(root, text="Esperando datos...", font=('calibri', 25, 'bold'), background='black', foreground='white')
etiqueta.pack(pady=10)

# Acuaizacion de los datos
actualizar_etiqueta()
actualizar_hora()

# Configuración del gráfico en tiempo real
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, graficar_datos, interval=1000)  # Actualizar cada segundo

def cerrar_ventana():
    ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", cerrar_ventana)

insertar_button = tk.Button(root, text="Guardar", command=lambda: Guardar_Datos(), bg="#8bff82", font=("Arial Black", 11))
insertar_button.place(x=350, y=300)

buscar_button = tk.Button(root, text="Consultar", command=lambda: buscar_Datos(), bg="#07FBEF",
                          font=("Arial Black", 11))
buscar_button.place(x=200, y=300)

resultados = tk.Listbox(root, width=70, height=10, font=("Arial Black", 10), fg="black")
resultados.place(x=150, y=400)
resultados.configure(bg="#ffffff")

# Iniciar el bucle principal de Tkinter
root.mainloop()
