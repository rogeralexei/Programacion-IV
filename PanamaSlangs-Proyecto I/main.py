#Resticciones:  Elaborar una aplicación de línea de comandos en Python que sirva cuyo propósito sea mantener un 
# diccionario de palabras del slang panameño (xopa, mopri, otras). Las palabras y su significado deben ser almacenadas 
# dentro de una base de datos SQLite. Las opciones dentro del programa deben incluir como mínimo: 
# a) Agregar nueva palabra, b) Editar palabra existente, c) Eliminar palabra existente, 
# d) Ver listado de palabras, e) Buscar significado de palabra, f) Salir

from functions import add,delete,edit,display,get_def,control,main

if __name__=="__main__":
    main(opcion=True)