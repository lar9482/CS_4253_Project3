import pandas as pd
import openpyxl
import os
import sys
from pathlib import Path

def save_values(dictionary, file_name):
    df = pd.DataFrame.from_dict(dictionary.items()).transpose()
    
    if (not Path(os.path.join(sys.path[0], file_name) + '.xlsx')):
        print()
    wb = openpyxl.load_workbook(os.path.join(sys.path[0], file_name) + '.xlsx') 
    sheet = wb.active 
    for index, row in df.iterrows():
        sheet.append(row.values.tolist())
  
    wb.save(os.path.join(sys.path[0], file_name) + '.xlsx')