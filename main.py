from pprint import pprint

import re
import csv

def get_data_from_csv(csv_filename):
    with open(csv_filename, encoding="utf-8") as f:
      rows = csv.reader(f, delimiter=",")
      contacts_list = list(rows)

    return contacts_list

def set_data_to_csv(csv_filename, result_contacts_list):
    with open(f"{csv_filename}", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(result_contacts_list)

def fio_edit(contact):
    fio = f"{contact[0]} {contact[1]} {contact[2]}".strip().split()
    fio_dict = {
        'lastname': fio[0],
        'firstname': fio[1],
        'surname': fio[2] if len(fio) == 3 else ""
    }

    return fio_dict

def phone_edit(contact):
    phone_pattern = r"\+?[7|8]\s*(\(*\d{3}\)*)\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})"
    secondary_phone_pattern = r"\s+(\d{4})"

    phone_format_with_bracket = r"+7(\1)\2-\3-\4"
    phone_format_no_bracket = r"+7\1\2-\3-\4"
    secondary_phone_format = r"доб.\1"

    phone_result = re.search(phone_pattern, contact[5])
    if phone_result is not None:
        if "(" in phone_result.group():
            phone = re.sub(phone_pattern, phone_format_no_bracket, phone_result.group())
        else:
            phone = re.sub(phone_pattern, phone_format_with_bracket, phone_result.group())
        secondary_phone_result = re.search(secondary_phone_pattern, contact[5])
        if secondary_phone_result is not None:
            secondary_phone = re.sub(secondary_phone_pattern, secondary_phone_format, secondary_phone_result.group())
            contact[5] = f"{phone} {secondary_phone}"
        else:
            contact[5] = f"{phone}"

def table_repetitions_edit(contacts_list):
    result_contacts_list = [contacts_list[0]]
    lastnames_list = []
    firstnames_list = []
    contact_added = False

    for contact in contacts_list[1:]:
        if contact[0] not in lastnames_list or contact[1] not in firstnames_list:
            for contact2 in contacts_list:
                if contact != contact2 and contact[0] == contact2[0] and contact[1] == contact2[1]:
                    new_contact = []
                    for column in range(len(contact)):
                        if contact[column] != '':
                            new_contact.append(contact[column])
                        else:
                            new_contact.append(contact2[column])
                    result_contacts_list.append(new_contact)
                    contact_added = True

            if not contact_added:
                result_contacts_list.append(contact)
            contact_added = False

            lastnames_list.append(contact[0])
            firstnames_list.append(contact[1])

    return result_contacts_list



if __name__ == "__main__":
    contacts_list = get_data_from_csv("phonebook_raw.csv")

    for contact in contacts_list[1:]:
        fio = fio_edit(contact)
        contact[0] = fio['lastname']
        contact[1] = fio['firstname']
        contact[2] = fio['surname']

        phone_edit(contact)
        result_contacts_list = table_repetitions_edit(contacts_list)
        set_data_to_csv("result_phonebook.csv", result_contacts_list)