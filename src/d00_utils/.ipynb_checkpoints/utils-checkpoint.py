import pandas as pd
import numpy as np
import sqlite3 as sqli
import os
from sqlalchemy import create_engine
from IPython.display import Markdown
from IPython.display import display
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from statistics import mean

DB_PATH = "../src/d01_data/"

"""
PRINTING FUNCTIONS 
"""

def md(input):
    display(Markdown(input))
    
def line(text):
    print("----------------------------------------------------------------------")
    md(f"##### **{text}**")
    print("----------------------------------------------------------------------")

# Function for formatting salary on "xK $"
def to_k_usd(x):
    return str(int((x / 1000))) + "K $"

#add devise on fig
def add_dollar(fig):
    fmt = '${x:,.0f}'
    tick = mtick.StrMethodFormatter(fmt)
    fig.yaxis.set_major_formatter(tick) 
    
"""
PANDAS SHORTCUTS
"""

#display all duplicated rows for all cols
def show_duplicated_rows(ds):
    dup_ds = ds[ds.duplicated()]
    if len(dup_ds) == 0:
        md("*Aucune ligne dupliquée*")
    else:
        display(dup_ds)
        
#display all duplicated rows for some cols only
def show_duplicated_cells(ds, cols):
    dup_ds = ds[ds.duplicated(subset = cols)]
    if len(dup_ds) == 0:
        md(f"{str(cols)} : Aucune valeur dupliquée")
    else:
        md(f"{str(cols)} : {len(dup_ds)}")


        
def rename_cols(df, new_names):
    old_names = list(df.columns)
    for old_name in old_names:
        if old_name not in new_names:
            new_names[old_name] = old_name.lower()
    df.rename(columns = new_names, inplace = True)
    
    
def quick_view(df, table_name):
    md(f"## {table_name}")
    md("**Shape**")
    display(df.shape)
    md("**Sample**")
    md("**Types**")
    display(df.dtypes)
    md("**Sample**")
    display(df.sample(5))
    
def show_all_values(serie, col_name):
    md(col_name)
    display(pd.DataFrame(data=serie.value_counts()).sort_values(by = col_name))
    
def rename_cols(df, new_names):
    old_names = list(df.columns)
    for old_name in old_names:
        if old_name not in new_names:
            new_names[old_name] = old_name.lower()
    df.rename(columns = new_names, inplace = True)
    

    
"""
DATAFRAME TO SQL 
"""


#from a dataframe get sql to create tables, file must be corrected with pk, fk and correct datatypes
def create_tables_sql_file(dataframes):
    query = ""
    for table_name, df in dataframes.items():
        query += pd.io.sql.get_schema(df, table_name)+";"
    with open(f"{DB_PATH}tables.sql", "w") as f:
        f.write(query)

#delete db file and create a new one with sqlite
def create_database(db_name):
    os.system(f"rm {DB_PATH}{db_name}.db")
    os.system(f"sqlite3 {DB_PATH}{db_name}.db < {DB_PATH}tables.sql")

#insert dataframe data into db
def dataframe_to_insert(dataframes, db_name):
    conn = create_engine(f"sqlite:///{DB_PATH}{db_name}.db")
    for table_name, dt in dataframes.items():
        dt.to_sql(table_name, conn, if_exists="append", index = False)
    
def save_to_sql(dataframes, db_name):
    create_tables_sql_file(dataframes)
    create_database(db_name)
    dataframe_to_insert(dataframes, db_name)
    
def load_from_sql(db_name, table_name):
    conn = create_engine(f"sqlite:///{DB_PATH}{db_name}.db")
    return pd.read_sql_table(table_name, conn) 