import logging
logger = logging.getLogger('ProjectBA')
import gspread
import pandas as pd
from tenacity import *

class accounts():

    def __init__(self, current_row = 2):
        
        gc = gspread.service_account(filename='Users\\Keane\\Files\\Scripts\\Project BA\\Keys\\blue-archive-391407-c429819ca8dd.json')
        self.ss = gc.open_by_url("https://docs.google.com/spreadsheets/d/1r1t6aHqlaNB6qB5sViatFLzO3hmFTkFcJULVj1Jub70"),
        self.sh = self.ss[0].get_worksheet(0),
        self.sh2 = self.ss[0].get_worksheet(1),
        self.current_row = current_row
        self.col_map = {
            'account': 2,
            'pyro' : 3,
            '3stars': 4,
            'email': 5,
            'pw': 6,
            'status': 7,
            'daily': 8,
            'timestamp': 9,
            'region': 10,
            'port': 11
        }

        logger.info('Accounts Initiated.')

    # Generic Functions with Retry (Due to Google API Rate Limits)

    @retry(stop=stop_after_attempt(5), wait = wait_fixed(60), before_sleep=before_sleep_log(logger, logging.INFO))
    def get_cell(self, row, col):
        if row is None:
            row = self.current_row
        return self.sh[0].cell(row, self.col_map[col]).value

    @retry(stop=stop_after_attempt(5), wait = wait_fixed(60), before_sleep=before_sleep_log(logger, logging.INFO))
    def set_cell(self, row, col, value):
        if row is None:
            row = self.current_row
        self.sh[0].update_cell(row, self.col_map[col], value)

    @retry(stop=stop_after_attempt(5), wait = wait_fixed(60), before_sleep=before_sleep_log(logger, logging.INFO))
    def set_cell2(self, row, col, value):
        self.sh2[0].update_cell(row, col, value)

    @retry(stop=stop_after_attempt(5), wait = wait_fixed(60), before_sleep=before_sleep_log(logger, logging.INFO))
    def sort_col(self, col):
        self.sh[0].sort((self.col_map[col], 'asc'))

    @retry(stop=stop_after_attempt(5), wait = wait_fixed(60), before_sleep=before_sleep_log(logger, logging.INFO))
    def get_last_row(self, value, col):
        last_row = self.current_row
        current_val = self.get_cell(last_row, col)
        while current_val == value:
            last_row += 1
            current_val = self.get_cell(last_row, col)
        return last_row - 1

    @retry(stop=stop_after_attempt(5), wait = wait_fixed(60), before_sleep=before_sleep_log(logger, logging.INFO))
    def next_row(self):
        self.current_row += 1

    @retry(stop=stop_after_attempt(5), wait = wait_fixed(60), before_sleep=before_sleep_log(logger, logging.INFO))
    def get_entire_sheet(self):
        headers_and_data = self.sh[0].get_all_values()
        headers = headers_and_data[0]
        data = headers_and_data[1:]
        return pd.DataFrame(data, columns = headers)
    
    # BA specific setters

    def set_pyro(self, value, row = None):
        self.set_cell(row, 'pyro', value)

    def set_3stars(self, value, row = None):
        self.set_cell(row, '3stars', value)

    def set_daily(self, value, row = None):
        self.set_cell(row, 'daily', value)

    def set_timestamp(self, value, row = None):
        self.set_cell(row, 'timestamp', value)

    # BA specific getters

    def get_email(self, row = None):
        return self.get_cell(row, 'email')

    def get_port(self, row = None):
        return self.get_cell(row, 'port')

    def get_pw(self, row = None):
        return self.get_cell(row, 'pw')

    def get_status(self, row = None):
        return self.get_cell(row, 'status')

    def get_daily(self, row = None):
        return self.get_cell(row, 'daily')

    def get_account_name(self, row = None):
        return self.get_cell(row, 'account')