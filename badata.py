class badata():
    def __init__(self):
        self.coords = {
            # Generic
            'single_confirm': (970, 750, 1, 1, 50, 30, 0.2),
            'dual_cancel': (770, 750, 1, 1, 50, 10, 0.2),
            'dual_confirm': (1150, 750, 1, 1, 50, 10, 0.2),
            'back_top_left': (85, 54, 1, 3, 5, 5, 0.2),
            # Momotalk
            'momotalk_box': (250, 215, 1, 1, 30, 20, 0.2),
            'momotalk_msg': (250, 400, 1, 1, 30, 20, 0.2),
            'momotalk_out': (1680, 175, 1, 1, 10, 10, 0.2),
            # Mail
            'mail_opn': (1715, 55, 1, 2, 10, 10, 1),
            'mail_clm': (1700, 1005, 3, 2, 20, 5, 0.2),
            'mail_cls': (1855, 35, 1, 3, 20, 20, 0.2),
            # In Game Menu
            'menu_opn': (1835, 55, 1, 1, 25, 10, 0.2),
            'menu_cls': (1275, 330, 1, 1, 20, 10, 0.2),
            'menu_acc': (1150, 450, 1, 1, 30, 10, 0.2),
            # In Game Account Menu
            'menu_acc_cnt': (1530, 325, 1, 1, 30, 10, 0.2),
            'menu_acc_cls': (1435, 205, 1, 1, 20, 10, 0.2),
            'menu_acc_logout': (1340, 700, 1, 1, 50, 10, 0.2),
            # Pulls
            'recruit_opn': (1365, 965, 1, 5, 10, 10, 0.2),
            'recruit_change_banner': (1880, 590, 1, 2, 2, 2, 0.2),
            'recruit_tenpull': (1680, 780, 1, 1, 10, 5, 0.2),
            'recruit_skip': (1785, 74, 1, 1, 5, 5, 0.2),
            'recruit_aftertenpull': (960, 945, 1, 3, 5, 5, 0.2),
            'recruit_again': (1190, 940, 1, 3, 5, 5, 0.2),
            # Login
            'opener_signin': (1180, 550, 1, 6, 50, 10, 0.2),
            'nexon_cancel_email': (1185, 220, 1, 1, 1, 1, 0.2),
            'nexon_email': (760, 220, 1, 1, 50, 10, 0.2),
            'nexon_pass': (760, 315, 1, 1, 50, 10, 0.2),
            'nexon_login': (960, 430, 1, 1, 50, 10, 0.2),
            'login_arona': (1765, 175, 2, 5, 20, 20, 0.2),
            'login_notice_one': (1765, 175, 1, 2, 20, 20, 0.2),
            'login_notice_two': (1400, 150, 1, 2, 20, 20, 0.2),
            # Reroll Specific
            'reroll_select_guest_account': (735, 635, 1, 2, 5, 1, 0.2),
            'reroll_confirm_guest_account': (1068, 657, 1, 2, 5, 1, 0.2),
            'reroll_name': (940, 555, 1, 1, 5, 5, 0.2),
            'reroll_confirm': (940, 735, 4, 2, 5, 5, 0.2),
            'reroll_name_2': (960, 425, 1, 1, 10, 5, 0.2),
            'story_menu': (1810, 60, 1, 1, 10, 5, 0.2),
            'story_forward': (1815,175, 1, 1, 5, 5, 0.2),
            'first_battle_aoe': (1450, 430, 1, 1, 5, 5, 0.2),
            'second_battle_tank': (1710, 205, 1, 1, 10, 10, 0.2),
            'third_battle_enter': (1675, 360, 1, 2, 5, 5, 0.2),
            'third_battle_tile1': (775, 705, 1, 1, 5, 5, 0.2),
            'third_battle_tile2': (1013, 705, 1, 1, 5, 5, 0.2),
            'third_battle_tile3': (1146, 586, 1, 1, 5, 5, 0.2),
            'third_battle_to_lobby': (760, 987, 1, 2, 5, 5, 0.2),
            'reset_account': (1340, 643, 1, 1, 5, 5, 0.2),
            'reset_ba': (970, 510, 1, 1, 10, 5, 0.2),
            'students': (497, 970, 1, 3, 5, 5, 0.2),
            'students_first': (225, 430, 1, 5, 10, 10, 0.2),
            'students_levelup': (1408, 217, 1, 2, 10, 10, 0.2),
            'students_skillone': (1114, 555, 2, 2, 5, 5, 0.2),
            'students_skill_levelup': (1730, 550, 2, 2, 5, 5, 0.2),
            'students_sort': (1565, 180, 1, 1, 5, 5, 0.2),
            'students_sort_stars': (644, 255, 1, 1, 5, 5, 0.2),
            'students_sort_confirm': (1150, 855, 1, 1, 5, 5, 0.2),
            # Battle Generic
            'battle_skill_one': (1310, 930, 1, 1, 5, 5, 0.2),
            'battle_skill_two': (1480, 930, 1, 1, 5, 5, 0.2),
            'battle_start_mission': (1400, 800, 1, 1, 10, 5, 0.2),
            'battle_formation': (1805, 260, 1, 5, 5, 5, 0.2),
            'battle_formation_confirm': (1727, 894, 1, 5, 5, 5, 0.2),            
            'battle_confirm': (1750, 980, 1, 1, 5, 5, 0.2),
            'battle_auto': (1814, 1012, 1, 1, 5, 5, 0.2),
            'battle_rate_confirm': (950, 980, 1, 5, 5, 2, 0.2),
            'mission_complete_confirm': (1550, 988, 1, 3, 5, 5, 0.2),

        }

        self.s_coords = {
            'menu_acc_down': {
                'start': (970, 830),
                'stop': (970, 310),
                'duration': 500,
                'repeat': 2
            },
            'students_down': {
                'start': (960, 645),
                'stop': (960, 545),
                'duration': 500,
                'repeat': 1
            }
        }

        self.three_star_students = ['Aru', 'Eimi', 'Haruna', 'Hifumi', 'Hina', 'Hoshino', 'Iori', 'Maki', 'Neru', 'Izumi', 'Shiroko', 'Shun', 'Sumire', 'Tsurugi', 'Hibiki', 'Karin', 'Saya', 'Mashiro', 'Izuna', 'Aris', 'Midori', 'Cherino', 
'Yuzu', 'Azusa', 'Koharu', 'Azusa (Swimsuit)', 'Mashiro (Swimsuit)', 'Hifumi (Swimsuit)', 'Hina (Swimsuit)', 'Iori (Swimsuit)', 'Shiroko (Cycling)', 'Shun (Small)', 'Saya (Casual)', 'Neru (Bunny)', 'Karin (Bunny)', 'Asuna (Bunny)', 'Natsu', 'Hatsune Miku', 'Ako', 'Cherino (Hot Spring)', 'Chinatsu (Hot Spring)', 'Nodoka (Hot Spring)', 'Aru (New Year)', 'Mutsuki (New Year)', 'Serika (New Year)', 'Wakamo', 'Sena', 'Chihiro', 'Mimori', 'Ui', 'Hinata', 'Marina', 'Miyako', 'Saki', 'Miyu', 'Kaede', 'Iroha', 'Tsukuyo', 'Misaki', 'Hiyori', 'Atsuko', 'Wakamo (Swimsuit)', 'Nonomi (Swimsuit)', 'Hoshino (Swimsuit)', 'Izuna (Swimsuit)', 'Chise (Swimsuit)', 'Saori', 'Moe', 'Kazusa', 'Kokona', 'Utaha (Cheer Squad)', 'Noa', 'Akane (Bunny)', 'Yuuka (Track)', 'Mari (Track)', 'Himari', 'Shigure', 'Serina (Christmas)', 'Hanae (Christmas)', 'Haruna (New Year)', 'Fuuka (New Year)', 'Mine', 'Mika', 'Megu', 'Kanna', 'Sakurako', 'Toki', 'Nagisa', 'Koyuki', 'Kayoko (New Year)', 'Haruka (New Year)', 'Kaho', 'Aris (Maid)', 'Toki (Bunny)', 'Reisa', 'Rumi', 'Mina', 'Minori', 'Miyako (Swimsuit)', 'Saki (Swimsuit)']
        self.other_students = ['Akane', 'Chise', 'Akari', 'Hasumi', 'Nonomi', 'Kayoko', 'Mutsuki', 'Junko', 'Serika', 'Tsubaki', 'Yuuka', 'Haruka', 'Asuna', 'Kotori', 'Suzumi', 'Pina', 'Airi', 'Fuuka', 'Hanae', 'Hare', 'Utaha', 'Ayane', 'Chinatsu', 'Kotama', 'Juri', 'Serina', 'Shimiko', 'Yoshimi', 'Shizuko', 'Momoi', 'Nodoka', 'Hanako', 'Tsurugi (Swimsuit)', 'Izumi (Swimsuit)', 'Kirino', 'Mari', 'Tomoe', 'Fubuki', 'Michiru', 'Ayane (Swimsuit)', 'Shizuko (Swimsuit)', 'Hibiki (Cheer Squad)', 'Hasumi (Track)', 'Junko (New Year)', 'Yuzu (Maid)', 'Miyu (Swimsuit)']
        self.base_path = 'Users\Keane\Files\Scripts\Project BA'