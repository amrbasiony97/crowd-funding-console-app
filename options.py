import auth, menus
import crud

def __pass__():
    pass

menu_options = {
    1: auth.login,
    2: auth.register,
    3: menus.print_main_menu,
    4: exit
}

dashboard_options = {
    1: 'auth.login',
    2: crud.view_all_projects,
    3: crud.view_my_projects,
    4: 'exit',
    5: 'exit',
    6: 'exit',
    7: 'exit',
    8: __pass__
}