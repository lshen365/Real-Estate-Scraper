from tkinter import *
from Property_Grab import Property_Grab
from For_Sale_Parser import For_Sale


class Gui:
    def __init__(self, master):
        self.master = master
        master.title = "GUI"
        self.create_widgets()

    def create_widgets(self):
        self.result_text = StringVar()
        self.rentVar = IntVar()
        self.fsbaVar = IntVar()
        self.fsboVar = IntVar()
        self.forAuctionVar = IntVar()
        self.foresaleForecloserVar = IntVar()
        self.premarketForecloserVar = IntVar()
        master = self.master
        self.zipcode = Label(master, text="Enter Zipcode: ", pady=10)
        self.zipcode_value = Text(master, height=1, width=20)
        self.zipcode_enter = Button(master, text="Search", padx=2, command=self.search_result)
        self.result_label = Label(master, textvariable=self.result_text)

        self.zipcode.grid(row=0, column=0)
        self.zipcode_value.grid(row=0, column=1)
        self.zipcode_enter.grid(row=0, column=3)
        self.result_label.grid(row=1, column=1)

        # Filter Lables and Checkboxes
        self.filter_label = Label(master, text="Search Filters:", font=5)
        self.rental_checkbox = Checkbutton(master, text="Rental Property", variable=self.rentVar)
        self.foresale_forecloser_checkbox = Checkbutton(master, text="For Sale Forecloser Property",
                                                        variable=self.foresaleForecloserVar)
        self.premarket_forecloser_checkbox = Checkbutton(master, text="PreMarket Pre Foreclosure",
                                                         variable=self.premarketForecloserVar)
        self.forSaleByAgent = Checkbutton(master, text="FSBA", variable=self.fsbaVar)
        self.forSaleByOwner = Checkbutton(master, text="FSBO", variable=self.fsboVar)
        self.forAuction = Checkbutton(master, text="For Auction", variable=self.forAuctionVar)

        # Filter Lables and Checkboxes GRID
        self.filter_label.grid(row=3, column=0, sticky=W, pady=10)
        self.rental_checkbox.grid(row=4, column=0, sticky=W, pady=2, )
        self.forSaleByAgent.grid(row=4, column=1, sticky=W, pady=2)
        self.forSaleByOwner.grid(row=4, column=2, sticky=W, pady=2)
        self.forAuction.grid(row=4, column=3, sticky=W, pady=2)
        self.foresale_forecloser_checkbox.grid(row=4, column=4, sticky=W, pady=2)
        self.premarket_forecloser_checkbox.grid(row=4, column=5, sticky=W, pady=2)

    def search_result(self):
        def find_link():
            # try:
            zipcode = self.zipcode_value.get("1.0", 'end-1c')
            property_link = Property_Grab(zipcode, self.retreive_button_status())
            if property_link.zipcodes_get(zipcode):
                url = property_link.generate_link()
            else:
                print("Zipcode data does not exist. Searching it up now...")
                property_link.add_to_database()
                print("Trying again now...")
                property_link.zipcodes_get(zipcode)
                url = property_link.generate_link()
            self.result_text.set("Successfully generated Link")
            self.result_label.configure(foreground="green")
            return url

        # except :
        #     self.result_label.configure(foreground = "red")
        #     self.result_text.set("Failed to generate Link")

        url = find_link()
        if url is not None:
            For_Sale(url).interate_thru_property()
            self.result_text.set("Successfully Loaded Files")
            self.result_label.configure(foreground="green")

    def retreive_button_status(self):
        def get_rent():
            if bool(self.rentVar.get()):
                return "true"
            else:
                return "false"

        def get_premarket():
            if bool(self.premarketForecloserVar.get()):
                return "true"
            else:
                return "false"

        def get_foresale():
            if bool(self.foresaleForecloserVar.get()):
                return "true"
            else:
                return "false"

        def get_fsba():
            if bool(self.fsbaVar.get()):
                return "true"
            else:
                return "false"

        def get_fsbo():
            if bool(self.fsboVar.get()):
                return "true"
            else:
                return "false"

        def get_forAuction():
            if bool(self.forAuctionVar.get()):
                return "true"
            else:
                return "false"

        return get_rent(), get_fsba(), get_fsbo(), get_forAuction(), get_foresale(), get_premarket()


root = Tk()
my_gui = Gui(root)
root.mainloop()
