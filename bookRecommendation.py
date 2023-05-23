import database as db
mainDB = db.mainDB()
import numpy as np

def findFrequentlyPurchasedBooks():
    '''
    Find frequently Purchased Books:
    '''
    return mainDB.getFrequentlyPurchasedBookInfo()

def findBookCountsForRecommend(arrayList, booksCost, priceList, sumValue):
    '''
    Recommend No. of books to Purchase books equally:
        arrayList = Initialize with numpy ones (list)
        booksCost = Total Books cost to analyse (int)
        priceList = Books price list (list)
        sumValue = Sum used for analyse the result (int)
    '''
    for index in range(len(arrayList)):
        sumValue += arrayList[index] * priceList[index][0]

    if (sumValue > booksCost):
        return 0
    elif (sumValue == booksCost):
        return 1
    else:
        return arrayList + findBookCountsForRecommend(arrayList, booksCost, priceList, sumValue)



if __name__=='__main__':
    print ("Find Frequently Purchased Books")
    print (findFrequentlyPurchasedBooks())
    print ('================================')

    # Find Book Counts For Recommend
    countListRslt = findBookCountsForRecommend(np.ones((4,), dtype=int), 500, [[40], [25], [25], [27]], 0)
    print (countListRslt)
    print ('================================')
