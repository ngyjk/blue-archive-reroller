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
import baauto
import gsheets
from multiprocessing.pool import ThreadPool as Pool
server = AdbClient(host="127.0.0.1", port=5037)
os.chdir('..\..\..\..\..')

def daily_connect_run_shut(device, df_slice, update_students = False, accounts = None):
    try:
        logger.info(f'Starting daily for {device}.')
        dvc = baauto.bad(server, port = int(device), df_slice = df_slice, accounts = accounts)
        dvc.open_and_hide()
        dvc.connect()
        dvc.open_ba_app()
        dvc.daily_claims(update_students)
        dvc.disconnect()
        dvc.kill_process()
        return device
    except:
        logger.critical(f'[{device}] Crashed.', exc_info = True)
        dvc.disconnect()
        dvc.kill_process()

def daily_login(update_students = False):

    accounts = gsheets.accounts()
    accounts.sort_col('port')
    df = accounts.get_entire_sheet()
    df = df[df['status'] == 'linked']
    df = df[df['daily'] != 'done']
    device_ports = []

    for device in set(df['device_port'].values):
        if int(device) >= 9000:
            continue
        df_slice = df[df['device_port'] == device]
        device_ports.append((device, df_slice, update_students, accounts))
        logger.info(f'{device} mapped to accounts: {list(df_slice.account.values)}')

    with Pool(processes = 2) as pool:
        results = pool.starmap(daily_connect_run_shut, device_ports)
    
    #for device, df_slice, update_students, accounts in device_ports:
        #daily_connect_run_shut(device, df_slice, update_students, accounts)

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
    dvc.reroll(banner_shift = 3, stage = 'a')
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
    #daily_login(update_students=True)
    #adhoc(5645)
    rerolls(reset_account = False, banner_shift = 3,targets = ['harunanewyear', 'fuukanewyear', 'himari', 'ako', 'iroha'])
    #adhoc(5645)
    logger.info(f"The start time is : {starttime}")
    logger.info(f"The time difference is : {timeit.default_timer() - starttime}")
    quit()


# Auto Kill / Start Server
# Error Handling for Various Scenarios (App crash, emulator crash)
# Re-write ocrfuncs to capture current state
# Fix Foreground Window Error
# Dashboard for Accounts
# Optimize API calls to gspread
# Path Management
# Seperate Re-Roll Script


















0