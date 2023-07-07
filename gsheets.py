import logging
logger = logging.getLogger('ProjectBA')
import gspread
import time


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

        logger.info('Accounts Initiated')

    def get_cell(self, row, col):

        attempts = 0

        while attempts < 6:
            try:
                return self.sh[0].cell(row, self.col_map[col]).value
            except:
                attempts += 1
                logger.info(f'Google API Error Attempt {attempts}; Waiting 30s for Retry')
                time.sleep(30)
        
        logger.critical('Multiple Google API Failures, exiting')

    def set_cell(self, row, col, value):
        self.sh[0].update_cell(row, self.col_map[col], value)

    def set_cell2(self, row, col, value):
        self.sh2[0].update_cell(row, col, value)

    def sort_col(self, col):
        self.sh[0].sort((self.col_map[col], 'asc'))

    def get_last_row(self, value, col):
        last_row = self.current_row
        current_val = self.get_cell(last_row, col)
        while current_val == value:
            last_row += 1
            current_val = self.get_cell(last_row, col)
        return last_row - 1

    def next_row(self):
        self.current_row += 1
        if self.get_cell(self.current_row, 'status') == '':
            self.in_progress = False
            return False
        return True
    
    # BA specific setters

    def set_pyro(self, value):
        self.set_cell(self.current_row, 'pyro', value)

    def set_3stars(self, value):
        self.set_cell(self.current_row, '3stars', value)

    def set_daily(self, value):
        self.set_cell(self.current_row, 'daily', value)

    def set_timestamp(self, value):
        self.set_cell(self.current_row, 'timestamp', value)

    # BA specific getters

    def get_email(self):
        return self.get_cell(self.current_row, 'email')

    def get_port(self):
        return self.get_cell(self.current_row, 'port')

    def get_pw(self):
        return self.get_cell(self.current_row, 'pw')

    def get_status(self):
        return self.get_cell(self.current_row, 'status')

    def get_daily(self):
        return self.get_cell(self.current_row, 'daily')

    def get_account_name(self):
        return self.get_cell(self.current_row, 'account')