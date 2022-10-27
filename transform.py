
# -------------- IMPORTACION DE LIBRERIAS ------------------ #
import os
import sys
import re
import pandas as pd
import numpy as np
import chardet

# ------------- VARIABLES GLOBALES --------------------------#
ruta = 'C:/files/PI/Raw/' #ruta donde se cargan los archivos a transoformar
ruta_export = 'C:/files/PI/Out/' #ruta donde se colocan los archivos transformados





# -------------- PROCESOS DE TRANSFORMACION PARA CADA TIPO DE ARCHIVO ---------------- #
# en este ejemplo hacemos para .json y .csv #

def transform_json (nombre_archivo):
    ''' 
    Este es todo el subproceso de transformacion de los archivos json, partiendo desde el nombre del archivo
    entrega el archivo .csv transformado, en la carpeta: 'Out' (de acuerdo a la ruta establecida en la var global) 
    Es solo codigo, todos los comments de todo el proceso y las explicaciones estan en el archivo 'notebook precio json'
    '''
    
    codfecha = (nombre_archivo.split('.')[0])[-8:]
    fecha_carga = codfecha[0:4]+'/'+codfecha[4:6]+'/'+codfecha[6:8]    
    dfprecio = pd.read_json(str(ruta)+str(nombre_archivo))

    def sacar_espacios(df):
        '''
        Quitar espacios vacíos de de ambos lados de las cols con strings.
        '''
        sacar_espacios = lambda x: x.strip() if isinstance(x, str) else x
        return df.applymap(sacar_espacios)
    sacar_espacios(dfprecio)

    dfprecio['precio']=np.where(dfprecio['precio']=='',0,dfprecio['precio'])
    dfprecio['producto_id']=dfprecio['producto_id'].astype(str)
    dfprecio['sucursal_id']=dfprecio['sucursal_id'].astype(str)
    dfprecio['precio']=dfprecio['precio'].astype(float)
    dfprecio[dfprecio['precio'].isnull()|dfprecio['producto_id'].isnull()|dfprecio['sucursal_id'].isnull()]
    dfprecio[dfprecio['producto_id'].isnull()]
    lista_sin_cod_prod = dfprecio[dfprecio['sucursal_id'].isnull()].index.tolist()
    dfprecio.drop(lista_sin_cod_prod, inplace=True)
    dfprecio['cant']=dfprecio['producto_id'].apply(lambda x: len(str(x)))
    dfprecio['id2']=dfprecio['producto_id'].apply(lambda x: x[-13:])
    dfprecio['caractid2']=dfprecio['id2'].apply(lambda x: re.findall('\D',x))
    dfprecio.pop('cant')
    dfprecio.pop('id2')
    dfprecio.pop('caractid2')
    dfprecio_aux=dfprecio['sucursal_id'].str.split('-', expand=True)
    dfprecio_aux[0]=dfprecio_aux[0].astype(int)
    dfprecio_aux[1]=dfprecio_aux[1].astype(int)
    dfprecio_aux[2]=dfprecio_aux[2].astype(int)
    dfprecio_aux['sucursal_id']=dfprecio_aux[0].astype(str)+'-'+dfprecio_aux[1].astype(str)+'-'+dfprecio_aux[2].astype(str)
    dfprecio['sucursal_id']=dfprecio_aux['sucursal_id']
    dfprecio['fecha']=fecha_carga
    dfprecio.rename(columns={'producto_id': 'Id_Producto', 'sucursal_id': 'Id_Sucursal'}, inplace=True)
    dfprecio.insert(0, 'Id', 0)
    nombre_archivo_out = 'producto_precio_' + str(codfecha) + '.csv'
    dfprecio.to_csv(ruta_export+nombre_archivo_out, index=False, encoding='utf-8-sig')


def transform_csv (nombre_archivo):
    ''' 
    Este es todo el subproceso de transformacion de los archivos csv, partiendo desde el nombre del archivo
    entrega el archivo .csv transformado, en la carpeta: 'Out' (de acuerdo a la ruta establecida en la var global) 
    Es solo codigo, todos los comments de todo el proceso y las explicaciones estan en el archivo 'notebook precio csv'.
    '''
    codfecha = (nombre_archivo.split('.')[0])[-8:]
    fecha_carga = codfecha[0:4]+'/'+codfecha[4:6]+'/'+codfecha[6:8]
    archivo = open(str(ruta)+str(nombre_archivo), 'rb')
    rawdata=archivo.read()
    archivo.close()
    encod=chardet.detect(rawdata)['encoding']
    dfprecio = pd.read_csv(str(ruta)+str(nombre_archivo), encoding=encod)

    def sacar_espacios(df):
        '''
        Quitar espacios vacíos de de ambos lados de las cols con strings.
        '''
        sacar_espacios = lambda x: x.strip() if isinstance(x, str) else x
        return df.applymap(sacar_espacios)
    sacar_espacios(dfprecio)

    dfprecio['precio']=dfprecio['precio'].astype(float)
    dfprecio[dfprecio['precio'].isnull()|dfprecio['producto_id'].isnull()|dfprecio['sucursal_id'].isnull()]
    lista_sin_cod_prod = dfprecio[dfprecio['sucursal_id'].isnull()].index.tolist()
    dfprecio.drop(lista_sin_cod_prod, inplace=True)
    dfprecio['cant']=dfprecio['producto_id'].apply(lambda x: len(str(x)))
    dfprecio['id2']=dfprecio['producto_id'].apply(lambda x: x[-13:])
    dfprecio['caractid2']=dfprecio['id2'].apply(lambda x: re.findall('\D',x))
    dfprecio.pop('cant')
    dfprecio.pop('id2')
    dfprecio.pop('caractid2')
    dfprecio_aux=dfprecio['sucursal_id'].str.split('-', expand=True)
    dfprecio_aux[0]=dfprecio_aux[0].astype(int)
    dfprecio_aux[1]=dfprecio_aux[1].astype(int)
    dfprecio_aux[2]=dfprecio_aux[2].astype(int)
    dfprecio_aux['sucursal_id']=dfprecio_aux[0].astype(str)+'-'+dfprecio_aux[1].astype(str)+'-'+dfprecio_aux[2].astype(str)
    dfprecio['sucursal_id']=dfprecio_aux['sucursal_id']
    dfprecio['fecha']=fecha_carga
    dfprecio.rename(columns={'producto_id': 'Id_Producto', 'sucursal_id': 'Id_Sucursal'}, inplace=True)
    dfprecio.insert(0, 'Id', 0)
    nombre_archivo_out = 'producto_precio_' + str(codfecha) + '.csv'
    dfprecio.to_csv(ruta_export+nombre_archivo_out, index=False, encoding='utf-8-sig')



# -------------- PROGRAMA TRANSFORM ------------------ #
# en esta parte se hace la transformacion de los archivos y se entregan en la carpeta establecida

cont_dir_Raw = os.listdir(ruta) #obtengo el cont. del directorio en una lista

# para todos los archivos en el directorio efectúa la transformación que le corresponda y obtengo el resultado en la carpeta de salida
for i,j in enumerate(cont_dir_Raw):
    extension = cont_dir_Raw[i].split('.')[1]
    if extension == 'csv':
        transform_csv(cont_dir_Raw[i])
    elif extension == 'json':
        transform_json(cont_dir_Raw[i])
    else:
        print('No hay archivos factibles de carga.')

# falta toda la programacion de casos de errores y mover archivos procesados correctamente a otra carpeta.
