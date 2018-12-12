from mapping_dict_list import *
import re
import pandas as pd
import numpy as np
import requests



def map_customer_nearest_branch(pincode, csv_writer, csv_writer_error):
    if is_customer_in_served_state(pincode):
        if cust_pincode_to_branch_pincode_map_dict[pincode] == 0:
            if str(pincode) not in unique_all_fsfb_branch_codes[0]:
                state_code = get_pincode_first_two_digits(pincode)
                state_all_branch_pincode = get_all_state_branch_pincodes(state_code)
                closest_branch_pincode = get_short_distance_branch_pincode(pincode, state_all_branch_pincode, csv_writer, csv_writer_error)
                cust_pincode_to_branch_pincode_map_dict[pincode] = closest_branch_pincode
            else:
                cust_pincode_to_branch_pincode_map_dict[pincode] = pincode
    else:
        cust_pincode_to_branch_pincode_map_dict[pincode] = 560035


def is_customer_in_served_state(pincode):
    return (get_pincode_first_two_digits(pincode) in all_states_served_pincode)


def get_pincode_first_two_digits(pincode):
    return int(pincode/10000)


def get_all_state_branch_pincodes(state_code):
    state_first_two_digits_all = get_state_all_first_two_digits(state_code)
    return get_branch_codes(state_first_two_digits_all)


def get_state_all_first_two_digits(state_code):
    for idx,state in enumerate(all_states):
        if state_code in state:
            return all_states[idx]


def get_branch_codes(state_first_two_digits_all):
    all_state_branch_codes = []
    for first_two_digit in state_first_two_digits_all:
        lst = all_branch_pincodes_for_first_two_digits[first_two_digit]
        if(len(lst) > 0):
            for value in lst:
                all_state_branch_codes.append(value)
    return all_state_branch_codes

def produce_unique_fsfb_branch_pincodes(series_of_branch_pincodes):
    unique_all_fsfb_branch_codes.append(list(np.unique(series_of_branch_pincodes)))


def produce_list_of_all_state_branch_pincodes(list_of_unique_branch_pincodes, list_of_pincodes_first_two_digits):
    for pin in list_of_pincodes_first_two_digits:
        list_pin = list(pd.Series(list_of_unique_branch_pincodes).apply(lambda x: 0 if re.match(str(pin),x)==None else int(x)))
        all_branch_pincodes_for_first_two_digits[pin] = list(list(filter(lambda list_pin: list_pin != 0, list_pin)))

# #TODO remove the function below.
# def get_short_distance_branch_pincode(orgin_pincode, destination_list_of_pincode,csv_writer):
#     number_of_dest = len(destination_list_of_pincode)
#     num_of_hits.append(number_of_dest)
#     return 560035

def get_short_distance_branch_pincode(origin_pincode, destination_list_of_pincode, csv_writer, csv_writer_error):
    distance_matrix = []
    closest_destination = 0

    for dest in destination_list_of_pincode:
        print("orgin_pincode: {} destination: {}".format(origin_pincode, dest))
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric"

        try:
            r = requests.get(url+'&origins='+str(origin_pincode)+'&destinations='+str(dest)+'&key=AIzaSyAwmWLmzibtkntESWyZYckRrw4kUQhqvvw&region=IN')
            distance = float((r.json()['rows'][0])['elements'][0]['distance']['text'].replace('km', '').replace(',', '').strip())
            print("the distance between the origin and pincode is: {}".format(distance))
            duration = (r.json()['rows'][0])['elements'][0]['duration']['text']
            out_status = r.json()['status']
            element_status = (r.json()['rows'][0])['elements'][0]['status']
            distance_matrix.append((origin_pincode, dest, out_status, element_status, distance, duration))
            csv_writer.writerow([origin_pincode, dest, out_status, element_status, distance, duration])
        except Exception as e:
            csv_writer_error.writerow([origin_pincode, dest])
            print("The error is ",e)

        # TODO remove the following break from the code.
        # break

    try:
        df = pd.DataFrame(distance_matrix, columns=['origin', 'destination', 'out_status', 'element_status', 'distance', 'duration'])
        closest_destination = df.loc[df['distance'] == min(df['distance']),'destination']
        closest_destination = closest_destination[closest_destination.index[0]]
        return closest_destination
    except Exception as e:
        print("The error is ", e)












