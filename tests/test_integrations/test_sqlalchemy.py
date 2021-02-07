import os
from anythingtoanywhere import copy


SQLITE_FILE_PATH = os.getcwd()


def test_https_to_sqlalchmy():
    url = (
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
        "archived_data/archived_daily_case_updates/01-21-2020_2200.csv"
    )
    conn_string = "sqlite:///anythingtoanywhere.db"
    copy(url, conn_string, dest_table_name="covid", dest_if_exists="replace")
