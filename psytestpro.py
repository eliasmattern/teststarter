import os.path
import webbrowser
import tkinter as tk

# mac os can't initialise Tk after the imports of the components / views.  starts tk before pygame is initialised
tk_root = tk.Tk()
tk_root.withdraw()
import pygame
import sys
from pygame.locals import *
from datetime import datetime, timedelta
from components import InputBox, Button
from views import CreateScheduleDisplay, SuiteConfig, SettingsView
import re
from services import TranslateService, LanguageConfiguration, PsyTestProConfig, get_resource_path
import pandas as pd


class PsyTestPro:
    def __init__(self, id: str = '', suite: str = '', time: str = '', custom_variables: dict = {}):
        self.screen = pygame.display.get_surface()
        if self.screen == None:
            try:
                pygame.init()
                self.screen = pygame.display.set_mode((0, 0))
                pygame.display.toggle_fullscreen()
            except pygame.error as e:
                print(f"Pygame fullscreen toggle error: {e}")
                # Alternative method to set fullscreen
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                print("Fullscreen mode set using alternative method")

        self.width, self.height = pygame.display.get_surface().get_rect().size
        pygame.display.set_caption('PsyTestPro')
        app_icon = pygame.image.load(get_resource_path('./img/logo.png'))
        pygame.display.set_icon(app_icon)
        pygame.scrap.init()
        self.psyTestProConfig = PsyTestProConfig()
        self.psyTestProConfig.load_suites()
        self.lang = 'en'
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.input_boxes: dict[str, InputBox] = {}
        self.buttons: list[Button] = []
        self.errors = []
        self.language_config = LanguageConfiguration()
        self.translateService = TranslateService(self.language_config)
        self.lang = self.load_config_language()
        self.id = id
        self.suite = suite
        self.time = time
        self.custom_variables = []
        self.custom_variables_dict = custom_variables
        for key, value in custom_variables.items():
            self.custom_variables.append(value)
        self.suite_config_display = SuiteConfig(self.translateService)
        self.create_input_boxes()
        self.is_running = True
        self.start_time = None
        self.settings_view = SettingsView()
        self.settings = self.psyTestProConfig.get_settings()
        self.background_color = pygame.Color(self.settings['backgroundColor'])
        self.primary_color = pygame.Color(self.settings['primaryColor'])
        self.inactive_button_color = pygame.Color(self.settings['inactiveButtonColor'])
        self.button_text_color = pygame.Color(self.settings["buttonTextColor"])
        self.button_color = pygame.Color(self.settings["buttonColor"])
        self.logo_image = pygame.image.load(get_resource_path('./img/logo.png'))

        while self.is_running:
            self.handle_events()
            self.clear_screen()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def is_valid_time_format(slef, datetime_str: str):
        # This pattern strictly matches DD/MM/YYYY HH:MM:SS
        pattern = r'^(?:[01]\d|2[0-3]):[0-5]\d$'
        return re.match(pattern, datetime_str) is not None

    def create_input_boxes(self):
        custom_variables = self.psyTestProConfig.load_custom_variables()
        labels = ['participantId', 'suite', 'startTime']
        suite_string = ''

        for suite in self.psyTestProConfig.suites:
            suite_string = suite_string + str(suite) + ', '
        if ',' in suite_string:
            suite_string = suite_string[:-2]

        information = ['', '(' + suite_string + ')', 'hh:mm']
        initial_text = [self.id, self.suite, self.time]
        if len(self.custom_variables) == len(custom_variables):
            for value in custom_variables:
                labels.append(value)
                information.append('')
            for variable in self.custom_variables:
                initial_text.append(variable)
        else:
            for value in custom_variables:
                labels.append(value)
                information.append('')
                initial_text.append('')
        x = self.width // 2
        y = self.height // 2 - 100
        spacing = 60
        for label, text, info in zip(labels, initial_text, information):
            if len(self.input_boxes) > 2:
                input_box = InputBox(x, y, 400, 40, label, None, '', text, desc=label + ' ' + info)
                self.input_boxes[label] = input_box
            else:
                input_box = InputBox(x, y, 400, 40, label, self.translateService, '', text,
                                     desc=self.translateService.get_translation(label) + ' ' + info)
                self.input_boxes[label] = input_box
            y += spacing

        exit_button = Button(x - 75, y + 60, 100, 40, 'exit', self.exit, self.translateService)
        submit_button = Button(x + 75, y + 60, 100, 40, 'submit', self.save_details, self.translateService)
        settings_button = Button(self.width - 175, 100, 250, 40, 'settings',
                                 lambda: self.show_settings_screen(),
                                 self.translateService)
        create_suite_button = Button(self.width - 175, 150, 250, 40, 'configureTestBattery',
                                          lambda: self.configure_test_battery(),
                                          self.translateService)

        self.buttons.append(exit_button)
        self.buttons.append(settings_button)
        self.buttons.append(create_suite_button)
        self.buttons.append(submit_button)

    def load_config_language(self):
        self.language_config.read_language_config()
        language = self.language_config.get_language()
        if len(language) > 0:
            self.translateService.set_language(language)
            self.lang = language

    def change_language(self, lang: str):
        self.errors.clear()
        self.translateService.set_language(lang)
        self.language_config.update_language_config(lang)

    def handle_events(self):
        def get_input_index(step):
            custom_variables = self.psyTestProConfig.load_custom_variables()
            index_to_key = {0: 'participantId', 1: 'suite', 2: 'startTime'}
            key_to_index = {'participantId': 0, 'suite': 1, 'startTime': 2}
            count = 3
            for value in custom_variables:
                index_to_key[count] = value
                key_to_index[value] = count
                count += 1
            index = 0
            for key, input_box in self.input_boxes.items():
                if input_box.is_selected:
                    self.input_boxes[key].is_selected = False
                    index = key_to_index[key] + step
                    break
            if 0 <= index < len(self.input_boxes):
                return index_to_key[index]
            elif index < 0:
                return index_to_key[len(self.input_boxes) - 1]
            else:
                return index_to_key[0]

        for event in pygame.event.get():
            for key, box in self.input_boxes.items():
                box.handle_event(event)
            for button in self.buttons:
                button.handle_event(event)
            if event.type == KEYDOWN:
                mods = pygame.key.get_mods()
                if mods != 4097 and event.key == K_TAB:
                    index = get_input_index(1)
                    self.input_boxes[index].is_selected = True
                elif mods & mods == 4097 and event.key == K_TAB:  # Check if Sjhift is pressed
                    index = get_input_index(-1)
                    self.input_boxes[index].is_selected = True
                elif event.key == K_BACKSPACE:
                    pass
                elif event.key == K_RETURN:
                    if self.buttons[3].is_active:
                        self.save_details()
            elif event.type == pygame.MOUSEBUTTONUP and self.logo_image.get_rect().collidepoint(event.pos):
                if event.button == 1:
                    webbrowser.open('https://github.com/eliasmattern/PsyTestPro')
            else:
                if len(self.input_boxes.get('startTime').text) == 1 and self.input_boxes.get(
                        'startTime').text.isnumeric() and 2 < int(self.input_boxes.get('startTime').text) < 10:
                    self.input_boxes.get('startTime').text = '0' + self.input_boxes.get('startTime').text
                if len(self.input_boxes.get('startTime').text) == 2 and self.input_boxes.get(
                        'startTime').text[1].isnumeric() and int(self.input_boxes.get(
                    'startTime').text) > 23:
                    self.input_boxes.get('startTime').text = self.input_boxes.get('startTime').text[0]
                if len(self.input_boxes.get('startTime').text) == 3:
                    if self.input_boxes.get('startTime').text[2] != ":":
                        self.input_boxes.get('startTime').text = self.input_boxes.get('startTime').text[
                                                                 :2] + ':' + self.input_boxes.get('startTime').text[
                                                                             2:3]
                if len(self.input_boxes.get('startTime').text) > 5:
                    self.input_boxes.get('startTime').text = self.input_boxes.get('startTime').text[:5]
                if len(self.input_boxes.get('startTime').text) == 4:
                    if self.input_boxes.get('startTime').text[3].isnumeric() and int(
                            self.input_boxes.get('startTime').text[3]) >= 6:
                        self.input_boxes.get('startTime').text = self.input_boxes.get('startTime').text[
                                                                 :3] + '0' + self.input_boxes.get('startTime').text[
                                                                             3:4]
                self.input_boxes.get('startTime').text = re.sub("[^0-9:]", "",
                                                                self.input_boxes.get('startTime').text)

    def clear_screen(self):
        self.screen.fill(self.background_color)

    def draw(self):
        def validate_inputs(suites: list):
            is_id_valid = len(self.input_boxes['participantId'].text) != 0
            is_suite_valid = self.input_boxes['suite'].text in suites
            is_start_time_valid = self.is_valid_time_format(self.input_boxes['startTime'].text)

            # Define validation checks and corresponding error messages
            index_to_key = {0: 'participantId', 1: 'suite', 2: 'startTime'}

            custom_variables = self.psyTestProConfig.load_custom_variables()
            count = 3
            for value in custom_variables:
                index_to_key[count] = value
                count += 1
            if self.input_boxes['participantId'].text and self.input_boxes['suite'].text and self.input_boxes[
                'startTime'].text:
                validation_checks = [
                    (lambda text: len(text) != 0, 'idError'),
                    (lambda text: text in suites, 'suiteError'),
                    (self.is_valid_time_format, 'startTimeError')
                ]

                for validation_check, error_key in validation_checks:
                    is_valid = validation_check(
                        self.input_boxes[index_to_key[validation_checks.index((validation_check, error_key))]].text)

                    error_translation = self.translateService.get_translation(error_key)
                    if not is_valid and error_translation not in self.errors:
                        self.errors.append(error_translation)
                    elif is_valid and error_translation in self.errors:
                        self.errors.remove(error_translation)

            if is_id_valid and is_suite_valid and is_start_time_valid:
                return True
            else:
                return False

        y = self.height // 2 - 200
        x = self.width // 2

        font = pygame.font.Font(None, int(64))
        text_surface = font.render(self.translateService.get_translation('psytestpro'), True, self.primary_color)
        text_rect = text_surface.get_rect()
        self.screen.blit(text_surface, (x - text_rect.width // 2, y))
        self.screen.blit(self.logo_image, (20, 20))

        for key, box in self.input_boxes.items():
            box.draw(self.screen)

        is_input_valid = validate_inputs(self.psyTestProConfig.suites)

        for button in self.buttons:
            button.draw(self.screen)

        if is_input_valid:
            self.buttons[3].set_active(True)
            self.buttons[3].set_color(self.button_color)
        else:
            self.buttons[3].set_active(False)
            self.buttons[3].set_color(self.inactive_button_color)

        if self.psyTestProConfig.error_msg == '':
            for item in self.errors:
                if self.translateService.get_translation('experimentNotFound') in item:
                    self.errors.remove(item)
        else:
            is_in_errors = False
            for item in self.errors:
                if self.translateService.get_translation('experimentNotFound') in item:
                    is_in_errors = True
            if not is_in_errors:
                self.errors.append(self.translateService.get_translation('experimentNotFound'))

        if len(self.errors) > 0:
            font = pygame.font.Font(None, 24)
            x = self.width // 2
            y = self.height - font.get_linesize() - font.get_linesize() * len(self.errors)

            for error in self.errors:
                text_surface = font.render(error, True, pygame.Color('red'))
                self.screen.blit(text_surface, (x - text_surface.get_rect().width // 2, y))
                y += font.get_linesize()

    def exit(self):
        self.is_running = False

    def custom_sort(self, item):
        return datetime.strptime(item[1]['datetime'], '%d/%m/%Y %H:%M:%S')

    def start_suite(self, start_time: datetime, participant_info: dict, custom_variables: dict):
        global schedule
        isHab = '_list' in self.psyTestProConfig.current_suite
        schedule = {}
        current_tasks = self.psyTestProConfig.current_tasks
        if len(self.psyTestProConfig.error_msg) > 0:
            return
        tasks = []
        types = {}
        values = {}
        positions = {}
        times: list[str] = []
        states = {}
        sorted_tasks = sorted(current_tasks.items(), key=lambda item: item[1]['position'])

        current_tasks = {k: v for k, v in sorted_tasks}

        for task, details in current_tasks.items():
            tasks.append(task)
            times.append(details['time'])
            states[task] = details['state']
            positions[task] = details['position']
            types[task] = details['type'] if 'type' in details else ''
            values[task] = details['value'] if 'value' in details else ''
        previous_time = start_time
        for i, _ in enumerate(times):
            exp_variable = tasks[i]
            if times[i - 1]:
                activation_time = previous_time + timedelta(hours=int(times[i - 1].split(':')[0]),
                                                            minutes=int(
                                                                times[i - 1].split(':')[1])) if i > 0 else start_time
                previous_time = activation_time
                schedule[exp_variable] = activation_time.strftime('%d/%m/%Y %H:%M:%S')

        edited_schedule = {}
        for key, value in schedule.items():
            edited_schedule.update(
                {key: {'datetime': value, 'state': states[key], 'type': types[key], 'value': values[key],
                       'position': positions[key]}})

        schedule = dict(sorted(edited_schedule.items(), key=self.custom_sort))
        for _, task in schedule.items():
            if datetime.strptime(task['datetime'], '%d/%m/%Y %H:%M:%S') < datetime.now():
                task['state'] = 'skip'

        file_name = self.save_suite_info(participant_info)

        CreateScheduleDisplay(schedule, participant_info, PsyTestPro, custom_variables, isHab, file_name).display()
        self.input_boxes = {}

    def save_details(self):
        participant_id = self.input_boxes['participantId'].text
        suite = self.input_boxes['suite'].text
        start_time = self.input_boxes['startTime'].text

        start_time = datetime.combine(datetime.now().date(), datetime.strptime(start_time, '%H:%M').time())
        current_time = datetime.now()

        timestamp = current_time.strftime("%Y.%m.%d %H:%M:%S")
        participant_info = {'participant_id': participant_id, 'suite': suite, 'start_time': start_time,
                            'timestamp': timestamp}

        custom_variables = self.psyTestProConfig.load_custom_variables()

        variables = {}

        for value in custom_variables:
            participant_info[value] = self.input_boxes[value].text
            variables[value] = self.input_boxes[value].text

        self.psyTestProConfig.load_suite_tasks(suite)
        self.start_suite(start_time, participant_info, variables)

    def save_suite_info(self, participant_info: dict[str, str]):
        if not os.path.exists(get_resource_path('./logs')):
            os.makedirs(get_resource_path('./logs'))
        table = {}
        names = []
        values = []
        for key, value in participant_info.items():
            names.append(key)
            values.append(value)

        table['info'] = names
        table['value'] = values

        datetime_string = str(participant_info['start_time'])

        filename = participant_info['participant_id'] + '_' + participant_info[
            'suite'] + '_' + datetime_string + '_log' + '.xlsx'
        filename = filename.replace(' ', '_')
        filename = filename.replace('-', '_')
        filename = filename.replace(':', '_')
        df = pd.DataFrame(data=table)
        df.to_excel(get_resource_path('./logs/' + filename), index=False)
        return filename

    def show_settings_screen(self):
        participant_id = self.input_boxes['participantId'].text
        suite = self.input_boxes['suite'].text
        start_time = self.input_boxes['startTime'].text
        custom_variables = self.psyTestProConfig.load_custom_variables()

        variables = {}

        for value in custom_variables:
            variables[value] = self.input_boxes[value].text

        self.settings_view.display(PsyTestPro, self.translateService,
                                   self.language_config, participant_id, suite,
                                   start_time, variables)

    def configure_test_battery(self):
        old_custom_variables = self.psyTestProConfig.load_custom_variables()

        self.suite_config_display.display(PsyTestPro)
        old_experiements = self.psyTestProConfig.suites

        self.psyTestProConfig.load_suites()
        custom_variables = self.psyTestProConfig.load_custom_variables()

        if old_experiements != self.psyTestProConfig.suites or custom_variables != old_custom_variables:
            self.buttons = []
            self.input_boxes = {}
            self.create_input_boxes()


PsyTestPro()
