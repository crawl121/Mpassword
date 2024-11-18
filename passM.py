import json  # for database
import getpass  # for password entry without echoing
import os  # for file handling
import pyfiglet 

# Dependency Check
try:
    import pyfiglet
except ImportError:
    print("[!] Please install pyfiglet to run this program: pip install pyfiglet")

# Function to print fancy title
def print_title(title):
    title = pyfiglet.figlet_format(title)
    print(title)

# File to store user data
USER_DATA_FILE = 'user_data.json'

# Load user data from file
def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

# Save user data to file
def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Function to create a master password
def create_master_password():
   
    master_pass = getpass.getpass("[+] Enter your master password: ")
    confirm_pass = getpass.getpass("[+] Confirm your master password: ")
    if master_pass != confirm_pass:
        print("[!] Passwords do not match. Please try again.")
        return create_master_password()
    else:
        return master_pass

# Function to sign up a new user
def sign_up():
    data = load_user_data()
    
    gmail = input("[+] Enter your Gmail: ")
    username = input("[+] Create a username: ")
    
    while username in data:
        print("[!] Username already in use. Try a different one.")
        username = input("[+] Create a username: ")
    
    master_pass = create_master_password()
    
    data[username] = {
        "gmail": gmail,
        "master_password": master_pass,
        "applications": {}
    }
    
    save_user_data(data)
    
    print(">>Sign-up successful. Returning to main menu.<<")

# Function to authenticate master password
def authenticate_master_password(data, username):
    master_pass = getpass.getpass("[+] Enter your master password: ")
    if master_pass == data[username]["master_password"]:
        return True
    else:
        print("Incorrect master password.")
        return False

# Function to add new data for the user
def add_new_data(data, username):
    print("Add new data:")
    login_type = input("[+] Enter login type (e.g., Google, Facebook): ")
    app_name = input("[+] Enter application name: ")
    app_username = input("[+] Enter application username: ")
    app_password = getpass.getpass("[+] Enter application password:")
    backup_key = input("[+] Enter backup key or authentication key (or 'None'): ")
    recovery_email = input("[+] Enter recovery email or 'None'): ")
    
    data[username]["applications"][app_name] = {
        "login_type": login_type,
        "app_username": app_username,
        "app_password" :app_password,
        "backup_key": backup_key,
        "recovery_email": recovery_email
    }
    
    save_user_data(data)
    print(">>Data added successfully.<<")

# Function to search existing data for the user
def search_existing_data(data, username):
    app_name = input("[+] Enter application name to search: ")
    
    if app_name not in data[username]["applications"]:
        print("[!] No data found.")
        return
    
    print("Data found for", app_name)
    print("1. View data (read-only)")
    print("99. Go back")
    
    option = input("Your choice: ")
    
    if option == "1":
        app_data = data[username]["applications"][app_name]
        print("       >> Application Data: <<")
        print(">> Login Type:", app_data["login_type"])
        print(">> Username:", app_data["app_username"])
        print(">> Application password " , app_data["app_password"])
        print(">> Backup Key:", app_data["backup_key"])
        print(">> Recovery Email:", app_data["recovery_email"])
    elif option == "99":
        print(">> Returning to the previous screen. <<")

# Main function to start the application
def main():
    while True:
        print_title("ZWN _ CRAWL")
        print("1. Login")
        print("2. Sign up")
        print("3. Quit")
        
        option = input("[+] Your choice: ")
        
        if option == "1":
            data = load_user_data()
            username = input("[+] Enter your username: ")
            if username in data:
                if authenticate_master_password(data, username):
                    while True:
                        print(">>Login successful. Choose an option: <<")
                        print("1. Add new data")
                        print("2. Search existing data")
                        print("3. Log out")
                        
                        choice = input("[+] Your choice: ")
                        
                        if choice == "1":
                            add_new_data(data, username)
                        elif choice == "2":
                            search_existing_data(data, username)
                        elif choice == "3":
                            break
                        else:
                            print("[!] Invalid choice. Try again.")
                else:
                    print("[!] Master password authentication failed.")
            else:
                print("[!] User not found.")
        
        elif option == "2":
            sign_up()
        
        elif option == "3":
            print(">> Goodbye! <<")
            break
        
        else:
            print("[!] Invalid option. Try again.")

# Run the application
if __name__ == "__main__":
    main()
