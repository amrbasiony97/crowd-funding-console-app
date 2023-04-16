import os, json
import menus
# from options import dashboard_options
import options

def enter_dashboard(user):
    print(f"<<< Welcome Back, {user['first_name']} {user['last_name']} >>>\n")

    projects_file = "projects.json"
    if not os.path.exists(projects_file):
        with open(projects_file, "w") as f:
            json.dump([], f)

    login_user_file = "login.json"
    with open(login_user_file, "w") as f:
        json.dump({
            "id": user['id'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "email": user['email'],
            "phone": user['phone']
        }, f)
    
    menus.print_dashboard_menu()
    while True:
        choice = input("\ndashboard> ")
        try:
            if(choice.isdigit()):
                choice = int(choice)
                if choice in options.dashboard_options:
                    options.dashboard_options[choice]()
                    if choice == 8:
                        menus.print_main_menu();
                        break;
                else:
                    raise Exception("Enter a number from the list")
            else:
                raise Exception("Only numbers are valid")
        except Exception as e:
            print(e)
