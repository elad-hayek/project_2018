# -*- coding: utf-8 -*-
import sys
import os

class ActivateShortcuts():
    def __init__(self):
        self.__action = ''
        self.__argument = ''
        self.__remote_shortcut_activation = {'open folder': self.open_folder, 'open url': self.open_url, 'open program': self.open_program, 'open cmd': self.open_cmd, 'open settings': self.open_settings}

    def open_folder(self):
        os.system(self.__argument[:2]+' && cd '+self.__argument+' && start.')

    def open_url(self):
        pass

    def open_program(self):
        pass

    def open_cmd(self):
        pass

    def open_settings(self):
        pass

    def set_action(self, action):
        self.__action = action

    def set_argument(self, argument):
        self.__argument = argument

    def activate_action(self):
        self.__remote_shortcut_activation[self.__action]()


def main():
    activate_shortcut = ActivateShortcuts()
    activate_shortcut.set_action(sys.argv[1])
    print sys.argv[:]
    if sys.argv[2]:
        activate_shortcut.set_argument(sys.argv[2])
    activate_shortcut.activate_action()



if __name__ == '__main__':
    main()