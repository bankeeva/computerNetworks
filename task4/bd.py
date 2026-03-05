import psycopg2


def to_sql(data_frame, connection=None, cursor=None):
    try:
        connection = psycopg2.connect(
            user="1",
            password="1",
            host="localhost",
            port="5432",
            database="1"
        )
        cursor = connection.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habr_pars (
            id SERIAL PRIMARY KEY,
            title TEXT,
            author TEXT,
            datetime TEXT,
            views TEXT
        );
        """)

        if data_frame is None or data_frame.empty:
            connection.commit()
            return 0

        df = data_frame[["title", "author", "datetime", "views"]].copy()

        for _, row in df.iterrows():
            cursor.execute(
                f"""
                INSERT INTO habr_pars (title, author, datetime, views)
                VALUES (%s, %s, %s, %s)
                """,
                (row["title"], row["author"], row["datetime"], row["views"])
            )
        connection.commit()

    except Exception as error:
        print("Ошибка при подключении к PostgreSQL", error)
    finally:
        cursor.close()
        connection.close()


def from_sql(connection=None, cursor=None):
    try:
        connection = psycopg2.connect(
            user="1",
            password="1",
            host="localhost",
            port="5432",
            database="1"
        )
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, title, author, datetime, views
            FROM habr_pars
            ORDER BY id DESC
            """
        )
        rows = cursor.fetchall()

        return [{
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "datetime": row[3],
            "views": row[4]
        } for row in rows]

    except Exception as error:
        print("Ошибка при подключении к PostgreSQL", error)
    finally:
        cursor.close()
        connection.close()
