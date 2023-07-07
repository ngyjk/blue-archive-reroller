import logging
import sys
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('ProjectBA')
logger.setLevel(logging.INFO)
import os
from ppadb.client import Client as AdbClient
import timeit
os.chdir('Files\Scripts\Project BA')
import baauto
import gsheets
server = AdbClient(host="127.0.0.1", port=5037)
os.chdir('..\..\..\..\..')

def daily_login(update_students = False):

    accounts = gsheets.accounts()
    accounts.sort_col('port')
    complete = False
    current_port = 0

    while complete == False:
        while current_port == 0:
            if accounts.get_status() == 'linked' and accounts.get_daily() != 'done':
                current_port = accounts.get_port()
            elif int(accounts.get_port()) > 8999:
                logger.info('All Accounts Finished')
                complete = True
                break
            else:
                logger.info(f'{accounts.get_account_name()} Already done, skipping')
                accounts.next_row()
        if complete:
            break
        first_row = accounts.current_row
        last_row = accounts.get_last_row(current_port, 'port')
        logger.info(f'Going through accounts from row {first_row} to {last_row} at {current_port}')
    
        dvc = baauto.bad(server, int(current_port), accounts = accounts, first_row = first_row, last_row = last_row)
        dvc.open_and_hide()
        dvc.connect()
        dvc.open_ba_app()
        if dvc.daily_claims(update_students) == 'complete':
            complete = True
        dvc.disconnect()
        dvc.kill_process()
        current_port = 0

def rerolls(reset_account = False, banner_shift = 3, targets = ['haruna(newyear)', 'haruna(newyear', 'fuuka(newyear)', 'fuuka(newyear', 'himari', 'ako', 'iroha']):
    dvc = baauto.bad(server, 5645)
    dvc.open_and_hide()
    dvc.connect()
    dvc.open_ba_app()
    dvc.connect()
    if reset_account:
        dvc.reset_account()
    dvc.multi_reroll(banner_shift = banner_shift, targets = targets)
    dvc.disconnect()

def adhoc(dvc_port = 5645):
    dvc = baauto.bad(server, dvc_port)
    dvc.connect()
    dvc.reroll(banner_shift = 3)
    #dvc.pulls()
    #print(dvc.ocr_texts())
    #dvc.pulls(3)
    #dvc.triple_student()
    #dvc.accounts.set_cell(2, 'daily', 5)
    #dvc.get_pyro()
    #dvc.daily_claims()
    dvc.open_ba_app()
    dvc.disconnect()

if __name__ == "__main__":

    starttime = timeit.default_timer()
    daily_login(update_students=True)
    #adhoc(5645)
    rerolls(reset_account = False, banner_shift = 3,targets = ['harunanewyear', 'fuukanewyear', 'himari', 'ako', 'iroha'])
    #adhoc(5645)
    logger.info(f"The start time is : {starttime}")
    logger.info(f"The time difference is : {timeit.default_timer() - starttime}")
    quit()


# Settle Logging - Done
# Optimize API calls to gspread
# Multi-Processing for Logins 
# Auto Kill / Start Server
# Error Handling for Various Scenarios (App crash, emulator crash)
# Re-write ocrfuncs to capture current state
# Fix Foreground Window Error
# Dashboard for Accounts
# Optimize API calls to gspread
# Path Management
# Seperate Re-Roll Script


















0