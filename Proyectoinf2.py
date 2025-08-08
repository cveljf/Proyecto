import sqlite3
from tkinter import *
from tkinter import messagebox


def crear_base():
    conn = sqlite3.connect('sistema_entregas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
            telefono TEXT,
            email TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            fecha_envio TEXT NOT NULL,
            direccion_destino TEXT NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    ''')
    conn.commit()
    conn.close()

crear_base()


def agregar_cliente():
    if not nombre_cliente.get() or not direccion_cliente.get():
        messagebox.showerror("Error", "Nombre y dirección son obligatorios.")
        return
    conn = sqlite3.connect('sistema_entregas.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (nombre, direccion, telefono, email) VALUES (?, ?, ?, ?)',
                   (nombre_cliente.get(), direccion_cliente.get(), telefono_cliente.get(), email_cliente.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
    limpiar_campos_cliente()

def agregar_envio():
    if not cliente_id_envio.get() or not fecha_envio.get() or not direccion_envio.get() or not estado_envio.get():
        messagebox.showerror("Error", "Todos los campos de envío son obligatorios.")
        return
    try:
        conn = sqlite3.connect('sistema_entregas.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO envios (cliente_id, fecha_envio, direccion_destino, estado) VALUES (?, ?, ?, ?)',
                       (int(cliente_id_envio.get()), fecha_envio.get(), direccion_envio.get(), estado_envio.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Envío agregado correctamente.")
        limpiar_campos_envio()
    except ValueError:
        messagebox.showerror("Error", "ID de cliente debe ser un número.")

def mostrar_envios_clientes():
    conn = sqlite3.connect('sistema_entregas.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT clientes.id, clientes.nombre, envios.fecha_envio, envios.direccion_destino, envios.estado
        FROM clientes
        INNER JOIN envios ON clientes.id = envios.cliente_id
    ''')
    registros = cursor.fetchall()
    conn.close()
    if not registros:
        messagebox.showinfo("Registros", "No hay datos para mostrar.")
        return
    texto = ""
    for r in registros:
        texto += f"Cliente #{r[0]} - {r[1]} | Fecha: {r[2]} | Destino: {r[3]} | Estado: {r[4]}\n"
    messagebox.showinfo("Envíos y Clientes", texto)

def limpiar_campos_cliente():
    nombre_cliente.set("")
    direccion_cliente.set("")
    telefono_cliente.set("")
    email_cliente.set("")

def limpiar_campos_envio():
    cliente_id_envio.set("")
    fecha_envio.set("")
    direccion_envio.set("")
    estado_envio.set("")


ventana = Tk()
ventana.title("Sistema de Entregas - Grupo 12")
ventana.geometry("600x500")
ventana.config(bd=15)


nombre_cliente = StringVar()
direccion_cliente = StringVar()
telefono_cliente = StringVar()
email_cliente = StringVar()


cliente_id_envio = StringVar()
fecha_envio = StringVar()
direccion_envio = StringVar()
estado_envio = StringVar()


marco_clientes = LabelFrame(ventana, text="Alta de Clientes", padx=10, pady=10)
marco_clientes.pack(fill="x", pady=5)

Label(marco_clientes, text="Nombre:").grid(row=0, column=0, sticky="e")
Entry(marco_clientes, textvariable=nombre_cliente).grid(row=0, column=1)

Label(marco_clientes, text="Dirección:").grid(row=1, column=0, sticky="e")
Entry(marco_clientes, textvariable=direccion_cliente).grid(row=1, column=1)

Label(marco_clientes, text="Teléfono:").grid(row=2, column=0, sticky="e")
Entry(marco_clientes, textvariable=telefono_cliente).grid(row=2, column=1)

Label(marco_clientes, text="Email:").grid(row=3, column=0, sticky="e")
Entry(marco_clientes, textvariable=email_cliente).grid(row=3, column=1)

Button(marco_clientes, text="Agregar Cliente", command=agregar_cliente).grid(row=4, columnspan=2, pady=5)


marco_envios = LabelFrame(ventana, text="Alta de Envíos", padx=10, pady=10)
marco_envios.pack(fill="x", pady=5)

Label(marco_envios, text="ID Cliente:").grid(row=0, column=0, sticky="e")
Entry(marco_envios, textvariable=cliente_id_envio).grid(row=0, column=1)

Label(marco_envios, text="Fecha de Envío (AAAA-MM-DD):").grid(row=1, column=0, sticky="e")
Entry(marco_envios, textvariable=fecha_envio).grid(row=1, column=1)

Label(marco_envios, text="Dirección Destino:").grid(row=2, column=0, sticky="e")
Entry(marco_envios, textvariable=direccion_envio).grid(row=2, column=1)

Label(marco_envios, text="Estado:").grid(row=3, column=0, sticky="e")
Entry(marco_envios, textvariable=estado_envio).grid(row=3, column=1)

Button(marco_envios, text="Agregar Envío", command=agregar_envio).grid(row=4, columnspan=2, pady=5)


Button(ventana, text="Mostrar Envíos con Clientes", command=mostrar_envios_clientes).pack(pady=10)

ventana.mainloop()
