# Con esto preparamos el fichero report.csv
# y lo marcamos como escritura: 'w' (write)
f = open('report.csv', 'w')

f.write("1") # Un "1" pero sin salto de linea
f.write("2\n") # un "2" pero con salto de linea

# la funcion write solo acepta strings, asi que si queremos imprimir un array
# lo tenemos que pasar a string
f.write(str([1,2]))

# Y salto de linea
f.write("\n")

# Cerramos el fichero
f.close()

## OUTPUT DEL PROGRAMA
# 12
# [1, 2]
