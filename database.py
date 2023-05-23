import pandas as pd
import sqlite3
from datetime import date

class DataBaseClass:
        def __init__(self, transactionID, conn):
                self.transactionID = transactionID
                self.conn = conn

        def executeQuery(self, query, action):
                '''
                Execute given query:
                        query - 'Select * from BookDetails',
                        action - 'get', 'Update', 'Insert'
                '''
                currentCursor = self.conn.cursor()
                currentCursor.execute(query)
                if (action == 'get'):
                        return currentCursor.fetchall()

        def getBookIDList(self, title):
                query = "SELECT BookID FROM LibraryBooks WHERE (Title = \"{}\") AND (IsExists = 1)".format(title)
                return self.executeQuery(query, 'get')

        def getAllBooksList(self):
                query = 'SELECT * from BookDetails'
                return pd.DataFrame(self.executeQuery(query, 'get'))

        def getAllTransactionLogs(self):
                query = 'SELECT * from TransactionLogs ORDER by TransactionID DESC'
                return pd.DataFrame(self.executeQuery(query, 'get'))

        def getCurrentBookTransactionDetailsRow(self, bookId):
                query = '''SELECT TransactionID FROM TransactionLogs
                WHERE (BookID = {bookId})
                AND (ReservationDate is NOT NULL)
                And (CheckoutDate is NULL)'''.format(bookId=int(bookId))

                return self.executeQuery(query, 'get')

        def getFrequentlyPurchasedBookInfo(self,):
               query = '''SELECT t1.Title, t1.totalCount, bd.Genre, bd.Price FROM 
                        (SELECT lb.BookID, lb.Title, sum(tl.BookCount) as totalCount FROM LibraryBooks lb
                        LEFT JOIN (SELECT BookID, count(BookID) as BookCount
                        FROM TransactionLogs GROUP by BookID  ) tl
                        WHERE tl.BookID = lb.BookID GROUP by lb.Title) t1
                        LEFT JOIN BookDetails bd WHERE bd.Title = t1.Title
                        ORDER by t1.totalCount DESC LIMIT 30'''

               return pd.DataFrame(self.executeQuery(query, 'get'))

        def getCurrentBookCountInBookDetailsRow(self, bookId):
                query = '''SELECT BookCount, BookDetails.Title  FROM
                        LibraryBooks INNER JOIN BookDetails
                        WHERE (LibraryBooks.BookID = {})
                        AND (LibraryBooks.Title = BookDetails.Title)'''.format(int(bookId))

                return self.executeQuery(query, 'get')

        def getBooksListToReturn(self):
                query = '''SELECT  lb.BookID, tl.MemberID, lb.Title, tl.CheckoutDate FROM LibraryBooks lb
                        LEFT JOIN TransactionLogs tl
                        WHERE (lb.BookID = tl.BookID)
                        AND (lb.IsExists = 0) AND (tl.ReturnDate is NULL) AND (tl.ReservationDate is NULL)'''

                return pd.DataFrame(self.executeQuery(query, 'get'))


        def searchBook(self, selectedText, filterType):
                searchQuery = "SELECT * from  BookDetails WHERE  ({filterType} LIKE '%{selectedText}%')".format(filterType=filterType, selectedText=selectedText)
                return pd.DataFrame(self.executeQuery(searchQuery, 'get'))

        def proceedToCheckoutInDB(self, bookItems, memberID, bookIDsList):
                checkoutBookIdList = []
                reserveBookIDList = []
                iter = 0

                for index in range(len(bookItems)):
                        canCheckout = bookItems[index][3]
                        if (not(canCheckout)):
                                query = '''SELECT BookID, reserveCount FROM LibraryBooks
                                        WHERE (Title = \"{title}\")
                                        ORDER by reserveCount
                                        LIMIT 1'''.format(title=bookItems[index][0])
                                reserveBookIDList.extend(self.executeQuery(query, 'get'))
                                iter+=1
                        else:
                                checkoutBookIdList.append(bookIDsList[index-iter])

                checkoutDate = reservationDate = date.today().strftime("%d/%m/%Y")
                if (len(reserveBookIDList)):
                        self.insertBooksInDBTransactions(reserveBookIDList, reservationDate, memberID, isDBreservation = True)
                        self.updateLibraryBookDB(reserveBookIDList, isDBreservation = True)

                if (len(checkoutBookIdList)):
                        self.insertBooksInDBTransactions(checkoutBookIdList, checkoutDate, memberID, isDBreservation = False)
                        self.updateLibraryBookDB(checkoutBookIdList, isDBreservation = False)
                        self.updateBookDetails(bookItems)

        def insertBooksInDBTransactions(self, idList, date, memberID, isDBreservation):
                insertValueList = ()
                resultValues = ''
                transactionId = self.transactionID

                for index in idList:
                        idValue = int(index[0]) if isDBreservation else index
                        value = (transactionId, idValue, date, memberID)
                        insertValueList = (*insertValueList,value)
                        transactionId +=1

                self.transactionID = transactionId

                for i in range(len(insertValueList)):
                        resultValues = resultValues + str(insertValueList[i])
                        if (i < len(insertValueList)-1):
                                resultValues += ','

                if (isDBreservation):
                        insertQuery = "INSERT INTO TransactionLogs (TransactionID, BookID, ReservationDate, MemberID) VALUES {}".format(resultValues)
                else:
                        insertQuery = "INSERT INTO TransactionLogs (TransactionID, BookID,  CheckoutDate, MemberID) VALUES {}".format(resultValues)

                self.executeQuery(insertQuery, 'insert')

        def returnBookInLibrary(self, memberID, bookID, checkoutDate):
                isAnyReservationExist = self.isAnyReservationExistForBookIDInDB(bookID)
                if (len(isAnyReservationExist)):
                        reservationCount = int(str(isAnyReservationExist[0]).strip('()').strip(','))
                        self.updateReserveCountInLibraryBooksDB(reservationCount, bookID)
                        transactionRowID = int(str(self.getCurrentBookTransactionDetailsRow(bookID)[0]).strip('()').strip(','))
                        self.updateCheckoutDateInTransactionDB(transactionRowID)
                else:
                        currentRow = self.getCurrentBookCountInBookDetailsRow(bookID)[0]
                        bookCount = int(currentRow[0])+1
                        title = currentRow[1]
                        self.updateBookCountInDB(bookCount, title)

                self.updateReturnDateInTransactionDB(memberID, bookID, checkoutDate)

        # Update functions

        def updateLibraryBookDB(self, bookIdList, isDBreservation):
                if (isDBreservation):
                        for item in bookIdList:
                                count = item[1]
                                updateQuery = '''UPDATE LibraryBooks SET reserveCount = {reserveCount} WHERE BookID = {bookId}'''.format(reserveCount=count+1, bookId=item[0])
                                currentCursor = self.conn.cursor()
                                currentCursor.execute(updateQuery)
                                self.executeQuery(updateQuery, 'update')
                        
                else:
                        for index in bookIdList:
                                updateQuery = "UPDATE LibraryBooks SET IsExists = 0 WHERE BookID = {}".format(index)
                                self.executeQuery(updateQuery, 'update')

        def updateBookCountInDB(self, count, title):
                updateQuery = "UPDATE BookDetails SET BookCount = {count} WHERE Title = \"{title}\" ".format(count=count, title=title)
                self.executeQuery(updateQuery, 'update')

        def updateBookDetails(self, bookItems):
                for book in bookItems:
                        if (book[3] != 0):
                                title =book[0]
                                count = book[3] - 1
                                self.updateBookCountInDB(count, title)
                # conn.commit()

        def updateReturnDateInTransactionDB(self, memberID, bookID, checkoutDate):
                returnDate = date.today().strftime("%d/%m/%Y")
                updateQuery = "UPDATE TransactionLogs SET ReturnDate = \"{returnDate}\" WHERE (MemberID = {memberID}) AND (CheckoutDate = \"{checkoutDate}\") AND (BookID = {bookID})".format(returnDate=returnDate, memberID=int(memberID), bookID=int(bookID), checkoutDate=checkoutDate)
                self.executeQuery(updateQuery, 'update')
        
        def updateReserveCountInLibraryBooksDB(self, reservationCount, bookID):
                updateQuery = '''UPDATE LibraryBooks
                        SET reserveCount = {reservationCount}
                        WHERE BookID = {bookID}'''.format(bookID=bookID, reservationCount=reservationCount-1)
                self.executeQuery(updateQuery, 'update')

        def updateCheckoutDateInTransactionDB(self, transactionRowID):
                CheckoutDate = date.today().strftime("%d/%m/%Y")
                updateQuery = '''UPDATE TransactionLogs
                        SET CheckoutDate = "{CheckoutDate}", ReservationDate = NULL
                        WHERE TransactionID = {transactionRowID}'''.format(CheckoutDate=CheckoutDate, transactionRowID=transactionRowID)

                self.executeQuery(updateQuery, 'update')

        def isAnyReservationExistForBookIDInDB(self, bookID):
                query = '''SELECT reserveCount FROM LibraryBooks
                        WHERE (BookID = {}) 
                        AND (reserveCount > 0)'''.format(int(bookID))
                return self.executeQuery(query, 'get')

def mainDB(): 
        transactionID = 197
        conn = sqlite3.connect('Library.db')
        return DataBaseClass(transactionID, conn)

if __name__=='__main__':
	mainDB()
