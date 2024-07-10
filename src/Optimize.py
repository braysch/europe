import time
from General import save_data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def optimize_ysa(driver, master_list):
    # automatically format data for ysa site
    # (e.g. 5555555555 -> 555-555-5555)
    total_opt = 0

    for member in master_list:
        try:
            if member.ysa_edit_link != "":

                time.sleep(1)
                # go to ysa profiles edit link for each member
                driver.get(member.ysa_edit_link)

                print("----------\n")
                print(member.preferred_name.upper(), member.last_name.upper() + "\n")

                ysa_email_edit_box = driver.find_element_by_xpath("//input[@data-field='email']")
                ysa_email = ysa_email_edit_box.get_attribute("value")
                # make sure email is lower case and remove extra spacing
                ysa_opt_email = ysa_email_edit_box.get_attribute("value").lower().rstrip(" ").lstrip(" ")

                if ysa_opt_email != ysa_email:
                    ysa_email_edit_box.clear()
                    ysa_email_edit_box.send_keys(ysa_opt_email)
                    print("\t" + ysa_email + " >>> " + ysa_opt_email + "\n")
                    member.email = ysa_opt_email
                    total_opt += 1

                # phone number is already formatted on ysaprofiles.org

                ysa_street_edit_box = driver.find_element_by_xpath("//input[@data-field='street_address']")
                ysa_street = driver.find_element_by_xpath("//input[@data-field='street_address']").get_attribute(
                    "value")
                ysa_opt_street = optimize_street(ysa_street)
                if ysa_opt_street != ysa_street:
                    ysa_street_edit_box.clear()
                    ysa_street_edit_box.send_keys(ysa_opt_street)
                    print("\t" + ysa_street + " >>> " + ysa_opt_street + "\n")
                    member.street_address = ysa_opt_street
                    total_opt += 1

                ysa_street_2_edit_box = driver.find_element_by_xpath("//input[@data-field='street_address_2']")
                ysa_street_2 = driver.find_element_by_xpath("//input[@data-field='street_address_2']").get_attribute(
                    "value")
                ysa_opt_street_2 = optimize_street(ysa_street_2)
                if ysa_opt_street_2 != ysa_street_2:
                    ysa_street_2_edit_box.clear()
                    ysa_street_2_edit_box.send_keys(ysa_opt_street_2)
                    print("\t" + ysa_street_2 + " >>> " + ysa_opt_street_2 + "\n")
                    member.street_address_2 = ysa_opt_street_2
                    total_opt += 1

                finish_editing = driver.find_element_by_xpath("//a[@class='button green large']")
                finish_editing.click()

        except Exception as e:
            print(member.first_name, member.last_name, " is no longer a member of the 43rd ward")
    print("\n"+str(total_opt)+" optimization(s) made")
    save_data(master_list)


def optimize_cjc(driver, master_list):
    # automatically format data for cjc site
    # (e.g. 5555555555 -> 555-555-5555)
    total_opt = 0

    for member in master_list:
        try:
            if member.cjc_edit_link != "":

                time.sleep(1)
                # go to edit page for each cjc member
                driver.get(member.cjc_edit_link)

                wait = WebDriverWait(driver, 10)
                edit_button = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "btn-edit")))
                edit_button.click()

                print("----------\n")
                print(member.preferred_name.upper(), member.last_name.upper() + "\n")

                email_edit_box = driver.find_element_by_id("email")
                email = email_edit_box.get_attribute("value")
                # format the email
                opt_email = email_edit_box.get_attribute("value").lower().rstrip(" ").lstrip(" ")

                if opt_email != email:
                    email_edit_box.clear()
                    email_edit_box.send_keys(opt_email)
                    print("\t" + email + " >>> " + opt_email + "\n")
                    member.alt_email = opt_email
                    total_opt += 1

                # format the phone number
                phone_edit_box = driver.find_element_by_id("phone")
                phone = phone_edit_box.get_attribute("value")
                opt_phone = optimize_phone(phone)

                if opt_phone != phone:
                    phone_edit_box.clear()
                    phone_edit_box.send_keys(opt_phone)
                    print("\t" + phone + " >>> " + opt_phone + "\n")
                    member.alt_phone = opt_phone
                    total_opt += 1

                # address is already formatted on churchofjesuschrist.org

                wait = WebDriverWait(driver, 10)
                save_button = driver.find_element_by_xpath("//button[@ng-click='save()']")
                save_button.click()

        except Exception as e:
            print(e)
    print("\n"+str(total_opt)+" optimization(s) made")
    save_data(master_list)


def optimize_phone(phone):
    # put phone number in this format -> xxx-xxx-xxxx
    if phone != "":
        phone = filter(str.isdigit, phone)
        p_a = [digit for digit in phone]
        if len(p_a) == 10:
            opt_phone = (p_a[0] + p_a[1] + p_a[2] + "-" + p_a[3] + p_a[4] + p_a[5] + "-" + p_a[6] + p_a[7] + p_a[8] + p_a[9])
        elif len(p_a) == 11:
            opt_phone = (p_a[0] + "-" + p_a[1] + p_a[2] + p_a[3] + "-" + p_a[4] + p_a[5] + p_a[6] + "-" + p_a[7] + p_a[8] + p_a[9]) + p_a[10]
        else:
            opt_phone = phone
        return opt_phone
    return phone


def optimize_street(street):
    # remove spacing
    # directions are represented by a single letter, not spelled out
    street = street.rstrip(" ").lstrip(" ")
    street = street.replace("  ", " ")
    street = street.replace("North", "N").replace("north", "N")
    street = street.replace("East", "E").replace("east", "E")
    street = street.replace("West", "W").replace("west", "W")
    street = street.replace("South", "S").replace("south", "S")
    street = street.replace("Apt.", "Apt").replace("apt.", "Apt")
    street = street.replace("apt", "Apt")
    street = street.replace("#", "Apt ")
    street = street.replace(" po ", " PO ")
    street = street.replace("Basement", "Bsmt").replace("basement", "Bsmt").replace("basement Apt", "Bsmt")

    return street
