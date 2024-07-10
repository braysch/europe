from Person import Person
import os
import time
from datetime import datetime

# place for useful tools I use a lot and are not specific to any of the EUROPE functions
def load_data(path):
    # read data from file and create an array of Person objects
    saved_master_list = []
    f = open(path)

    date_last_extracted = f.readline().strip("\n")
    member_count = int(f.readline().strip("\n"))

    for x in range(member_count):
        w = Person()
        w.first_name = f.readline().strip("\n")
        w.preferred_name = f.readline().strip("\n")
        w.middle_name = f.readline().strip("\n")
        w.last_name = f.readline().strip("\n")
        w.birthdate = f.readline().strip("\n")
        w.phone = f.readline().strip("\n")
        w.alt_phone = f.readline().strip("\n")
        w.email = f.readline().strip("\n")
        w.alt_email = f.readline().strip("\n")
        w.record = f.readline().strip("\n")
        w.ysa_profile = f.readline().strip("\n")
        w.street_address = f.readline().strip("\n")
        w.alt_street_address = f.readline().strip("\n")
        w.street_address_2 = f.readline().strip("\n")
        w.alt_street_address_2 = f.readline().strip("\n")
        w.city = f.readline().strip("\n")
        w.alt_city = f.readline().strip("\n")
        w.state = f.readline().strip("\n")
        w.house = f.readline().strip("\n")
        w.ysa_edit_link = f.readline().strip("\n")
        w.cjc_edit_link = f.readline().strip("\n")
        saved_master_list.append(w)

    return saved_master_list


def save_data(master_list):
    # Save data to text file
    print("Saving Data to '/data'")

    f = open(os.getcwd() + "\\..\\data\\43rd Ward Master List.txt", "w+")
    f.write(str(datetime.now())+"\n")
    f.write(str(len(master_list))+"\n")
    for member in master_list:
        f.write(member.first_name+"\n")
        f.write(member.preferred_name+"\n")
        f.write(member.middle_name+"\n")
        f.write(member.last_name+"\n")
        f.write(member.birthdate+"\n")
        f.write(member.phone+"\n")
        f.write(member.alt_phone+"\n")
        f.write(member.email+"\n")
        f.write(member.alt_email+"\n")
        f.write(str(member.record)+"\n")
        f.write(str(member.ysa_profile)+"\n")
        f.write(member.street_address+"\n")
        f.write(member.alt_street_address+"\n")
        f.write(member.street_address_2+"\n")
        f.write(member.alt_street_address_2+"\n")
        f.write(member.city+"\n")
        f.write(member.alt_city+"\n")
        f.write(member.state+"\n")
        f.write(member.house+"\n")
        f.write(member.ysa_edit_link+"\n")
        f.write(member.cjc_edit_link+"\n")
    print("43rd Ward Master List successfully updated and saved!")
    f.close()


def isolate_ysa(master_list):
    # filter master list by members with ysa profiles
    ysa_list = []
    for member in master_list:
        if member.ysa_profile == "True" and member.record == "False":
            ysa_list.append(member)
    return ysa_list


def isolate_record(master_list):
    # filter master list by members with records
    record_list = []
    for member in master_list:
        if member.ysa_profile == "False" and member.record == "True":
            record_list.append(member)
    return record_list


def isolate_both(master_list):
    # filter master list by members who have a record AND a profile
    both_list = []
    for member in master_list:
        if member.ysa_profile == "True" and member.record == "True":
            both_list.append(member)
    return both_list


def find_object_from_name(name, master_list):
    # get Person object from name
    for member in master_list:
        if member.preferred_name == name.split()[0] and member.last_name == name.split()[1]:
            return member


def ysa_login(driver):
    # log on to ysaprofiles.org
    print("\nNavigating to ysaprofiles.org")
    driver.get("https://ysaprofiles.org/")

    #ysa_value = input("\nEnter your phone number or email: ")
    ysa_value = "5555555555" # ysa profiles uses your phone number to log in
    ysa_value_textbox = driver.find_element_by_id("name")
    ysa_value_textbox.send_keys(ysa_value)

    login_button = driver.find_element_by_id("create-auth")
    login_button.click()

    ysa_code = input("Enter the verification code sent to your device: ")
    ysa_code_textbox = driver.find_element_by_id("verify-code-value")
    ysa_code_textbox.send_keys(ysa_code)

    ysa_verify_button = driver.find_element_by_id("verify-code")
    ysa_verify_button.click()

    time.sleep(1)


def cjc_login(driver):
    # log on to churchofjesuschrist.org
    print("\nNavigating to churchofjesuschrist.org\n")

    driver.get(
        "https://login.churchofjesuschrist.org/?service=200&goto=https%3A%2F%2Fwww.churchofjesuschrist.org%2F%3Flang%3Deng")

    #cjc_username = input("Enter your churchofjesuschrist.org username: ")
    cjc_username = "username"
    #cjc_password = input("Enter your churchofjesuschrist.org password: ")
    cjc_password = "password"

    cjc_username_textbox = driver.find_element_by_id("username")
    cjc_username_textbox.send_keys(cjc_username)

    cjc_password_textbox = driver.find_element_by_id("password")
    cjc_password_textbox.send_keys(cjc_password)

    sign_in_button = driver.find_element_by_id("sign-in")
    sign_in_button.click()

def load_date(path):
    # get timestamp of last extraction date from data file
    f = open(path)
    date_last_extracted = f.readline().strip("\n")
    return date_last_extracted