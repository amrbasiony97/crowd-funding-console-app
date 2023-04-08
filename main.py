import auth
from menus import print_main_menu

print("<<< Crowd-Funding App >>>\n")
options = {
    1: auth.login,
    2: auth.register,
    3: print_main_menu,
    4: exit
}

print_main_menu()
while True:
    choice = input("\nmain> ")
    try:
        if(choice.isdigit()):
            choice = int(choice)
            if choice in options:
                options[choice]()
            else:
                raise Exception("Enter a number from the list")
        else:
            raise Exception("Only numbers are valid")
    except Exception as e:
        print(e)