from collections import defaultdict
cust_pincode_to_branch_pincode_map_dict = defaultdict(int)

# TODO probably remove the default dict below.
#cust_cif_to_branch_pincode_map_dict = defaultdict(int)

all_branch_pincodes_for_first_two_digits = defaultdict(int)
unique_all_fsfb_branch_codes = []
num_of_hits = []



tamil_nadu = [60, 61, 62, 63, 64, 65, 66]
andhra_pradesh = [51, 52, 53]
gujarat = [36, 37, 38, 39]
karnataka = [56, 57, 58, 59]
madhya_pradesh = [45, 46, 47, 48]
maharashtra = [40, 41, 42, 43, 44]
#puducherry = [60]
rajasthan = [30, 31, 32, 33, 34]
haryana = [12, 13]
delhi = [11]

all_states_served_pincode = [60, 61, 62, 63, 64, 65, 66, 51, 52, 53, 36, 37, 38, 39, 56, 57, 58, 59, 45, 46, 47, 48, 40, 41, 42, 43, 44, 30, 31, 32, 33, 34, 12, 13,11]
all_states = [tamil_nadu, andhra_pradesh, gujarat, karnataka, madhya_pradesh, maharashtra, rajasthan, haryana, delhi]


