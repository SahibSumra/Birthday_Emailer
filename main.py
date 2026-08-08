##################### Extra Hard Starting Project ######################
import pandas as pd
import smtplib
import datetime as dt
import random


MY_EMAIL = "laksahib7@gmail.com"
MY_PASSWORD = "ecuw xbpa zbki ssju"  

CSV_FILE = "birthdays.csv"

def Main():
    print("\n[1/3] Loading birthday database...")
    try:
        data_file = pd.read_csv(CSV_FILE)
        print("-> Database loaded successfully.")
    except FileNotFoundError:
        print(f"-> {CSV_FILE} not found. Creating a new database.")
        data_file = pd.DataFrame(columns=["name", "email", "year", "month", "day"])

    update_birthdays = input("\nDo you need to update birthday (yes or no)? ").lower()
    if update_birthdays == "yes":
        name = input("Who is it? ").title()
        email = input("What is their email? ").lower()
        year = int(input("What is their year of birth? "))
        month = int(input("What is their month of birth? "))
        day = int(input("What is their day of birth? "))
        
        new_row = {"name": name, "email": email, "year": year, "month": month, "day": day}
        
        data_list = data_file.to_dict(orient="records")
        data_list.append(new_row)
        data_file = pd.DataFrame(data_list)
        data_file.to_csv(CSV_FILE, index=False)
        print(f"-> Successfully added {name} to {CSV_FILE}!")

    ask_whether_to_do_daily_check = input("\nDo you want me to do daily check (yes or no)? ").lower()
    if ask_whether_to_do_daily_check == "yes":
        CheckAndSendBirthdays(data_file)

def CheckAndSendBirthdays(data_file):
    print("\n[2/3] Checking for matching birthdays today...")
    today = dt.datetime.now()
    today_month = today.month
    today_day = today.day
    
    matching_birthdays = data_file[(data_file["month"] == today_month) & (data_file["day"] == today_day)]
    
    if matching_birthdays.empty:
        print("-> No birthdays found for today!")
        return

    print(f"-> Found {len(matching_birthdays)} birthday(s) today. Connecting to Gmail...")
    
    try:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.connect("smtp.gmail.com", 587)
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            print("-> Connected and logged in successfully.")
            
            print("\n[3/3] Sending emails...")
            for index, row in matching_birthdays.iterrows():
                person_name = row["name"]
                person_email = row["email"]
                
                letter_num = random.randint(1, 3)
                try:
                    with open(f"letter_{letter_num}.txt") as letter_file:
                        contents = letter_file.read()
                    contents = contents.replace("[NAME]", person_name)
                    
                    connection.sendmail(
                        from_addr=MY_EMAIL, 
                        to_addrs=person_email, 
                        msg=f"Subject:Happy Birthday {person_name}\n\n{contents}"
                    )
                    print(f"Birthday email sent to {person_name}!")
                except FileNotFoundError:
                    print(f"Error: letter_templates/letter_{letter_num}.txt missing.")
                    
    except Exception as e:
        print(f"An error occurred: {e}")

Main()
