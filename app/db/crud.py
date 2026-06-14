from app.db.database import getDBConnection


def create_user(username, password_hash):
    connection = getDBConnection()
    cursor = connection.cursor()

    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(query, (username, password_hash))

    connection.commit()
    connection.close()


def get_users():
    connection = getDBConnection()
