import os
from pathlib import Path
from typing import Dict, List

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


def load_environment_variables_for_db():
    # load .env
    load_dotenv()
    return {
        "POSTGRES_USER": os.getenv("POSTGRES_USER"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "POSTGRES_DB": os.getenv("POSTGRES_DB"),
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
        "TABLE_NAME": os.getenv("TABLE_NAME"),
    }


def get_database_engine(env_vars):
    database_url = (
        f"postgresql://{env_vars['POSTGRES_USER']}:"
        f"{env_vars['POSTGRES_PASSWORD']}@"
        f"{env_vars['POSTGRES_HOST']}:"
        f"{env_vars['POSTGRES_PORT']}/"
        f"{env_vars['POSTGRES_DB']}"
    )
    return create_engine(database_url, echo=True)


def send_csv_to_db(filepath: Path, table_name: str) -> None:
    """
    Sends a CSV file to a database table.

    Args:
        filepath (Path): The path to the CSV file.
        table_name (str): The name of the table to send the data to.
        conn: The connection to the database.
    """
    db_env_vars = load_environment_variables_for_db()
    conn = get_database_engine(db_env_vars)
    df = pd.read_csv(filepath)
    df.to_sql(table_name, conn, if_exists="replace", index=False)


def send_xlsx_to_db(
    filepath: Path, table_name: Dict[str, str], sheets: List[str]
) -> None:
    """
    Sends an Excel file to a database table.

    Args:
        filepath (Path): The path to the Excel file.
        table_name (Dict[str:str]): A dictionary where the key is the sheet name and the value is the table name.
        sheets (List[str]): The names of the sheets to send to the database.
    Example:
        send_xlsx_to_db("data.xlsx", {"Sheet1": "table1", "Sheet2": "table2"}, ["Sheet1", "Sheet2"])
    """
    db_env_vars = load_environment_variables_for_db()
    conn = get_database_engine(db_env_vars)
    for sheet in sheets:
        df = pd.read_excel(filepath, sheet_name=sheet)
        df.to_sql(table_name[sheet], conn, if_exists="replace", index=False)
