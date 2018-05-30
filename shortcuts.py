# -*- coding: utf-8 -*-
"""
Description:    creates a shortcut using AutoHotKey syntax. It creates a file
                for each shortcut entry from the user and activates the
                process.
                It adds the shortcut to a database and saves it to a json file
                for later retrieval. It also deletes shortcuts, checks argument
                input and present a message accordingly.

name:           Elad Hayek
date:           2.2.18
file name:      shortcuts.py
"""
import subprocess
import os
from Tkinter import *
import tkFileDialog
import wx
import pickle
import tkMessageBox
import getpass
import copy

CLOSE_PROCESS_BY_NAME_PATH = 'close_process.ahk'

HOT_KEYS_PROGRAM_PATH = 'AutoHotkey.exe'

SCRIPTS_PATH = r'C:\Users\%s\AppData\Roaming' \
               r'\Microsoft\Windows\Start Menu\Programs\Startup'


HOT_KEYS_TEMPLATE = """#NoTrayIcon
~*{5}::
if GetKeyState("{0}") & GetKeyState("{1}") & GetKeyState("{2}")
 & GetKeyState("{3}")& GetKeyState("{4}")"""

ACTIONS_WITHOUT_OPEN = ['shutdown', 'restart']


class ShortCuts:
    def __init__(self):
        """
        creates a user profile for the program
        """
        self.__argument = GetArgument()
        self.__remote_computer_activation = False
        self.__add_open = 'open '
        self.__shortcut_sequence = ''
        self.__computer_name = ''
        self.__shortcut_script_path = ''
        self.__shortcuts_templates = {'restart': 'Shutdown, 2 %s',
                                      'shutdown': 'Shutdown, 1 %s',
                                      'open folder': 'Run, %s',
                                      'open url': 'Run, chrome.exe %s',
                                      'open settings': 'Run, control %s',
                                      'open cmd': 'Run, cmd %s',
                                      'open file': 'Run, %s',
                                      'open connection to activate'
                                      ' remote shortcut':
                                      'Run, python activate_remote_data.py'
                                      ' "{0}" "{1}" "{2}"'}

        self.__current_shortcuts = {'open folder': {}, 'open url': {},
                                    'open file': {}, 'open cmd': {},
                                    'open settings': {}, 'shutdown': {},
                                    'restart': {}}

        self.__files_ending_counter = {'folder': 0, 'url': 0, 'file': 0,
                                       'cmd': 0, 'settings': 0, 'shutdown': 0,
                                       'restart': 0}

        self.__user_choice = ''

        self.__shortcut_function_activation = {'open folder': self.open_folder,
                                               'open url': self.open_url,
                                               'open settings':
                                               self.open_settings,
                                               'open cmd': self.open_cmd,
                                               'open file': self.open_file,
                                               'shutdown': self.shutdown,
                                               'restart': self.restart}

    def restart(self):
        """
        uses the run_action_sequence_for_shortcut to restart the computer
        """
        self.run_action_sequence_for_shortcut('restart')

# -----------------------------------------------------------------------------
    def shutdown(self):
        """
        uses the run_action_sequence_for_shortcut to shutdown the computer
        """
        self.run_action_sequence_for_shortcut('shutdown')

# -----------------------------------------------------------------------------
    def open_folder(self):
        """
        uses the run_action_sequence_for_shortcut to open a folder shortcut
        """
        if not self.__remote_computer_activation:
            self.__argument.choose_folder_manager()
        if self.__argument.get_argument():
            if self.__remote_computer_activation:
                if self.__argument.get_argument().split('$$')[1]:
                    self.run_action_sequence_for_shortcut('folder')
            else:
                self.run_action_sequence_for_shortcut('folder')

# -----------------------------------------------------------------------------
    def open_url(self):
        """
        uses the run_action_sequence_for_shortcut to open a URL shortcut
        """
        if not self.__remote_computer_activation:
            self.__argument.ask_text_from_user('open url')
        if self.__argument.get_argument():
            if self.__remote_computer_activation:
                if self.__argument.get_argument().split('$$')[1]:
                    self.run_action_sequence_for_shortcut('url')
            else:
                self.run_action_sequence_for_shortcut('url')

# -----------------------------------------------------------------------------
    def open_settings(self):
        """
        uses the run_action_sequence_for_shortcut to open a control panel
        shortcut
        """
        self.run_action_sequence_for_shortcut('settings')

# -----------------------------------------------------------------------------
    def open_cmd(self):
        """
        uses the run_action_sequence_for_shortcut to open a cmd shortcut
        """
        self.run_action_sequence_for_shortcut('cmd')

# -----------------------------------------------------------------------------
    def open_file(self):
        """
        uses the run_action_sequence_for_shortcut to open a file shortcut
        """
        if not self.__remote_computer_activation:
            self.__argument.choose_file_manager()
        if self.__argument.get_argument():
            if self.__remote_computer_activation:
                if self.__argument.get_argument().split('$$')[1]:
                    self.run_action_sequence_for_shortcut('file')
            else:
                self.run_action_sequence_for_shortcut('file')

# -----------------------------------------------------------------------------
    def get_shortcut_sequence(self):
        """
        returns the last entered shortcut sequence
        """
        return self.__shortcut_sequence

# -----------------------------------------------------------------------------
    def set_remote_computer_activation_flag(self, state):
        """
        sets the remote activation flag to true or false

        :arg state = the state of the flag (true or false)
        :type state = bool
        """
        self.__remote_computer_activation = state

# -----------------------------------------------------------------------------
    def set_users_choice(self, choice):
        """
        sets the users choice of action

        :arg choice = the action the user chose
        :type choice = string
        """
        self.__user_choice = choice

# -----------------------------------------------------------------------------
    def get_users_choice(self):
        """
        returns the action the user chose
        """
        return self.__user_choice

# -----------------------------------------------------------------------------
    def set_shortcut_sequence(self, user_sequence):
        """
        sets the shortcut sequence

        :arg user_sequence = the sequence the user entered
        :type user_sequence = string
        """
        self.__shortcut_sequence = user_sequence
        self.__shortcut_sequence = self.__shortcut_sequence.split('+')

# -----------------------------------------------------------------------------
    def set_shortcut_argument(self, argument):
        """
        sets the user argument

        :arg argument = the user shortcut argument
        :type argument = string
        """
        self.__argument.set_argument(argument)

# -----------------------------------------------------------------------------
    def run_action_sequence_for_shortcut(self, shortcut_type):
        """
        run the series of action to create a shortcut file and activate the
        shortcut

        :arg shortcut_type = the action the user chose
        :type shortcut_type = string

        """
        self.__shortcut_script_path =\
            SCRIPTS_PATH+'\\'+self.__computer_name+'_'+shortcut_type+str(
                self.__files_ending_counter[shortcut_type])+'.ahk'

        self.__shortcut_script_path = self.__shortcut_script_path % getpass.\
            getuser()
        print self.__shortcut_script_path
        ahk_file = open(self.__shortcut_script_path, 'w')

        if shortcut_type in ACTIONS_WITHOUT_OPEN:
            self.__add_open = ''
        ahk_file.write(self.write_to_file(self.__add_open+shortcut_type))
        ahk_file.close()

        self.activate_ahk_files(self.__shortcut_script_path)

        self.add_to_history(self.__add_open+shortcut_type,
                            self.__computer_name+'_'+shortcut_type+str(
                                self.__files_ending_counter[
                                    shortcut_type])+'.ahk')

        self.__files_ending_counter[shortcut_type] += 1
        self.__add_open = 'open '

# -----------------------------------------------------------------------------

    def write_new_shortcut(self, computer_name, computer_current_shortcuts,
                           computer_files_ending_counter, argument=''):
        """
        activate the correct shortcut function from the actions dictionary

        :arg computer_name = the chosen computer name
        :type computer_name = string

        :arg computer_current_shortcuts = the dictionary with the computer
        current shortcuts information.
        :type computer_current_shortcuts = dictionary

        :arg computer_files_ending_counter = the dictionary with the file
        ending counters.
        :type computer_files_ending_counter = dictionary

        :arg argument = the remote argument that was added by user or added
        remotely.
        :type argument = string
        """
        if argument:
            self.__remote_computer_activation = True
            self.set_shortcut_argument(argument)
        else:
            self.__remote_computer_activation = False
        self.__files_ending_counter = copy.deepcopy(
            computer_files_ending_counter)
        self.__current_shortcuts = copy.deepcopy(computer_current_shortcuts)
        self.__computer_name = computer_name
        self.__shortcut_function_activation[self.__user_choice]()
        self.set_shortcut_argument('')

# -----------------------------------------------------------------------------

    def write_to_file(self, shortcut_name):
        """
        returns the string of AutoHotKey syntax to write the shortcut

        :arg shortcut_name = the action the user chose
        :type shortcut_name = string
        """

        sequence_format_list = self.check_sequence_length()
        if self.__computer_name == 'My Computer' and not\
                self.__remote_computer_activation:
                # for shortcuts manually written by the user to my computer
            string_to_write = HOT_KEYS_TEMPLATE.format(
                *sequence_format_list)+'\n{'+self.__shortcuts_templates[
                    shortcut_name] % self.__argument.get_argument() + '\n}'

        elif self.__computer_name == 'My Computer' and\
                self.__remote_computer_activation:
                # for shortcuts that been written remotely to my computer
            string_to_write = HOT_KEYS_TEMPLATE.format(
                *sequence_format_list)+'\n{'+self.__shortcuts_templates[
                    shortcut_name] % self.__argument.get_argument().split(
                        '$$')[1] + '\n}'

        else:  # for shortcuts that the user wrote for remote computer
            string_to_write = HOT_KEYS_TEMPLATE.format(
                *sequence_format_list)+'\n{'+self.__shortcuts_templates[
                    'open connection to activate remote shortcut'].format(
                        *self.__argument.get_argument().split('$$')) + '\n}'
        return string_to_write

# -----------------------------------------------------------------------------

    def check_sequence_length(self):
        """
        checks the user sequence entry and return a list with all the keys
        """
        sequence_format_list = self.__shortcut_sequence[:]

    # if the sequence is shorter than 6 fill the blanks with the last letter
        if len(sequence_format_list) < 6:
            for i in range(6-len(sequence_format_list)):
                sequence_format_list.append(sequence_format_list[-1])

        return sequence_format_list
# -----------------------------------------------------------------------------

    def delete_shortcut(self, shortcut_type, file_name,
                        computer_current_shortcuts):
        """
        deletes a shortcut file and end it's process

        :arg shortcut_type = the action the user chose
        :type shortcut_type = string

        :arg file_name = the shortcut file name
        :type file_name = string

        :arg computer_current_shortcuts = the dictionary with the computer
        current shortcuts information.
        :type computer_current_shortcuts = dictionary
        """
        self.__current_shortcuts = computer_current_shortcuts
        file_to_delete = self.__current_shortcuts[shortcut_type][file_name][2]
        self.activate_ahk_files(CLOSE_PROCESS_BY_NAME_PATH, file_name)
        os.remove(file_to_delete)
        self.__current_shortcuts[shortcut_type].__delitem__(file_name)
# -----------------------------------------------------------------------------

    def get_current_shortcuts(self):
        """
        returns the current shortcuts dictionary
        """
        return self.__current_shortcuts

# -----------------------------------------------------------------------------
    def get_file_ending_counter(self):
        """
        returns the files ending counters dictionary
        """
        return self.__files_ending_counter

# -----------------------------------------------------------------------------

    def activate_ahk_files(self, file_path, argument=''):
        """
        activates ahk files with subprocess

        :arg file_path = the shortcut file path
        :type file_path = string

        :arg argument = the argument for the subprocess
        :type argument = string
        """
        subprocess.Popen([HOT_KEYS_PROGRAM_PATH, file_path, argument])
# -----------------------------------------------------------------------------

    def add_to_history(self, shortcut_type, file_name):
        """
        adds a shortcut to the current shortcuts dictionary

        :arg shortcut_type = the action the user chose
        :type shortcut_type = string

        :arg file_name = the shortcut file name
        :type file_name = string
        """
        if self.__remote_computer_activation:
            if self.__argument.get_argument().split('$$')[1] == ';;':
                self.__argument.set_argument('')
            else:
                self.__argument.set_argument(
                    self.__argument.get_argument().split('$$')[1])

        self.__current_shortcuts[shortcut_type][file_name] = (
            self.__argument.get_argument(), self.__shortcut_sequence,
            self.__shortcut_script_path)


class GetArgument:
    def __init__(self):
        self.___argument = ''

# -----------------------------------------------------------------------------
    def ask_text_from_user(self, action, marks=''):
        """
        opens a text dialog for argument entry from user

        :arg action = the action the user chose
        :type action = string

        :arg marks = additional marks for the user
        :type marks = string
        """

        frame = wx.Frame(None, -1, action)
        frame.SetDimensions(0, 0, 200, 50)

        # Create text input
        dlg = wx.TextEntryDialog(frame,
                                 'Enter '+action.split()[1].upper()+'\n'+marks,
                                 'Text Entry')
        if dlg.ShowModal() == wx.ID_OK:
            self.___argument = dlg.GetValue()
            dlg.Destroy()
            self.___argument = dlg.GetValue()
        else:
            self.___argument = ''
            dlg.Destroy()
            self.___argument = dlg.GetValue()

# -----------------------------------------------------------------------------
    def open_error_dialog(self, error):
        """
        opens an error message

        :arg error = the desired error message
        :type error = string
        """
        root = Tk()
        root.withdraw()
        tkMessageBox.showerror("Error", error)

# -----------------------------------------------------------------------------
    def choose_folder_manager(self):
        """
        opens a folders manager for the user to choose a folder
        """
        root = Tk()
        root.withdraw()
        root.filename = tkFileDialog.askdirectory(mustexist=True, parent=root,
                                                  initialdir='/',
                                                  title='Select a folder')
        self.___argument = root.filename
        self.___argument = root.filename

# -----------------------------------------------------------------------------
    def choose_file_manager(self):
        """
        opens a files manager for the user to choose a file
        """
        root = Tk()
        root.withdraw()
        root.filename = tkFileDialog.askopenfilename(initialdir="/",
                                                     title="Select file")
        self.___argument = root.filename
        self.___argument = root.filename

# -----------------------------------------------------------------------------
    def get_argument(self):
        """
        returns the user chosen argument
        """
        return self.___argument

# -----------------------------------------------------------------------------
    def set_argument(self, argument):
        """
        sets the user argument

        :arg argument = the user shortcut argument
        :type argument = string
        """
        self.___argument = argument


def main():
    pass


if __name__ == '__main__':
    main()
