import PySimpleGUI as sg
import dbmanager as db
import platform

main_font = "Monospace 11 bold"

def styled_input(key):
    return sg.Input(font="Monospace 11", text_color="#FFB067", background_color="#002134", key=key, pad=(5,5))

def clearAddInput(window):
    window["title"].update("")
    window['author'].update("")
    window['genre'].update('')
    window["publication_date"].update("")
    window["isbn"].update("")

def clearSearchInput(window):
    window["search_title"].update("")
    window['search_author'].update("")
    window['search_genre'].update('')
    window["search_publication_date"].update("")
    window["search_isbn"].update("")

def assignIcon():
    system = platform.system()
    if system == "Windows":
        return "./img/app.ico"
    elif system == "Linux":
        return "./img/app_icon.png"
    elif system == "Darwin":
        return "./img/app_icon.png"
    else:
        return None

def createLayout():



    add_book_left_column = [

        [sg.Text('Title', font=main_font),sg.Text('*', font=main_font, text_color="red")],
        [sg.Text('Author',font=main_font),sg.Text('*', font=main_font, text_color="red")],
        [sg.Text('Genre',font=main_font)],
        [sg.Text('Publication Date',font=main_font)],
        [sg.Text('ISBN',font=main_font),sg.Text('*', font=main_font, text_color="red")],
    
    ]
    add_book_right_column = [

        [styled_input("title")],
        [styled_input("author")],
        [styled_input("genre")],
        [styled_input("publication_date")],
        [styled_input("isbn")],

    ]
    add_book_layout = [

        [sg.Text('Please enter book information, fields marked with * are required',font="Monospace 14 bold")],
        [sg.Column(add_book_left_column, element_justification='left'), sg.Column(add_book_right_column, element_justification='center')],
        [sg.Button('Add Book')]
    
    ]
    search_left_col = [

        [sg.Text('Title',font=main_font)],
        [sg.Text('Author',font=main_font)],
        [sg.Text('Genre',font=main_font)],
        [sg.Text('Publication Date',font=main_font )],
        [sg.Text('ISBN',font=main_font)]

    ]
    search_right_col =[

        [styled_input('search_title')],
        [styled_input('search_author')],
        [styled_input('search_genre')],
        [styled_input('search_publication_date')],
        [styled_input("search_isbn")],

    ]

    filter_layout = [

        [sg.Text('Please enter your search criteria',font="Monospace 14 bold")],
        [sg.Column(search_left_col, element_justification="left"), sg.Column(search_right_col, element_justification="center")],
        [sg.Button('Search'), sg.Button('Display All Books')],
    ]

    layout =[
        [sg.Frame("Add Book", layout=add_book_layout, expand_x=True, font="Monospace 18 bold")],
        [sg.Frame("Search Books", layout=filter_layout, expand_x=True, font="Monospace 18 bold")],
        [sg.Frame("Status",
                  layout=[[sg.Text("Welcome! Inventory Operational", key="status", font=main_font, text_color="green")]],
                  expand_x=True,
                  font="Monospace 18 bold"
        )],
        [sg.Text("To delete a book, right-click -> delete book",font=main_font)],
        [sg.Table(
            values=[],
            headings=['ID', 'Title', 'Author', 'Genre', 'Publication Date', 'ISBN'], 
            key='table',
            auto_size_columns=False,
            expand_x=True,
            justification="center",
            col_widths=[3,30,30,30,30,4,20],
            font = "Monospace 11",
            enable_events=True,
            right_click_selects=True,
            right_click_menu=['&Right', ['Remove Book']]
            )
        ],
        [sg.Frame("Export Data",
                  layout=[[sg.Button("Export CSV", size=(15))]],
                  expand_x=True,
                  font="Monospace 18 bold",
                  element_justification="center"
        )]
        ]
    
    return layout

def createGUI():
    
    custom_window_theme= {
        'BACKGROUND': '#465178',
        'TEXT': '#FFB067',
        'INPUT': '#C8C4C1',
        'TEXT_INPUT': '#000000',
        'SCROLL': '#FFB067',
        'BUTTON': ('#FFB067', '#002134'),
        'PROGRESS': ('#FFB067', '#002134'),
        'BORDER': 1,
        'SLIDER_DEPTH': 0,
        'PROGRESS_DEPTH': 0}

    sg.theme_add_new("custom1", custom_window_theme)
    sg.theme("custom1")
    layout = createLayout()

   

    window = sg.Window("Book Inventory", layout, finalize=True, icon=assignIcon())
    tableData = None

    while True:

        event, values = window.read(timeout = 100)

        if event in (sg.WIN_CLOSED, 'close'):
            break

        if event == "Add Book":
            
            title = str(values['title']).strip().upper() if values['title'] else ""
            author = str(values['author']).strip().upper() if values['author'] else ""
            genre = str(values['genre']).strip().upper() if values['genre'] else ''
            publication_date = values['publication_date'] if values['publication_date'] else ""
            isbn = values['isbn'] if values['isbn'] else ''

            res = db.addBook(title, author, genre, publication_date, isbn)

            if res:
                tableData = db.filterBooks()
                window['status'].update("Book added successfully!")
                window['status'].update(text_color = "green")
                window["table"].update(tableData) # select * from books
                window["title"].update("")
                window['author'].update("")
                clearAddInput(window)


            else:
                window['status'].update("Book couldn't be added!")
                window['status'].update(text_color = "red")
                # check logs

        if event == "Search":

            if db.isEmpty():
                window['status'].update("The inventory is currently empty")
                window['status'].update(text_color = "green")
                tableData = [[]]
                window['table'].update(tableData)
                clearSearchInput(window)
                continue

            title = str(values['search_title']).strip().upper() if values['search_title'] else ""
            author = str(values['search_author']).strip().upper() if values['search_author'] else ""
            genre = str(values['search_genre']).strip().upper() if values['search_genre'] else ''
            publication_date = values['search_publication_date'] if values['search_publication_date'] else ""
            isbn = values['search_isbn'] if values['search_isbn'] else ''

            res = db.filterBooks(title,author,genre,publication_date,isbn)

            if res:
                window['status'].update("Displaying results of your search")
                window['status'].update(text_color = "green")
                tableData = res
                window['table'].update(tableData)
                clearSearchInput(window)
            else:
                window['status'].update("Your search failed. Try modifying criteria.")
                window['status'].update(text_color = "red")
            
        if event == "Remove Book":

            bookID = tableData[values['table'][0]][0]
            sg.popup(bookID)
            
            if db.deleteBook(bookID):
                if db.isEmpty():
                    window['status'].update(f"Book id={bookID} was deleted. Inventory empty")
                    window['status'].update(text_color = "green")
                    tableData = [[]]
                    window['table'].update(tableData)
                else:
                    window['status'].update(f"Book id={bookID} was deleted successfully")
                    window['status'].update(text_color = "green")
                    tableData = db.filterBooks()
                    window['table'].update(tableData)
            else:
                window['status'].update("Internal error, couldn't delete the book")
                window['status'].update(text_color = "red")

        if event == "Display All Books":

            res = db.filterBooks()
            if res:
                window['status'].update("Displaying all books")
                window['status'].update(text_color = "green")
                tableData = res
                window['table'].update(tableData)
                clearSearchInput(window)
                continue

            if db.isEmpty():
                window['status'].update("Inventory is currently empty")
                window['status'].update(text_color = "green")
                tableData = [[]]
                window['table'].update(tableData)
            else:
                window['status'].update("Internal error, couldn't display all books")
                window['status'].update(text_color = "red")

        if event == "Export CSV":

            if db.isEmpty():
                window['status'].update("Export failed, inventory is currently empty")
                window['status'].update(text_color = "red")
                tableData = [[]]
                window['table'].update(tableData)
            else:
                filename = sg.popup_get_file('Please select a file to save', save_as=True, icon=assignIcon)
                if filename and db.exportCSV(filename):
                    window['status'].update(f"Exported successfully to f{filename}")
                    window['status'].update(text_color = "green")
                else:
                    window['status'].update(f"Export to {filename} failed")
                    window['status'].update(text_color = "red")

    window.close()





    