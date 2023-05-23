import database as db
mainDB = db.mainDB()

def returnBookInLibraryDB(memberID, bookID, checkoutDate):
    '''
    Return Books to Library DB:
        checkoutDate = checkout Date (String)
        memberID = Member ID (int)
        bookID = Book ID (int)
    '''
    mainDB.returnBookInLibrary(memberID, bookID, checkoutDate)

if __name__=='__main__':
    print ('================================')
    returnBookInLibraryDB(1232, 1, 11/11/2022)
    print ('================================')