import json, os, re, datetime
from prettytable import PrettyTable

projects_file = "projects.json"
if not os.path.exists(projects_file):
    with open(projects_file, "w") as f:
        json.dump([], f)

counter_file = "counter.json"
users_file = "users.json"
login_file = "login.json"
prompt = ""

with open(counter_file, 'r') as f:
    counter_db = json.load(f)
with open(users_file, 'r') as f:
    users_db = json.load(f)
with open(projects_file, 'r') as f:
    projects_db = json.load(f)

def view_all_projects():
    global projects_db
    global users_db
    
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
    global projects_db
    global login_user
    with open(login_file, 'r') as f:
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
    global counter_db
    global login_db
    global projects_db
    global prompt
    prompt = "create-project"

    with open(login_file, 'r') as f:
        login_user = json.load(f)

    if "projects" not in counter_db[0]:
        counter_db[0]["projects"] = 0

    print(f"\nEnter title")
    title = input(f"{prompt}> ")

    print(f"\nEnter details")
    details = input(f"{prompt}> ")

    total_target = int(get_input(
        "^\d*$",
        "total target in EGP"
    ))

    valid_date = False
    while not valid_date:
        print(f"\nEnter start date as following: 'YYYY-MM-DD'")
        start_date = input(f"{prompt}> ")
        valid_date = validate_date(start_date)

    valid_date = False
    while not valid_date:
        print(f"\nEnter end date as following: 'YYYY-MM-DD'")
        end_date = input(f"{prompt}> ")
        valid_date = validate_date(end_date)
    
    counter_db[0]["projects"] += 1

    new_project = {
        "id": counter_db[0]["projects"],
        "title": title,
        "details": details,
        "total_target": total_target,
        "start_date": start_date,
        "end_date": end_date,
        "user_id": login_user['id']
    }
    
    projects_db.append(new_project)
    with open(projects_file, "w") as f:
        json.dump(projects_db, f)
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

def validate_date(date_text):
        try:
            datetime.date.fromisoformat(date_text)
        except ValueError:
            print("Incorrect date format, range")
            return False
        return True