# Execute min_times_k for several values of n and k

from min_times_k_algor import MinTimesK

def csvline(filehandler,*args):
    string = ";".join(map(str,args)) + "\n"
    filehandler.write(string)

# Con esto preparamos el fichero report.csv
# y lo marcamos como escritura: 'w' (write)
f = open('report.csv', 'w')

# csvline(f,10,20,[[1,2]])
# csvline(f,11,21,[[2,2]],"pepe")

# Cerramos el fichero
# f.close()

## output del programa
# 10,20,[[1, 2]]
# 11,21,[[2, 2]],pepe


for n in range(2,40):
	for k in range(2,n+1):
	
		min_t_k = MinTimesK(n,k)
		min_t_k.solve()

		csvline(f, n, k, min_t_k.results.min_times_k())

		print "loop:",n,k

		# print n, k, min_t_k.results.min_times_k()

f.close()
