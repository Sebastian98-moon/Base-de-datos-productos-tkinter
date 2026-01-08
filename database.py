
import sqlite3
conexion = sqlite3.connect("Productos.db")

cursor= conexion.cursor()

cursor.execute('''
               create table if not exists Productos(
                   id integer primary key autoincrement,
                   nombre text not null,
                   precio real not null
               )''')
conexion.commit()

# ==========================

def agregarProducto(producto, precio):
    cursor.execute('''
        insert into productos(nombre, precio)
        values (?,?)
        ''',(producto, precio))
            
    conexion.commit()
                   
        
def verProducto():
    cursor.execute("select * from productos")
    resultado = cursor.fetchall()
    return resultado
    
    
def eliminarProducto(id):
                     
    cursor.execute("delete from productos where id =?",(id,)) #-- > El (id, ) hace que se genere una tupla y no se genere un error, ya el execute no lo toma como valido
    conexion.commit()
    return
        
def actualizarProducto(id, nuevo_nombre, nuevoPrecio):
    cursor.execute('''
                   update productos
                   set nombre = ?, precio = ?
                   where id = ? 
                   ''' ,(nuevo_nombre, nuevoPrecio, id))
    conexion.commit()
    return
         





