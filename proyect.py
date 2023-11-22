import serial
import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from time import strftime

ser = serial.Serial('COM3', 9600)
# Conexion
client = MongoClient("mongodb://root12023:root2023@localhost:27017/?authMechanism=DEFAULT&authSource=admin")
db = client["Arduino"]
collection = db["TemperaturayHumedad"]

# Funcion para Recibir e imprimir los datos desde el arduino
def actualizar_etiqueta():
    data = ser.readline().decode('utf-8').rstrip()
    etiqueta.config(text="Dato recibido: " + data)
    root.after(1000, actualizar_etiqueta)

# Funcion para imprimir la fecha y hora en tiempo real
def actualizar_hora():
    string_hora = strftime('%H:%M:%S %p')
    etiqueta_hora.config(text=string_hora)
    string_fecha = strftime('%d/%m/%Y')
    etiqueta_fecha.config(text=string_fecha)
    root.after(1000, actualizar_hora)


def Guardar_Datos():
    Datos_Arduino = ser.readline().decode('utf-8').rstrip()
    Datos_Hora = strftime('%H:%M:%S %p')
    Datos_Fecha = strftime('%d/%m/%Y')
    documento = {"Datos": Datos_Arduino, "Fecha": Datos_Fecha,"Hora": Datos_Hora}
    result = collection.insert_one(documento)
    messagebox.showinfo("Genial", f"Documento insertado con id: {result.inserted_id}!")

def buscar_Datos():
    resultados.delete(0, tk.END)
    for doc in collection.find():
        resultados.insert(tk.END, f"Datos: {doc['Datos']},Fecha: {doc['Fecha']},Hora: {doc['Hora']}")

# Diseño de Ventana
root = tk.Tk()
root.title("Datos desde Arduino")
root.geometry("800x600")

# Elementos de la GUI
#-----------------------------------------Hora-----------------------------------------------------
etiqueta_hora = tk.Label(root, font=('calibri', 50, 'bold'), background='black', foreground='white')
etiqueta_hora.pack(anchor='center')
#-----------------------------------------Fecha------------------------------------------------------
etiqueta_fecha = tk.Label(root, font=('calibri', 50, 'bold'), background='red', foreground='black')
etiqueta_fecha.pack(anchor='center')
#----------------------------------------------Arduino-------------------------------------------------------------------
etiqueta = tk.Label(root, text="Esperando datos...",font=('calibri', 25, 'bold'), background='black', foreground='white')
etiqueta.pack(pady=10)

# Acuaizacion de los datos
actualizar_etiqueta()
actualizar_hora()

def cerrar_ventana():
    ser.close()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", cerrar_ventana)

insertar_button = tk.Button(root, text="Guardar", command=Guardar_Datos, bg="#8bff82",font = ("Arial Black", 11))
insertar_button.place(x=350, y=300)

buscar_button = tk.Button(root, text="Consultar", command=buscar_Datos,bg="#07FBEF",font = ("Arial Black", 11))
buscar_button.place(x=200, y=300)

resultados = tk.Listbox(root, width=70, height=10,font = ("Arial Black",10),fg="black")
resultados.place(x=150, y=400)
resultados.configure(bg="#ffffff")

# Iniciar el bucle principal de Tkinter
root.mainloop()