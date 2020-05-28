# Create a class called Account which will be an abstract class for three other classes called CheckingAccount,
# SavingsAccount and BusinessAccount. Manage credits and debits from these accounts through an ATM style program.

import random
import json
from pathlib import Path
from passlib.context import CryptContext

# Hash password/authenticate

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000)


def encrypt_password(password):
    return pwd_context.hash(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)

# create json file if it does not exist


my_file = Path(
    "C:\\Users\\Acer\\Desktop\\Bank_Project\\CustomerDatabase.json")
if my_file.is_file():
    pass

else:
    with open('CustomerDatabase.json', 'w') as f:
        f.write('{"all_customers":[{}]}')

# Customer Class


class Customer:
    def __init__(self, name, email, password, customer_id_num):
        self.name = name
        self.email = email
        self.password = password
        self.customer_id_num = customer_id_num


# Abstract Account Class

class Account:
    def __init__(self, account_type, balance, owner):
        self.account_type = account_type
        self.balance = balance
        self.owner = owner
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        print(
            f'You have deposited ${amount} your new account balance is ${self.balance}')
        self.transactions.append(f'Deposit of ${amount}')

    def withdraw(self, amount):
        if amount > self.balance:
            print(
                f'Not enough funds! You have ${self.balance} in your account')
        else:
            self.balance -= amount
            print(
                f'You withdrew ${amount} your new account balance is ${self.balance}')
            self.transactions.append(f'Withdraw of ${amount}')

    def transaction_history(self):
        transaction_string = ''
        for item in self.transactions[::-1]:
            transaction_string += '\n' + item
        print('Your Transactions from newest to oldest:' + transaction_string)


class SavingsAccount(Account):
    pass


class CheckingAccount(Account):
    pass


class BusinessAccount(Account):
    pass


# Convert JSON to Python OBJ

def convert_cstmr_to_obj(database):
    for name_key in database["all_customers"]:
        for second_key in name_key:
            name_key[second_key]["Customer"] = Customer(name_key[second_key]["Customer"]["name"],
                                                        name_key[second_key]["Customer"]["email"],
                                                        name_key[second_key]["Customer"]["password"],
                                                        name_key[second_key]["Customer"]["customer_id_num"])


def convert_accnt_to_obj(database):
    for name_key in database["all_customers"]:
        for second_key in name_key:
            if name_key[second_key]["Savings Account"]:
                transactions = name_key[second_key]["Savings Account"]["transactions"]
                name_key[second_key]["Savings Account"] = \
                    SavingsAccount(name_key[second_key]["Savings Account"]["account_type"],
                                   name_key[second_key]["Savings Account"]["balance"],
                                   name_key[second_key]["Savings Account"]["owner"])
                for item in transactions:
                    name_key[second_key]["Savings Account"].transactions.append(
                        item)
    for name_key in database["all_customers"]:
        for second_key in name_key:
            if name_key[second_key]["Checking Account"]:
                transactions = name_key[second_key]["Checking Account"]["transactions"]
                name_key[second_key]["Checking Account"] = \
                    SavingsAccount(name_key[second_key]["Checking Account"]["account_type"],
                                   name_key[second_key]["Checking Account"]["balance"],
                                   name_key[second_key]["Checking Account"]["owner"])
                for item in transactions:
                    name_key[second_key]["Checking Account"].transactions.append(
                        item)
    for name_key in database["all_customers"]:
        for second_key in name_key:
            if name_key[second_key]["Business Account"]:
                transactions = name_key[second_key]["Business Account"]["transactions"]
                name_key[second_key]["Business Account"] = \
                    SavingsAccount(name_key[second_key]["Business Account"]["account_type"],
                                   name_key[second_key]["Business Account"]["balance"],
                                   name_key[second_key]["Business Account"]["owner"])
                for item in transactions:
                    name_key[second_key]["Business Account"].transactions.append(
                        item)


# Convert obj to dictionary for JSON

def convert_cstmr_to_dict(database):
    for name_key in database["all_customers"][0]:
        database["all_customers"][0][name_key]["Customer"] = database["all_customers"][0][name_key]["Customer"].__dict__


def convert_accnt_to_dict(database):
    for name_key in database["all_customers"][0]:
        if database["all_customers"][0][name_key]["Savings Account"]:
            database["all_customers"][0][name_key]["Savings Account"] = \
                database["all_customers"][0][name_key]["Savings Account"].__dict__
    for name_key in database["all_customers"][0]:
        if database["all_customers"][0][name_key]["Checking Account"]:
            database["all_customers"][0][name_key]["Checking Account"] = \
                database["all_customers"][0][name_key]["Checking Account"].__dict__
    for name_key in database["all_customers"][0]:
        if database["all_customers"][0][name_key]["Business Account"]:
            database["all_customers"][0][name_key]["Business Account"] = \
                database["all_customers"][0][name_key]["Business Account"].__dict__


# ATM menu functions

def main_menu():
    print("Welcome to Kyle's Bank Services")
    selection = ''
    while selection.lower() != 'login' and selection.lower() != 'new customer' and \
            selection.lower() != 'close program':
        selection = input(
            'Would you like to Login, New Customer, or Close Program? ')

    if selection.lower() == 'login':
        return 'Login'

    elif selection.lower() == 'new customer':
        return 'New Customer'

    elif selection.lower() == 'close program':
        return 'Close Program'


def login():
    name = input("Please enter your name: ")
    try:
        with open('CustomerDatabase.json') as file:
            customer_db = json.load(file)
        convert_cstmr_to_obj(customer_db)
        if customer_db["all_customers"][0][name]:
            password = input('Please enter your password: ')

            if check_encrypted_password(password, customer_db["all_customers"][0][name]['Customer'].password):
                print('Welcome ' + name + ' you are logged in')
                return name

            else:
                print('Incorrect password')
                return 'Main Menu'
    except KeyError:
        return 'Not found'


def open_json_read():
    with open('CustomerDatabase.json') as file:
        customer_db = json.load(file)
    return customer_db


def open_json_write(database):
    with open('CustomerDatabase.json', 'w') as file:
        json.dump(database, file)


def create_customer():
    customer_db = open_json_read()
    convert_cstmr_to_obj(customer_db)

    name = input("Please enter your full name: ")

    for all_items in customer_db["all_customers"]:
        for name_key in all_items:
            if name_key == name:
                print('Customer Already Exists!')
                return None

    email = input("Please enter your email address: ")

    customer_id_num = 0
    while customer_id_num not in range(10000, 100000):

        customer_id_num = random.randint(10000, 99999)

        for key in customer_db["all_customers"][0]:
            for second_key in customer_db["all_customers"][0][key]:
                try:
                    if customer_db["all_customers"][0][key][second_key].customer_id_num == customer_id_num:
                        customer_id_num = 0
                except AttributeError:
                    continue

    convert_cstmr_to_dict(customer_db)
    while True:

        password = input("Please enter a password: ")

        password_check = input("Please confirm your password: ")

        if password == password_check:

            password = encrypt_password(password)

            customer_db["all_customers"][0][name] = {
                "Customer": Customer(name, email, password, customer_id_num).__dict__,
                "Savings Account": None,
                "Checking Account": None,
                "Business Account": None}

            open_json_write(customer_db)
            return name
        else:
            print("Passwords don't match")


def user_menu():
    selection = ''
    while selection.lower() != 'open account' and \
            selection.lower() != 'view accounts' and \
            selection.lower() != 'logout':
        selection = input('Would you like to Open Account, View Accounts, '
                          'or Logout? ')

    if selection.lower() == 'open account':
        return 'Open Account'
    elif selection.lower() == 'view accounts':
        return 'View Accounts'
    elif selection.lower() == 'logout':
        return 'Logout'


def pick_account(name):
    customer_db = open_json_read()
    convert_accnt_to_obj(customer_db)
    account_list = []
    for key in customer_db["all_customers"][0][name]:
        if customer_db["all_customers"][0][name][key]:
            try:
                account_list.append(
                    customer_db["all_customers"][0][name][key].account_type)
            except AttributeError:
                pass

    if len(account_list) == 1:
        print(f'You will view your {account_list[0]}')
        return account_list[0]

    elif len(account_list) == 2:

        which_account = ''
        while which_account.lower() != account_list[0].lower() and \
                which_account.lower() != account_list[1].lower():
            which_account = input(
                f'Do you want to view your {account_list[0]} or {account_list[1]}? ')
        if which_account.lower() == account_list[0].lower():
            return account_list[0]
        else:
            return account_list[1]

    else:
        which_account = ''
        while which_account.lower() != account_list[0].lower() and \
                which_account.lower() != account_list[1].lower() and \
                which_account.lower() != account_list[2].lower():
            which_account = input(f'Do you want to view your {account_list[0]}, '
                                  f'{account_list[1]}, or {account_list[2]}? ')
        if which_account.lower() == account_list[0].lower():
            return account_list[0]
        elif which_account.lower() == account_list[1].lower():
            return account_list[1]
        else:
            return account_list[2]


def view_account(name, account):
    customer_db = open_json_read()
    convert_accnt_to_obj(customer_db)
    selection = ''
    while selection.lower() != 'withdraw' and \
            selection.lower() != 'deposit' and \
            selection.lower() != 'transaction history':
        selection = input('Would you like to Withdraw, Deposit, '
                          'or Transaction History ')

    if selection.lower() == 'withdraw':
        withdraw_amount = ''
        while not withdraw_amount.isnumeric():
            withdraw_amount = input('How much would you like to withdraw? ')
        customer_db["all_customers"][0][name][account].withdraw(
            int(withdraw_amount))

    elif selection.lower() == 'deposit':
        deposit_amount = ''
        while not deposit_amount.isnumeric():
            deposit_amount = input('How much would you like to deposit? ')
        customer_db["all_customers"][0][name][account].deposit(
            int(deposit_amount))

    elif selection.lower() == 'transaction history':
        customer_db["all_customers"][0][name][account].transaction_history()

    convert_accnt_to_dict(customer_db)
    open_json_write(customer_db)


def create_account(name):
    customer_db = open_json_read()
    convert_accnt_to_obj(customer_db)
    account_type = ''

    while account_type.lower() != 'savings account' and \
            account_type.lower() != 'checking account' and \
            account_type.lower() != 'business account':
        account_type = input('Would you like to open a Savings Account, '
                             'Checking Account, or Business Account? ')

    if account_type.lower() == 'savings account':
        if not customer_db["all_customers"][0][name]['Savings Account']:
            deposit = int(input('How much would you like to deposit? '))
            print(f'Your Savings Account now has ${deposit}')
            customer_db["all_customers"][0][name]['Savings Account'] = \
                SavingsAccount('Savings Account', deposit, name)
            customer_db["all_customers"][0][name]['Savings Account'].transactions.append(
                f"Deposit of ${deposit}")
        else:
            print('You already have a Savings Account')

    elif account_type.lower() == 'checking account':
        if not customer_db["all_customers"][0][name]['Checking Account']:
            deposit = int(input('How much would you like to deposit? '))
            print(f'Your Checking Account now has ${deposit}')
            customer_db["all_customers"][0][name]['Checking Account'] = \
                CheckingAccount('Checking Account', deposit, name)
            customer_db["all_customers"][0][name]['Checking Account'].transactions.append(
                f'Deposit of ${deposit}')
        else:
            print('You already have a Checking Account')

    else:
        if not customer_db["all_customers"][0][name]['Business Account']:
            deposit = int(input('How much would you like to deposit? '))
            print(f'Your Business Account now has ${deposit}')
            customer_db["all_customers"][0][name]['Business Account'] = \
                BusinessAccount('Business Account', deposit, name)
            customer_db["all_customers"][0][name]['Business Account'].transactions.append(
                f'Deposit of ${deposit}')
        else:
            print('You already have a Business Account')
    convert_accnt_to_dict(customer_db)
    open_json_write(customer_db)


# Main system operations
while True:

    early_break = False
    while True:
        main_men = main_menu()
        if main_men == 'Login':
            login_attempt = login()
            if login_attempt == 'Main Menu':
                continue
            elif login_attempt == 'Not found':
                print('User not found!')
                continue

            else:
                while True:
                    user_input = user_menu()
                    if user_input == 'Open Account':
                        create_account(login_attempt)

                    elif user_input == 'View Accounts':
                        view_account(
                            login_attempt, pick_account(login_attempt))
                    else:
                        break
            break

        elif main_men == 'New Customer':
            entered_name = create_customer()
            if entered_name:
                create_account(entered_name)
                while True:
                    user_input = user_menu()
                    if user_input == 'Open Account':
                        create_account(entered_name)
                    elif user_input == 'View Accounts':
                        view_account(entered_name, pick_account(entered_name))
                    else:
                        break
                break
            else:
                continue

        else:
            early_break = True
            break

    if early_break:
        break
    close_program = ''
    while close_program.lower() != 'yes' and close_program.lower() != 'no':
        close_program = input('Would you like to close the program? ')

    if close_program.lower() == 'yes':
        break
    else:
        continue
