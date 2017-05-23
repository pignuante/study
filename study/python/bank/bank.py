class Bank:
    description = "this is a very simply implemented bank class"
    def __init__(self, name="KOREA"):
        self.name        = name
        self.__balance   = 10000000000
        self.__customers = {"Using": 1000000, "HongDu": 20000000, 
                            "CDE"  : 1500000, "JH"    : 300000000}
        self.interst = 1.25
    @property
    def balance(self):
        return self.__balance
    @balance.setter
    def balance(self, money):
        self.__balance += money
    def deposit(self, money): # saving
        self.balance += money
    def withdraw(self, money):
        if (self.balance >= money):
            self.balance -= money
            return 0
        return 1
    def remit(self, to, money):
        if (self.__customers.get(to, 0)):
            self.__customers[to] += money
            return 0
        return 1
    def printCustomers(self):
        for name, money in self.__customers.items():
            print("Name : {n},\t Money : {m}".format(n=name, m=money))
        print()
    def run(self):
        print("Run Bank Class")
        while (True):
            print()
            print("1. Customer List")
            print("2. Deposit")
            print("3. withdraw")
            print("4. remit")
            print("5. end")
            
            curr = int(input("Enter number : "))
            
            if (curr == 1):
                self.printCustomers()
            elif (curr == 2):
                while True:
                    money = int(input("Enter money : "))
                    if (money > 0):
                        self.deposit(money)
                        break
                    print("Enter Positive Number")
            elif (curr == 3):
                while True:
                    money = int(input("Enter money : "))
                    if (money > 0):
                        if (self.withdraw(money)):
                            print("There is not enough balance.")
                        break
                    print("Enter Positive Number")
            elif (curr == 4):
                to = str(input("Who? : ")); 
                while True:
                    money = int(input("Enter money : "))
                    if (money > 0):
                        if (self.remit(to, money)):
                            print("Wrong person!")
                        break
                    print("Enter Positive Number")
            elif (curr == 5):
                print("Bye!")
                break
            else:
                print("Wrong Command!")
        print()

if __name__ == "__main__":
    bank = Bank()
    bank.run()
