import os
import sys
import competition
import utility_functions
import subprocess as sub
import test
from pathlib import Path
import display_graphs
import table_creation


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait():
    return isinstance(input('Press Enter to continue...'), str)

def display_title():
    clear()
    title = """
    ██████╗ ██╗   ██╗██████╗  ██████╗                                                      
    ██╔══██╗██║   ██║██╔══██╗██╔════╝                                                      
    ██████╔╝██║   ██║██████╔╝██║  ███╗                                                     
    ██╔═══╝ ██║   ██║██╔══██╗██║   ██║                                                     
    ██║     ╚██████╔╝██████╔╝╚██████╔╝                                                     
    ╚═╝      ╚═════╝ ╚═════╝  ╚═════╝                                                      
                                                                                        
    ██████╗ ██████╗ ███╗   ███╗██████╗ ███████╗████████╗██╗████████╗██╗ ██████╗ ███╗   ██╗
    ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██║╚══██╔══╝██║██╔═══██╗████╗  ██║
    ██║     ██║   ██║██╔████╔██║██████╔╝█████╗     ██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║
    ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══╝     ██║   ██║   ██║   ██║██║   ██║██║╚██╗██║
    ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗   ██║   ██║   ██║   ██║╚██████╔╝██║ ╚████║
    ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝   ╚═╝   ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                        

                                                                
    """
    print(title)
    return wait()
    

def display_top_menu():
    clear()
    menu = """
    Main Menu

        1. Run New Competition
        2. Modify, or Delete Records
        3. Display Players
        4. Display Events
        5. Display Winners
        6. Look Up Player ID
        7. Display Player Stats
        8. Display Graphs and Exit

    Select an option: """
    print(menu, end='')
    
def handle_choice(conn, curr):
    while True:
        try:
            choice = int(input())
            if choice < 1 or choice > 9:
                raise ValueError
            else:
                break
        except:
            print('The choice is not valid, choose again. ')
    
    if choice == 1:
        return run_new_competition(conn, curr)

    elif choice == 2:
        return modify_record(conn, curr)

    elif choice == 3:
        return display_players(conn, curr)

    elif choice == 4:
        return display_events(conn, curr)

    elif choice == 5:
        return display_winners(conn, curr)

    elif choice == 6:
        return look_up(conn, curr)

    elif choice == 7:
        return player_stats(conn, curr)
    
    elif choice == 8:
        display_graphs.run_dash()

    else:
        return False

def display_player_stats_menu():
    clear()
    menu = """
    Player Statistics

        1. All Player Stats
        2. Player Stats by Event ID
        3. Top Scores by Event
        4. Finalists
        5. Exit
    
    Select an Option: """
    print(menu, end='')

def player_stats(conn, curr):
    while True:
        display_player_stats_menu()
        while True:
            try:
                choice = int(input())
                if choice < 1 or choice > 5:
                    raise ValueError
                else:
                    break
            except:
                print('The choice is not valid, choose again: ', end='')
        if choice == 1:
            clear()
            utility_functions.player_stats_by_all(curr)
            wait()
        elif choice == 2:
            clear()
            utility_functions.player_stats_by_event_id(curr)
            wait()
        elif choice == 3:
            clear()
            utility_functions.player_stats_by_top_scores(curr)
            wait()
        elif choice == 4:
            clear()
            utility_functions.player_stats_by_finals(curr)
            wait()
        else:
            return True

def run_new_competition(conn, curr):
    clear()
    print('Running new Competition...')
    competition.main_code(conn, curr, 25)
    print('Finished')
    return wait()

def display_modify_menu():
    clear()
    menu = """
    Modify Record

        1. Delete by player ID
        2. Modify by Player ID
        3. Return to Main Menu

    Select an option: """
    print(menu, end='')

def modify_record(conn, curr):
    while True:
        display_modify_menu()
        while True:
            try:
                choice = int(input())
                if choice < 1 or choice > 3:
                    raise ValueError
                else:
                    break
            except:
                print('The choice is not valid, choose again: ', end='')
        
        if choice == 1:
            clear()
            print('Deleting player by ID\n')
            utility_functions.delete_player_by_id(conn, curr)
            wait()

        elif choice == 2:
            clear()
            utility_functions.update_player_by_id(conn, curr)
            wait()
        else:
            return True

def display_players_menu():
    clear()
    menu = """
    Display Player Information

        1. Players Alphabetically
        2. Players by Player ID
        3. Players by Event
        4. Male Players
        5. Female Players
        6. Return to Main Menu

    Select an option: """
    print(menu, end='')

def display_players(conn, curr):
    while True:
        display_players_menu()
        while True:
            try:
                choice = int(input())
                if choice < 1 or choice > 6:
                    raise ValueError
                else:
                    break
            except:
                print('The choice is not valid, choose again: ', end='')
        
        if choice == 1:
            clear()
            utility_functions.display_player_by_name(curr)
            wait()

        elif choice == 2:
            clear()
            utility_functions.list_players(curr)
            wait()

        elif choice == 3:
            clear()
            utility_functions.players_by_event(curr)
            wait()
        
        elif choice == 4:
            clear()
            utility_functions.male_players(curr)
            wait()
        
        elif choice == 5:
            clear()
            utility_functions.female_players(curr)
            wait()

        else:
            return True


        
def display_events(conn, curr):
    clear()
    utility_functions.list_events(curr)
    return wait()

def display_winners(conn, curr):
    clear()
    print('Winners\n')
    utility_functions.winners_by_event(curr)
    return wait()

def look_up(conn, curr):
    clear()
    print('Look up Player by ID\n')
    while True:
        try:
            name = str(input('Enter the player\'s full name: ')).title()
            if len(name.split()) != 2:
                print('\nPlayer name must be a first name and last name. Ex: Bob Dylan')
                raise ValueError
            age = int(input('Enter the player\'s age: '))
            event_id = int(input('Enter the event ID the player participated in: '))
            utility_functions.lookup_id(name, event_id, age, curr)
            break
        except ValueError:
            print('Please enter information which is correctly formatted\n')
            
    return wait()

def main():
    conn, curr = utility_functions.connect()

    events = [('ErangelSolo', 25)]
    awards = [{'First': '$5000', 'Second': '$2500', 'Third': '$1000'}]

    if len(sys.argv) > 1:
        if sys.argv[1] == '-t':
            clear()
            test.testing(curr)
        else:
            print('Arguments not recognized, terminating program.')
            return
    else:
        if not table_creation.isredundant(curr):
            table_creation.create_tables(events, awards, conn, curr)

            for event in events:
                competition.run_competition(event, conn, curr)
                game_creation.Game.team_id = 1

        display_title()
        
        while True:
            display_top_menu()
            if not handle_choice(conn, curr):
                conn.close()
                break

if __name__ == '__main__':
    main()