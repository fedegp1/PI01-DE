# -- librerias --
import os
import mysql.connector as mysql

# -- var globales --
ruta = 'C:/files/PI/Out/' #ruta donde se encuentran los archivos transformados
ruta_preq = 'C:/files/PI/' #ruta donde se ubica la prequery

# me conecto a la base de datos
db = mysql.connect(
    host = '127.0.0.1',
    user = 'root',
    passwd = '0000',
)
cursor = db.cursor() #instancio el cursor

# abro el prequery para hacer el LOAD almacenado en un archivo .txt llamado load_data
# llamo prequery al query de carga, pero al que le falta colocarle el nombre del archivo input.
archivo = open(str(ruta_preq)+'load_data.txt')
pre_query=archivo.read() 
archivo.close()


# --- PROGRAMA LOAD 
# en esta parte se hace la carga de los archivos y se quitan de la carpeta una vez cargados

cont_dir_Out = os.listdir(ruta) #obtengo el cont. del directorio en una lista
cursor.execute('USE pi01') # uso la bd


# para todos los archivos en el directorio efectúa la carga
for i,j in enumerate(cont_dir_Out):
    query = pre_query.replace('NOMBRE_DEL_ARCHIVO',str(ruta)+str(cont_dir_Out[i])) #completo el prequery y dejo el query armado
    cursor.execute(query) #ejecuto el query de load
    db.commit() #hago commit de los cambios
    os.remove(str(ruta)+str(cont_dir_Out[i])) #elimino el archivo para que no se repita la carga en la prox ejecucion del script

