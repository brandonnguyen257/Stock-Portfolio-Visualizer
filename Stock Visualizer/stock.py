import yfinance as yf
import json
import time
from datetime import date

#the StockPortfolio class holds a LIST of all the stocks in a indiviuals portfolio
class StockPortfolio:
    portfolio=[]        #LIST that holds the stocks of current portfolio
    size=0              #INT that keeps track of size of portfolio
    totalInvested=0     #FLOAT that keeps track of total amount invested
    totalReturn=0
    def __init__(self):
        self.portfolio=[]
        self.size=0
        self.totalInvested=0
        self.totalReturn=0
        self.dictSector={}

    def __init__(self,portfolioDict):
        self.portfolio=[]
        myStocks=portfolioDict.get('stocks')  #retrives dict of stocks from JSON
        for key,value in myStocks.items():
            tempStock=Stock(value)
            self.portfolio.append(tempStock)
            self.incSize()
            self.totalInvested+=(tempStock.shares*tempStock.averageCost)
        self.totalReturn=portfolioDict["totalReturn"]
        self.dictSector=portfolioDict.get('dictSector')
        

    def sectorDebug(self):
        print("inside sectorDebug()")
        for sector,tickerList in self.dictSector.items():
            print(sector)
            for ticker in tickerList:
                print("\t"+ticker)

    def tempSectorMake(self):
        sectorList=[]
        #iterate through portfolio
        for stock in self.portfolio:
            tempSector=stock.details["sector"]
            #checks if sector sexists in list
            if tempSector not in sectorList:
                #creates sector entry in dict
                self.dictSector[tempSector]=[]  
                sectorList.append(tempSector) 
            #adds stock to dict             
            self.dictSector[tempSector].append(stock.ticker)

    """inc size by 1"""
    def incSize(self):
        self.size+=1
    
    """updates size"""
    def updateSize(self,size):
        self.size=size
        
    """updates the SHARES of a STOCK"""          
    def updateStock(self,stock,shares,avgCost):
        #type: (str,float,float)  
        for x in self.portfolio:
            if x.ticker==stock:
                x.shares=shares
                x.averageCost=avgCost
                return
        print("Stock Does Not Exist")


    """Adds a STOCK to portfolio"""
    def addStock(self,stock):
        #type: (Stock)
        for tempStock in self.portfolio:
            #case where Stock exists in portfolio
            if (stock.ticker==tempStock.ticker):
                tempStock.shares=stock.shares
                tempStock.averageCost=stock.averageCost
                tempStock.totalReturn=tempStock.getTotalReturn()
                return
        #case where stock does not exist in portfolio
        self.portfolio.append(stock)
        self.incSize()
        self.totalInvested+=(stock.shares*stock.averageCost)
    
    """Removes a STOCK from portfolio"""
    def removeStock(self,stock):
        #type: (str)
        targetStock=stock.lower()
        for x in self.portfolio:
            if targetStock==x.ticker.lower():
                self.totalInvested-=(x.shares*x.averageCost)
                self.portfolio.remove(x)
                return True
        print("Stock Does Not Exist In Portfolio")
        return False
        
    """updates the lastClosingPrice of each stock within portfolio"""
    def refreshPortfolio(self):
        newTotalReturn=0
        for stock in self.portfolio:
            tempGain=stock.refreshStock()
            newTotalReturn+=tempGain
        self.totalReturn=round(newTotalReturn,2)
   
    """prints data about each stock within portfolio"""
    def prettyPrint(self):
        print("Stock\tAvg Cost\tShares\tClosing Price\tTotal Return")
        for x in self.portfolio:
            print(x.ticker+"\t$"+str(x.averageCost)+"\t\t"+str(round(x.shares,3))+"\t$"+str(x.lastClosingPrice)+"\t\t"+str(x.totalReturn))
        dashString="-"*55
        print(dashString+"\n\t\t\t\t$"+str(round(self.totalInvested,2))+"\t$"+str(self.totalReturn))
    
    def __str__(self):
        return str(self.portfolio)
    
    def __len__(self):
        return self.size
    
    """creates a JSON friendly dictionary to be saved and stored"""
    def toJson(self):
        #type(self) -> JSON
        stockDict={}
        for temp in self.portfolio:
            stockDict.update(temp.toJson())
        portfolioDict={'size':self.size,'totalReturn':self.totalReturn,'dictSector':self.dictSector,'stocks':stockDict}
        return portfolioDict


#the Stock class holds all the data of an individual stock
class Stock:
    # ticker: STR that holds ticker symbol
    # company: STR that holds the company name
    # lastClosingPrice: FLOAT that holds last closing price
    # averageCost: FLOAT that holds portfolio's avg cost of stock 
    # shares: FLOAT that holds portfolio's shares of stock
    # totalReturn FLOAT that holds the indvidual stocks totalReturn
    """
    Stock() can be initialized in 3 different ways
        1.case where param is a dict from loading from JSON files
        2.case where param is a new stock not in portfolio using .info
        3.case where param is a new stock not in portfolio using .history
    """
    def __init__(self,tempStock,shares=None,avg=None):
        #case where give param is a Dict (ex. loading from JSON files)
        if(shares==None or avg==None):
            self.ticker=tempStock["ticker"]
            self.company=tempStock["company"]
            self.lastClosingPrice=tempStock["lastClosingPrice"]
            self.averageCost=tempStock["averageCost"]
            self.shares=tempStock["shares"]       
            self.totalReturn=tempStock["totalReturn"]
            self.details=tempStock["details"]
        #case where param is a brand new stock not in portfolio
        else:    
            self.details={}
            #gets stock info
            try:
                data = yf.Ticker(tempStock).info
                self.company=data["shortName"]
                self.lastClosingPrice=data["regularMarketPreviousClose"]
                self.ticker=tempStock
                self.shares=shares
                self.averageCost=avg
                self.totalReturn=self.getTotalReturn()
                self.addDetails()
            #case where stock.info() doesnt work, calls history to get lastClosingPrice
            except:
                todayDate=date.today()     #get current date
                self.ticker=tempStock
                self.shares=shares
                self.averageCost=avg
                data = yf.Ticker(tempStock).history(start=todayDate,close=todayDate)
                self.lastClosingPrice=data["Close"][0]
                self.company=self.ticker
                self.totalReturn=self.getTotalReturn()
                self.addDetails()

    """updates avgerageCost"""  
    def updateAverageCost(self,avg):
        self.averageCost=avg
    
    """updates shares"""  
    def updateShares(self,shares):
        self.shares=shares
    
    """refreshes current stock to get latest closing price"""
    def refreshStock(self):
        todayDate=date.today()
        data = yf.Ticker(self.ticker).history(start=todayDate,close=todayDate)
        self.lastClosingPrice=data["Close"][0]
        self.totalReturn=self.getTotalReturn()
        return self.totalReturn

    def addDetails(self):
        tempList=["dividendYield","city","state","sector","marketCap","fullTimeEmployees","averageVolume"]
        try:
            data = yf.Ticker(self.ticker).info
            for x in tempList:
                if(data[x]==None):
                    self.details[x]="N/A"
                else:
                    self.details[x]=data[x]
        except:
            for x in tempList:
                self.details[x]="N/A"
            
        

            


        # self.details["dividendYield"]=data["dividendYield"]
        # print(data["dividendYield"])
        # self.details["city"]=data["city"]
        # self.details["state"]=data["state"]
        # self.details["sector"]=data["sector"]
        # self.details["marketCap"]=data["marketCap"]
        # self.details["fullTimeEmployees"]=data["fullTimeEmployees"]
        # self.details["averageVolume"]=data["averageVolume"]




    def getTotalReturn(self):
        return round((self.shares*self.lastClosingPrice)-(self.shares*self.averageCost),2)
    
    def __str__(self):
        return str(self.ticker)+" $"+str(self.averageCost)+ " " +str(self.shares)
    
    def toJson(self):
        stockDict={self.ticker:self.__dict__}
        return stockDict
    
    def prettyPrint(self):
        print(self.ticker," ",self.shares," ",self.averageCost," ",self.lastClosingPrice," ",self.totalReturn)
    
