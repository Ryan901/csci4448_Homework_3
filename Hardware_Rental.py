#Ryan Murphy
#Collaborators: None
#
# A note on syntax: Because python does not support private variables in classes I followed the standard notation of starting all
# private variables and functions with an underscore (_) to indicate that they are private. 

# Note on execution: In my implementation I randomly generate both the customers and tools as well as forcing customers to wait a
# random amount of time before returning to rent a new tool, this amount of time could be between 0 and 4 days for regular and 
# casual customers and between 7 and 12 days for Business customers. However in an attempt to make grading easier I found a seed
# that I believe demonstrates that the program meets all the requirements. If you want to change it or remove the set seed it is the
# first line of the section commented as Main.
from random import randint, seed, shuffle
class Store():
    def __init__(self):
        self._inventory=[]
        self._activeRentals=[]
        self._completeRentals=[]
        self._totalIncome=0
    
    def generate_inventory(self,categoryPrices,numTools):
        '''Generate a random selection of tools in the provided categories with the specified price'''
        for i in range(0,numTools):
            categories=list(categoryPrices.keys())
            randCat=categories[randint(0,len(categories)-1)]
            self._inventory.append(Tool(randCat+" "+str(i),randCat, categoryPrices[randCat]))


    def return_rentals(self,day):
        '''Process rental returns that are due back today. Return tools to inventory. '''
        for rental in list(self._activeRentals):
            if rental.check_due(day):
                rental.returned_by_customer()
                self._inventory+=rental.get_tools()
                self._completeRentals.append(rental)
                self._activeRentals.remove(rental)
                
    def add_rental(self,rental):
        '''Take new rental record and file it in active rentals and take payment. '''
        self._activeRentals.append(rental)
        self._totalIncome+=rental.get_total()

    def get_inventory_count(self):
        ''' Return number of tools in inventory. '''
        return len(self._inventory)

    def get_some_tools(self,numberTools):
        ''' Randomly select the requested number of tools from inventory and return them. '''
        tools=[]
        i=0
        while i < numberTools and len(self._inventory)>0:
            index=randint(0,len(self._inventory)-1)
            tools.append(self._inventory.pop(index))
            i+=1
        return tools
    
    def print_results(self):
        '''Print Inventory, Financial and Rental Records. '''
        print("{} tools in invetory.\n".format(self.get_inventory_count()))
        print("Tool Inventory".center(68)+"\n")
        tools= [tool.get_name() for tool in self._inventory]
        print (tools)
        print("Total Income: {}".format(self._totalIncome))
        print("Active Rentals".center(68)+"\n")
        for rental in self._activeRentals:
            print(rental)
        print("Completed Rentals".center(68)+"\n")
        tempSorted=sorted(self._completeRentals,key=lambda x: x.get_start_date(),reverse=False)
        for rental in tempSorted:
            print(rental)
        

class Rent ():
    def __init__(self):
        pass
    def rent (self, customer, store, day):
        raise NotImplementedError

class BusinessRent (Rent):
    def rent(self, customer, store, day):
        tempRental=Rental(store.get_some_tools(3),day,7,customer)
        store.add_rental(tempRental)
        customer.add_rental(tempRental)

class CasualRent (Rent):
    def __init__(self):
        self._durationMin=1
        self._durationMax=2
        self._toolMin=1
        self._toolMax=2
    def rent (self, customer, store, day):
        duration=randint(self._durationMin,self._durationMax)
        toolCount=randint(self._toolMin,self._toolMax)
        toolCount=min(toolCount,3-customer.get_total_tools())
        tempRental=Rental(store.get_some_tools(toolCount),day,duration,customer)
        store.add_rental(tempRental)
        customer.add_rental(tempRental)
    
class RegularRent (CasualRent):
    def __init__(self):
        self._durationMin=3
        self._durationMax=5
        self._toolMin=1
        self._toolMax=3

class Tool ():
    def __init__(self,name,category,price):
        self._name=str(name)
        self._price=price
        self._category=str(category)
    def get_price(self):
        return self._price
    def get_name(self):
        return self._name
    def __str__(self):
        return self._category.ljust(20)+self._name.ljust(20)+(str(self._price)+".00").rjust(10)

class Customer ():
    def __init__(self,name,rentalType):
        self._rentals=[]
        self._totalTools=0
        self._name=name
        self._nextProject=randint(0,10)
        self._rentalType=rentalType
    def add_rental (self, rental):
        self._rentals.append(rental)
        self._totalTools+=rental.get_tool_count()
    def remove_rental (self, rental):
        self._totalTools-=rental.get_tool_count()
        self._rentals.remove(rental)
    def rent(self,store,day):
        self._rentalType.rent(self,store,day)
    def check_store_stock(self,store, day):
        '''Check if I need more tools and if the store has tools to give to me.'''
        return day==self._nextProject and store.get_inventory_count()>0 and self._totalTools<3
    def _set_next_project(self,day):
        '''Decide when I will be looking to rent tools again '''
        self._nextProject=day+randint(0,4)
    def visit(self,store,day):
        '''Go to the store to rent tools.'''
        self._rentalType.rent(self,store,day)
        self._set_next_project(day)
    def get_total_tools(self):
        return self._totalTools
    def get_name(self):
        return self._name
   
class BusinessCustomer (Customer):
    def check_store_stock(self,store,day):
        return store.get_inventory_count() >=3 and day >= self._nextProject and self._totalTools==0
    def _set_next_project(self,day):
        '''Decide when I will be looking to rent tools again '''
        self._nextProject=day+randint(7,12)

        
class Rental ():
    def __init__(self, tools, day, duration, customer):
        self._tools=tools
        self._startDate=day
        self._duration=duration
        self._customer=customer
        self._total=0
        self._calc_total()
        self._toolCount=len(tools)
    def returned_by_customer(self):
        '''Remove this rental from its customers rentals'''
        self._customer.remove_rental(self)
    def _calc_total(self):
        for tool in self._tools:
            self._total+=tool.get_price()
        self._total=self._total*self._duration
    def check_due(self, date):
        return self._startDate+self._duration == date
    
    def get_start_date(self):
        return self._startDate

    def get_total(self):
        return self._total

    def get_tools(self):
        return self._tools
    
    def get_tool_count(self):
        return self._toolCount

    def __str__(self):
        result=" Rental ".center(68,"#")+"\n"
        result+="# Name: {}".format(self._customer.get_name()).ljust(36) + "Day: {}".format(self._startDate).center(30)+" #\n"
        result+="#"+"-"*66+"#\n"
        result+="# Category".ljust(22)+"Tool".ljust(20)+"Rate".rjust(9)+"Days".center(6)+"SubTot".center(10)+"#\n"
        result+="#"+"-"*66+"#\n"
        for tool in self._tools:
            result+="# "+str(tool)+str(self._duration).center(5)+(str(self._duration*tool.get_price())+".00").center(10)+"#\n"
        result+="#"+" "*66+"#\n"
        result+="#"+" "*46+"Total: ".rjust(10)+(str(self._total)+".00").ljust(10)+"#\n"
        result+="#"*68
        return result

class Simulator():
    def __init__(self):
        self._customerCount=10
        self._toolCount=20
        self._categoryPrices={"Painting":25, "Concrete":15, "Plumbing":30, "Woodwork":10, "Yardwork":12}
        self._customerTypes=["Business","Casual","Regular"]
        self._customers=[]
        self._store=None
        self._day=1
    
    def generate_customers(self):
        busRent=BusinessRent()
        regRent=RegularRent()
        casRent=CasualRent()
        for i in range(0,self._customerCount):
            randType=self._customerTypes[randint(0,2)]
            if randType == "Business":
                self._customers.append(BusinessCustomer("Customer "+str(i),busRent))
            elif randType == "Regular":
                self._customers.append(Customer("Customer "+str(i),regRent))
            elif randType == "Casual":
                self._customers.append(Customer("Customer "+str(i),casRent))
    
    def generate_store(self):
        self._store=Store()
        self._store.generate_inventory(self._categoryPrices,self._toolCount)
    
    def _run_day(self):
        ''' Activates customers and checks if they are starting a new project and if there are tools available in the store for them
        if both requirements are met the customer goes to the store and rents some tools.  '''
        self._store.return_rentals(self._day)
        shuffle(self._customers)
        for customer in self._customers:
            if customer.check_store_stock(self._store,self._day):
                customer.visit(self._store,self._day)
        self._day+=1
        
    def run(self):
        while self._day<=35:
            self._run_day()

    def print_results(self):
        self._store.print_results()


# Main
seed(13)
sim=Simulator()
sim.generate_customers()
sim.generate_store()
sim.run()
sim.print_results()