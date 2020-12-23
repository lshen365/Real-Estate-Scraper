from tkinter import *
class Gui():
    def __init__(self,master):
        self.rentVar = IntVar()
        self.fsbaVar = IntVar()
        self.fsboVar = IntVar()
        self.forAuctionVar = IntVar()
        self.foresaleForecloserVar = IntVar()
        self.premarketForecloserVar = IntVar()
        self.master = master
        master.title = ("GUI")
        self.zipcode = Label(master,text = "Enter Zipcode: ",pady = 10)
        self.zipcode_value = Text(master,height = 1, width = 20)
        self.zipcode_enter = Button(master,text="Search",padx = 2, command = self.get_zipcode)


        self.zipcode.grid(row=0,column = 0)
        self.zipcode_value.grid(row=0,column = 1)
        self.zipcode_enter.grid(row=0,column=3)

        #Filter Lables and Checkboxes
        self.filter_label = Label(master, text = "Search Filters:" , font = 5)
        self.rental_checkbox = Checkbutton(master, text="Rental Property", variable = self.rentVar, command = self.get_rent)
        self.foresale_forecloser_checkbox = Checkbutton(master, text="For Sale Forecloser Property" , variable = self.foresaleForecloserVar, command = self.get_foresale)
        self.premarket_forecloser_checkbox = Checkbutton(master,text = "PreMarket Pre Foreclosure", variable = self.premarketForecloserVar, command = self.get_premarket)
        self.forSaleByAgent = Checkbutton(master, text="FSBA", variable = self.fsbaVar, command = self.get_fsba)
        self.forSaleByOwner = Checkbutton(master,text= "FSBO", variable = self.fsboVar, command = self.get_fsbo)
        self.forAuction = Checkbutton(master, text="For Auction", variable = self.forAuctionVar, command = self.get_forAuction)

        #Filter Lables and Checkboxes GRID
        self.filter_label.grid(row = 3, column = 0, sticky = W, pady = 10)
        self.rental_checkbox.grid(row = 4, column = 0, sticky = W, pady = 2,)
        self.forSaleByAgent.grid(row = 4, column = 1,sticky = W, pady = 2)
        self.forSaleByOwner.grid(row = 4, column = 2, sticky = W, pady = 2)
        self.forAuction.grid(row = 4,column = 3, sticky = W, pady = 2)
        self.foresale_forecloser_checkbox.grid(row = 4, column = 4, sticky = W, pady = 2)
        self.premarket_forecloser_checkbox.grid(row = 4, column = 5, sticky = W, pady = 2)

    def get_zipcode(self):
        return self.zipcode_value.get("1.0",END)
        # self.foresale_forecloser_checkbox.pack()

    def get_rent(self):
        print(self.rentVar.get())
        return self.rentVar.get()

    def get_premarket(self):
        print(self.premarketForecloserVar.get())
        return self.premarketForecloserVar.get()

    def get_foresale(self):
        print(self.foresaleForecloserVar.get())
        return self.foresaleForecloserVar.get()

    def get_fsba(self):
        print(self.fsbaVar.get())
        return self.fsbaVar.get()

    def get_fsbo(self):
        print(self.fsboVar.get())
        return self.fsboVar.get()

    def get_forAuction(self):
        print(self.forAuctionVar.get())
        return self.forAuctionVar.get()





root = Tk()
my_gui = Gui(root)
root.mainloop()
