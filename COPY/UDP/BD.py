import pymysql

connection = pymysql.connect("127.0.0.1",
                             "admin",
                             "1539321441",
                             "beatsalsa",)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `databeats` (`FK_ID_CANCION`, `FK_CEDULA_USUARIO`, `BEATS`, `DELAY`, `FECHA`) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
        cursor.execute(sql, ("2","2", "betass","0.3255"))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

finally:
    connection.close()
