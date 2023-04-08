from getpass import getpass
import json, os, re
from dashboard import enter_dashboard

filename = "users.json"
if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)

prompt = ""

def login():
    global prompt
    prompt = "login"
    print(f"<<< {prompt} >>>")
    email = get_input(
        "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "email"
    )
    password = get_password(
        "^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        "password"
    )
    with open(filename, "r") as f:
        db = json.load(f)
    for db_user in db:
        if db_user["email"] == email and db_user["password"] == password:
            enter_dashboard(db_user)

def register():
    global prompt
    global filename
    prompt = "register"
    with open(filename, 'r') as f:
        db = json.load(f)

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
        email = get_input(
            "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "email"
        )
        for db_email in db:
            if email != db_email:
                duplicate_email = False
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
    phone = get_input(
        "^(010|011|012|015)\d{8}$",
        "phone number"
    )
    new_user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "phone": phone
    }
    
    db.append(new_user)
    with open(filename, "w") as f:
        json.dump(db, f)

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

def get_password(rgx, field):
    valid_input = False
    while not valid_input:
        try:
            print(f"\nEnter {field}")
            data = getpass(f"{prompt}> ")
            pattern = re.compile(rgx)
            valid_input = pattern.fullmatch(data)
            if not valid_input:
                raise Exception(f"Invalid {field}")
        except Exception as e:
            print(e)
    return data
