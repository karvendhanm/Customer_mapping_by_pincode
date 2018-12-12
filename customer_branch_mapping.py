import pandas as pd
import numpy as np
import mapping_functions
from mapping_dict_list import *
import csv

data_dir = "C:/Users/John/PycharmProjects/customer_mapping/data"

# This portion of the code could be used when the file crashes.
try:
    cust_closest_branch_list_temp = []
    df = pd.read_csv(data_dir + '/customer_mapping_file_written_csv.csv')
    for origin in list(np.unique(df['origin'])):
        df_ = df.loc[df['origin'] == origin, :]
        closest_destination = df_.loc[df_['distance'] == min(df_['distance']), 'destination']
        closest_destination = closest_destination[closest_destination.index[0]]
        cust_closest_branch_list_temp.append([origin, closest_destination])
        df_temp = pd.DataFrame(cust_closest_branch_list_temp, columns=['cust_pincode', 'closest_branch_pincode'])
        df_temp.to_csv(data_dir + "/cust_closest_branch_mapping_DONT_DELETE.csv", index=False)

except Exception as e:
    print(e)

# try statement read a csv file 'cust_closest_branch_mapping.csv' if it exists, and then populate a dictionary called
# cust_pincode_to_branch_pincode_map_dict. cust_pincode_to_branch_pincode_map_dict maps the customer pincode(key) with the
# nearest FSFB branch pincode(value).
try:
    temp_list = []
    df_read = pd.read_csv(data_dir+"/cust_closest_branch_mapping_DONT_DELETE.csv")
    temp_list = df_read.to_dict(orient = 'split')
    for idx in temp_list['data']:
        cust_pincode_to_branch_pincode_map_dict[idx[0]] = idx[1]
except Exception as e:
    print(e)

# Reading in the files as a dataframe
# TODO map the correct input files. Ask shebin regarding those two CIF numbers
df_cust_pincode = pd.read_csv(data_dir+"/cust_and_pin_code_tiniset.csv", dtype={'cif':np.str,'cust_pin_code':np.int64})
df_branch_pincode = pd.read_csv(data_dir+"/branch_and_pin_code.csv", dtype = str)

# This function 'produce_unique_fsfb_branch_pincodes' just produces the number of pincodes
#  FSFB serves and stores them in a list. Even if there are multiple branches in a
# particular pincode, even then we just calculate that we are serving just one pincode.
mapping_functions.produce_unique_fsfb_branch_pincodes(df_branch_pincode['branch_pin_code'])
print("Number of pincodes FSFB serves pan India: %d"%len(unique_all_fsfb_branch_codes[0]))


# This function populates a dict which has first two digits of the pincode FSFB serves as a
#  key, and all the pincodes that match those first two digits as a list.
mapping_functions.produce_list_of_all_state_branch_pincodes(unique_all_fsfb_branch_codes[0], all_states_served_pincode)
number_of_unique_pincode_branches = sum([len(lst_branch) for lst_branch in list(all_branch_pincodes_for_first_two_digits.values())])
print("Number of branches mapped: %d"%(number_of_unique_pincode_branches))

# TODO this code below must be refactored.
###########################
csv_file = open(data_dir+"/customer_mapping_file_written_csv.csv", "a", newline='')
csv_writer = csv.writer(csv_file)

file_empty_check = open(data_dir+"/customer_mapping_file_written_csv.csv", "rb")
if(file_empty_check.readline() == b''):
    csv_writer.writerow(["origin", "destination", "out_status", "element_status", "distance", "duration"])
file_empty_check.close()
###########################
###########################
csv_error_file = open(data_dir+"/customer_mapping_error_pincodes.csv", "a", newline='')
csv_writer_error = csv.writer(csv_error_file)

file_empty_check_error = open(data_dir+"/customer_mapping_error_pincodes.csv", "rb")
if(file_empty_check_error.readline() == b''):
    csv_writer_error.writerow(["origin", "destination"])
file_empty_check_error.close()
############################

df_cust_pincode['cust_pin_code'].apply(lambda x: mapping_functions.map_customer_nearest_branch(x, csv_writer, csv_writer_error))
csv_file.close()
csv_error_file.close()

# Saving the results in a csv file for future usage
#TODO see if we can incorporate the below line of code
df = pd.DataFrame(list(cust_pincode_to_branch_pincode_map_dict.items()), columns=['cust_pincode','closest_branch_pincode'])
df.to_csv(data_dir+"/cust_closest_branch_mapping_DONT_DELETE.csv", index = False)

# # TODO make suitable adjustments for this code
# print(sum(num_of_hits))

df_all_google_api_data = pd.read_csv(data_dir+"/customer_mapping_file_written_csv.csv")
df_cust_pincode['closest_branch_pincode'] = df_cust_pincode['cust_pin_code'].apply(lambda x: cust_pincode_to_branch_pincode_map_dict[x])
df_cust_pincode = pd.merge(df_cust_pincode, df_all_google_api_data, how='left',left_on=['cust_pin_code','closest_branch_pincode'], right_on = ['origin','destination'])
df_cust_pincode = df_cust_pincode.drop(['origin','destination'],axis = 1)
df_cust_pincode.fillna(0, inplace = True)

df_cust_pincode.to_csv(data_dir+"/final_csv.csv", index = False)





























