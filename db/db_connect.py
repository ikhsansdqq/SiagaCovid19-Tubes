import mysql.connector

db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Hoodwink77!",
    "database": "covdb"
}

if __name__ == '__main__':
    try:
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            host_info = connection.get_server_info()
            print(f"Connected to: {host_info}")

            cursor = connection.cursor()
            query = "SELECT NIKPELAPOR, NAMAPELAPOR, NAMATERLAPOR, ALAMATTERLAPOR, GEJALA FROM DATASTORE"

            cursor.execute(query)

            rows = cursor.fetchall()

            for row in rows:
                print("-" * 20)
                print("NIK PELAPOR:", row[0])
                print("PELAPOR:", row[1])
                print("TERLAPOR:", row[2])
                print("ALAMAT:", row[3])
                print("GEJALA:", row[4])

    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
    finally:
        if connection.is_connected():
            print("")
            print("-" * 20)
            cursor.close()
            connection.close()
            print("Connection closed.")