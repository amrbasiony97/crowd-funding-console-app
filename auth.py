from getpass import getpass
import json, os, re, bcrypt
from dashboard import enter_dashboard

users_file = "users.json"
if not os.path.exists(users_file):
    with open(users_file, "w") as f:
        json.dump([], f)

counter_file = "counter.json"
if not os.path.exists(counter_file):
    with open(counter_file, "w") as f:
        json.dump([{}], f)

prompt = ""

def login():
    global prompt
    prompt = "login"
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
    login_failed = True
    for db_user in users_db:
        if db_user["email"] == email and bcrypt.checkpw(
            password.encode('utf-8'),
            db_user['password'].encode('utf-8')
        ):
            login_failed = False
            enter_dashboard(db_user)
    if login_failed:
        print("Invalid credentials")

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
        duplicate_email = check_duplicate_email(email)
        if duplicate_email:
            print("Email already exists")
        else:
            break
    
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

    duplicate_phone = True
    while duplicate_phone:
        phone = get_input(
            "^(010|011|012|015)\d{8}$",
            "phone number"
        )
        duplicate_phone = check_duplicate_phone(phone)
        if duplicate_phone:
            print("Phone already exists")
        else:
            break

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

def check_duplicate_email(email):
    with open(users_file, 'r') as f:
        users_db = json.load(f)
    for user in users_db:
        if email == user['email']:
            return True
    return False

def check_duplicate_phone(phone):
    with open(users_file, 'r') as f:
        users_db = json.load(f)
    for user in users_db:
        if phone == user['phone']:
            return True
    return False