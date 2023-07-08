import logging
logger = logging.getLogger('ProjectBA')
from adbfuncs import dvc
import badata
import ocrfuncs
import time
import random
from datetime import datetime

class bad(dvc):

    def __init__(self, server, port, host = "127.0.0.1", accounts = None, df_slice = None):

        super().__init__(server, port, host)

        self.ba_data = badata.badata()
        self.three_star_students = [ocrfuncs.adjust_text(student) for student in self.ba_data.three_star_students]
        self.three_star_students.sort(key = len)
        self.other_students = [ocrfuncs.adjust_text(student) for student in self.ba_data.other_students]
        self.coords = self.ba_data.coords
        self.s_coords = self.ba_data.s_coords
        self.accounts = accounts
        if df_slice is not None:
            self.df = df_slice.reset_index()
            self.df['index'] += 2 # Same row number as on google sheets

    # Generic Functions

    def tap_coords(self, coords_name):
        logger.info(f'Tapping: {coords_name}')
        c = self.coords[coords_name]
        self.tap(c[0], c[1], c[2], c[3], c[4], c[5], c[6])

    def swipe_coords(self, coords_name):
        logger.info(f'Swiping: {coords_name}')
        c = self.s_coords[coords_name]
        self.swipe(c['start'][0], c['start'][1],
                   c['stop'][0], c['stop'][1],
                   c['duration'], c['repeat'])
    
    # Daily Claim

    def daily_claims(self, update_students = False):

        for index, row in self.df.iterrows():
            logger.info(f'Starting {row["account"]} on {self.port}.')
            self.daily_claim(sheet_number = row['index'], 
                             use_accounts = False, 
                             account_name = row['account'],
                             email = row['email'], 
                             password = row['pw'], 
                             update_students = update_students)
        logger.info(f'Finished daily claims for {self.port}.')

    def daily_claim(self, sheet_number = None, use_accounts = False, account_name = '', email = '', password = '', update_students = False):

        if use_accounts:
            email = self.accounts.get_email()
            password = self.accounts.get_pw()
        self.login(email, password)
        self.claim_mail()
        self.update_sheets(account_name = account_name, update_students = update_students, sheet_number = sheet_number)
        self.logout()

    def login(self, email, password):

        ocr = ocrfuncs.listener(self.get_screenshot, ['Menu', 'Sign in with Nexon ID'], 5, 0)
        if ocr == 'menu':
            self.tap()
            time.sleep(10)
        self.tap_coords('opener_signin')
        self.nexon_login(email, password)
        ocr =  ocrfuncs.listener(self.get_screenshot, ['Notice', 'Day 1'], 5, 5)
        if ocr == 'notice':
            self.tap_coords('dual_cancel')
            self.tap_coords('single_confirm')
            ocrfuncs.listener(self.get_screenshot, ['Notice', 'Day 1'], 5, 5)
            self.tap_coords('login_arona')
            self.login_notices()
            self.tap_coords('login_notice_two')
        else:
            self.tap_coords('login_arona')
            self.login_notices()
            self.tap_coords('login_notice_two')

    def login_notices(self):
        self.tap_coords('login_notice_one')
        time.sleep(5)
        self.tap_coords('login_notice_two')
    
    def claim_mail(self):
        self.tap_coords('mail_opn')
        self.tap_coords('mail_clm')
        self.tap_coords('mail_cls')

    def logout(self):
        self.tap_coords('menu_opn')
        self.tap_coords('menu_acc')
        self.swipe_coords('menu_acc_down')
        self.tap_coords('menu_acc_logout')
        self.tap_coords('dual_confirm')

    def nexon_login(self, email, password):
        self.tap_coords('nexon_cancel_email')
        self.tap_coords('nexon_email')
        self.type(email)
        time.sleep(3)
        self.tap_coords('nexon_pass')
        self.type(password)
        time.sleep(3)
        self.tap_coords('nexon_login')

    def update_sheets(self, account_name = None, sheet_number = None, update_students = False):

        if update_students:
            if account_name is None:
                account_name = self.accounts.get_account_name(row = sheet_number)
            self.accounts.set_3stars(self.get_students(account = account_name, main_page = 'home'), row = sheet_number)
        self.accounts.set_pyro(self.get_pyro(), row = sheet_number)
        self.accounts.set_daily('done', row = sheet_number)
        self.accounts.set_timestamp(str(datetime.now()).split('.')[0], row = sheet_number)

    # Pulls

    def pulls(self, banner_shift = 0):

        def arona_animation():
            time.sleep(5)
            self.tap()
            self.tap_coords('recruit_skip')
        
        self.tap_coords('recruit_opn')
        time.sleep(4)
        for i in range(banner_shift):
            self.tap_coords('recruit_change_banner')
        self.tap_coords('recruit_tenpull')
        self.tap_coords('dual_confirm')
        
        within_ten = True

        while within_ten:
            within_single = True
            arona_animation()
            while within_single:
                result = ocrfuncs.listener(self.get_screenshot, ['Skip', 'Skip >', 'Skip >>', 'Confirm', 'Weapons Used', 'Birthday', 'We recruited a new student!'])
                # First Ten-Pull after reroll
                if result in ['werecruitedanewstudent']:
                    self.tap(2)
                    self.tap_coords('recruit_aftertenpull')
                    within_single = False
                    within_ten = False
                # If 3-Star Pulled, single tap needed
                if result in ['weaponsused', 'birthday']:
                    self.tap()
                    self.tap_coords('recruit_skip')
                    # pulled_character = ocrfuncs.listener(self.get_screenshot, self.students, limit = 1, lower = True, remove_whitespace = True)
                # Skiperinos
                if result in ['skip', 'skip>', 'skip>>']:
                    # pulled_character = ocrfuncs.listener(self.get_screenshot, self.students, limit = 1, lower = True, remove_whitespace = True)
                    # To save somewhere
                    # print(pulled_character)
                    self.tap_coords('recruit_skip')
                # Doned
                if result == 'confirm':
                    first_ten_check = ocrfuncs.listener(self.get_screenshot, ['We recruited a new student!'], 5, 5, 1)
                    if first_ten_check == 'werecruitedanewstudent':
                        self.tap(times = 2)
                        self.tap_coords('recruit_aftertenpull')
                        within_single = False
                        within_ten = False
                    else:
                        self.tap_coords('recruit_aftertenpull')
                        within_single = False
                        self.tap_coords('recruit_again')
                        self.tap_coords('dual_confirm')
                        # Check if out of tenpulls
                        result2 = ocrfuncs.listener(self.get_screenshot, ['Purchase?'], 5, 5, 1)
                        if result2 == 'purchase':
                            self.tap_coords('dual_cancel')
                            self.tap_coords('dual_cancel')
                            self.tap_coords('third_battle_to_lobby')
                            self.tap_coords('menu_opn')
                            within_ten = False

                        # Fix Loop for first ten

    # One Time Reroll

    def multi_reroll(self, banner_shift, targets, max_loop = 10):

        evaluate = True
        loop = 1

        while evaluate and loop < max_loop:

            results = self.reroll(banner_shift)
            #self.accounts.set_cell2(loop, 1, results)

            for target in targets:
                if target in results:
                    evaluate = False

            loop += 1

            logger.info(f'Reset & Continue reroll: {evaluate}')

            if evaluate and loop < max_loop:
                self.reset_account()

    def reroll(self, banner_shift = 0, user = 'temp'):
        
        self.new_account()
        self.forward_story()
        self.battle_one()
        self.forward_story()
        self.forward_story()
        self.battle_two()
        self.pulls()
        self.battle_three()
        ocrfuncs.listener(self.get_screenshot, ['Day 1'], 5, 5)
        self.tap_coords('login_arona')
        self.momotalk_tut()
        time.sleep(3)
        self.claim_mail()
        time.sleep(3)
        self.learn_link()
        self.pulls(banner_shift)
        time.sleep(5)
        self.login_notices()
        time.sleep(7)
        self.triple_student()
        return self.get_students(account = user)


    def forward_story(self):
        ocrfuncs.listener(self.get_screenshot, ['Menu'], 5, 1)
        self.tap_coords('story_menu')
        self.tap_coords('story_forward')
        self.tap_coords('dual_confirm')

    def new_account(self):
        
        ocrfuncs.listener(self.get_screenshot, ['Menu'], 5, 0)
        self.tap()
        time.sleep(10)
        check = ocrfuncs.listener(self.get_screenshot, ['enteryourname', 'Play with Guest Account', 'Confirm'], 5, 0)
        if check == 'playwithguestaccount':
            self.tap_coords('reroll_select_guest_account')
            self.tap_coords('reroll_confirm_guest_account')
            ocrfuncs.listener(self.get_screenshot, ['Confirm'], 5, 0)
            self.tap_coords('single_confirm')
        if check == 'confirm':
            self.tap_coords('single_confirm')
        self.tap_coords('reroll_name')
        name = random.choice(['Thomas', 'Stacy', 'Dave', 'Greg' , 'Rachel', 'Fae', 'Charles'])
        self.type(name)
        time.sleep(7)
        self.tap_coords('reroll_confirm')
        #self.tap_coords('reroll_name_2')
        #self.type('Name')
        #time.sleep(7)
        #self.tap_coords('single_confirm')
        #self.tap_coords('single_confirm')
        ocrfuncs.listener(self.get_screenshot, [f'Welcome to the Shittim Chest, {name} Sensei', f'Welcome to the Shittim Chest, {name} Sensei.'], 5, 10)
        self.tap_coords('single_confirm')

    def battle_one(self):
        ocrfuncs.listener(self.get_screenshot, ['Let me tell you about the Skill'], 5, 5)
        self.tap(times = 8)
        ocrfuncs.listener(self.get_screenshot, ['The enemy has appeared'], 5, 5)
        self.tap(times = 3)
        self.tap_coords('battle_skill_two')
        self.tap_coords('first_battle_aoe')
        time.sleep(5)
        ocrfuncs.listener(self.get_screenshot, ["Now try using Yuuka's skill", 'tap Yuuka.'], 5, 5)
        self.tap(times = 3)
        self.tap_coords('battle_skill_one')
        self.tap(times = 1)
        time.sleep(5)
        self.tap(times = 1)
        ocrfuncs.listener(self.get_screenshot, ['Confirm'], 5, 15)
        self.tap_coords('battle_confirm')

    def battle_two(self):
        ocrfuncs.listener(self.get_screenshot, ['The students will automatically', 'take cover upon finding cover', 'spots.'], 5, 10)
        self.tap(times = 6)
        self.forward_story()
        time.sleep(10)
        self.forward_story()
        time.sleep(10)
        self.forward_story()
        self.forward_story()
        ocrfuncs.listener(self.get_screenshot, ["We're up against a Crusader", 'Tank!'], 5, 5)
        self.tap(times = 4)
        self.tap_coords('battle_skill_one')
        self.tap_coords('second_battle_tank')
        time.sleep(15)
        ocrfuncs.listener(self.get_screenshot, ['Confirm'], 5, 5)
        self.tap_coords('battle_confirm')
        self.forward_story()
        self.forward_story()
        time.sleep(5)
        self.tap()
        self.tap_coords('dual_confirm')
        ocrfuncs.listener(self.get_screenshot, ['Now the real work begins', 'Now the real work begins!'], 5, 5)
        self.tap(times = 3)

    def battle_three(self):

        ocrfuncs.listener(self.get_screenshot, ['We have to stop the enemies', 'disturbing the peace in Kivotos!'], 5, 5)
        self.tap()
        self.tap_coords('third_battle_enter')
        self.tap_coords('battle_start_mission')
        ocrfuncs.listener(self.get_screenshot, ['Before you is a strategy map.', 'Arrange the students into units', 'to handle bigger operations.'], 5, 5)
        self.tap(times = 2)
        self.tap_coords('third_battle_tile1')
        ocrfuncs.listener(self.get_screenshot, ["Why don't we add the students", 'we just recruited?'], 5, 3)
        self.tap()
        self.tap_coords('battle_formation')
        self.tap(times = 10)
        self.tap_coords('battle_formation_confirm')
        self.tap()
        self.tap_coords('battle_confirm')
        ocrfuncs.listener(self.get_screenshot, ['Tap the Begin Mission button to', 'start!'], 5, 3)
        self.tap()
        self.tap_coords('battle_confirm')
        time.sleep(5) # possible breakage
        self.tap(times = 2)
        self.tap_coords('third_battle_tile2')
        time.sleep(10) # possible breakage
        self.tap_coords('battle_auto')
        ocrfuncs.listener(self.get_screenshot, ['Confirm', 'Battle Complete'], 5, 15)
        self.tap_coords('battle_confirm')
        ocrfuncs.listener(self.get_screenshot, ['S', 'Acquired Rank!'], 5, 2)
        self.tap_coords('battle_rate_confirm')
        ocrfuncs.listener(self.get_screenshot, ['You cannot move an ally unit', 'that just moved.'], 5, 5)
        self.tap(times = 2)
        self.tap_coords('battle_confirm')
        ocrfuncs.listener(self.get_screenshot, ["It's our turn again!"], 5, 2)
        self.tap(times = 3)
        self.tap_coords('third_battle_tile3')
        ocrfuncs.listener(self.get_screenshot, ['Confirm'], 5, 15)
        self.tap_coords('battle_confirm')
        time.sleep(6)
        self.tap_coords('mission_complete_confirm')
        ocrfuncs.listener(self.get_screenshot, ['That should cover the basics of', 'battle.'], 5, 10)
        self.tap(times = 3)
        self.tap_coords('third_battle_to_lobby')

    def momotalk_tut(self):
        ocrfuncs.listener(self.get_screenshot, ['bulk of your work.', 'Great job, Sensei! This is the', 'Schale lobby.'], 5, 1)
        self.tap(times = 3)
        time.sleep(3)
        self.tap_coords('momotalk_box')
        self.tap(times = 6)
        self.tap_coords('momotalk_msg')
        self.tap()
        self.tap_coords('momotalk_msg')
        self.tap(times = 3)
        self.tap_coords('momotalk_out')

    def learn_link(self):
        self.tap(times = 2)
        self.tap_coords('menu_opn')
        self.tap_coords('menu_acc')
        time.sleep(1)
        self.tap_coords('mail_cls')
        time.sleep(1)
        self.tap()
        self.tap_coords('menu_acc_cnt')
        self.tap(times = 4)
        self.tap_coords('menu_acc_cls')
        self.tap_coords('menu_cls')

    def triple_student(self):
        self.tap_coords('students')
        self.tap(times = 2)
        self.tap_coords('students_first')
        self.tap(times = 8)
        self.tap_coords('students_levelup')
        self.tap(times = 6)
        self.tap_coords('back_top_left')
        self.tap(times = 2)
        self.tap_coords('students_first')
        self.tap(times = 8)
        self.tap_coords('back_top_left')
        self.tap(times = 2)
        self.tap_coords('students_first')
        self.tap(times = 4)
        self.tap_coords('students_skillone')
        self.tap(times = 3)
        self.tap_coords('students_skill_levelup')
        self.tap(times = 8)
        self.tap_coords('back_top_left')
        self.tap_coords('back_top_left')

    def get_students(self, account, main_page = 'students'):

        if main_page == 'home':
            self.tap_coords('students')
        self.tap_coords('students_sort')
        self.tap_coords('students_sort_stars')
        self.tap_coords('students_sort_confirm')
        self.get_screenshot(self.ba_data.base_path + f'\Images\Accounts\{account}.png')
        self.swipe_coords('students_down')
        pulled_characters = self.extract_students()
        logger.info(f'Pulled: {pulled_characters}')
        self.tap_coords('back_top_left')
        return ','.join(pulled_characters)

    def get_pyro(self):
        path = self.get_screenshot(self.ba_data.base_path + f'\Images\Screen.png')
        ocrfuncs.crop_image(path, path, 1250, 27, 1500, 92)
        return ocrfuncs.get_all_text(path)[0]

    def reset_account(self):
        self.tap_coords('menu_opn')
        self.tap_coords('menu_acc')
        time.sleep(1)
        self.tap_coords('mail_cls')
        self.tap_coords('reset_account')
        self.tap_coords('reset_ba')
        self.type('BlueArchive')
        time.sleep(7)
        self.tap_coords('dual_confirm')
        self.tap_coords('dual_confirm')
        time.sleep(1)
        self.tap_coords('single_confirm')

    def extract_students(self, image_path = None):

        if image_path == None:
            texts = ocrfuncs.get_all_text(self.get_screenshot())
        else:
            texts = ocrfuncs.get_all_text(image_path)
        texts = [ocrfuncs.adjust_text(text) for text in texts]
        # Filter out 2-star students
        texts = [student for student in texts if student not in self.other_students]
        found = []

        temp_three_star_students = self.three_star_students.copy()

        for three_star_student in temp_three_star_students:
            if three_star_student in texts:
                found.append(three_star_student)
                texts.remove(three_star_student)
                temp_three_star_students.remove(three_star_student)

        texts = ''.join(texts)

        for three_star_student in temp_three_star_students:
            if three_star_student in texts:
                found.append(three_star_student)
                temp_three_star_students.remove(three_star_student)

        found = list(set(found))

        return found
