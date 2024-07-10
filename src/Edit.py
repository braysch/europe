from Person import Person


def merge(ysa, cjc):
    merged = Person()
    # cjc first name is prioritized
    merged.first_name = cjc.first_name
    # get preferred name from profile if it is blank in record
    if cjc.preferred_name == "":
        merged.preferred_name = ysa.first_name
    else:
        merged.preferred_name = cjc.preferred_name
    merged.middle_name = cjc.middle_name
    merged.last_name = cjc.last_name
    # profile birthday is prioritized (it has to match cjc to be created)
    merged.birthdate = ysa.birthdate
    # if the following information is inconsistent, it's not apparent which source is more accurate,
    # so we have alternative variables to store them until we figure it out
    if ysa.email != cjc.email:
        merged.alt_email = cjc.email
    merged.email = ysa.email
    if ysa.phone != cjc.phone:
        merged.alt_phone = cjc.phone
    merged.phone = ysa.phone
    if ysa.street_address != cjc.street_address:
        merged.alt_street_address = cjc.street_address
    merged.street_address = ysa.street_address
    if ysa.street_address_2 != cjc.street_address_2:
        merged.alt_street_address_2 = cjc.street_address_2
    merged.street_address_2 = ysa.street_address_2
    if ysa.city != cjc.city:
        merged.alt_city = cjc.city
    merged.city = ysa.city
    merged.ysa_profile = True
    merged.record = True
    merged.ysa_edit_link = ysa.ysa_edit_link
    merged.cjc_edit_link = cjc.cjc_edit_link

    return merged


def merge_option(list_1, list_2):
    # check for available merges (first and last name match)
    # this is for manual merging, not automatic
    options = []
    for x in list_1:
        for y in list_2:
            if x.last_name == y.last_name and x not in options:
                options.append(x)
    return options


def display_merge_options(list_1, list_2):
    print("MEMBERS TO MERGE"+" "*6+"MEMBERS TO MERGE WITH\n")
    max_1 = len(list_1)
    max_2 = len(list_2)
    if max_1 > max_2:
        max_m = max_1
    else:
        max_m = max_2
    index = 0
    while index < max_m:
        if index < max_1:
            print(list_1[index].preferred_name, list_1[index].last_name, " "*(20-(len(list_1[index].preferred_name+list_1[index].last_name))), end='')
        else:
            print(" "*22, end='')
        if index < max_2:
            print(list_2[index].first_name, list_2[index].last_name)
        else:
            print("")
        index += 1
