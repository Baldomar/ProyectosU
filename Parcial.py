import tkinter as tk
from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
from PIL import Image, ImageTk

# Conexion
client = MongoClient("mongodb://root12023:root2023@localhost:27017/?authMechanism=DEFAULT")
db = client["Bodega"]
collection = db["Registros"]

# Funcion para insertar
def insertar_Registro():
    nombre = nombre_entry.get()
    edad = int(edad_entry.get())
    documento = {"nombre": nombre, "edad": edad}
    result = collection.insert_one(documento)
    messagebox.showinfo("Genial", f"Registro insertado con _id: {result.inserted_id}")

# Funcion para buscar
def buscar_Registro():
    resultados.delete(0, tk.END)
    for doc in collection.find():
        resultados.insert(tk.END, f"Nombre: {doc['nombre']}, Edad: {doc['edad']}")

# Funcion para actualizar
def actualizar_Registro():
    seleccionado = resultados.curselection()
    if seleccionado:
        indice = seleccionado[0]
        # Obtener el ID del documento seleccionado
        documento_id = collection.find()[indice]["_id"]
        # Obtener los nuevos valores para actualizar
        nuevo_nombre = nombre_entry.get()
        nueva_edad = int(edad_entry.get())
        # Actualizar el documento
        collection.update_one({"_id": documento_id}, {"$set": {"nombre": nuevo_nombre, "edad": nueva_edad}})
        messagebox.showinfo("Genial", "Registro actualizado correctamente.")
        buscar_Registro()
    else:
        messagebox.showerror("Error", "Seleccione un registro para actualizar.")

# Funcion para eliminar
def eliminar_Registro():
    seleccionado = resultados.curselection()
    if seleccionado:
        indice = seleccionado[0]
        documento_id = collection.find()[indice]["_id"]
        # Eliminar el documento
        collection.delete_one({"_id": documento_id})
        messagebox.showinfo("Genial", "Registro eliminado correctamente.")
        buscar_Registro()
    else:
        messagebox.showerror("Error", "Seleccione un registro para eliminar.")

#Funcion para limpiar los campos
def limpiar_campos():
    nombre_entry.delete(0, tk.END)
    edad_entry.delete(0, tk.END)

# Crear Ventana
ventana = tk.Tk()
ventana.title("Aplicacion CRUD de MongoDB")


# Cargar la imagen de fondo
background_image = Image.open("entorno_virtual/Fondo.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = Label(ventana, image=background_photo)
background_label.place(x=0, y=0, relwidth=1,relheight=1)

# Elementos de la GUI
fuente_negrita = ("Cambria", 12, "bold")
nombre_label = tk.Label(ventana, text="Nombre: ", bg='Black', fg='White',font=fuente_negrita)
nombre_entry = tk.Entry(ventana)
edad_label = tk.Label(ventana, text="Edad: ", bg='Black', fg='White',font=fuente_negrita)
edad_entry = tk.Entry(ventana)

# Contenedor para los botones
botones_frame = tk.Frame(ventana)

# Colores para los botones
color_insertar = "#8bff82" 
color_buscar = "dark gray"
color_actualizar = "yellow"
color_eliminar = "red"

# Fuente en negrita
fuente_negrita = ("Cambria", 11, "bold")
insertar_button = tk.Button(botones_frame, text="Insertar", command=insertar_Registro, bg=color_insertar, font=fuente_negrita)
buscar_button = tk.Button(botones_frame, text="Buscar", command=buscar_Registro, bg=color_buscar, font=fuente_negrita)
actualizar_button = tk.Button(botones_frame, text="Actualizar", command=actualizar_Registro, bg=color_actualizar, font=fuente_negrita)
eliminar_button = tk.Button(botones_frame, text="Eliminar", command=eliminar_Registro, bg=color_eliminar, font=fuente_negrita)
limpiar_button = tk.Button(botones_frame, text="Limpiar", command=limpiar_campos, font=fuente_negrita)
resultados = tk.Listbox(ventana, width=60, height=20)  # Ajuste de tamaño del Listbox

# Elementos de Ventana
nombre_label.pack(pady=5)
nombre_entry.pack(pady=5)
edad_label.pack(pady=5)
edad_entry.pack(pady=5)

# Empaquetar los botones en el contenedor en línea horizontal
buscar_button.pack(side=tk.LEFT, padx=5)
insertar_button.pack(side=tk.LEFT, padx=5)
actualizar_button.pack(side=tk.LEFT, padx=5)
eliminar_button.pack(side=tk.LEFT, padx=5)
limpiar_button.pack(side=tk.LEFT, padx=5)
botones_frame.pack(pady=10)  
resultados.pack()

# Tamaño
ventana.geometry("800x600")

# Iniciar
ventana.mainloop()


