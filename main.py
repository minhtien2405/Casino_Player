import sys
import random
import json
from datetime import datetime
import time
import os


class User:
    def __init__(self, id, name, last_time, money, chips=0):
        self.id = id
        self.name = name
        self.last_time = last_time
        self.money = money
        self.chips = chips


CHIP_COST = 11
CHIP_SELL = 10
MONEY_START = 1000


def play_craps(object):
    current_chips = object.chips
    count = 1
    promt = 0
    while True:
        money_bet = int(input("how much you want to bet:"))
        if money_bet <= object.money:
            break
    while True:
        if current_chips <= 0:
            print('Your chip is not enough$. Please recharge to play the game')
            object.chips = current_chips
            return object
        else:
            s1 = random.randint(1, 6)
            s2 = random.randint(1, 6)
            k = s1 + s2
            print(f"Rolling pair of dice in turn {count}...")
            time.sleep(2)
            print(f"your points is {k} ({s1}+{s2})")
            if ((k == 7) or (k == 11)) and (count == 1):
                print("You win!")
                current_chips += 1
                break
            elif (k in [2, 3, 12]) and (count == 1):
                print("Your lose!")
                money_bet = 0 - money_bet
                current_chips -= 1
                break
            elif (count > 1) and (k == promt):
                print("You win!")
                current_chips += 1
                break
            elif (count > 1) and (k == 7):
                print("Your lose!")
                money_bet = 0 - money_bet
                current_chips -= 1
                break
            elif count == 1:
                promt = k
        count += 1
    object.money += money_bet
    print("Your current money is {:.2f}$, Your current chips is {}.".format(object.money, object.chips))
    object.chips = current_chips
    return object


def play_agd(object):
    current_chips = object.chips
    count = 1
    promt = 0
    while True:
        money_bet = int(input("how much you want to bet:"))
        if money_bet <= object.money:
            break
    while True:
        if current_chips <= 0:
            print('Your money is not enough$. Please recharge to play the game')
            object.chips = current_chips
            return object
        else:
            s1 = random.randint(1, 6)
            s2 = random.randint(1, 6)
            k = s1 + s2
            print(f"Rolling pair of dice in turn {count}...")
            time.sleep(2)
            print(f"your points is {k} ({s1}+{s2})")
            if ((k == 12) or (k == 11)) and (count == 1):
                print("You win!")
                current_chips += 1
                break
            elif (k == 2) and (count == 1):
                print("Your lose!")
                money_bet = 0 - money_bet
                current_chips -= 1
                break
            elif (count > 1) and (k > promt):
                print("You win!")
                current_chips += 1
                break
            elif (count > 1) and (k <= promt):
                print("Your lose!")
                money_bet = 0 - money_bet
                current_chips -= 1
                break
            elif count == 1:
                promt = k
        count += 1
    object.chips = current_chips
    object.money += money_bet
    print("Your current money is {:.2f}$, Your current chips is {}.".format(object.money, object.chips))
    return object


def buy_chip(__obj):
    while True:
        try:
            numbers_of_chips = int(input("Enter your number of chips you want to buy (-1: Out of buying chips):"))
        except:
            print("Number of chips you want to buy must be interger!!!")
        if numbers_of_chips == -1:
            print("Completed exit buying!")
            return __obj
        elif (numbers_of_chips * CHIP_COST <= __obj.money) and (numbers_of_chips > 0):
            __obj.money -= numbers_of_chips * CHIP_COST
            __obj.chips += numbers_of_chips
            print(f"Completed buying {__obj.chips} chips, your current money is {__obj.money}")
            return __obj
        else:
            print("Number of chips you buy is invalid!!!")


def sell_chip(__obj):
    while True:
        try:
            numbers_of_chips = int(input("Enter your number of chips you want to sell (-1: Out of selling chips):"))
        except:
            print("Number of chips you want to buy must be interger!!!")
        if numbers_of_chips == -1:
            print("Completed exit selling!")
            return __obj
        elif (numbers_of_chips <= __obj.chips) and (numbers_of_chips > 0):
            __obj.money += numbers_of_chips * CHIP_SELL
            __obj.chips -= numbers_of_chips
            print(f"Completed selling {numbers_of_chips} chips, your current money is {__obj.money}$")
            return __obj
        else:
            print("Number of chips you buy is invalid!!!")


def save_game(object, users, checking):
    if checking == True:
        for i in range(len(users)):
            if users[i]["id"] == id_user and users[i]["name"] == name_user:
                users[i]["money"] = object.money
                break
    else:
        users.append(object.__dict__)
    # print(users, type(users))
    json_obj = json.dumps(users, indent=4)
    with open('history.json', 'w') as f:
        f.write(json_obj)
    print("Save game finished.")


def status_report(object, users, checking, saved):
    print("Your current money is {:.2f}$, Your current chips is {}.".format(object.money, object.chips))
    choice = input("Do you want to continue (Y: continue, otherwise: Quit game)? ")
    if choice not in ["Y", "y"]:
        cash_out(object, users, checking, saved)


def cash_out(object, users, checking, saved):
    # print(type(users))
    if saved == True:
        print("Thank you for playing! Your money is {:.2f}$.".format(object.money))
        sys.exit()
    else:
        print("You have not saved yet...")
        while True:
            choice_saving = input("Do you want to save? (Y/N): ").upper()
            if choice_saving in ["Y", "N"]:
                if choice_saving == "Y":
                    saved = True
                    save_game(object, users, checking)
                    print("Thank you for playing! Your money is {:.2f}$, Your current chips is {}.".format(object.money,
                                                                                                           object.chips))
                else:
                    print("Thanks you for playing!")
                sys.exit()


def select_in_range(prompt, min, max):
    choice = input(prompt)
    while not choice.isdigit() or int(choice) < min or int(choice) > max:
        choice = input(prompt)
    choice = int(choice)
    return choice


def read_users_from_json():
    with open("history.json", "r+") as file:
        try:
            data = json.load(file)
        except:
            data = []
            json.dump(data, file)
        if not isinstance(data, list):
            return [data]
        return data


def show_menu():
    print("Main Menu:")
    print("---------------------------------------------------")
    print("| Option 1: Buy chips.                            |")
    print("| Option 2: Sell chips.                           |")
    print("| Option 3: Play craps.                           |")
    print("| Option 4: Play Arup's Game of Dice.             |")
    print("| Option 5: Status Report.                        |")
    print("| Option 6: Quit.                                 |")
    print("---------------------------------------------------")


def user_checking(id_user, name_user, users):
    name_checking = False
    id_checking = False
    for entry in users:
        if entry["name"] == name_user:
            name_checking = True
            break
    for entry in users:
        if entry["id"] == id_user:
            id_checking = True
            break
    if id_checking and name_checking:
        return True
    elif not id_checking:
        return False
    else:
        return None


if __name__ == '__main__':
    users = read_users_from_json()
    saved = False
    while True:
        id_user = input("Please enter your id: ")
        name_user = input("Please enter your name: ").lower().title()
        if user_checking(id_user, name_user, users) == None:
            print("Invalid account!!")
            continue
        checking = user_checking(id_user, name_user, users)
        break
    time_current = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if checking == True:
        print(f"Welcome back, {name_user}!")
        for entry in users:
            if entry["id"] == id_user and entry["name"] == name_user:
                __obj = User(id_user, name_user, time_current, entry["money"], entry["chips"])
                break
    elif checking == False:
        print(f"Welcome to us, {name_user}!")
        __obj = User(id_user, name_user, time_current, MONEY_START)
    print(f"You have had got {__obj.money}$ and {__obj.chips} chips in my wallet")

    while True:
        show_menu()
        choice = select_in_range("Select an option (1-6):", 1, 6)
        if choice == 1:
            __obj = buy_chip(__obj)
        elif choice == 2:
            __obj = sell_chip(__obj)
        elif choice == 3:
            __obj = play_craps(__obj)
        elif choice == 4:
            __obj = play_agd(__obj)
        elif choice == 5:
            status_report(__obj, users, checking, saved)
        elif choice == 6:
            cash_out(__obj, users, checking, saved)
        time.sleep(2)
        os.system('cls')
