import PySimpleGUI as sg
import dbmanager as db

def createLayout():

    layout =[
        
        [sg.Text('Title'), sg.InputText(key='title')],
        [sg.Text('Author'), sg.InputText(key='author')],
        [sg.Text('Genre'), sg.InputText(key='genre')],
        [sg.Text('Publication Date'), sg.InputText(key='publication_date')],
        [sg.Text('ISBN'), sg.InputText(key='isbn')],
        [sg.Button('Add Book')],
        [sg.Text('_' * 60)],
        [sg.Text('Filter Books')],
        [sg.Text('Search by Title'), sg.InputText(key='search_title')],
        [sg.Text('Search by Author'), sg.InputText(key='search_author')],
        [sg.Text('Search by Genre'), sg.InputText(key='search_genre')],
        [sg.Text('Search by Publication Date' ), sg.InputText(key='search_publication_date')],
        [sg.Text('Search by ISBN' ), sg.InputText(key="search_isbn")],
        [sg.Button('Search')],
        [sg.Table(
            values=[], 
            headings=['ID', 'Title', 'Author', 'Genre', 'Publication Date', 'ISBN'], 
            key='table',
            auto_size_columns=False,
            expand_x=True,
            justification="center",
            col_widths=[3,20,20,20,20,20,20]
            )
        ]
        #,[sg.Button('Export CSV'), sg.Button('Export JSON')]
        
        ]
    
    return layout

def createGUI():
    
    custom_window_theme= {
        'BACKGROUND': '#465178',
        'TEXT': '#FFB067',
        'INPUT': '#C8C4C1',
        'TEXT_INPUT': '#000000',
        'SCROLL': '#c7e78b',
        'BUTTON': ('#FFB067', '#002134'),
        'PROGRESS': ('#FFB067', '#002134'),
        'BORDER': 1,
        'SLIDER_DEPTH': 0,
        'PROGRESS_DEPTH': 0}

    sg.theme_add_new("custom1", custom_window_theme)
    sg.theme("custom1")
    layout = createLayout()
    window = sg.Window("Book Inventory", layout, finalize=True)

    while True:

        event, values = window.read(timeout = 100)

        if event in (sg.WIN_CLOSED, 'close'):
            break

        if event == "Add Book":
            
            title = values['title']
            author = values['author']
            genre = values['genre']
            publication_date = values['publication_date']
            isbn = values['isbn']

            res = db.addBook(title, author, genre, publication_date, isbn)

            if res:
                sg.popup("Book added successfully!")
                window["table"].update(db.filterBooks()) # select * from books
            else:
                sg.popup("Book couldn't be added...")
                # check logs

        if event == "Search":
            title = values['search_title']
            author = values['search_author']
            genre = values['search_genre']
            publication_date = values['search_publication_date']
            isbn = values['search_isbn']

            res = db.filterBooks(title,author,genre,publication_date,isbn)

            if res:
                sg.popup("Book added successfully!")
                window['table'].update(res)

            else:
                sg.popup("Your search failed. Try again please!")
            
    
    window.close()





    