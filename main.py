from menus import print_main_menu
import options

print("<<< Crowd-Funding App >>>\n")
print_main_menu()

while True:
    choice = input("\nmain> ")
    try:
        if(choice.isdigit()):
            choice = int(choice)
            if choice in options.menu_options:
                options.menu_options[choice]()
            else:
                raise Exception("Enter a number from the list")
        else:
            raise Exception("Only numbers are valid")
    except Exception as e:
        print(e)