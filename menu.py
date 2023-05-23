from tkinter import *
from tkinter import messagebox
import database as db
import bookSearch, bookCheckout, bookReturn, bookRecommendation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MainGUI:
    def __init__(self,window, database):
        self.__mainWin=window
        self.database = database
        self.__mainWin.title("Library Management System")
        self.__mainWin.config(bg="white")
        self.__mainWin.geometry('1400x750')
        self.__mainWin.minsize(1400, 750)
        self.__mainWin.maxsize(1400, 750)
        self.bookListData = database.getAllBooksList()
        self.search_text = ''
        self.checkoutItems = []
        self.bookIDList = []
        self.findEachBookCount = []
        self.credictScore = 2000
        self.temp=0
        self.__createNavigationBar()
        self.canvas = self.setCanvas()
        self.__displayAllBooksList()

    def __createApplicationColor(self):
        # Colors needs to be changes
        return {"nero": "#252726", "orange": "#FF8700", "darkorange": "#FE6101", "darkblue": "#00003f"}

    def setCanvas(self):
        '''
        Create Canvas:
        '''
        myCanvas = Canvas(self.__mainWin, highlightbackground="white")
        myCanvas.pack(side=LEFT, fill=BOTH, expand=1, padx=(250, 0), pady=(42, 38))
        return myCanvas

    def __createNavigationBar(self):
        '''
        Navigation Bar
        '''
        color  = self.__createApplicationColor()
        navRoot = Frame(self.__mainWin, bg=color["darkblue"], height=1000, width=250)
        navRoot.place(x=0, y=0)
        Label(navRoot, text = "UK Library", fg="White", bg="#ef476f", font="BahnschriftLight 16 bold", width=22, pady=5).place(x=0, y=0)
        Button(navRoot, text="Dashboard", font="BahnschriftLight 15", bg=color["darkblue"], fg="#fff", activebackground="gray17", activeforeground="green", bd=0, command = self.__displayAllBooksList).place(x=25, y=80)
        Button(navRoot, text="Book Checkout", font="BahnschriftLight 15", bg=color["darkblue"], fg="#fff", activebackground="gray17", activeforeground="green", bd=0, command = self.__displayCheckout).place(x=25, y=125)
        Button(navRoot, text="Book Return", font="BahnschriftLight 15", bg=color["darkblue"], fg="#fff", activebackground="gray17", activeforeground="green", bd=0, command = self.__displayReturnBook).place(x=25, y=170)
        Button(navRoot, text="Recommended Books", font="BahnschriftLight 15", bg=color["darkblue"], fg="#fff", activebackground="gray17", activeforeground="green", bd=0, command = self.__displayRecommendedBooks).place(x=25, y=215)
        Button(navRoot, text="Transaction Logs", font="BahnschriftLight 15", bg=color["darkblue"], fg="#fff", activebackground="gray17", activeforeground="green", bd=0, command = self.__displayTransactionLogs).place(x=25, y=260)

        topFrame = Frame(self.__mainWin, bg="#edede9", height=50, width=1300)
        topFrame.place(x=250, y=0)

        # Button section
        Label(topFrame, text="Search", background="#edede9", fg="black", font="BahnschriftLight 15 bold").place(x=20, y=8)
        self.searchEntry = Entry(topFrame, width=35, background="#CBC8C5", bd=0, highlightbackground="#a2d2ff", fg="black", font="BahnschriftLight 12", insertbackground="#333")
        self.searchEntry.place(x=90, y=15)
        self.searchEntry.bind("<KeyRelease>", lambda event: self.searchBooks(event))
        Label(topFrame, text="|", background="#edede9", fg="#8e9aaf", font="BahnschriftLight 19 bold").place(x=395, y=5)
        Label(topFrame, text="Filter By:", background="#edede9", fg="black", font="BahnschriftLight 14 bold").place(x=405, y=8)
        filterTypes = ['Title', 'Author', 'Genre']
        self.SeletedFilter = StringVar(topFrame)
        self.SeletedFilter.set(filterTypes[0])
        bookIDOptionMenu = OptionMenu(topFrame, self.SeletedFilter, *filterTypes, command = self.updateSearchFilterType)
        bookIDOptionMenu.config(width=5, bg="#a2d2ff", fg="black")
        bookIDOptionMenu.place(x=485, y=10)

        # Credits Info
        Label(topFrame, text="Credits: £{}".format(self.credictScore), fg="#003049", font="BahnschriftLight 15 bold", background="#edede9").place(x=950, y=10)

    # GUI for Search Functions
    def updateSearchFilterType(self, filterType):
        '''
        Update search filter:
            filterType - > 'title', 'author', 'genre' (string)
        '''
        self.bookListData = bookSearch.searchBooksList(self.search_text, filterType)
        self.__displayAllBooksList()

    def searchBooks(self, event):
        '''
        Update search books:
            event - > key release event (char)
            searchText -> search Text
        '''
        self.search_text = bookSearch.refactorSearchText(event, self.search_text)
        filterType = self.SeletedFilter.get()
        self.updateSearchFilterType(filterType)

    def clearSearch(self):
        '''
        Clear search filter:
            set searchEntry to 0
        '''
        self.search_text = ''
        self.searchEntry.delete(0, END)
        self.bookListData = bookSearch.clearSearch()
        self.__displayAllBooksList()

    # Display Books List
    def __displayAllBooksList(self):
        '''
        Display all Books in the Books Details DB
        '''
        myCanvas = self.canvas
        self.addToCartButtonList = []
        self.addToReservation = []
        if (self.temp == 0):
            myscrollbar=Scrollbar(self.__mainWin,orient=VERTICAL, command=myCanvas.yview)
            myscrollbar.pack(side=RIGHT,fill=Y)
            myCanvas.configure(yscrollcommand=myscrollbar.set)
            myCanvas.bind('<Configure>', lambda e: myCanvas.configure(scrollregion=myCanvas.bbox("all")))
            myCanvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll((-1) * (e.delta), "units"))
            # myCanvas.bind('<MouseWheel>', lambda e: myCanvas.yview_scroll(-1*(e.delta/120), "units"))
            self.temp = 1
        else:
            myCanvas.delete('all')

        secondFrame = Frame(myCanvas, bg="white", padx=45, pady=40, background="white")
        myCanvas.create_window((0, 0), window=secondFrame, anchor="ne", width=1150, height=5380)

        if (len(self.search_text)):
            Label(secondFrame, text='Search Result for \'{}\''.format(self.search_text),  background="white", font="BahnschriftLight 15", fg="green").place(x=0, y=-30)
            Button(secondFrame,  text='Clear Filter', bg="gray", fg="black", command=self.clearSearch).place(x=195+(len(self.search_text)*6), y=-30)
        if (len(self.bookListData)):
            if (not(len(self.search_text))):
                Label(secondFrame, text='Discover Books', bg="white", fg="#333", font="Bahnschrift 22 bold").place(x=0, y=-30)
            for index, row in self.bookListData.iterrows():
                cardFrame = Frame(secondFrame, bg="White", highlightbackground="#eee", highlightthickness=2, width=600, padx=10, pady=10)
                cardFrame.pack(fill=BOTH, pady=10)
                bookFrame = Frame(cardFrame, highlightbackground="black", highlightthickness=2, width=50, height=50, bg="white")
                bookFrame.pack(side=LEFT, anchor=W, padx=(15, 0), pady=(2,0))
                Label(bookFrame, text="No \n Image", fg="gray", bg="white").pack(side=LEFT, anchor=W, padx=8, pady=10)
                Label(cardFrame, text=row[0].upper(),  background="white", font="Bahnschrift 17 bold", fg="#222").pack(side=TOP, anchor=W, padx=(20, 0), pady=(2,0))
                Label(cardFrame, text="Author: {author},   Genre: {genre}".format(author = row[1], genre = row[2]),  background="white", font="BahnschriftLight 15", fg="#333").pack(side=TOP, anchor=W, padx=(20, 0))
                if (row[3] == 0):
                    removeReserveBook = Button(cardFrame, text='Clear Select', bg="green", fg="black", command=lambda index=index, isReservation = True: self.removeCart(index, isReservation))
                    removeReserveBook.place(x=900, y=1)
                    reserveBooks = Button(cardFrame, text='Reserve Book', bg="green", fg="black", command=lambda index=index, isReservation = True: self.updateCart(index, isReservation))
                    reserveBooks.place(x=900, y=1)
                    self.addToReservation.append(reserveBooks)
                    self.addToCartButtonList.append("None")
                    Label(cardFrame, text="Not Available", bg="white", fg="red").place(x=910, y=30)
    
                else:
                    removeCartButton = Button(cardFrame, text='Remove Cart', bg="green", fg="black", command=lambda index=index, isReservation = False: self.removeCart(index, isReservation))
                    removeCartButton.place(x=900, y=1)
                    addCartButton = Button(cardFrame, text='Add to cart', bg="green", fg="black", width=10, command=lambda index=index, isReservation = False : self.updateCart(index,  isReservation))
                    addCartButton.place(x=900, y=1)
                    self.addToCartButtonList.append(addCartButton)
                    self.addToReservation.append("None")
                    Label(cardFrame, text="Not Available", bg="white", fg="red").place(x=900, y=30)
                    Label(cardFrame, text="Available books: {}".format(row[3]), bg="white", fg="green").place(x=900, y=30)
            
        else:
            Label(secondFrame, text='No Records',  background="white", font="BahnschriftLight 25", fg="red").place(x=280, y=250)

    # Cart GUI Functions
    def __displayCheckout(self):
        '''
        Display all Checkout details DB
        '''
        myCanvas = self.canvas
        myCanvas.delete('all')
        secondFrame = Frame(myCanvas, padx=20, pady=20, background="white")
        myCanvas.create_window((0, 0), window=secondFrame, anchor="ne", width=1150, height=4400)

        if (len(self.checkoutItems) == 0):
            noBookInCart = Frame(secondFrame, bg="#264653", highlightbackground="#264653", highlightthickness=2, padx=80,pady=40)
            noBookInCart.place(x=400, y=100)
            Label(noBookInCart, text="Add Books to Check Out", background="#264653", font="Bahnschrift 17 bold", fg="#fff").pack(side=TOP, anchor='nw', pady=(0, 10))
            Button(noBookInCart, text="Add Books", command=self.__displayAllBooksList).pack(side="top", anchor='w', padx=(50, 0), pady=(0, 10))
        else:
            Label(secondFrame, text="Books Checkout", bg="white", fg="#333", font="Bahnschrift 22 bold").pack(side=TOP, anchor=W, padx=(15,0), pady=(0, 10))
            for index in range(len(self.checkoutItems)):
                bookIdsList = self.database.getBookIDList(self.checkoutItems[index][0])
                booksCartFrame = Frame(secondFrame, bg="White",width=500)
                booksCartFrame.pack(side="top", anchor='w', padx=(15,0), pady=(0, 10))
                bookTitle = Label(booksCartFrame, text="{sno}. {item}".format(sno=index+1, item=self.checkoutItems[index][0]), fg="#576574", font="Bahnschrift 16 bold", bg="white")
                if (self.checkoutItems[index][5]):
                    bookTitle.pack(side=TOP, anchor='nw', padx=(0, 300), pady=(0, 48))
                    Label(booksCartFrame, text="This Book will be Reserved", bg="orange", fg="#fff").place(x=15, y=30)
                    Frame(booksCartFrame, bg="White", width=300, highlightbackground="#eee", highlightthickness="2").place(x=15, y=70)
                else:
                    bookTitle.pack(side=TOP, anchor='nw', padx=(0, 650), pady=(0, 70))
                    Label(booksCartFrame, text="Choose BookID:", font="Bahnschrift 13", bg="white", fg="#333").place(x=15, y=30)
                    selectedBookId = StringVar(booksCartFrame)
                    selectedBookId.set(bookIdsList[0])
                    convertedIDAsInt = int(selectedBookId.get().strip('()').strip(','))
                    self.bookIDList.append(convertedIDAsInt)
                    bookIDOptionMenu = OptionMenu(booksCartFrame, selectedBookId, *bookIdsList, command=lambda selectedBookId=selectedBookId, index=index: self.updateBookIdList(selectedBookId, index))
                    bookIDOptionMenu.config(bg="white", fg="black")
                    bookIDOptionMenu.place(x=123, y=30)
                    Button(booksCartFrame, text='Remove', fg="black", highlightbackground="#ef233c", highlightthickness=2, bd=0, background="white", command = lambda item = self.checkoutItems[index]: self.removeCartItem(item)).place(x=520, y=28)
                    Label(booksCartFrame, text="Available Items: {}".format(self.checkoutItems[index][3]), bg="white", fg="green").place(x=15, y=55)
                    Frame(booksCartFrame, bg="White", width=600, highlightbackground="#eee", highlightthickness="2").place(x=15, y=85)

            checkoutFrame = Frame(secondFrame, bg="White", highlightbackground="#f0ead2", highlightthickness=2, padx=10, pady=10)
            checkoutFrame.place(x=740, y=30)
            self.checkoutTotalBooksLabelTitle = Label(checkoutFrame, text="Proceed to Checkout", background="white", font="Bahnschrift 17 bold", fg="#6b9080")
            self.checkoutTotalBooksLabelTitle.pack(side=TOP, anchor='w', padx=70, pady=(0, 140))
            Label(checkoutFrame, text="Enter MemberID:", fg="#003049", font="Bahnschrift 13 bold", bg="white").place(x=2, y=40)
            memberId = Entry(checkoutFrame, background="white", fg="black", bd=0, highlightbackground="#a2d2ff", highlightthickness=2, insertbackground="#333")
            memberId.place(x=118, y=41)
            invalidMemberId = Label(checkoutFrame, text="4 digit ID (eg='1111')", font="Bahnschrift 12", fg="green", bg="white")
            invalidMemberId.place(x=115, y=65)
            Label(checkoutFrame, text="Total Books Count: {}".format(len(self.checkoutItems)), font="Bahnschrift 13 bold", fg="#669bbc", bg="white").place(x=2, y=90)
            checkoutButton = Button(checkoutFrame, text="Submit", background="red", highlightbackground="#0077b6", highlightthickness=2, bd=0, command = lambda invalidMemberId = invalidMemberId, memberId = memberId: self.checkoutBookSection(memberId, invalidMemberId))
            checkoutButton.place(x=2, y=123)

    def removeCartItem(self, item):
        '''
        Remove cart from checkoutList:
            item = Checkout Item (list)
        '''
        self.checkoutItems.remove(item)
        self.__displayCheckout()

    def checkoutBookSection(self, memberId, invalidMemberId):
        '''
        Checkout Books:
            memberId = Member Id(int)
            invalidMemberId (Label)
        '''
        memberID = memberId.get()
        if (bookCheckout.isMemberIDValid(memberID)):
            self.checkoutItems, self.bookIDList = bookCheckout.proceedToCheckout(self.checkoutItems, int(memberID), self.bookIDList)
            self.bookListData = self.database.getAllBooksList()
            memberId.insert(0, END)
            checkoutSuccessfull()
            self.__displayCheckout()
        else:
            invalidMemberId['text'] = 'Enter a Valid Input'
            invalidMemberId['fg'] = 'red'

    def updateCart(self, index, isReservation):
        '''
        update Carts:
            index = checkout items index (int)
            isReservation = is Reservation check (Boolean)
        '''
        self.checkoutItems.append(bookCheckout.getCheckoutListItem(list(self.bookListData.values[index]), isReservation, self.checkoutItems, 'a'))
        if (isReservation):
            self.addToReservation[index].place_forget()
        else:
            self.addToCartButtonList[index].place_forget()

    def removeCart(self, index, isReservation):
        '''
        Remove Carts:
            index = checkout items index (int)
            isReservation = is Reservation check (Boolean)
        '''
        self.checkoutItems.remove(bookCheckout.getCheckoutListItem(list(self.bookListData.values[index]), isReservation, self.checkoutItems, 'r'))
        if (isReservation):
            self.addToReservation[index].place(x=900, y=1)
        else:
            self.addToCartButtonList[index].place(x=900, y=1)

    def updateBookIdList(self, selectedBookId, index):
        '''
        Update BookId List:
            selectedBookId = Book ID (int)
            index = BookID items index (int)
        '''
        self.bookIDList[index] = int(str(selectedBookId).strip('()').strip(','))


    # GUI Return
    def __displayReturnBook(self):
        '''
        Display Return Books UI
        '''
        myCanvas = self.canvas
        myCanvas.delete('all')
        secondFrame = Frame(myCanvas, padx=20, pady=20, background="white")
        myCanvas.create_window((0, 0), window=secondFrame, anchor="ne", width=1150, height=4300)

        returnBooksList = self.database.getBooksListToReturn()
        
        if (len(returnBooksList)):
            yaxis = 115
            for index, bookItem in returnBooksList.iterrows():
                Frame(secondFrame, bg="white", highlightbackground="gray", highlightthickness=2, width=1100, height=50, pady=10).place(x=10, y=yaxis-10)
                Label(secondFrame, text=bookItem[0], bg="white", fg="black").place(x=15, y=yaxis)
                Label(secondFrame, text=bookItem[1], bg="white", fg="black").place(x=120, y=yaxis)
                Label(secondFrame, text=bookItem[2], bg="white", fg="black").place(x=290, y=yaxis)
                Label(secondFrame, text=bookItem[3], bg="white", fg="black").place(x=740, y=yaxis)
                Button(secondFrame, text="Return Books", bg="blue", fg="black", command= lambda memberID=bookItem[1], bookID=bookItem[0], checkoutDate=bookItem[3]: self.returnBook(memberID, bookID, checkoutDate)).place(x=900, y=yaxis)
                # Frame(secondFrame, bg="white", highlightbackground="gray", highlightthickness=1, width=1300).place(x=15, y=yaxis+30)
                yaxis+=65
        else:
            Label(secondFrame, text="No Records", bg="white", fg="red", font="Bahnschrift 15").place(x=290, y=115)

        Label(secondFrame, text="Pending Books", bg="white", fg="#333", font="Bahnschrift 22 bold").place(x=15, y=10)
        Label(secondFrame, text="BookID", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=15, y=70)
        Label(secondFrame, text="Member ID", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=120, y=70)
        Label(secondFrame, text="Book Title", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=290, y=70)
        Label(secondFrame, text="Checkout Date", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=740, y=70)
    
    def returnBook(self, memberID, bookID, checkoutDate):
        '''
        Return Books in DB:
            memberId = Member Id(int)
            bookID = Book ID (int)
            checkoutDate = Checkout Date (String)
        '''
        bookReturn.returnBookInLibraryDB(memberID, bookID, checkoutDate)
        self.bookListData = self.database.getAllBooksList()
        self.__displayReturnBook()

    # Display Recommendation
    def __displayRecommendedBooks(self):
        '''
        Display Recommended Books in UI
        '''
        myCanvas = self.canvas
        myCanvas.delete('all')
        secondFrame = Frame(myCanvas, padx=20, pady=20, background="#fff")
        myCanvas.create_window((0, 0), window=secondFrame, anchor="ne", width=1158, height=5380)
        Label(secondFrame, text="Books in Demand", fg="black", font="Bahnschrift 22 bold", bg="white").pack(side=TOP, anchor=W, padx=(15, 10))

        # Bar chart for frequently purchased books
        frequentlyPurchasedBookInfo = bookRecommendation.findFrequentlyPurchasedBooks()

        bookListForBarGraph = frequentlyPurchasedBookInfo.iloc[:,:2]
        bookListForBarGraph.set_index(0, inplace=True)
        frequentlyPurchasedBookFigure = plt.Figure(figsize=(22, 12), dpi=48)
        axis = frequentlyPurchasedBookFigure.add_subplot(111)
        bar = FigureCanvasTkAgg(frequentlyPurchasedBookFigure, secondFrame)
        bar.get_tk_widget().place(x=-10, y=30)
        bookListForBarGraph.plot(kind='bar', stacked=True, ax=axis,ylim=(0, 30), ylabel='No of time purchased', xlabel="Books ID")
        axis.legend(['Book Title'])

        # Highly Purchased Books by Genre
        genreRecommendation = frequentlyPurchasedBookInfo.iloc[:,1:3]
        genreRecommendationListWithCount = genreRecommendation.groupby(by=2).sum().sort_values(by=1, ascending=False)
        Label(secondFrame, text="Highly Purchased Genre", bg="white", fg="#333", font="Bahnschrift 22 bold").place(x=720, y=690)
        Frame(secondFrame, highlightbackground="#457b9d", background="white", highlightthickness=2, width=280, height=350).place(x=715, y=760)

        Label(secondFrame, text="Genre Name", fg="#576574", font="Bahnschrift 13 bold", bg="white").place(x=730, y=770)
        Label(secondFrame, text="Purchased Books \n Count", fg="#576574", font="Bahnschrift 13 bold", bg="white").place(x=850, y=770)
        yaxis = 810
        for index, recommendedGenre in genreRecommendationListWithCount.iterrows():
            Label(secondFrame, text=index, bg="white", fg="black").place(x=730, y=yaxis)
            Label(secondFrame, text=recommendedGenre.iloc[0], bg="white", fg="black").place(x=910, y=yaxis)
            yaxis+=35

        priceList = frequentlyPurchasedBookInfo.iloc[:10,3:4].values.tolist()

        Label(secondFrame, text="Purchase New Books", bg="white", fg="#333", font="Bahnschrift 22 bold").place(x=25, y=690)
        Label(secondFrame, text="Update Amount", bg="white", fg="black", font="Bahnschrift 14").place(x=25, y=730)
        booksCost = Entry(secondFrame, width=15, background="white", bd=0, highlightbackground="#a2d2ff", fg="black", font="BahnschriftLight 12", insertbackground="#333")
        booksCost.place(x=165, y=730)
        booksCost.insert(0, self.credictScore)
        Button(secondFrame, text="Find Books", background="blue", highlightbackground="#0077b6", highlightthickness=2, bd=0, command= lambda: self.findRecommendedBooksForLibrarian(booksCost, priceList)).place(x=305, y=730)

        # Label(secondFrame, highlightbackground="#457b9d", background="white", highlightthickness=2, width=580, height=287).place(x=15, y=730)
        if (len(self.findEachBookCount)):
            Frame(secondFrame, highlightbackground="#457b9d", background="white", highlightthickness=2, width=650, height=350).place(x=25, y=760)
            Label(secondFrame, text="Title", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=30, y=767)
            Label(secondFrame, text="Genre", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=250, y=767)
            Label(secondFrame, text="Price", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=415, y=767)
            Label(secondFrame, text="Total Books", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=560, y=767)
            yaxis = 800
            for index, recommendedGenre in frequentlyPurchasedBookInfo.head(10).iterrows():
                title = recommendedGenre[0] if len(recommendedGenre[0]) < 30 else recommendedGenre[0][0:30]
                Label(secondFrame, text=title, bg="white", fg="black").place(x=30, y=yaxis)
                Label(secondFrame, text=recommendedGenre[2], bg="white", fg="black").place(x=250, y=yaxis)
                Label(secondFrame, text=recommendedGenre[3], bg="white", fg="black").place(x=410, y=yaxis)
                Label(secondFrame, text=self.findEachBookCount[index], bg="white", fg="black").place(x=560, y=yaxis)
                yaxis+=28

    def findRecommendedBooksForLibrarian(self, booksCost, priceList):
        '''
        Find Equally splited Books Counts with details:
            booksCost - Given Book Cost (Int)
            priceList - Accumulated Price List from transaction DB (List) 
        '''
        self.credictScore = int(booksCost.get())
        arrayList = np.ones((10,), dtype=int)
        self.findEachBookCount = bookRecommendation.findBookCountsForRecommend(arrayList, self.credictScore, priceList, sumValue=0)
        self.__displayRecommendedBooks()
        self.__createNavigationBar()


    # Display Transaction logs
    def __displayTransactionLogs(self):
        '''
        Display Transaction logs UI
        '''
        myCanvas = self.canvas
        myCanvas.delete('all')
        secondFrame = Frame(myCanvas, padx=20, background="white")
        myCanvas.create_window((0, 0), window=secondFrame, anchor="ne", width=1150, height=10000)

        cardFrame1 = Frame(secondFrame, bg="White", width=600)
        cardFrame1.pack(fill=BOTH)
        Label(cardFrame1, text='',  background="white", width=60, font="Bahnschrift 17 bold", fg="blue").pack(side=TOP, anchor=W, pady=(0,70))
        Label(cardFrame1, text="Activity Logs", bg="white", fg="#333", font="Bahnschrift 22 bold").place(x=15, y=10)
        Label(cardFrame1, text="Book ID", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=15, y=70)
        Label(cardFrame1, text="Reservation Date", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=160, y=70)
        Label(cardFrame1, text="Checkout Date", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=420, y=70)
        Label(cardFrame1, text="Return Date", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=680, y=70)
        Label(cardFrame1, text="Member ID", fg="#576574", font="Bahnschrift 16 bold", bg="white").place(x=900, y=70)

        transactionLogs = self.database.getAllTransactionLogs()
        for index, row in transactionLogs.iterrows():
            cardFrame = Frame(secondFrame, bg="White",width=600)
            cardFrame.pack(fill=BOTH)
            Label(cardFrame, text='',  background="white", width=60, font="Bahnschrift 17 bold", fg="blue").pack(side=TOP, anchor=W, pady=(0,25))
            Label(cardFrame, text=row[1], fg="#333", background="white").place(x=15, y=20)
            reservationDate = '-' if row[2] == None else row[2]
            Label(cardFrame, text=reservationDate, fg="#333", background="white").place(x=160, y=20)
            checkoutDate = '-' if row[3] == None else row[3]
            returnDate = '-' if row[4] == None else row[4]
            Label(cardFrame, text=checkoutDate, fg="#333", background="white").place(x=420, y=20)
            Label(cardFrame, text=returnDate, fg="#333", background="white").place(x=680, y=20)
            Label(cardFrame, text=row[5], fg="#333", background="white").place(x=900, y=20)

def checkoutSuccessfull():
    '''
    Message box for successfull checkout
    '''
    messagebox.showinfo(title=None, message="Books are Checked Out Successfully")


###############################
####------MAIN----------#######
###############################


def main():
    window = Tk()
    dataBase = db.mainDB()
    MainGUI(window, dataBase)
    window.mainloop()

if __name__=='__main__':
    main()

