import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# Conexión a la base de datos MySQL
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='logistica_envios',
            user='root',
            password=''
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Error de conexión", f"No se puede conectar a la base de datos: {e}")
        return None

# Función para agregar un nuevo envío
def add_envio():
    numero_seguimiento = entry_numero_seguimiento.get()
    origen = entry_origen.get()
    destino = entry_destino.get()
    fecha_entrega = entry_fecha_entrega.get()
    estado = entry_estado.get()
    
    if numero_seguimiento and origen and destino and fecha_entrega:
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            query = """INSERT INTO Envios (NumeroSeguimiento, Origen, Destino, FechaEntregaPrevista, Estado) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (numero_seguimiento, origen, destino, fecha_entrega, estado))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Éxito", "Envío agregado correctamente.")
            clear_entries()
        except Error as e:
            messagebox.showerror("Error", f"Error al agregar el envío: {e}")
    else:
        messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")

# Función para mostrar todos los envíos
def show_envios():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Envios")
        records = cursor.fetchall()
        listbox_envios.delete(0, tk.END)
        for row in records:
            listbox_envios.insert(tk.END, row)
        cursor.close()
        connection.close()
    except Error as e:
        messagebox.showerror("Error", f"Error al mostrar los envíos: {e}")

# Función para actualizar el estado de un envío
def update_envio():
    id_envio = entry_id.get()
    nuevo_estado = entry_nuevo_estado.get()
    
    if id_envio and nuevo_estado:
        try:
            connection = connect_to_db()
            cursor = connection.cursor()
            query = "UPDATE Envios SET Estado = %s WHERE ID = %s"
            cursor.execute(query, (nuevo_estado, id_envio))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Éxito", "Estado del envío actualizado correctamente.")
            clear_entries()
        except Error as e:
            messagebox.showerror("Error", f"Error al actualizar el estado del envío: {e}")
    else:
        messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")

# Función para limpiar los campos de entrada
def clear_entries():
    entry_numero_seguimiento.delete(0, tk.END)
    entry_origen.delete(0, tk.END)
    entry_destino.delete(0, tk.END)
    entry_fecha_entrega.delete(0, tk.END)
    entry_estado.delete(0, tk.END)
    entry_id.delete(0, tk.END)
    entry_nuevo_estado.delete(0, tk.END)

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Gestión de Envíos")

# Etiquetas y campos de entrada
tk.Label(root, text="Número de Seguimiento").grid(row=0, column=0)
entry_numero_seguimiento = tk.Entry(root)
entry_numero_seguimiento.grid(row=0, column=1)

tk.Label(root, text="Origen").grid(row=1, column=0)
entry_origen = tk.Entry(root)
entry_origen.grid(row=1, column=1)

tk.Label(root, text="Destino").grid(row=2, column=0)
entry_destino = tk.Entry(root)
entry_destino.grid(row=2, column=1)

tk.Label(root, text="Fecha de Entrega Prevista").grid(row=3, column=0)
entry_fecha_entrega = tk.Entry(root)
entry_fecha_entrega.grid(row=3, column=1)

tk.Label(root, text="Estado").grid(row=4, column=0)
entry_estado = tk.Entry(root)
entry_estado.grid(row=4, column=1)
entry_estado.insert(0, "En tránsito")

# Botón para agregar envío
tk.Button(root, text="Agregar Envío", command=add_envio).grid(row=5, column=0, columnspan=2)

# Listbox para mostrar envíos
listbox_envios = tk.Listbox(root, width=100)
listbox_envios.grid(row=6, column=0, columnspan=2)

# Botón para mostrar envíos
tk.Button(root, text="Mostrar Envíos", command=show_envios).grid(row=7, column=0, columnspan=2)

# Actualizar estado de un envío
tk.Label(root, text="ID del Envío").grid(row=8, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=8, column=1)

tk.Label(root, text="Nuevo Estado").grid(row=9, column=0)
entry_nuevo_estado = tk.Entry(root)
entry_nuevo_estado.grid(row=9, column=1)

tk.Button(root, text="Actualizar Estado", command=update_envio).grid(row=10, column=0, columnspan=2)

# Ejecutar la aplicación
root.mainloop()
