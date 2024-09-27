import sqlite3 as sql

# method creates the database and the table to store books, can be
# safely called multiple times, the query checks for existence of a table in the db
def setupDb():

    con = sql.connect('books.db')
    cursor = con.cursor()

    cursor.execute(

        '''
        CREATE TABLE IF NOT EXISTS Books(
            id INTEGER PRIMARY KEY AUT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT DEFAULT "Unknown",
            publication_date TEXT DEFAULT "Unknown",
            ISBN TEXT UNIQUE NOT NULL
        );
        '''
    )

    cursor.close()
    con.commit()
    con.close()

# self-explanatory
def addBook(title, author, genre, publication_date, ISBN):

    con = sql.connect('books.db')
    cursor = con.cursor()
    
    try:
        # ? placeholders to prevent injections
        cursor.execute(
            '''
            INSERT INTO Books (title, author, genre, publication_date, ISBN)
            VALUES (?, ?, ?, ?, ?)
            ''', (title, author, genre, publication_date, ISBN)
        )
        con.commit()
        return True
    except sql.Error as err:
        print(err) # logs error in console
        return False
    finally:
        con.close()

# filters books based on parameters provided, returns the query result or False
def filterBooks(title='', author='', genre='', publication_date='', ISBN = ''):

    con = sql.connect('books.db')
    cursor = con.cursor()

    # depending on the parameters provided in a different module, will create a query and pass the parameters
    # prevents sql injections with placeholders
    query = 'SELECT * FROM Books WHERE TRUE'
    params = []

    if title:
        query += f" AND title=?"
        params.append(title)
    if author:
        query += f" AND author= ?"
        params.append(author)
    if genre:
        query += f" AND genre= ?"
        params.append(genre)
    
    if publication_date:
        query += f" AND publication_date= ?"
        params.append(publication_date)
    
    if ISBN:
        query += f" AND ISBN= ?"
        params.append(ISBN)

    query+=";"
    try:
        res = cursor.execute(query, params)
        return res # list of tuples matching criteria

    except sql.Error as err:
        print(err) # logs errors in console
        return False

    finally:
        cursor.close()
        con.close()
        