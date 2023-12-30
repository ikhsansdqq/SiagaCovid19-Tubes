import asyncio
import aiomysql
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_data_row(nikpelapor_count, row):
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

async def fetch_data_parallel():
    start_time = time.time()

    # Your MySQL configuration
    db_config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "12345",
        "db": "covdb"
    }

    nikpelapor_count = {}  # Dictionary to store the count of each NIKPELAPOR

    try:
        async with aiomysql.connect(**db_config) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT NIKPELAPOR, NAMAPELAPOR, NAMATERLAPOR, ALAMATERLAPOR, GEJALA FROM DATAIMPORTED")
                rows = await cursor.fetchall()

                with ThreadPoolExecutor(max_workers=4) as executor:
                    await asyncio.gather(*[asyncio.to_thread(fetch_data_row, nikpelapor_count, row) for row in rows])

    except aiomysql.Error as e:
        print("Error connecting to the database:", e)
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time} seconds")

async def main():
    await fetch_data_parallel()

if __name__ == '__main__':
    asyncio.run(main())
