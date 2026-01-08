import tkinter as tk
from tkinter import messagebox # --> Cuadros de mensajes
from database import agregarProducto, verProducto, eliminarProducto, actualizarProducto # --> Funciones importadas 

# =================================================================================================



productosEnMemoria = [] #-- > Variable global que guarda la lista de productos de la BD

def agregarProductoDesdeTK():
    '''
    Obtiene los datos ingresados en los Entry de la interfaz gráfica
    y agrega un producto a la base de datos.

    - Valida que el nombre del producto no esté vacío.
    - Valida que el precio sea un número válido.
    - Valida que el precio sea mayor a cero.
    - Si ocurre un error, muestra un messagebox con el motivo.
    - Si los datos son correctos, llama a la función agregarProducto()
      y limpia los campos de entrada.
      
    '''

    producto = producto1texto.get() # --> Obtiene lo que se escribio en el ENTRY Producto1texto
    if producto == "":
        messagebox.showerror("Error", "El nombre del producto no puede estar vacio")
        return
    try:
        precio = float(precio1texto.get()) # --> Obiente el precio que se escribio en el ENTRY Precio1texto
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un numero valido.") # --> Muestra una ventana de error si se coloca algo que no sea una numero
        return
    if precio <=0:
        messagebox.showerror("Error", "El precio del producto no puede ser negativo") # --> Muestra una ventana de error si se coloca numeros negativos
        return
    agregarProducto(producto, precio)
    
    producto1texto.delete(0, tk.END)
    precio1texto.delete(0, tk.END)
   
def verProductosDesdeTk():
    '''
    Obtiene los productos desde la base de datos y los muestra
    en la Listbox de la interfaz gráfica.

    - Limpia la Listbox antes de cargar los datos.
    - Consulta los productos usando la función verProducto().
    - Guarda los productos en la variable global productosEnMemoria
      para poder reutilizarlos (por ejemplo, al eliminar un producto).
    - Inserta cada producto en la Listbox con un formato legible.
    
    '''
    
    global productosEnMemoria  # Convertimos la varible en global para poder modificarla
    
    listaProductos.delete(0, tk.END) # Esto elimina la lista antes de mostrarla para que aparezca vacio
    productosEnMemoria = verProducto()
    for P in productosEnMemoria:
        listaProductos.insert(tk.END, f"ID: {P[0]} | Producto: {P[1]} | Precio: ${P[2]:,.2f} ")
            
def borrarProductosDesdeTk():
    '''
    Elimina un producto seleccionado desde la Listbox de la interfaz gráfica.

    - Obtiene el índice del elemento seleccionado en la Listbox.
    - Valida que haya un producto seleccionado.
    - Usa el índice para acceder al producto correspondiente
      en la lista productosEnMemoria.
    - Extrae el ID del producto seleccionado.
    - Solicita confirmación al usuario mediante un messagebox.
    - Si el usuario confirma, elimina el producto de la base de datos,
      actualiza la Listbox y muestra un mensaje de confirmación.
      
      '''
      
    borrar = listaProductos.curselection() # --> Obtengo la posicion del producto en la lista
    if borrar == ():
        messagebox.showwarning("Error", "No seleccionaste ningun producto para eliminar")
        return
    n = borrar[0] # --> Creo una variable que obtiene el indice del producto seleccionado
    
    producto = productosEnMemoria[n] # --> Creo una varible que contiene la variable global pasandole el indice del produco seleccionado 
    id = producto[0] # --> Obtengo el indice del producto que seleccione
    
    respuesta = messagebox.askyesno("Borrar", "Desea elminar el producto seleccionado?")
    if respuesta:
        eliminarProducto(id)
        verProductosDesdeTk()
        messagebox.showinfo("Eliminado", f"{producto} eliminado correctamente") 
        
def actualizarProductoDesdeTk():
    '''
    Actualiza un producto seleccionado desde la interfaz gráfica (Tkinter).

    Esta función obtiene el producto seleccionado en la lista visual,
    valida los datos ingresados por el usuario (nombre y precio),
    y si todo es correcto, llama a la función que actualiza el producto
    en la base de datos.

    Validaciones realizadas:
    - Verifica que haya un producto seleccionado en la lista.
    - Comprueba que el nombre del producto no esté vacío.
    - Convierte el precio a número y valida que sea un valor válido.
    - Verifica que el precio sea mayor a cero.

    En caso de error, se muestra un mensaje al usuario mediante
    cuadros de diálogo y se cancela la operación.

    No retorna ningún valor.
    
    '''
    seleccionar = listaProductos.curselection()
    if seleccionar == ():
        messagebox.showwarning("Error", "No seleccionaste ningun producto para actualizar")
        return
    n = seleccionar[0]
    seleccion = productosEnMemoria[n]
    id = seleccion[0]
    
    producto = producto1texto.get()
    if producto == "":
        messagebox.showerror("Error", "El nombre del producto no puede estar vacio")
        return
    try:
        precio = float(precio1texto.get())
    except ValueError:
        messagebox.showerror("Error", "El precio del producto debe ser un numero valido")
        return
    if precio <=0:
        messagebox.showerror("Error", "El precio del producto no puede ser negativo")
        return
    
    actualizarProducto(id, producto, precio)
    producto = messagebox.showinfo("Actualizado", "Producto actualizado correctamente")
    producto1texto.delete(0, tk.END) # Hace que el producto actualizado se borre del Entry producto
    precio1texto.delete(0, tk.END) # Hace que el producto actulizado se borre del Entry precio
    
def controlar_botones_por_seleccion(event=None):
    '''
    Controla el estado de los botones según la selección de productos en la lista.

    Esta función verifica si el usuario seleccionó un producto en la lista
    de productos (Listbox). Dependiendo de si hay o no una selección,
    habilita o deshabilita los botones de eliminar y actualizar.

    Funcionamiento:
    - Si no hay ningún producto seleccionado, los botones se deshabilitan.
    - Si hay un producto seleccionado, los botones se habilitan.

    El parámetro `event` se utiliza para que la función pueda ser llamada
    desde un evento de Tkinter (por ejemplo, al hacer clic en la lista),
    aunque no se use directamente dentro de la función.

    No retorna ningún valor.
    
    '''
    cargar_productos_en_entry()
    activar = listaProductos.curselection() # Llamamos a la lista de productos con .Curselection()
    
    if activar:
        botonEliminar.config(state=tk.NORMAL)
        botonActualizar.config(state=tk.NORMAL)
    else:
        botonEliminar.config(state=tk.DISABLED)
        botonActualizar.config(state=tk.DISABLED)
        
    # ==== Forma funcional pero no simplificada ===
    
    # if activar == ():
    #     botonEliminar.config(state=tk.DISABLED) # Si la TUPLA se encuentra vacia el boton se desactiva
    # elif activar == (0, ): # Si la Tupla tiene algo el boton se habilita, ya que con (0, ) decimos que la tupla tiene algo dentro
    #     botonEliminar.config(state=tk.NORMAL)
    
    # if activar == ():
    #     botonActualizar.config(state=tk.DISABLED)
    # elif activar == (0, ):
    #     botonActualizar.config(state=tk.NORMAL) 
    
def cargar_productos_en_entry(event=None):
    '''
     Carga en los campos Entry los datos del producto seleccionado en la lista.

    Esta función obtiene el índice del producto seleccionado en el Listbox
    y utiliza esa posición para acceder a los datos almacenados en memoria.
    Luego, completa automáticamente los campos de texto (Entry) del nombre
    y del precio con la información del producto seleccionado.

    Funcionamiento:
    - Verifica que exista una selección en la lista de productos.
    - Obtiene el producto correspondiente desde la lista en memoria.
    - Limpia los campos Entry antes de insertar los nuevos valores.
    - Inserta el nombre y el precio del producto en sus respectivos Entry.

    El parámetro `event` permite que la función sea utilizada como manejador
    de eventos de Tkinter, por ejemplo al seleccionar un elemento del Listbox.

    No retorna ningún valor.
    '''
    
    ver = listaProductos.curselection() # --> La lista de productos obtiene el indice del producto que seleccione.
    global productosEnMemoria # --> Llamamos a la variente global que tiene los productos de la BD
    
    if ver == ():
        return
    n = ver[0]
    
    producto = productosEnMemoria[n]
    producto1texto.delete(0, tk.END) # --> Borramos la casilla del Entry del producto
    producto1texto.insert(0, producto[1]) # --> Agregamos el nuevo (o no) nombre del producto
    precio1texto.delete(0, tk.END) # --> Borramos la casilla del Entry del precio
    precio1texto.insert(0, producto[2]) # --> Ingresamos el nuevo precio 
   

# ===========================================================
     
ventana = tk.Tk()
frame_agregar = tk.Frame(ventana) # --> Creamos una FRAME que este dentro de la ventana principal (Ventana)
frame_agregar.grid(row=0, column=0, padx=20, pady=20, sticky="nw") # --> Lo posicionamos dentro de la ventana para poder verlo

frame_lista = tk.Frame(ventana) # --> Volvemos a crear otro FRAME que va a tener otros tipos de datos en la ventana
frame_lista.grid(row=0, column=1, padx=20, pady=20, sticky="nw")

# ===========================================================

# == Ventana para agregar productos ==

ventana.geometry("600x300")
ventana.title("Base de Datos de Productos")

producto1 = tk.Label(frame_agregar, text = "Ingrese el nombre del producto: ")
producto1.grid(row=1, column=0, sticky="w") # --> Con GRID posicionamos todo lo que este dentro de FRAME 

producto1texto = tk.Entry(frame_agregar)
producto1texto.grid (row=3, column=0, pady=5)

precio1 = tk.Label(frame_agregar, text ="Ingrese el precio: $")
precio1.grid(row=4, column=0, sticky="w")

precio1texto = tk.Entry(frame_agregar)
precio1texto.grid(row=5, column=0, pady=5)

botonAgregar = tk.Button(frame_agregar, text = "Agregar producto", command= agregarProductoDesdeTK)
botonAgregar.grid(row=7, column=0, pady=10)

# ===============================================================

# == Ventana para ver los productos y/o eliminar producto

listaProductos = tk.Listbox(frame_lista, width=50, height=10) 
listaProductos.grid(row=0, column=0, sticky="ns") # --> Configuro la posicion con GRID
listaProductos.bind('<<ListboxSelect>>', controlar_botones_por_seleccion) # Puede haber un solo BIND, lo optimo es hacer una funcion que tengro todos los botones que quieras desabilitar y/o hablitar, ya que los bind se superponen uno sobre otro.


scroll = tk.Scrollbar(frame_lista, orient="vertical") # --> Creo la Scrollbar
scroll.grid(row=0, column=1, sticky="ns")

listaProductos.config(yscrollcommand=scroll.set) # --> Configuro el metodo para que la lista de productos obtenga la posicion del Scrollbar
scroll.config(command=listaProductos.yview) # --> Configuto el metodo para que la Scrollbar se posicione sobre la lista de productos


botonVer = tk.Button(frame_lista, text = "Ver los productos", command=verProductosDesdeTk)
botonVer.grid(row=1, column=0, pady=10, sticky="w")

botonEliminar = tk.Button(frame_lista, text = "Eliminar seleccionado", command= borrarProductosDesdeTk, state=tk.DISABLED)
botonEliminar.grid(row=1, column=0, pady=10, sticky="e")

botonActualizar = tk.Button(frame_lista, text = "Actualizar el producto", state=tk.DISABLED, command=actualizarProductoDesdeTk)
botonActualizar.grid(row=2, column=0, pady=11, sticky='e')







ventana.mainloop()


