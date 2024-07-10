import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime
from Person import Person
from Extract import extract
from General import load_data
from Edit import merge_option, display_merge_options, merge
from General import isolate_ysa, isolate_both, isolate_record, find_object_from_name, ysa_login, cjc_login, save_data
from Report import display_incon, display_changes, status_report
from Optimize import optimize_phone, optimize_street, optimize_ysa, optimize_cjc

title = "\nEUROPE Ver 1.0"
print(title)
print("Developed by Bradan Schwanke\n")
print("Accessing the World Wide Web")

try:
    master_list = load_data(os.getcwd() + "\\..\\data\\43rd Ward Master List.txt")
    old_list = load_data(os.getcwd() + "\\..\\data\\Backup.txt")
except Exception:
    time.sleep(0.5)
    print("\n### ERROR: The data file is either corrupted or missing ###")
    time.sleep(0.5)
    print("It is suggested that you extract new data")
    master_list = []

master_list.sort(key=lambda a: a.last_name, reverse=False)
ysa_list = isolate_ysa(master_list)
record_list = isolate_record(master_list)
both_list = isolate_both(master_list)
# record_list is a list of members who have official church records moved into the area
# ysa_list is a list of members who have created a YSA profile

while True:
    print("\n\tMAIN MENU")
    print("\n\t1) Extract")
    print("\t2) Update")
    print("\t3) Report")
    print("\t4) Optimize")
    print("\t5) Publish")
    print("\t6) Edit")
    print("\n\t?) Help")
    print("\n\tq) Quit\n")

    choice = input(">> ")

    if choice == "q":
        exit()

    if choice == "?":
        # display info about each of the options
        print("Extract - Pulls member data from both ysaprofiles.org and churchofjesuschrist.org")
        print("Update - Moves in records for pending ysa profiles")
        print("Report - Displays full ward list and discrepancies")
        print("Optimize - Standardizes the format of information")
        print("Publish - Creates Master List and Ward Census and saves them to /data")
        print("Edit - Change member information")

    if choice == '1':
        # extract data from churchofjesuschrist.org and ysaprofiles.org
        # saves the data to a text file called 43rd Ward Master List.txt
        driver = webdriver.Chrome("C:\\Users\\heroo\\PycharmProjects\\europe\\src\\chromedriver.exe")

        new_master_list = extract(driver)
        print("Extraction Complete!")
        final_ans = "n"
        while final_ans != "y":
            save = input("Would you like to save the data? (y) or (n)")
            if save == "n":
                final_ans = input("Are you sure you want to discard this extraction? (y) or (n)")
                if final_ans == "y":
                    print("Extraction discarded.")
            else:
                save_data(new_master_list)
                master_list = new_master_list
                final_ans = "y"
                # I save the extracted data to 43rd Ward Master List.txt,
                # but I never move the old extracted data to Backup.txt,
                # which means I must have been doing that manually

    elif choice == '3':
        # display membership data
        print("\n\t\tREPORT")
        print("\n\t\t1) Ward Status Report")
        print("\n\t\t2) Display Inconsistencies")
        print("\n\t\t3) Display Changes")

        choice = input("\t\t>> ")

        if choice == '1':
            # display total members, members with only records, members with only profiles, and members with both
            status_report(master_list)

        if choice == '2':
            # display discrepancies for each user between record data and profile data
            display_incon(both_list)

        if choice == '3':
            # display the changes made since the last extraction (members moved in/out)
            display_changes(old_list, master_list)

    elif choice == '4':
        # standardize data format on sites
        choice = input("Optimize [ysa], [cjc], or [both]?")

        driver = webdriver.Chrome("C:\\Users\\heroo\\PycharmProjects\\europe\\src\\chromedriver.exe")

        if choice == "ysa":
            ysa_login(driver)
            time.sleep(1)
            optimize_ysa(driver, master_list)
        elif choice == "cjc":
            cjc_login(driver)
            time.sleep(1)
            optimize_cjc(driver, master_list)
        elif choice == "both":
            ysa_login(driver)
            cjc_login(driver)
            optimize_ysa(driver, master_list)
            optimize_cjc(driver, master_list)

    elif choice == '6':
        # only option is 1) merge two members
        driver = webdriver.Chrome("C:\\Users\\heroo\\PycharmProjects\\europe\\src\\chromedriver.exe")

        print("\n\t\tEDIT")
        print("\n\t\t1) Merge\n")
        choice = input()

        options_1 = merge_option(record_list, ysa_list)
        options_2 = merge_option(ysa_list, record_list)
        print("\n")
        display_merge_options(options_1, options_2)
        print("\nWhich member would you like to merge?")
        name_1 = input(">> ")
        merge_1 = find_object_from_name(name_1, master_list)
        print("\nPOSSIBLE MERGES\n")
        for item in options_2:
            if item.last_name == merge_1.last_name:
                print(item.preferred_name, item.last_name)
        print("\nMerge", merge_1.preferred_name, merge_1.last_name, "with who?")
        name_2 = input(">> ")
        merge_2 = find_object_from_name(name_2, master_list)

        cjc_login(driver)
        time.sleep(1)

        print("Navigating to", merge_1.cjc_edit_link)

        driver.get(merge_1.cjc_edit_link)
        wait = WebDriverWait(driver, 10)
        edit_button = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "btn-edit")))
        edit_button.click()

        # update preferred name on churchofjesuschrist.org
        preferred_name_box = driver.find_elements_by_xpath("//input[@ng-model='name.given']")[1]
        preferred_name_box.clear()
        preferred_name_box.send_keys(merge_2.preferred_name)

        # update preferred last name on churchofjesuschrist.org
        preferred_last_name_box = driver.find_elements_by_xpath("//input[@ng-model='name.family']")[1]
        preferred_last_name_box.clear()
        preferred_last_name_box.send_keys(merge_1.last_name)
        #mission_language_box = driver.find_element_by_id("missionCountry")
        #mission_language_box.send_keys("\t")
        #save_button = driver.switch_to.active_element
        wait = WebDriverWait(driver, 10)
        save_button = driver.find_element_by_xpath("//button[@ng-click='save()']")
        save_button.click()

        print("Preferred name successfully updated!")
        p = merge(merge_1, merge_2)
        master_list.remove(merge_1)
        master_list.remove(merge_2)
        master_list.append(p)
        print(merge_1.preferred_name, merge_1.last_name, "merged with", merge_2.preferred_name, merge_2.last_name)
        save_data(master_list)
        master_list.sort(key=lambda a: a.last_name, reverse=False)



