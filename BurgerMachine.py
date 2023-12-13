from enum import Enum
import sys
from BurgerMachineExceptions import ExceededRemainingChoicesException, InvalidChoiceException, InvalidStageException, NeedsCleaningException, OutOfStockException
from BurgerMachineExceptions import InvalidPaymentException, InvalidCombinationException, NoItemChosenException

class Usable:
    name = ""
    quantity = 0
    cost = 99

    def __init__(self, name, quantity = 10, cost=99):
        self.name = name
        self.quantity = quantity
        self.cost = cost

    def use(self):
        self.quantity -= 1
        if (self.quantity < 0):
            raise OutOfStockException
        return self.quantity 

    def in_stock(self):
        return self.quantity > 0
    def __repr__(self) -> str:
        return self.name

class Bun(Usable):
    pass

class Patty(Usable):
    pass

class Topping(Usable):
    pass

class STAGE(Enum):
    Bun = 1
    Patty = 2
    Toppings = 3
    Pay = 4

class BurgerMachine:
    # Constants https://realpython.com/python-constants/
    USES_UNTIL_CLEANING = 15
    MAX_PATTIES = 3
    MAX_TOPPINGS = 3


    buns = [Bun(name="No Bun", cost=0), Bun(name="White Burger Bun", cost=1), Bun("Wheat Burger Bun", cost=1.25),Bun("Lettuce Wrap", cost=1.5)]
    patties = [Patty(name="Turkey", quantity=20, cost=1), Patty(name="Veggie", quantity=20, cost=1), Patty(name="Beef", quantity=10, cost=1)]
    toppings = [Topping(name="Lettuce", quantity=10, cost=.25), Topping(name="Tomato", quantity=10, cost=.25), Topping(name="Pickles", quantity=10, cost=.25), \
    Topping(name="Cheese", quantity=10, cost=.25), Topping(name="Ketchup", quantity=10, cost=.25),
    Topping(name="Mayo", quantity=10, cost=.25), Topping(name="Mustard", quantity=10, cost=.25),Topping(name="BBQ", quantity=10, cost=.25)] 


    # variables
    remaining_uses = USES_UNTIL_CLEANING
    remaining_patties = MAX_PATTIES
    remaining_toppings = MAX_TOPPINGS
    total_sales = 0
    total_burgers = 0

    inprogress_burger = []
    currently_selecting = STAGE.Bun

    # rules
    # 1 - bun must be chosen first
    # 2 - can only use items if there's quantity remaining
    # 3 - patties can't exceed max
    # 4 - toppings can't exceed max
    # 5 - proper cost must be calculated and shown to the user
    # 6 - cleaning must be done after certain number of uses before any more burgers can be made
    # 7 - total sales should calculate properly based on cost calculation
    # 8 - total_burgers should increment properly after a payment
    

    def pick_bun(self, choice):
        if self.currently_selecting != STAGE.Bun:
            raise InvalidStageException
        for c in self.buns:
            if c.name.lower() == choice.lower():
                c.use()
                self.inprogress_burger.append(c)
                return
        raise InvalidChoiceException

    def pick_patty(self, choice):
        if self.currently_selecting != STAGE.Patty:
            raise InvalidStageException
        if self.remaining_uses <= 0:
            raise NeedsCleaningException
        if self.remaining_patties <= 0:
            raise ExceededRemainingChoicesException
        for f in self.patties:
            if f.name.lower() == choice.lower():
                f.use()
                self.inprogress_burger.append(f)
                self.remaining_patties -= 1
                self.remaining_uses -= 1
                return
        raise InvalidChoiceException

    def pick_toppings(self, choice):
        if self.currently_selecting != STAGE.Toppings:
            raise InvalidStageException
        if self.remaining_toppings <= 0:
            raise ExceededRemainingChoicesException
        for t in self.toppings:
            if t.name.lower() == choice.lower():
                t.use()
                self.inprogress_burger.append(t)
                self.remaining_toppings -= 1
                return
        raise InvalidChoiceException

    def reset(self):
        self.remaining_patties = self.MAX_PATTIES
        self.remaining_toppings = self.MAX_TOPPINGS
        self.inprogress_burger = []
        self.currently_selecting = STAGE.Bun

    def clean_machine(self):
        self.remaining_uses = self.USES_UNTIL_CLEANING
        
    def handle_bun(self, bun):
        self.pick_bun(bun)
        self.currently_selecting = STAGE.Patty

    def handle_patty(self, patty):
        if not self.inprogress_burger:
            raise InvalidCombinationException
        elif patty == "next":
            self.currently_selecting = STAGE.Toppings
        else:
            self.pick_patty(patty)


    def handle_toppings(self, toppings):
        if not self.inprogress_burger:
            raise InvalidCombinationException
        if toppings == "done" and any(item in self.patties + self.toppings for item in self.inprogress_burger):
            self.currently_selecting = STAGE.Pay
        elif toppings == "done":
            raise NoItemChosenException
        else:
            self.pick_toppings(toppings)


    def handle_pay(self, expected, total):
        if self.currently_selecting != STAGE.Pay:
            raise InvalidStageException
        if total == f"{expected:.2f}":
            print("Thank you! Enjoy your burger!")
            self.total_burgers += 1
            self.total_sales += expected # only if successful
            #print(f"Total sales so far {self.total_sales}")
            self.reset()
        else:
            raise InvalidPaymentException
        
    def print_current_burger(self):
        print(f"Current Burger: {','.join([x.name for x in self.inprogress_burger])}")

    def calculate_cost(self):
        # TODO add the calculation expression/logic for the inprogress_burger
        # Gagan Indukala Krishna Murthy - gi36 - 1st March 2023
        # Summary: Keeping cost initially as zero
        self.cost = 0
        # adding the input item cost from the user in a loop for ever input of items.
        for item in self.inprogress_burger:
            self.cost += item.cost
        return round(self.cost, 2) # round the numbers after decimal
        

    def run(self):
        try:
            if self.currently_selecting == STAGE.Bun:
                # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
                bun = input(f"What type of bun would you like {', '.join(list(map(lambda c:c.name.lower(), filter(lambda c: c.in_stock(), self.buns))))}?\n")
                self.handle_bun(bun)
                self.print_current_burger()
            elif self.currently_selecting == STAGE.Patty:
                patty = input(f"Would type of patty would you like {', '.join(list(map(lambda f:f.name.lower(), filter(lambda f: f.in_stock(), self.patties))))}? Or type next.\n")
                try:
                    self.handle_patty(patty)
                    # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
                    # Summary: If the patty is exceeded more than 3 then we are automatically going to the next stage after displaying error message as output to the user
                    # Changed to toppings stage
                except ExceededRemainingChoicesException:
                    print("Sorry! You've exceeded the maximum number of pattys that you can select, please choose a topping")
                    self.print_current_burger()
                    self.currently_selecting = STAGE.Toppings
            elif self.currently_selecting == STAGE.Toppings:
                toppings = input(f"What topping would you like {', '.join(list(map(lambda t:t.name.lower(), filter(lambda t: t.in_stock(), self.toppings))))}? Or type done.\n")
                try:
                    self.handle_toppings(toppings)
                    # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
                    # Summary:If the toppings is exceeded more than 3 then we are automatically going to the next stage after displaying an erro as output to the user
                    # Changed to displaying the total cost stage and getting paid from the user
                except ExceededRemainingChoicesException:
                    print("Sorry! You've exceeded the maximum number of toppings; proceeding to the payment portal")
                    self.print_current_burger()
                    self.currently_selecting = STAGE.Pay
                    # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
                    # Summary: If there is no patty or toppings choosen then NoItemChosenException will be executed and we are redirecting to the patty stage
                except NoItemChosenException:
                    print("Please choose at least one patty or topping.")
                    self.currently_selecting = STAGE.Patty
            elif self.currently_selecting == STAGE.Pay:
                expected = self.calculate_cost()
                # show expected value as currency format
                # require total to be entered as currency format
                total = input(f"Your total is ${expected:.2f}, please enter the exact value.\n")
                try:
                    self.handle_pay(expected, total)
                    # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
                    # Summary: If the amount entered by  the user doesnot match the total amount. error message will be printed.
                    # user will be given another chance to enter the right amount
                except InvalidPaymentException:
                    print("You've entered a wrong amount. Please try again :)")
                    self.run()
                choice = input("What would you like to do? (order or quit)\n")
                if choice == "quit":
                    #exit() in recursive functions creates stackoverflow
                    # use return 1 to exit
                    print("Quitting the burger machine")
                    return 1
        # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
        # Summary: If any of the above input items from the user is out of stock then error message is displayed 
        # and the user will be redirected to select differnt items
        except OutOfStockException:
            print("The selected option is out of stock. Please select another option")
            # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
        # Summary: If the USES_UNTIL_CLEANING exceed 15 then the user will be promted with needs cleaning message as the output
        # when the user types "clean" then "the machine as been cleaned" is shown as the output and continued with normal activities 
        except NeedsCleaningException:
            choice = input("Sorry, The machine needs cleaning! Please type 'clean' to clean the machine \n")
            if choice.lower() == "clean":
                print("The machine has been cleaned, you can continue")
                self.clean_machine()
        # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
        # In any of the above stage if the user has entered a invalid choice the InvalidChoiceException is called 
        # and asked the user to choose again with the given options
        except InvalidChoiceException:
            print("You've entered an invalid choice. Please choose from the given options")
            self.run()
        except KeyboardInterrupt:
            # quit
            print("Quitting the burger machine")
            sys.exit()
        
        # handle OutOfStockException
            # show an appropriate message of what stage/category was out of stock
        # handle NeedsCleaningException
            # prompt user to type "clean" to trigger clean_machine()
            # any other input is ignored
            # print a message whether or not the machine was cleaned
        # handle InvalidChoiceException
            # show an appropriate message of what stage/category was the invalid choice was in
        # handle ExceededRemainingChoicesException
            # show an appropriate message of which stage/category was exceeded
            # move to the next stage/category
        # handle InvalidPaymentException
            # show an appropriate message
        except:
            # this is a default catch all, follow the steps above
            print("Something went wrong")
        
        self.run()

    def start(self):
        self.run()

    
if __name__ == "__main__":
    bm = BurgerMachine()
    bm.start()