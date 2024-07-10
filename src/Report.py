from General import find_object_from_name, load_date
import os


def display_incon(both_list):
    # display inconsistencies between record and profile
    print("\n----------\n")
    for member in both_list:
        print(member.preferred_name.upper(), member.last_name.upper())
        if member.phone != member.alt_phone.replace("-", "") and (member.phone != "" and member.alt_phone != ""):
            print("\tAlternate phone numbers: '"+member.phone+"' and '"+member.alt_phone+"'")
        if member.email != member.alt_email and (member.email != "" and member.alt_email != ""):
            print("\tAlternate emails: '"+member.email+"' and '"+member.alt_email+"'")
        if member.street_address != member.alt_street_address and (member.street_address != "" and member.alt_street_address != ""):
            print("\tAlternate street addresses: '"+member.street_address+"' and '"+member.alt_street_address+"'")
        if member.street_address_2 != member.alt_street_address_2 and (member.street_address_2 != "" and member.alt_street_address_2 != ""):
            print("\tAlternate apartment numbers: '"+member.street_address_2+"' and '"+member.alt_street_address_2+"'")
        if member.city != member.alt_city and (member.city != "" and member.alt_city != ""):
            print("\tAlternate cites: '"+member.city+"' and '"+member.alt_city+"'")
        print("\n----------\n")


def display_changes(old_list, master_list):
    # display who has been removed and who has been added to the membership list since the last extraction
    print("\nSINCE: "+load_date(os.getcwd() + "\\..\\data\\Backup.txt")+"\n")
    for old_member in old_list:
        if not find_object_from_name((old_member.preferred_name+" "+old_member.last_name), master_list):
            print(old_member.preferred_name, old_member.last_name, "was removed from the 43rd ward.")
    print("")
    for master_member in master_list:
        if not find_object_from_name((master_member.preferred_name+" "+master_member.last_name), old_list):
            print(master_member.preferred_name, master_member.last_name, "was added to the 43rd ward ::", master_member.street_address, master_member.street_address_2)
    print("\nLAST UPDATED: "+load_date(os.getcwd() + "\\..\\data\\43rd Ward Master List.txt"))


def status_report(master_list):
    # display a list of members and show whether they have a record, profile, or both
    print("\nALL MEMBERS\n")
    for person in master_list:
        print(person.preferred_name, person.last_name)
    print("\nMEMBERS WHO HAVE BOTH A RECORD AND A YSA PROFILE:\n")
    for person in master_list:
        if person.ysa_profile == "True" and person.record == "True":
            print(person.preferred_name, person.last_name)
    print("\nMEMBERS WHO ONLY HAVE A YSA PROFILE\n")
    for person in master_list:
        if person.ysa_profile == "True" and not person.record == "True":
            print(person.preferred_name, person.last_name)
    print("\nMEMBERS WHO ONLY HAVE A RECORD\n")
    for person in master_list:
        if not person.ysa_profile == "True" and person.record == "True":
            print(person.preferred_name, person.last_name)
