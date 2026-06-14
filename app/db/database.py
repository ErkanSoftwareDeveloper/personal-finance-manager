import pymysql


def getDBConnection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='finance_managerDB'
    )


try:
    connection = getDBConnection()
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")
