
import gspread

def append_row_if_unique(row_data = ['18erecs080.vicky@rietjaipur.ac.in']):
    spreadsheet_id = '1akZpxtRhFIm97X9ZIdlAm10nfs0_drWTo40rVvkI6zs'
    worksheet_name = 'Sheet1'
    unique_col_index = 0 

    gc = gspread.service_account(filename='ideationology-lab-b60654e44e37.json')
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet(worksheet_name)

    existing_data = worksheet.get_all_values()
    unique_element_exists = any(row_data[unique_col_index] == row[unique_col_index] for row in existing_data)

    if not unique_element_exists:
        worksheet.append_row(row_data)
        print("Row added successfully.")
    else:
        print("Row not added, element already exists.")

# row_data = ['hellovickykumar123@gmail.com']
# append_row_if_unique(row_data)
