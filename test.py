import utility_functions
import table_creation
import game_creation
import table_creation
from pathlib import Path
import time
import sys
import subprocess as sub


TIMEOUT = 5
SUBTIMEOUT = 1
STRTHEAD = '\033[93m'
STRTSUCC = '\033[92m'
STRTFAIL = '\033[91m'
END = '\033[0m'

SALESHISTORY = "SalesHistory.csv"
INVENTORY = "Inventory.csv"

def testAuto(test, number, function_name, curr):
    print("Testing_{} Utility_Functions: {}".format(number, function_name))
    try:
        eval("utility_functions.{}(curr)".format(function_name))
        print("\t\t\t...success\n")
        time.sleep(SUBTIMEOUT)
    except Exception as e:
        print("\t\t\t...FAIL\n")
        print(str(e))
        time.sleep(SUBTIMEOUT)
    print("----------------------")
    if test != 11:
        testing(curr)

def testing(curr):
    ##################################################
    print("Which test case would you like to test?")
    print("1. display_player_by_name")
    print("2. list_players")
    print("3. male_players")
    print("4. female_players")
    print("5. list_events")
    print("6. players_by_event")
    print("7. winners_by_event")
    print("8. lookup_id")
    print("9. Teamscores")
    print("10. Winners by Event")
    print("11. Test Everything")
    print("12. Start Program")
    print("13. Exit Everything")

    result = input("\nEnter the number: ")
    if result == '':
        return True
    else:
        test = int(result)

    if test == 1 or test == 11:
        testAuto(test, 1, "display_player_by_name", curr)

    if test == 2 or  test == 11:
        testAuto(test, 2, "list_players", curr)

    if test == 3 or test == 11:
        testAuto(test, 3, "male_players", curr)


    #################################################


    if test == 4 or test == 11:
        testAuto(test, 4, "female_players", curr)

    if test == 5 or test == 11:
        testAuto(test, 5, "list_events", curr)

    if test == 6 or test == 11:
        testAuto(test, 6, "players_by_event", curr)


    if test == 7 or test == 11:
        testAuto(test, 7, "winners_by_event", curr)

    if test == 8 or test == 11:
        print("Testing_8 Utility_Functions: lookup_id")
        try:
            name = input("Enter the name: ")
            event = input("Enter the event: ")
            age = int(input("Enter the age: "))

            utility_functions.lookup_id(name, event, age, curr)
            print("\t\t\t...success\n")
            time.sleep(SUBTIMEOUT)
        except Exception as e:
            print("\t\t\t...FAIL\n")
            print(str(e))
            time.sleep(SUBTIMEOUT)
        print("----------------------")
        testing(curr)
    if test == 9:
        teamscores = """
        Select * from TeamScores
        """
        utility_functions.print_table(teamscores, 'Teamscores', curr)
    if test == 10:
        winners = """select * from Awards"""
        utility_functions.print_table(winners, 'Team winners', curr)
    if test == 15:
        pass

    if test == 12:
        return True
    if test == 13:
        return False


if __name__ == "__main__":
    main()