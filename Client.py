import pymongo
import sys
import random
class Client:
    def __init__(self):
        self.r_name = ''
        """Connection with MongoDB"""
        try:
            self.connection = pymongo.MongoClient("localhost", 27017)
            self.database = self.connection["myClient"]
            self.user_collection = self.database["userCollect"]
            print("Connection Successful...")
        except Exception as err:
            print(err)

    def option(self):
        option = int(input('Press 1 to Register : Press 2 to Login: '))
        try:
            if option == 1:
                self.register()
            else:
                self.login()
        except Exception as err:
            print(err)

# ________________Checking exit Register and User_____________________
    def exitRegister(self,email):
        try:
            query = {"email":email}
            result = self.user_collection.find(query)
            for i in result:
                register_id = i.get("_id")
                print("User email : ",register_id)
            return register_id
        except Exception as err:
            print(err)

    def exitUser(self,email,passcode):
        try:
            query = {"email":email,"passcode":passcode}
            result = self.user_collection.find(query)
            for i in result:
                login_id = i.get("_id")
                print("User login ID : ",login_id)
            return login_id
        except Exception as err:
            print(err)

# _______________Checking Email____________________________
    def checkUsername(self):
        uname, my_string = self.validEmail(self.r_name)
        domain = ["@gmail.com", "@yahoo.com", '@icloud.com', '@outlook.com']
        print(uname)
        print(my_string)
        uflag = False
        dflag = False
        for i in uname:
            if i >= chr(48) and i <= chr(57) or i >= chr(65) and i <= chr(90) or i >= chr(97) and i <= chr(122):
                uflag = True
        for i in range(len(domain)):
            if my_string == str(domain[i]):
                print(my_string)
                dflag = True
                break
        if (uflag == True and dflag == True):
            print('Valid username...')
            flag = True
        else:
            print('Invalid username!')
            flag = False
        return flag

 # _______________Validation Email____________________________
    def validEmail(self, username):
        user_list: list = []
        uname_list: list = []
        uname: str = ''
        my_string: str = ''
        for i in username:
            user_list.append(i)
        for i in user_list:
            uname_list.append(i)
            if i == '@':
                break
        for i in uname_list:
            if i != '@':
                uname = uname + str(i)
        for i in range(len(uname), len(user_list)):
            my_string = my_string + str(user_list[i])
        return uname, my_string

# _______________Checking Passcode____________________________
    def validPasscode(self, passcode):
        # to check length
        if not len(passcode) <= 10 and not len(passcode) >= 6:
            return False
        # to check space
        for i in passcode:
            if i == chr(32):
                return False
        # to check digit 0-9
        if True:
            count = 0
            for i in passcode:
                if i >= chr(48) and i <= chr(57):
                    count = 1
            if count == 0:
                return False
        # to check special character
        if True:
            count = 0
            for i in passcode:
                if i >= chr(33) and i <= chr(47) or i >= chr(58) and i <= chr(64) or i >= chr(91) and i <= chr(
                    96) or i >= chr(123) and i <= chr(126):
                    count = 1
            if count == 0:
                return False
        # to check capital letters
        if True:
            count = 0
            for i in passcode:
                if i >= chr(65) and i <= chr(90):
                    count = 1
            if count == 0:
                return False
        # to check small letters
        if True:
            count = 0
            for i in passcode:
                if i >= chr(97) and i <= chr(122):
                    count = 1
            if count == 0:
                return False
        # if all conditions fail
        return True

# _______________Checking Digit___________________________
    def checkDigit(self, menu):
        flag = False
        for i in menu:
            if i >= chr(48) and i <= chr(57):
                flag = True
            else:
                flag = False
                break
        if flag == False:
            print('Your input is invalid!')
        return flag

    def insertion(self,userForm):
        try:
            userInformation = self.user_collection.insert_one(userForm)
            print('Data are inserted...',userInformation.inserted_id)

        except Exception as err:
            print(err)

#___________________Getting Data From Database_______________________
    def getUsername(self,login_id):
        try:
            query = {'_id':login_id}
            result = self.user_collection.find(query)
            for i in result:
                username = i.get('email')
            return username
        except Exception as err:
            print(err)
    def getPasscode(self,login_id):
        try:
            query = {'_id':login_id}
            result = self.user_collection.find(query)
            for i in result:
                passcode = i.get('passcode')
            return passcode
        except Exception as err:
            print(err)

    def getAmount(self,login_id):
        try:
            query = {'_id':login_id}
            result = self.user_collection.find(query)
            for i in result:
                amount = i.get('amount')
            return amount
        except Exception as err:
            print(err)

#_____________________Updating Data_____________________________
    def updateName(self,login_id,new_name):
        try:
            username = self.getUsername(login_id)
            result = self.user_collection.update_one(
                {"_id":login_id},
                { "$set" : {
                    "email": new_name
                }}
            )
            update_name = self.getUsername(login_id)
            print('Updating username is successful from {0} to {1}.'.format(username,update_name))
        except Exception as err:
            print(err)

    def updatePasscode(self,login_id,new_passcode):
        try:
            oldPasscode = self.getPasscode(login_id)
            result = self.user_collection.update_one(
                {"_id":login_id},
                { "$set" : {
                    "passcode": new_passcode
                }}
            )
            update_passcode = self.getPasscode(login_id)
            print('Updating passcode is successful from {0} to {1}.'.format(oldPasscode,update_passcode))
        except Exception as err:
            print(err)

    def updateAmount(self,login_id,new_amount):
        try:
            result = self.user_collection.update_one(
                {"_id":login_id},
                { "$set" : {
                    "amount": new_amount
                }}
            )
            update_amount = self.getAmount(login_id)
            username = self.getUsername(login_id)
            print('Current account balance of {0}: ${1}'.format(username,update_amount))
        except Exception as err:
            print(err)

#___________________Generating ID________________________________
    def checkingUserCount(self):
        try:
            count = self.user_collection.find({},{"_id":0,"email":1})
            name = []
            for i in count:
                name.append(i)
            count_id = len(name)
            print('Count user : ',count_id)
            return count_id+1
        except Exception as err:
            print(err)

#____________________Register Route___________________________
    def register(self):
        print('\n-----------This is Register Form---------\n')
        while True:
            r_username = input('Pls enter user name to register : ')
            self.r_name = r_username
            flagName :bool = self.checkUsername()
            if bool(flagName):
                while True:
                    r_passcode1 = input('Pls enter user passcode to register : ')
                    flagPw :bool = self.validPasscode(r_passcode1)
                    if bool(flagPw):
                        r_passcode2 = input('Pls enter again passcode to confirm : ')
                        if(r_passcode1 == r_passcode2):
                            exit_register = self.exitRegister(r_username)
                            if exit_register:
                                print('Data is already exit!')
                                self.login()
                            else:
                                amount = int(input('Pls enter your amount : '))
                                id = None
                                id = self.checkingUserCount()
                                print(id)
                                userForm: dict = {"_id":id, "email": r_username, "passcode": r_passcode1, "amount": amount}
                                print(userForm)
                                self.insertion(userForm)
                        break
                    else:
                        print('Invalid Passcode!')
                        continue
                break
            else:
                continue

#___________________Login Route______________________
    def login(self):
        print('\n-----------This is Login Form---------\n')
        l_username = input('Pls enter user name to login : ')
        l_passcode = input('Pls enter user passcode to login : ')
        login_id = self.exitUser(l_username,l_passcode)
        if login_id:
            print('Login Success...')
            self.menu(login_id)
        else:
            print('You cannot login!')

# _______________Account Detail Menu___________________________
    def detailAccount(self, login_id):
        print("\n----------ACCOUNT DETAIL----------")
        username = self.getUsername(login_id)
        name,email = self.validEmail(username)
        print("Account Holder: ", name.upper())
        print("Accout Email: ", username)
        print("Account Password: ", self.getPasscode(login_id))
        print("Available balance: $", self.getAmount(login_id))

# _______________Deposit Menu___________________________
    def depositMoney(self, login_id, deposit_amount):
        my_balance: int = self.getAmount(login_id)
        total_balance = my_balance + deposit_amount
        self.updateAmount(login_id,total_balance)

#_______________Transfer Menu___________________________
    def transferMoney(self, login_id, transfer_id, transfer_amount):
        my_balance: int = self.getAmount(login_id)
        receiver_balance: int = self.getAmount(transfer_id)
        if (my_balance >= transfer_amount):
            my_balance = my_balance - transfer_amount
            receiver_balance = receiver_balance + transfer_amount
            self.updateAmount(login_id,my_balance)
            self.updateAmount(transfer_id,receiver_balance)
        else:
            print("Insufficient fund!")
            print("Your balance is ${0} only.".format(my_balance))
            print("Try with lesser amount than balance.")

# _______________Withdraw Menu___________________________
    def withdrawMoney(self, login_id, withdraw_amount):
        my_balance: int = self.getAmount(login_id)
        if my_balance >= withdraw_amount:
            my_balance = my_balance - withdraw_amount
            print('${0} withdraw successful!'.format(withdraw_amount))
            print('Current account balance: $', my_balance)
            self.updateAmount(login_id,my_balance)
        else:
            print("Insufficient fund!")
            print("Your balance is ${0} only.".format(my_balance))
            print("Try with lesser amount than balance.")
            print()

# _______________Transaction Menu___________________________
    def menu(self, login_id ):
        print("""
                TRANSACTION 
            *******************
                Menu:
                1. Account Detail
                2. Deposit
                3. Transfer
                4. Withdraw
                5. Update
                6. Exit
            *******************
            """)
        while True:
            menu_input = input('\nEnter 1,2,3,4,5 or 6 : ')
            flag: bool = self.checkDigit(menu_input)
            if flag:
                if int(menu_input) == 1:
                    self.detailAccount(login_id)
                elif int(menu_input) == 2:
                    print("\n----------Deposit Money----------")
                    deposit_amount: int = int(input('How much you want to deposit : $'))
                    self.depositMoney(login_id, deposit_amount)
                elif int(menu_input) == 3:
                    print("\n----------Transfer Money----------")
                    transfer_username: str = input('Pls enter username to transfer : ')
                    transfer_id: int = self.exitRegister(transfer_username)
                    transfer_amount: int = int(input('How much you want to transfer : $'))
                    print("\n We get to transfer ID : ", transfer_id)
                    print("\n My ID : ", login_id)
                    self.transferMoney(login_id, transfer_id, transfer_amount)
                elif int(menu_input) == 4:
                    print("\n----------Withdraw Money----------")
                    withdraw_amount: int = int(input("How much you want to withdraw : $"))
                    self.withdrawMoney(login_id, withdraw_amount)
                elif int(menu_input) == 5:
                    print("""
                Update Account
            *****************
                 Menu:
                 1. Change name
                 2. Change password
                 3. Change amount
            *****************
                                """
                          )
                    while True:
                        menu = int(input('Enter 1,2 or 3 : '))
                        if (menu == 1):
                            while True:
                                newName = input('Enter you want to change email : ')
                                self.r_name = newName
                                flag: bool = self.checkUsername()
                                if flag:
                                    self.updateName(login_id, newName)
                                    break
                                else:
                                    continue
                        elif (menu == 2):
                            while True:
                                newPw = input('Enter you want to change password : ')
                                flag :bool = self.validPasscode(newPw)
                                if flag:
                                    self.updatePasscode(login_id, newPw)
                                    break
                                else:
                                    continue
                        elif (menu == 3):
                            newAmount = int(input('Enter you want to change amount : $'))
                            self.updateAmount(login_id, newAmount)
                        else:
                            break
                elif int(menu_input) == 6:
                    username = self.getUsername(login_id)
                    name,email = self.validEmail(username)
                    print(f"""
                 printing receipt..............
            ****************************************
                  Transaction is now complete.
                  Transaction number: {random.randint(10000, 1000000)}
                  Account holder: {name.upper()}
                  Account email: {username}
                  Account password: {self.getPasscode(login_id)}
                  Available balance: ${self.getAmount(login_id)}

                  Thanks for choosing us as your bank
            ****************************************
                        """)

                else:
                    self.firstOption()
                    break

# _______________Main____________________________
print("\n*******WELCOME TO BANK OF MYBANK*******")
print("___________________________________________________________\n")
print("----------ACCOUNT CREATION----------")
if __name__ == '__main__':
    while True:
        client : Client = Client()
        client.option()
