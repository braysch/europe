import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime
from Person import Person
from Edit import merge
from General import ysa_login, cjc_login
from Report import status_report


def extract(driver):

    master_list = []

    # LOGIN INFO
    # YSA PROFILE ACCESS

    # ysa_login(driver)
    cjc_login(driver)

    time.sleep(1)

    # navigate to churchofjesuschrist.org
    driver.get("https://lcr.churchofjesuschrist.org/records/member-list?lang=eng")
    # give it time to load
    time.sleep(3)
    # we need to scroll to the bottom so that the list of members is full loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    time.sleep(1)

    # find all the links on the page
    cjc_list_elements = driver.find_elements_by_tag_name('a')
    cjc_links = []
    counter = 1

    # save all the membership edit links to cjc_links
    for element in cjc_list_elements:
        cjc_link = str(element.get_attribute('href'))
        if cjc_link.startswith(
                "https://lcr.churchofjesuschrist.org/records/member-profile/") and cjc_link not in cjc_links:
            cjc_links.append(cjc_link)

    print("\n")

    for link in cjc_links:
        # navigate to each link
        print("Extracting data from", link, counter, "/", len(cjc_links))
        counter += 1
        driver.get(link)
        wait = WebDriverWait(driver, 10)
        # don't click on the edit button too early
        edit_button = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "btn-edit")))

        experiment = driver.find_elements_by_xpath("//dd[@class='ng-binding']")
        for x in experiment:
            print(x.get_attribute("value"))

        # edit the record
        edit_button.click()

        # create a new person object
        x = Person()
        x.cjc_edit_link = link

        # save all the required data on the page to our Person object
        try:
            given_name = driver.find_elements_by_xpath("//input[@ng-model='name.given']")[0].get_attribute("value")
            x.preferred_name = driver.find_elements_by_xpath("//input[@ng-model='name.given']")[1].get_attribute(
                "value")

            if len(given_name.split()) > 1:
                name_array = (given_name.split())
                x.first_name = name_array[0]
                x.middle_name = name_array[1]
            else:
                x.first_name = given_name

            if x.preferred_name == "":
                x.preferred_name = x.first_name

            x.last_name = driver.find_element_by_xpath("//input[@ng-model='name.family']").get_attribute("value")
            x.email = driver.find_element_by_id("email").get_attribute("value")
            x.phone_number = driver.find_element_by_id("phone").get_attribute("value")
            x.birthdate = driver.find_element_by_id("birthDate").get_attribute("value")
            x.street_address = driver.find_element_by_xpath("//input[@ng-model='address.street1']").get_attribute(
                "value")
            x.street_address_2 = driver.find_element_by_xpath("//input[@ng-model='address.street2']").get_attribute(
                "value")
            x.city = driver.find_element_by_xpath("//input[@ng-model='address.city']").get_attribute("value")
            # print(driver.find_element_by_xpath("//input[@ng-model='address.state']").get_attribute("value"))
            x.record = "True"

            # add the person to our master list
            master_list.append(x)

        except Exception as e:
            print("Exception:", e)

    # YSA PROFILES

    print("Attempting to access ysaprofiles.org")

    time.sleep(1)

    # this is the address to my specific ward
    # (ward = congregation)
    driver.get("https://ysaprofiles.org/members/ward-55b0242b8199e")

    if driver.current_url == "https://ysaprofiles.org/members/ward-55b0242b8199e":
        print("\nSuccessfully logged into ysaprofiles.org!\n")
    else:
        print("\nFailed to log into ysaprofiles.org\n")

    # get all the links on the page
    list_elements = driver.find_elements_by_tag_name('a')

    counter = 1
    links = []

    try:
        for element in list_elements:
            # save all the member edit links to links
            link = element.get_attribute('href')
            if link.startswith("https://ysaprofiles.org/individual") and link not in links:
                links.append(link)

        for link in links:
            # create a new person object
            y = Person()
            # unlike cjc.org, we don't have to press an edit button to get the data
            print("Extracting data from", link, counter, "/", len(links))
            counter += 1
            ysa_id = link.lstrip("https://ysaprofiles.org/individual-")
            y.ysa_edit_link = ("https://ysaprofiles.org/edit/individual-" + ysa_id)
            driver.get(y.ysa_edit_link)

            birthday_month = (driver.find_element_by_xpath("//input[@data-field='birthday_month']")).get_attribute(
                "value")
            birthday_day = (driver.find_element_by_xpath("//input[@data-field='birthday_day']")).get_attribute("value")
            birthday_year = (driver.find_element_by_xpath("//input[@data-field='birthday_year']")).get_attribute(
                "value")

            given_name = (driver.find_element_by_xpath("//input[@data-field='first_name']")).get_attribute("value")

            if len(given_name.split()) > 1:
                name_array = (given_name.split())
                y.first_name = name_array[0]
                y.middle_name = name_array[1]
            else:
                y.first_name = given_name

            y.preferred_name = y.first_name
            y.last_name = (driver.find_element_by_xpath("//input[@data-field='last_name']")).get_attribute("value")
            y.email = (driver.find_element_by_xpath("//input[@data-field='email']")).get_attribute("value")
            y.phone = (driver.find_element_by_xpath("//input[@data-field='phone']")).get_attribute("value")
            y.birthdate = (str(birthday_day) + " " + str(birthday_month) + " " + str(birthday_year))
            y.street_address = (driver.find_element_by_xpath("//input[@data-field='street_address']")).get_attribute(
                "value")
            y.street_address_2 = (
                driver.find_element_by_xpath("//input[@data-field='street_address_2']")).get_attribute(
                "value")
            y.ysa_profile = "True"

            for person in master_list:
                # if we come across someone on YSA profiles who has the same name as someone we found on cjc.org,
                # merge them together!
                # (ideally, I should have checked for matching birthdays too, but I never ran into any issues.)
                if (
                        y.first_name.lower().split() == person.first_name.lower().split() or y.first_name.lower().split() == person.preferred_name.lower().split()) and y.last_name.lower().split() == person.last_name.lower().split():
                    print("Merging", y.first_name, y.last_name, "and", person.first_name, person.last_name)
                    y = merge(y, person)
                    # removed cjc member from master list (we will replace it with the merged member)
                    master_list.remove(person)
                    break

            # add person to master list
            master_list.append(y)

    except Exception as e:
        print("Exception:", e)

    master_list.sort(key=lambda a: a.last_name, reverse=False)

    # display the members and whether they have a record/profile
    status_report(master_list)

    return master_list
