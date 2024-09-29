import dbmanager as db
import gui
def main():
    
    db.setupDb()
    gui.createGUI()
    return 0

if __name__ == "__main__":
    main()
    