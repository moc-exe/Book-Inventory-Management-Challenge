import sqlite3 as sql
import time
import csv

# method creates the database and the table to store books, can be
# safely called multiple times, the query checks for existence of a table in the db
def setupDb():

    con = sql.connect('books.db')
    cursor = con.cursor()

    cursor.execute(

        '''
        CREATE TABLE IF NOT EXISTS Books(
            id INTEGER PRIMARY KEY,
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

    q_title = title if title else None
    q_author = author if author else None
    q_genre = genre if genre else None
    q_publication_date = publication_date if publication_date else None
    q_ISBN = ISBN if ISBN else None

        
    try:
        # ? placeholders to prevent injections
        cursor.execute(
            '''
            INSERT INTO Books (title, author, genre, publication_date, ISBN)
            VALUES (?, ?, ?, ?, ?)
            ''', (q_title, q_author, q_genre, q_publication_date, q_ISBN)
        )
        con.commit()
        return True
    except sql.Error as err:
        print(err)
        with open("err_log.txt", "a") as file:
            file.write("\n")
            file.write(time.ctime()) #logs errors in a file
            file.write(str(err))
            file.write("\n")
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
        query += " AND title LIKE ?"
        params.append(f'%{title}%')
    if author:
        query += " AND author LIKE ?"
        params.append(f'%{author}%')
    if genre:
        query += ' AND genre LIKE ?'
        params.append(f'%{genre}%')
    
    if publication_date:
        query += f" AND publication_date LIKE ?"
        params.append(f'%{publication_date}%')
    
    if ISBN:
        query += f" AND ISBN LIKE ?"
        params.append(f'%{ISBN}%')

    query+=";"
    try:
        res = cursor.execute(query, params)
        return res.fetchall() # list of tuples matching criteria

    except sql.Error as err:
        print(err)
        with open("./err_log.txt", "a") as file:
            file.write("\n")
            file.write(time.ctime()) #logs errors in a file
            file.write(str(err))
            file.write("\n")
        return False

    finally:
        cursor.close()
        con.close()

# deletes a book from the db, when provided with a valid id, else returns false
def deleteBook(id):

    conn = sql.connect('books.db')
    cursor = conn.cursor()
    query = f"DELETE FROM Books WHERE id = {id};"

    try:

        res = cursor.execute(query)
        conn.commit()
        return True

    
    except sql.Error as err:
        with open("./err_log.txt", "a") as file:
            file.write("\n")
            file.write(time.ctime()) #logs errors in a file
            file.write(str(err))
            file.write("\n")
        return False
    
    finally:
        
        cursor.close()
        conn.close()

#checks if the db is empty
def isEmpty():

    conn = sql.connect('books.db')
    cursor = conn.cursor()
   
    try:
        cursor.execute("SELECT COUNT(*) FROM Books")
        count = cursor.fetchone()[0]
        if count == 0:
            return True
        else:
            return False
    except sql.Error as err: 
        with open("./err_log.txt", "a") as file:
            file.write("\n")
            file.write(time.ctime()) #logs errors in a file
            file.write(str(err))
            file.write("\n")
        return False
    finally:
        cursor.close()
        conn.close()

# helper to export to a csv file from the db, the filename is provided in the gui module
def exportCSV(filename):
    conn = sql.connect('books.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM Books')
        books = cursor.fetchall()
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Entry ID', 'Title', 'Author', 'Genre', 'Publication Date', 'ISBN'])
            writer.writerows(books)

        return True

    except sql.Error as err:
        with open("./err_log.txt", "a") as file:
            file.write("\n")
            file.write(time.ctime()) #logs errors in a file
            file.write(str(err))
            file.write("\n")
        return False
    
    finally:
        conn.close()
        