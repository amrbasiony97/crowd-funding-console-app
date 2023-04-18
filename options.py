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
    1: crud.create_project,
    2: crud.view_all_projects,
    3: crud.view_my_projects,
    4: crud.edit_project,
    5: 'exit',
    6: 'exit',
    7: menus.print_dashboard_menu,
    8: __pass__
}