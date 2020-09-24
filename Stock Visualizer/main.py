from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from stock import StockPortfolio
from stock import Stock

import sys
import json
import math
# from kivy.graphics import Rectangle
# from kivy.graphics import Color
# from kivy.graphics import Line
# from kivy.properties import ObjectProperty
# from kivy.uix.floatlayout import FloatLayout

#from kivy.uix.popup import Popup
brandonPortfolio={}

tempPortfolio={}


# Master Grid Display
# includes titleRow,StockRows,btnRow
class StockGrid(GridLayout):
    def __init__(self,**kwargs):
        super(StockGrid,self).__init__(**kwargs)
        self.cols=1
        self.addTitleRow()
        self.addStockRows()
        self.addButtonRow() 
        
    # brandonPortfolio.portfolio.sort(key=lambda x:x.shares*x.lastClosingPrice,reverse=True)        
    
    #adds title row  
    def addTitleRow(self):
        titleRowArray=["Ticker","Shares","Avg Cost","Last Closing","Return"]
        tempWidget=GridLayout(size_hint=(1,1))
        tempWidget.rows=1

        for entry in titleRowArray:
            tempLabel=Label(text=entry,bold=True,underline=True,color=[.69,.61,.85,1])
            tempWidget.add_widget(tempLabel)


        self.add_widget(tempWidget)
   
    #adds every row of stock from portfolio
    def addStockRows(self):
        for stock in tempPortfolio.portfolio:
            stockRowData=[stock.ticker,stock.shares,stock.averageCost,stock.lastClosingPrice,stock.totalReturn]
            self.add_widget(StockWidget(stockRowData,stock))
        
    #adds button features to bottom of display
    def addButtonRow(self):
        buttonRow=GridLayout()
        buttonRow.rows=1

        sortingAlphabetBtn=Button(text="Sort Alphabet")
        sortingAlphabetBtn.on_press=self.sortingAlphabet
        buttonRow.add_widget(sortingAlphabetBtn)

        refreshBtn=Button(text="Refresh")
        refreshBtn.on_press=self.refresh
        buttonRow.add_widget(refreshBtn)

        addNewStockBtn=Button(text="Add/Edit Stock")
        addNewStockBtn.on_press=self.addNewStock
        buttonRow.add_widget(addNewStockBtn)

        removeStockButton=Button(text="Remove Stock")
        removeStockButton.on_press=self.removeStock
        buttonRow.add_widget(removeStockButton)

        # sectorStockButton=Button(text="Sector Sort")
        # sectorStockButton.on_press=self.sectorSort
        # buttonRow.add_widget(sectorStockButton)

        self.add_widget(buttonRow)

    #WIP: sorts stocks by sectors
    def sectorSort(self):
        print("running sector sort")

    #function to go to addNewStock screen
    def addNewStock(self):
        screenManager.add_widget(AddStockScreen())
        screenManager.current="Add Stock"       

    #function to go to removeStock screen
    def removeStock(self):
        # print("removing Stock")
        screenManager.add_widget(RemoveStockScreen())
        screenManager.current="Remove Screen"

    #function that sorts stocks alphabetically
    def sortingAlphabet(self):
        tempPortfolio.portfolio.sort(key=lambda x:x.ticker,reverse=False)
        global mainScreen
        mainScreen=StockGridScreen()
        screenManager.switch_to(mainScreen)

    #updates stocks to show real time information
    def refresh(self):
        brandonPortfolio.refreshPortfolio()
        global mainScreen
        mainScreen=StockGridScreen()
        screenManager.switch_to(mainScreen)

#Label that will be used for the title row
class TitleLabel(Label):
    pass

#Label that will Display stock information
class StockLabel(Label):
    def __init__(self, **kwargs):
        super(StockLabel, self).__init__(**kwargs)        
    def updateText(self, newValue):
        self.text=str(newValue)

#Widget that displays a row of stock information
class StockWidget(GridLayout):
    #stockData: List that contains [ticker , shares, avgCost , lastCost, totalReturn]
    #                                  0        1       2          3          4
    #labelArray: list that contains labels of each data entry with corresponding indexes
    def __init__(self,stockData,stock,**kwargs):
        super(StockWidget,self).__init__(**kwargs)

        self.stockData=stockData
        self.stock=stock
        self.labelArray=[]
        self.rows=1
        
        self.ticker=TickerButton(text=str(self.stockData[0]))        
        self.ticker.bind(on_press=lambda x:self.tempBtn())
        self.labelArray.append(self.ticker)

        self.shares=StockLabel(text=str(self.stockData[1]))
        self.labelArray.append(self.shares)

        self.avgCost=StockLabel(text=str(self.stockData[2]))
        self.labelArray.append(self.avgCost)

        self.lastCost=StockLabel(text=str(self.stockData[3]))
        self.labelArray.append(self.lastCost)

        self.totalReturn=StockLabel(text=str(self.stockData[4]))
        self.labelArray.append(self.totalReturn)

        for data in self.labelArray:
            self.add_widget(data)
 
    def updateWidget(self,newValue):
        pass

    def tempBtn(self):
        screenManager.add_widget(StockDetailScreen(self.stock))
        screenManager.current="Setting"

#Button used for ticker to display details   
class TickerButton(Button):
    def __init__(self, **kwargs):
        super(TickerButton, self).__init__(**kwargs)      
        self.background_color=(0,0,0,0)

    def updateText(self, newValue):
        self.text=str(newValue)    


#Screen that shows Master Display
class StockGridScreen(Screen):
    def __init__(self, **kwargs):
        super(StockGridScreen, self).__init__(**kwargs)
        self.name="Main"
        tempGrid=StockGrid()
        self.add_widget(tempGrid)    
    
    def changeScene(self):
        screenManager.current="Setting"

#Screen that adds a stock
class AddStockScreen(Screen):
    def __init__(self, **kwargs):
        super(AddStockScreen, self).__init__(**kwargs)
        self.name="Add Stock"

        generalGrid=GridLayout()
        generalGrid.cols=1

        addStockGrid=GridLayout()
        addStockGrid.cols=2

        tickerTitle=Label(text="Ticker")
        self.tickerInput=TextInput(multiline=False,size_hint=(.01,.01))
        addStockGrid.add_widget(tickerTitle)
        addStockGrid.add_widget(self.tickerInput)

        shareTitle=Label(text="Share")
        self.shareInput=TextInput(multiline=False)
        addStockGrid.add_widget(shareTitle)
        addStockGrid.add_widget(self.shareInput)

        avgTitle=Label(text="Avg Cost")
        self.avgInput=TextInput(multiline=False)
        addStockGrid.add_widget(avgTitle)
        addStockGrid.add_widget(self.avgInput)

        generalGrid.add_widget(addStockGrid)

        backBtn=Button(text="Go Back To Main")
        backBtn.on_press=self.goMainScreen

        addStockBtn=Button(text="Add Stock",size_hint=(.1,.1))
        addStockBtn.on_press=self.addStock

        generalGrid.add_widget(addStockBtn)

        generalGrid.add_widget(backBtn)


        self.add_widget(generalGrid)    
    
    def addStock(self):
        try:
            tempTicker=str(self.tickerInput.text)
            tempShares=float(self.shareInput.text)
            tempAvg=float(self.avgInput.text)
            tempStock=Stock(tempTicker,shares=tempShares,avg=tempAvg)
            tempPortfolio.addStock(tempStock)
            tempPortfolio.portfolio.sort(key=lambda x:x.ticker,reverse=False)
            global mainScreen
            mainScreen=StockGridScreen()
            
            self.tickerInput.text=""
            self.shareInput.text=""
            self.avgInput.text=""
            self.goMainScreen()
            labelText="Stock Succesfully Added\nTicker: $"+tempTicker+"\nShares: "+str(tempShares)+"\navgCost: "+str(tempAvg)
            confirmPopup= Popup(title="Stock Added",content=Label(text=labelText),size_hint=(None,None),size=(400,400))
            confirmPopup.open()

        except:
            self.tickerInput.text=""
            self.shareInput.text=""
            self.avgInput.text=""
            invalidPopup= Popup(title="Invalid",content=Label(text="Stock Invalid"),size_hint=(None,None),size=(400,400))
            invalidPopup.open()

    def goMainScreen(self):
        screenManager.switch_to(mainScreen)
#Screen that shows details of specific stock
class StockDetailScreen(Screen):

    def __init__(self,stock, **kwargs):
        super(StockDetailScreen, self).__init__(**kwargs)
        #set class attributes
        self.name="Setting"
        self.stock=stock
        
        #create GridLayout to add to Screen class
        self.generalGrid=GridLayout()
        self.generalGrid.cols=1
        
        #add title of the Screen
        self.generalGrid.add_widget(Label(text=stock.company,bold=True,size_hint=(.05,.05)))
        
        #create inner GridLayout
        stockDataGrid=GridLayout()
        stockDataGrid.cols=2
        #create inner inner gridLayout
        mainDataGrid=self.getMainDataGrid()
        detailDataGrid=self.getDetailDataGrid()        
        stockDataGrid.add_widget(mainDataGrid)
        stockDataGrid.add_widget(detailDataGrid)
        
        #create and add button to go back
        self.generalGrid.add_widget(stockDataGrid)
        tempButton=Button(text="Back",size_hint=(.05,.05))
        tempButton.on_press=self.changeScene
        self.generalGrid.add_widget(tempButton)    

        #add GridLayout to Screen class
        self.add_widget(self.generalGrid)
    
    def changeScene(self):
        screenManager.switch_to(mainScreen)
    
    def getMainDataGrid(self):
        mainDataGrid=GridLayout()
        mainDataGrid.cols=1
        mainDataGrid.add_widget(Label(text="Ticker: "+self.stock.ticker))
        mainDataGrid.add_widget(Label(text="Shares: "+str(self.stock.shares)))
        mainDataGrid.add_widget(Label(text="Avg Cost: "+str(self.stock.averageCost)))
        mainDataGrid.add_widget(Label(text="Last Closing Price: "+str(self.stock.lastClosingPrice)))
        mainDataGrid.add_widget(Label(text="Return: "+str(self.stock.totalReturn)))
        return mainDataGrid

    def getDetailDataGrid(self):
        detailDataGrid=GridLayout()
        detailDataGrid.cols=1
        for key,value in self.stock.details.items():
            tempLabel=Label(text=key.title()+": "+str(value))
            detailDataGrid.add_widget(tempLabel)
        return detailDataGrid        

class SectorSortScreen(Screen):
    def __init__(self, **kwargs):
        super(SectorSortScreen, self).__init__(**kwargs)
        #set class attributes
        self.name="Sector Sort"
        

#Screen that removes a specific stock
class RemoveStockScreen(Screen):
    def __init__(self, **kwargs):
        super(RemoveStockScreen, self).__init__(**kwargs)
        self.name="Remove Screen"
        
        self.generalGrid=GridLayout()
        self.generalGrid.cols=1

        removeGrid=GridLayout()
        removeGrid.cols=2
        tickerLabel=Label(text="Enter Ticker: ")
        self.tickerInput=TextInput(multiline=False)
        removeGrid.add_widget(tickerLabel)
        removeGrid.add_widget(self.tickerInput)

        self.generalGrid.add_widget(removeGrid)
        
        removeBtn=Button(text="Remove Stock",size_hint=(.05,.05))
        removeBtn.on_press=self.remove 
        self.generalGrid.add_widget(removeBtn)

        homeBtn=Button(text="Go Back",size_hint=(.05,.05))
        homeBtn.on_press=self.goMainScreen 
        self.generalGrid.add_widget(homeBtn)

        self.add_widget(self.generalGrid)
    
    def remove(self):
        targetStock=self.tickerInput.text
        if(tempPortfolio.removeStock(targetStock)):
            global mainScreen
            mainScreen=StockGridScreen()
            self.goMainScreen()
            labelText="$"+targetStock+" Succesfully Removed"
            confirmPopup= Popup(title="Stock Removed",content=Label(text=labelText),size_hint=(None,None),size=(400,400))
            confirmPopup.open()
        else:
            self.tickerInput.text=""
            labelText="$"+targetStock+" Does Not Exist In Portfolio"
            confirmPopup= Popup(title="Stock Does Not Exit",content=Label(text=labelText),size_hint=(None,None),size=(400,400))
            confirmPopup.open()

    
    
    def goMainScreen(self):
        screenManager.switch_to(mainScreen)

class EditStockScreen(Screen):
    def __init__(self, **kwargs):
        super(EditStockScreen, self).__init__(**kwargs)
        self.name="Edit Screen"    


#"main" app to run
class StockVisualizerApp(App):
    def build(self):
        return screenManager
    
    def on_request_close(self,*args):
        
        return True
    


if __name__ == "__main__":
    myPortfolioDict={}
    
    #pulls data from "data base" (txt file) and parses it into a dictionary
    with open('stockPortfolio.json','r') as openfile:
        myPortfolioDict=json.load(openfile)
    brandonPortfolio=StockPortfolio(myPortfolioDict)
    tempPortfolio=brandonPortfolio

    screenManager= ScreenManager()
    mainScreen=StockGridScreen()
    screenManager.add_widget(mainScreen)
    StockVisualizerApp().run()
    #saves changes in portfolio back into "data base"
    with open("stockPortfolio.json", "w") as outfile: 
        json.dump(tempPortfolio.toJson(), outfile) 

