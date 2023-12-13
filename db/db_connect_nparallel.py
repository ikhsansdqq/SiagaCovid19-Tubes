import asyncio
import aiomysql
import time

async def fetch_data():
    start_time = time.time()

    # Your MySQL configuration
    db_config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "Hoodwink77!",
        "db": "covdb"
    }

    nikpelapor_count = {}  # Dictionary to store the count of each NIKPELAPOR

    try:
        async with aiomysql.connect(**db_config) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT NIKPELAPOR, NAMAPELAPOR, NAMATERLAPOR, ALAMATERLAPOR, GEJALA FROM DATAIMPORTED")
                rows = await cursor.fetchall()

                for row in rows:
                    nikpelapor = row[0]

                    # Update count in the dictionary
                    nikpelapor_count[nikpelapor] = nikpelapor_count.get(nikpelapor, 0) + 1

                    # Display only if there are multiple entries for NIKPELAPOR
                    if nikpelapor_count[nikpelapor] > 1:
                        # Process each row (replace with your own processing logic)
                        print("NIKPELAPOR:", nikpelapor)
                        print("NAMAPELAPOR:", row[1])
                        print("NAMATERLAPOR:", row[2])
                        print("ALAMATERLAPOR:", row[3])
                        print("GEJALA:", row[4])
                        print()

    except aiomysql.Error as e:
        print("Error connecting to the database:", e)
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time} seconds")

async def main():
    await fetch_data()

if __name__ == '__main__':
    asyncio.run(main())
