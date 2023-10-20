import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar

# Crear o conectar a la base de datos
conn = sqlite3.connect("calendario.db")
cursor = conn.cursor()

# Crear tabla para usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)
""")

# Crear tabla para fechas importantes
cursor.execute("""
CREATE TABLE IF NOT EXISTS fechas (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    fecha TEXT,
    descripcion TEXT
)
""")
conn.commit()

# Función para registrar un nuevo usuario
def registrar_usuario():
    username = entry_registro_usuario.get()
    password = entry_registro_contrasena.get()
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    messagebox.showinfo("Éxito", "Usuario registrado con éxito")

# Función para iniciar sesión
def iniciar_sesion():
    username = entry_inicio_usuario.get()
    password = entry_inicio_contrasena.get()
    cursor.execute("SELECT id FROM usuarios WHERE username = ? AND password = ?", (username, password))
    user_id = cursor.fetchone()
    if user_id:
        # Destruye la ventana de inicio de sesión y crea la ventana principal
        root.destroy()
        crear_ventana_principal(user_id[0])
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

# Función para crear la ventana principal
def crear_ventana_principal(user_id):
    def agregar_fecha():
        fecha = calendar.get_date()
        descripcion = entry_descripcion.get()
        cursor.execute("INSERT INTO fechas (user_id, fecha, descripcion) VALUES (?, ?, ?)", (user_id, fecha, descripcion))
        conn.commit()
        messagebox.showinfo("Éxito", "Fecha agregada con éxito")
        cargar_fechas()

    def notificar_fechas_importantes():
        hoy = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("SELECT fecha, descripcion FROM fechas WHERE user_id = ? AND fecha = ?", (user_id, hoy))
        fecha = cursor.fetchone()
        if fecha:
            mensaje = f"Hoy es tu día importante, {fecha[1]}. ¡No se te pase, chicuelo!"
            messagebox.showinfo("Recordatorio", mensaje)

    def cargar_fechas():
        cursor.execute("SELECT id, fecha, descripcion FROM fechas WHERE user_id = ?", (user_id,))
        fechas = cursor.fetchall()
        listbox_fechas.delete(0, tk.END)
        for fecha in fechas:
            listbox_fechas.insert(tk.END, f"{fecha[1]} - {fecha[2]}")

    def editar_fecha():
        seleccion = listbox_fechas.curselection()
        if seleccion:
            id_fecha = listbox_fechas.get(seleccion[0]).split(" - ")[0]
            nueva_descripcion = entry_nueva_descripcion.get()
            cursor.execute("UPDATE fechas SET descripcion = ? WHERE id = ?", (nueva_descripcion, id_fecha))
            conn.commit()
            cargar_fechas()
            entry_nueva_descripcion.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Fecha editada con éxito")

    def borrar_fecha():
        seleccion = listbox_fechas.curselection()
        if seleccion:
            id_fecha = listbox_fechas.get(seleccion[0]).split(" - ")[0]
            cursor.execute("DELETE FROM fechas WHERE id = ?", (id_fecha,))
            conn.commit()
            cargar_fechas()
            entry_nueva_descripcion.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Fecha eliminada con éxito")

    # Crear la ventana principal
    root2 = tk.Tk()
    root2.title("Calendario de Fechas Importantes")

    # Calendario
    calendar = Calendar(root2, selectmode="day")
    calendar.pack()

    # Campos y botón para agregar fechas
    label_descripcion = tk.Label(root2, text="Descripción:")
    entry_descripcion = tk.Entry(root2)
    button_agregar = tk.Button(root2, text="Agregar Fecha", command=agregar_fecha)

    label_descripcion.pack()
    entry_descripcion.pack()
    button_agregar.pack()

    # Lista de fechas
    listbox_fechas = tk.Listbox(root2)
    listbox_fechas.pack()

    # Campos y botones para editar y borrar fechas
    label_nueva_descripcion = tk.Label(root2, text="Nueva Descripción:")
    entry_nueva_descripcion = tk.Entry(root2)
    button_editar = tk.Button(root2, text="Editar Fecha", command=editar_fecha)
    button_borrar = tk.Button(root2, text="Borrar Fecha", command=borrar_fecha)

    label_nueva_descripcion.pack()
    entry_nueva_descripcion.pack()
    button_editar.pack()
    button_borrar.pack()

    # Cargar fechas existentes
    cargar_fechas()

    # Notificar fechas importantes al inicio de la aplicación
    notificar_fechas_importantes()

    # Mostrar la ventana principal
    root2.mainloop()

# Crear la ventana de inicio de sesión
root = tk.Tk()
root.title("Iniciar Sesión o Registrar Usuario")

# Etiquetas y campos para registro
label_registro_usuario = tk.Label(root, text="Usuario (Registro):")
entry_registro_usuario = tk.Entry(root)
label_registro_contrasena = tk.Label(root, text="Contraseña (Registro):")
entry_registro_contrasena = tk.Entry(root, show="*")
button_registrar = tk.Button(root, text="Registrar Usuario", command=registrar_usuario)

label_registro_usuario.pack()
entry_registro_usuario.pack()
label_registro_contrasena.pack()
entry_registro_contrasena.pack()
button_registrar.pack()

# Etiquetas y campos para inicio de sesión
label_inicio_usuario = tk.Label(root, text="Usuario (Inicio de Sesión):")
entry_inicio_usuario = tk.Entry(root)
label_inicio_contrasena = tk.Label(root, text="Contraseña (Inicio de Sesión):")
entry_inicio_contrasena = tk.Entry(root, show="*")
button_iniciar_sesion = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion)

label_inicio_usuario.pack()
entry_inicio_usuario.pack()
label_inicio_contrasena.pack()
entry_inicio_contrasena.pack()
button_iniciar_sesion.pack()

root.mainloop()
