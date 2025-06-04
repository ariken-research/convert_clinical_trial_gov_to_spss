import json
 
import pandas as pd
import pyreadstat
import sys
import os
from datetime import datetime, date

def replace_by_label_index(data, variable_info):
    output = []
    for element in data:
        element = str(element)
        if not element in variable_info["labels"]:
            element = variable_info["default_value"]
            #print (data)
            #print ("row value not found in labels:[{}]".format(element))
            #print (json.dumps(labels, indent = 2))
        
        val = variable_info["labels"][element]
        
        #Handle something specific, figure out what. TODO
        if not isinstance(val, int):
            if len(val) != 2:
                print("WOOHA?", val)
                sys.exit(-1)
            val = val[1]
        
        output.append(val)
        
    return output
    
def labels_to_spss_labels(labels):
    spss_labels = {}
    for key, val in labels.items():
        new_key              = val[1]
        new_val              = val[0]
        spss_labels[new_key] = new_val
    return spss_labels

def flexible_string_to_date(date_string: str) -> date | None:
    """
    Constructs a datetime.date object from a string.

    Handles formats: 'YYYY-MM-DD', 'YYYY-MM', and 'YYYY'.
    - 'YYYY' becomes YYYY-01-01.
    - 'YYYY-MM' becomes YYYY-MM-01.

    Args:
        date_string: The input string containing the date.

    Returns:
        A datetime.date object, or None if the string doesn't match
        any of the expected formats.
    """
    if not isinstance(date_string, str):
        print(f"Warning: Input '{date_string}' is not a string. Returning None.")
        return None

    formats_to_try = ['%Y-%m-%d', '%Y-%m', '%Y']

    for fmt in formats_to_try:
        try:
            # Try to parse the string with the current format
            dt_object = datetime.strptime(date_string, fmt)
            # If successful, return the date part
            return dt_object.date()
        except ValueError:
            # If parsing fails, try the next format
            continue

    # If none of the formats worked, return None or raise an error
    print(f"Warning: Could not parse date '{date_string}' with known formats. Returning None.")
    return None

input_path = "inputs"
input_json_fn  = os.path.join(input_path, "ctg-studies.json")
variable_fn    = os.path.join(input_path, "variables.json")

output_path = "outputs"
os.makedirs(output_path, exist_ok=True)
output_fn = os.path.join(output_path, "ctg-studies.sav")

debug_output_path = "debug_outputs"
os.makedirs(debug_output_path, exist_ok=True)
debug_variable_value_labels_fn = os.path.join(debug_output_path, "variable_value_labels.json")
debug_variable_format_fn       = os.path.join(debug_output_path, "debug_variable_format.json")
debug_excel_raw_json_in_xlsx   = os.path.join(debug_output_path, "debug_excel_raw_json.xlsx")
debug_output_in_xlsx           = os.path.join(debug_output_path, "debug_excel_output.xlsx")

"debug_excel_output_json.xlsx"
"debug_excel_output_json.xlsx"

with open(input_json_fn) as f:
    ctg_json_data = json.load(f)

clean_up_ctg_input = False
if clean_up_ctg_input:
    with open(input_json_fn, 'w', encoding='utf-8') as f:
        ctg_json_data.dump(ctg_json_data, f, indent=2)

variable_value_labels = {}
variable_format       = {}

with open(variable_fn) as f:
    print("Reading {} and setting column formats and labels..".format(variable_fn))
    variables = json.load(f)
    for variable_info in variables["Variables"]:
        SPSS_column_name                  = variable_info["SPSS_column_name"] 
        variable_format[SPSS_column_name] = variable_info["format"]
        if "labels" in variable_info:
            variable_value_labels[SPSS_column_name] = labels_to_spss_labels(variable_info["labels"])

    with open(debug_variable_value_labels_fn, 'w', encoding='utf-8') as f:
        json.dump(variable_value_labels, f, indent=2)
    with open(debug_variable_format_fn, 'w', encoding='utf-8') as f:
        json.dump(variable_format, f, indent=2)
    
    print("Reading variables.json and setting column formats and labels..")
    output_data      = []
    output_data_json = []
    for ctg_json_data_study in ctg_json_data:
        output_row      = {}
        output_row_json = {}

        for variable_info in variables["Variables"]:
            JSON_location     = variable_info["JSON_location"]
            SPSS_column_name  = variable_info["SPSS_column_name"] 
            SPSS_column_label = variable_info["SPSS_column_label"]
            action            = variable_info["action"] 

            ctg_json_content = ctg_json_data_study
            for location in JSON_location.split(","):
                try:
                    ctg_json_content = ctg_json_content[location]
                except KeyError as e:
                    variable_not_found = location
                    #variables_not_found.add(variable_not_found)
                    ctg_json_content = variables["Variables_not_found_default_values"][variable_not_found]
                except TypeError as e:
                    print("********************************************************************")
                    print("Searching for: ", JSON_location)
                    print("variable has the wrong type:", location)
                    print(e)
                    print(json.dumps(ctg_json_data_study, indent = 2))
                    print("********************************************************************")

            output_row_json[SPSS_column_name] = json.dumps(ctg_json_content, indent = 2)
            
            #print("Processing:", SPSS_column_name)
            
            if action == "multi-dict-response":
                dict_key         = variable_info["dict_key"]
                ctg_json_content = [dic[dict_key] for dic in ctg_json_content]
                action           = "multi-response"
                
            if action == "labels":
                output_val = replace_by_label_index([ctg_json_content], variable_info)[0]
            elif action == "multi-response":
                if variable_info.get("count"):
                    output_val = len(ctg_json_content)
                else:
                    if variable_info.get("take_max") or variable_info.get("sum"):
                        if len(ctg_json_content) == 0:
                            ctg_json_content = [variable_info["default_value"]]
                        
                        labels = replace_by_label_index(ctg_json_content, variable_info)
                    else:
                        print("wat doen we hier?", SPSS_column_name)
                        output_val = ctg_json_content
                        
                    if variable_info.get("take_max"):
                        output_val = max(labels)
                    else:
                        output_val = sum(labels)
               
            else:
                if variable_info["format"] == "EDATE10":
                    output_val = flexible_string_to_date(ctg_json_content)
                else:
                    output_val = ctg_json_content
            output_row[SPSS_column_name]  = output_val
                
            
        output_data.append(output_row)    
        output_data_json.append(output_row_json)    

output_variables_not_found = False
if output_variables_not_found:   
    print("-----------------------------------------------------------------")
    print ("Variables not found:")
    for variable_not_found in variables_not_found:
        print(variable_not_found)

write_raw_json_to_xlsx = True
if write_raw_json_to_xlsx:
    df_json = pd.DataFrame.from_dict(output_data_json)
    with pd.ExcelWriter(debug_excel_raw_json_in_xlsx) as writer:
        df_json.to_excel(writer)

df = pd.DataFrame.from_dict(output_data)
with pd.ExcelWriter(debug_output_in_xlsx) as writer:
    df.to_excel(writer) 

pyreadstat.write_sav(df, output_fn, variable_value_labels=variable_value_labels, variable_format = variable_format)            

    
sys.exit(-1)


     
#for k,v in variable_value_labels.items():
#    print("k,v:", k,v)
#sys.exit(-1)    
#print("variable_value_labels:", variable_value_labels)
#print("variable_format:"      , variable_format)

print(excel_to_spss_column_names)
df = df.rename(columns=excel_to_spss_column_names)

print(df.columns)
v = set()
for col in df.columns:
    if col in v:
        print ("col already found:", col)
    else:
        v.add(col)
print(len(df.columns), len(set(df.columns)))

with open('variables.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
    
pyreadstat.write_sav(df, output_fn, variable_value_labels=variable_value_labels, variable_format = variable_format)            
            
#for k,v in variable_value_labels.items():
#    print("k,v:", k,v)
#sys.exit(-1)    
#print("variable_value_labels:", variable_value_labels)
#print("variable_format:"      , variable_format)


#import json
#with open('your_input.json', 'r') as f: data = json.load(f)
# Assuming 'date_field' is the key holding 'YYYY-MM'
#for item in data:
#if 'date_field' in item and len(item['date_field']) == 7:
#item['date_field'] = item['date_field'] + '-01'
#with open('your_output.json', 'w') as f:json.dump(data, f, indent=4)