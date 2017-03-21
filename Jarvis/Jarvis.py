from os import system
from time import ctime
from colorama import Fore
from utilities.GeneralUtilities import wordIndex
from packages.music import play
from packages.todo import todoHandler
from packages import newws, mapps, picshow, evaluator
 
"""
    AUTHORS' SCOPE:
        We thought that the source code of Jarvis would
        be more organized if we treat Jarvis as Object.
        So we decided to create this Jarvis Class which
        implements the core functionality of Jarvis in a
        simpler way than the original __main__.py.
    HOW TO EXTEND JARVIS:
        If you would like to add extra functionality to
        Jarvis (for example new actions like "record" etc.)
        you only need to add this action to the action dict
        (look on __init__(self)) along with a apropriate
        function name. Then you need to implement this function
        as a local function on reactions() method.
    DETECTED ISSUES:
        * Furthermore, "near me" command is unable to find
        the actual location of our laptops.
"""
 
class Jarvis:
    # We use this variable at Breakpoint #1.
    # We use this in order to allow Jarvis say "Hi", only at the first interaction.
    first_reaction = True

    def __init__(self):
        """
        This constructor contains a dictionary with Jarvis Actions (what Jarvis can do).
        In alphabetically order.
        """
        self.actions = {"check ram": "check_ram",
                        "decrease volume": "decrease_volume",
                        "directions": "directions",           # Doesn't check if 'to' exist
                        "error": "error",
                        "evaluate": "evaluate",
                        "exit": "quit",
                        "goodbye": "quit",
                        "hotspot start": "hotspot_start",
                        "hotspot stop": "hotspot_stop",
                        "how are you?": "how_are_you",
                        "increase volume": "increase_volume",
                        "movies": "movies",
                        "music": "music",
                        "near": "near",
                        "news": "news",
                        "open camera": "open_camera",
                        "quit": "quit",
                        "search for a string in file": "string_pattern",
                        "show me pics of": "display_pics",
                        "todo": "todo",
                        "weather": "weather", 
                        "what time is it": "clock", 
                        "where am i": "pinpoint"        
                        }

    def reactions(self, key, data):
        """
        This function contains local functions which are implementing
        Jarvis' actions. In alphabetically order.
        :param key: the action which corresponds to a local function
                    eg. key = (How are you) (according to actions dictionary)
                    corresponds to how_are_you() function.
                Data: the data which corresponds to an extra input needed
                    eg. music method needs a song name. (music closer)
        :return: This method does not return any objects.
        """

        def check_ram():
            system("free -lm")

        def clock():
            print(Fore.BLUE + ctime() + Fore.RESET)

        def decrease_volume():
            system("pactl -- set-sink-volume 0 -10%")

        def directions():
            wordList = data.split()
            to_index = wordIndex(data, "to")
            if " from " in data:
                from_index = wordIndex(data, "from")
                if from_index > to_index:
                    toCity = " ".join(wordList[to_index + 1:from_index])
                    fromCity = " ".join(wordList[from_index + 1:])
                else:
                    fromCity = " ".join(wordList[from_index + 1:to_index])
                    toCity = " ".join(wordList[to_index + 1:])
            else:
                toCity = " ".join(wordList[to_index + 1:])
                fromCity = 0
            mapps.directions(toCity, fromCity)

        def display_pics():
            picshow.showpics(data)

        def error():
            """
            In case of an error or typo during user's input we notify the
            user that something went wrong or the command he send is not
            supported by Jarvis.
            :return: Nothing to return.
            """
            print(Fore.RED + "I could not identify your command..." + Fore.RESET)

        def evaluate():
            tempt = data.split(" ", 1) or ""
            if len(tempt) > 1:
                evaluator.calc(tempt[1])
            else:
                print(Fore.RED + "Error : Not in correct format" + Fore.RESET)

        def hotspot_start():
            system("sudo ap-hotspot start")
 
        def hotspot_stop():
            system("sudo ap-hotspot stop")

        def how_are_you():
            print(Fore.BLUE + "I am fine, How about you" + Fore.RESET)

        def increase_volume():
            system("pactl -- set-sink-volume 0 +3%")

        def movies():
            try:
                movie_name = raw_input(Fore.RED + "What do you want to watch?\n" + Fore.RESET)
            except:
                movie_name = input(Fore.RED + "What do you want to watch?\n" + Fore.RESET)
            system("ims " + movie_name)

        def music():
            play(data)

        def near():
            wordList = data.split()
            things = " ".join(wordList[0:wordIndex(data, "near")])
            if " me" in data:
                city = 0
            else:
                wordList = data.split()
                city = " ".join(wordList[wordIndex(data, "near") + 1:])
                print city
            mapps.searchNear(things, city)

        def news():
            newws.show_news()

        def open_camera():
            print "Opening Cheese ...... "
            system("cheese")

        def pinpoint():
            mapps.locateme()

        def quit():
            print(Fore.RED + "Goodbye, see you later!" + Fore.RESET)
            exit()

        def string_pattern():
            try:
                file_name = raw_input(Fore.RED + "Enter file name?:\n" + Fore.RESET)
                stringg = raw_input(Fore.GREEN + "Enter string:\n" + Fore.RESET)
            except:
                file_name = input(Fore.RED + "Enter file name?:\n" + Fore.RESET)
                stringg = input(Fore.GREEN + "Enter string:\n" + Fore.RESET)
            system("grep '" + stringg + "' " + file_name)

        def todo():
            todoHandler(data)

        def weather():
            mapps.weather()

        locals()[key]()  # we are calling the proper function which satisfies the user's command.
 
