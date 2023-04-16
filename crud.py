import json, os, re
from prettytable import PrettyTable

projects_file = "projects.json"
counter_file = "counter.json"

prompt = ""

def view_all_projects():
    with open(projects_file, 'r') as f:
        projects_db = json.load(f)
    with open("users.json", 'r') as f:
        users_db = json.load(f)
    
    table = PrettyTable()
    table.align = "l"
    table.field_names = ["Id", "Title", "Details", "Target (EGP)", "Start date", "End date", "Owner"]
    for project in projects_db:
        for user in users_db:
            if project['user_id'] == user['id']:
                user_name = f"{user['first_name']} {user['last_name']}"
                break

        table.add_row([
            project['id'], 
            project['title'], 
            project['details'], 
            project['total_target'], 
            project['start_date'], 
            project['end_date'],
            user_name
        ])
    print("\nAll Projects")
    print(table)

def view_my_projects():
    with open(projects_file, 'r') as f:
        projects_db = json.load(f)
    with open("login.json", 'r') as f:
        login_user = json.load(f)
    
    table = PrettyTable()
    table.align = "l"
    table.field_names = ["Id", "Title", "Details", "Target (EGP)", "Start date", "End date"]
    for project in projects_db:
        if project['user_id'] == login_user['id']:
            table.add_row([
                project['id'], 
                project['title'], 
                project['details'], 
                project['total_target'], 
                project['start_date'], 
                project['end_date']
            ])
    print("\nMy Projects")
    print(table)

def create_project():
    global prompt
    prompt = "create-project"
    print(f"<<< {prompt} >>>")
    email = get_input(
        "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "email"
    )
    password = get_password(
        "^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        "password"
    )
    with open(users_file, "r") as f:
        users_db = json.load(f)
    for db_user in users_db:
        if db_user["email"] == email and bcrypt.checkpw(
            password.encode('utf-8'),
            db_user['password'].encode('utf-8')
        ):
            enter_dashboard(db_user)

def register():
    global prompt
    global users_file
    prompt = "register"
    with open(users_file, 'r') as f:
        users_db = json.load(f)
    with open(counter_file, 'r') as f:
        counter_db = json.load(f)

    if "users" not in counter_db[0]:
        counter_db[0]["users"] = 0

    print(f"<<< {prompt} >>>")
    first_name = get_input(
        "^[a-zA-Z]+$",
        "first name"
    )
    last_name = get_input(
        "^[a-zA-Z]+$",
        "last name"
    )
    duplicate_email = True
    while duplicate_email:
        duplicate_email = False
        email = get_input(
            "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "email"
        )
        for db_email in users_db:
            if email == db_email:
                duplicate_email = True
                break
        if duplicate_email:
            print("Email already exists")
    
    password_not_match = True
    while password_not_match:
        password = get_password(
            "^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            "password"
        )
        confirm_password = get_password(
            "^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            "password again"
        )
        if password == confirm_password:
            password_not_match = False
        else:
            print("Password not matched")
    tmp_hash = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    password = tmp_hash.decode('utf-8')

    phone = get_input(
        "^(010|011|012|015)\d{8}$",
        "phone number"
    )

    counter_db[0]["users"] += 1

    new_user = {
        "id": counter_db[0]["users"],
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "phone": phone
    }
    
    users_db.append(new_user)
    with open(users_file, "w") as f:
        json.dump(users_db, f)
    with open(counter_file, "w") as f:
        json.dump(counter_db, f)

def get_input(rgx, field):
    valid_input = False
    while not valid_input:
        try:
            print(f"\nEnter {field}")
            data = input(f"{prompt}> ")
            pattern = re.compile(rgx)
            valid_input = pattern.fullmatch(data)
            if not valid_input:
                raise Exception(f"Invalid {field}")
        except Exception as e:
            print(e)
    return data
