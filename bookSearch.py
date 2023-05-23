import database as db
mainDB = db.mainDB()

def refactorSearchText(event, searchText):
    '''
    Return refactor search text:
        event = key pressed (event)
        searchText = Search text (String)
    '''
    if (event.char or event.keysym == 'BackSpace'):
        searchChar = event.char
        if (searchChar == "" and len(searchText)):
             return searchText.replace(searchText[len(searchText)-1], '')
        else:
            return searchText + (searchChar)

def searchBooksList(search_text, filterType):
    '''
    Return search list:
        searchText = Search text (String)
        filterType = Filter Type (string)
    '''
    return mainDB.searchBook(search_text, filterType)

def clearSearch():
    '''
    Reset search filter
    '''
    return mainDB.getAllBooksList()

if __name__=='__main__':
    # Search Working
    print ("Search List Item")
    searchListItem = searchBooksList('A Gam', 'title')
    print (searchListItem)
    print ('================================')
    # clear Search
    print(clearSearch())
    print ('================================')


