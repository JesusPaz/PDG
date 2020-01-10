# PDG - Beat de la Salsa
Proyecto de Grado de Jesús Hernando Paz Bolaños, estudiante de Ingeniería de Sistemas de la Universidad Icesi.

Nota: los scripts consumen directamente la base de datos, por lo tanto debe estar encendida. El archivo SesTotal.txt debe contener todos los logs generados.

Cuando las canciones ya sean marcadas por los usuarios es necesario ejecutar los siguientes scripts para limpiar los datos generados:

1) Check_bad_beats.py - Verifica que las canciones que tienen 3 repeticiones en realidad contengan esas 3 repeticiones, en caso contrario, va a imprimir las canciones que tienen datos faltantes.
2) Find_error_checksum_databeats.py  - Verifica los logs para encontrar inconsistencias en los datos, si las encuentra lee el log y lo reemplaza en la base de datos


Además, también se deben ejecutar estos scripts para obtener los datos necesarios para ejecutar los jupyter notebooks:

* find_gap.py    -   Se encarga de contar la cantidad de veces que aparece ese delay
* get_gap_hw.py  -   Calcula el delay del hardware para un usuario y para cada una de las sesiones y escribe los resultados.
* get_difference_between_delay.py  -   Encuentra la diferencia entre cada uno de los beats (ioi)
* 
