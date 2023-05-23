import database as db
import collections
mainDB = db.mainDB()

def isMemberIDValid(memberID):
    '''
    Check member ID is valid and return boolean:
        memberID = Member ID (int)
    '''
    return memberID and memberID.isnumeric() and len(memberID) == 4

def proceedToCheckout(checkoutItems, memberID, bookIDList):
    '''
    proceed to update checkoutItems in DB :
        checkoutItems = checkout items list  (list)
        memberID = Member ID (int)
        bookIDList = books details List (list)
    '''
    mainDB.proceedToCheckoutInDB(checkoutItems, memberID, bookIDList)
    checkoutItems = []
    bookIDList = []
    return checkoutItems, bookIDList

def getCheckoutListItem(listItem, isReservation, checkoutItems, action):
    '''
    Returns an listItem :
        listItem = book detail (list)
        isReservation = check reservation (boolean)
        checkoutItems = selected checkout items (list)
        action = 'a' - append or 'r' - remove  (char)
    '''
    listItem.append(isReservation)
    if (len(checkoutItems) and action == 'a'):
        canAppend = 1
        for item in checkoutItems:
            if collections.Counter(item) == collections.Counter(listItem):
                canAppend -= 1
                break

        if (canAppend):
            return listItem
    else:
        return listItem

if __name__=='__main__':
    # Test Function getCheckoutListItem
    print ('================================')
    bookList = ['A Game of Thrones', 'George R. R. Martin', 'Fantasy', 4, 40]
    print (getCheckoutListItem(bookList, False, [], 'a'))
    print ('================================')

    # Test proceedToCheckout will return Empty lists
    print ('================================')
    print(proceedToCheckout([['A Game of Thrones', 'George R. R. Martin', 'Fantasy', 4, 40, False]], 1232, [1]))
    print ('================================')

    # Invalid MemberID
    print ('Valid') if isMemberIDValid('232d') else print('Invalid')
    print ('Valid') if isMemberIDValid('1') else print('Invalid')
    print ('Valid') if isMemberIDValid('34848') else print('Invalid')
    # Valid MemberID
    print ('Valid') if isMemberIDValid('1234') else print('Invalid')

