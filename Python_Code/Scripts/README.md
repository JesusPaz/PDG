# PDG - Beat de la Salsa
Proyecto de Grado de Jesús Hernando Paz Bolaños, estudiante de Ingeniería de Sistemas de la Universidad Icesi.

Nota: los scripts consumen directamente la base de datos, por lo tanto debe estar encendida. El archivo SesTotal.txt debe contener todos los logs generados.

Cuando las canciones ya sean marcadas por los usuarios es necesario ejecutar los siguientes scripts para limpiar los datos generados:

1) Check_bad_beats.py - Verifica que las canciones que tienen 3 repeticiones en realidad contengan esas 3 repeticiones, en caso contrario, va a imprimir las canciones que tienen datos faltantes. Lo que se debe hacer con esos datos es revisar los logs y ver si esa canción existe y no fue insertada en la base de datos, en caso de que no exista en los logs quiere decir que el usuario no marcó esa canción, por lo tanto es necesario reducir en uno la cantidad de repeticiones de esa canción.

2) Find_error_checksum_databeats.py  - Verifica los logs para encontrar inconsistencias en los datos, si las encuentra lee el log y lo reemplaza en la base de datos. El anterior script debe ejecutarse primero ya que si no se hace se van a presentar errores con inconsistencias en la cantidad de repeticiones.

Para la depuración de las canciones se deben ejecutar los siguientes archivos:

* find_gap.py    -   Se encarga de contar la cantidad de veces que aparece ese delay
* get_gap_hw.py  -   Calcula el delay del hardware para un usuario y para cada una de las sesiones y escribe los resultados.
* get_difference_between_delay.py  -   Encuentra la diferencia entre cada uno de los beats (ioi)

Después de ser ejecutados los anteriores scripts se debe abrir jupyter notebook y ejecutar los siguientes archivos que se encuentran en la carpeta PDG/Python_Code/Jupyter_Files/:

* Delay_Processing.ipynb - Jupyter notebook para procesar el delay 
* Heatmap + KDE.ipynb - Jupyter notebook para calcular el sharpe ratio

Para después regresar a esta carpeta y ejecutar los siguientes scripts:

* process_data_apply_dl_hw.py - aplica el delay del hardware a los datos 
* Move_txt_and_wav.py - mueve los datos procesados y tambien los archivos a formato wav para poder escucharlos en Pure Data
