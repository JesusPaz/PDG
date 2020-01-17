# PDG - Beat de la Salsa
Proyecto de Grado de Jesús Hernando Paz Bolaños, estudiante de Ingeniería de Sistemas de la Universidad Icesi.

Cada una de las carpetas contiene diferentes archivos, y corresponden a lo siguiente:

* Client_Delay_Only.py - Versión del cliente en donde solamente los usuarios realizan la calibración, no marcan canciones.
* Client_Final - copia.py - Version final del cliente con todas las funcionalidades.
* Server_Final.py - Version final del servidor con todas las funcionalidades.

# Despliegue del software. 

Se debe ubicar un computador conectado por medio de ethernet a la sala en donde se encuentren los computadores que van a tener la función de cliente. En este computador debe estar prendido XAMPP con la base de datos activa, después se debe ejecutar el archivo de python llamado Server_Final.py. Antes de realizar esto, se debe consultar cual es la ip actual del computador conectado a la red, esta IP debe ser modificada en el archivo en la línea 13, la variable llamada HOST.

Ya que el servidor se encuentra en línea es necesario ejecutar cada uno de los clientes. Para este procedimiento se debe ubicar el archivo Client_Final - copia.py el alguna carpeta del computador pero teniendo en cuenta que en esa misma ubicación debe estar ubicada la carpeta Audio, que contiene todas las canciones que se van a reproducir. Cuando esto esté preparado de debe cambiar en el archivo Client_Final - copia.py en la línea 78 la variable HOST por la IP del servidor, debe ser la misma que se cambió anteriormente en el archivo del servidor.

# Indicaciones a los usuarios.

Si el usuario nunca ha participado en el experimento es necesario insertarlo en la base de datos en la tabla usuarios, este procedimiento se puede realizar fácilmente usando phpMyAdmin. Luego el usuario debe ingresar su documento en el software y lo primero que aparece es la ronda de calibración, en esta el usuario va a escuchar una canción de muestra de 30 segundos donde debe marcar con la barra espaciadora donde sienta que están ubicadas las blancas en la canción. Esta calibración sirve para que el usuario practique y se sienta preparado para la ronda de canciones reales. 

Cuando el usuario acaba la calibración, va a proceder a escuchar 10 canciones de salsa reales en donde debe realizar el mismo procedimiento que es marcar las blancas en la canción. Este procedimiento se realiza hasta que el usuario acaba todas las canciones y puede elegir si continúa o descansa un momento. 

En el caso se al realizar una cancion aparezca al terminar un mensaje de que los datos del usuario no tienen la calidad necesaria quiere decir que el usuario está haciendo algo mal o la canción comienza tarde. En el código se encuentran los límites mínimos y máximos que se tiene de bpm, por lo tanto si ese número es menor o mayor al límite saltara el error y el usuario debe repetir la canción. Se le debe decir a los usuarios que comienzan a marcar el pulso desde el momento 0 de la canción, sin importar que no comience la música y hasta el final de la canción. 




