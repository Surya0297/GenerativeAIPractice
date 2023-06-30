stock={}


def addToStock():

    id =input("Enter snack id:")
    if id in stock:
        print("Snack With this is already exists")
        return

    name =input("Enter snack name:")
    price=input("Enter snack price:")
    available=input("Enter snack availability:")

    snack={'name':name,'price':price,'available':available}
    stock[id]=snack
    print("Snack added")

def viewStock():
    if len(stock)>0:
        print(stock)
    else :
        print("No Snack In Stock")

def updateSnack():
    id =input("Enter snack id:")
    if id not in stock:
        print("Snack With this id doest not exists")
        return
    
    price=input("Enter snack price to be updated:")
    available=input("Enter snack availability to be updated:")
    snack=stock[id]
    snack['available']=available
    snack['price']=price
    stock[id]=snack
    print("***** Snack updated *****")

def removeSnack():
    id =input("Enter snack id:")
    if id not in stock:
        print("Snack With this id doest not exists")
        return
    del stock[id]
    print("**** Snack deleted ****")

def saleRecord():
    id =input("Enter snack id:")
    if id not in stock:
        print("Snack With this id doest not exists")
        return
    snack=stock[id]
    available=snack['available']
    if available=='yes':
        print(snack['name'],"sold")
    else:
        print(snack['name'],"out of stock")

def menu():
    while True:
        print('1: Add Snack')
        print('2: Update Snack')
        print('3: Remove Snack')
        print('4: Sale Snack')
        print('5: View Stock')
        print('6: Exit')
        
        choice=int(input("Enter Choice:"))

        if choice==1:
            addToStock()
            print()
        elif choice==2:
            updateSnack()
            print()
        elif choice==3:
            removeSnack()
            print()
        elif choice==4:
            saleRecord ()
            print()      
        elif choice==5:
            viewStock()
            print()
        elif choice==6:
            print("*** Thanks for using our services ***")
            break
              
menu()