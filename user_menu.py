# -*- coding: utf-8 -*-

from shortcuts import ShortCuts
import wx
import shortcut_menu_wx_skeleton

SPECIAL_CHARACTERS_SYMBOLS = [['Windows', '#'], ['Alt', '!'], ['Control', '^'], ['Shift', '+']]
SHORTCUT_OPTIONS = ['open folder', 'open url', 'open program', 'open cmd', 'open settings']
SHORTCUT_GRID_LABELS = {0: 'Action', 1: 'Argument', 2: 'Sequence'}


class Main(shortcut_menu_wx_skeleton.MainFrame):
    #constructor
    def __init__(self, parent):
        shortcut_menu_wx_skeleton.MainFrame.__init__(self, parent)
        self.__shortcuts_user = ShortCuts()

#-------------------------------------------------------------------------------
    def add_new_shortcut_menu(self, event):
        self.new_shortcut_panel.Show()
        self.main_panel.Hide()
        self.current_shortcuts_panel.Hide()
        self.add_special_characters_to_the_add_table()
        self.add_options_to_shortcut_list()

#-------------------------------------------------------------------------------
    def add_new_shortcut_to_the_list(self, event):
        self.__shortcuts_user.write_new_shortcut()

#-------------------------------------------------------------------------------
    def save_user_choice(self, event):
        print SHORTCUT_OPTIONS[self.shortcuts_choices.GetSelection()]
        self.__shortcuts_user.set_users_choice(SHORTCUT_OPTIONS[self.shortcuts_choices.GetSelection()])

#-------------------------------------------------------------------------------
    def add_special_characters_to_the_add_table(self):
        self.buttons_mapping_list.DeleteAllItems()
        for special_character in SPECIAL_CHARACTERS_SYMBOLS:
            self.buttons_mapping_list.AppendItem(special_character)

#-------------------------------------------------------------------------------
    def add_options_to_shortcut_list(self):
        if self.shortcuts_choices.IsEmpty():
            for shortcut in SHORTCUT_OPTIONS:
                self.shortcuts_choices.Append(shortcut)

#-------------------------------------------------------------------------------
    def check_sequence_input(self, event):
        self.__shortcuts_user.set_shortcut_sequence(self.sequence_text_control.GetValue())
        print self.sequence_text_control.GetValue()

#===============================================================================
    def show_current_shortcuts_menu(self, event):
        self.main_panel.Hide()
        self.current_shortcuts_panel.Show()
        self.new_shortcut_panel.Hide()
        self.change_shortcut_grid_labels()
        self.add_shortcuts_to_shortcut_grid()

#-------------------------------------------------------------------------------
    def change_shortcut_grid_labels(self):
        for key in SHORTCUT_GRID_LABELS:
            self.computer_shortcuts_grid.SetColLabelValue(key, SHORTCUT_GRID_LABELS[key])

#-------------------------------------------------------------------------------
    def add_shortcuts_to_shortcut_grid(self):
        print self.__shortcuts_user.get_current_shortcuts()
        row = 0
        for key in self.__shortcuts_user.get_current_shortcuts():
            col = 0
            if self.__shortcuts_user.get_current_shortcuts()[key]:
                for file_name in self.__shortcuts_user.get_current_shortcuts()[key]:
                    self.computer_shortcuts_grid.SetCellValue(row, col, key)
                    col += 1
                    argument = self.__shortcuts_user.get_current_shortcuts()[key][file_name][0]
                    self.computer_shortcuts_grid.SetCellValue(row, col, argument)
                    col += 1
                    sequence = '+'.join(self.__shortcuts_user.get_current_shortcuts()[key][file_name][1])
                    self.computer_shortcuts_grid.SetCellValue(row, col, sequence)
                    row += 1
                    col = 0

#===============================================================================
    def go_to_home_panel(self, event):
        self.main_panel.Show()
        self.current_shortcuts_panel.Hide()
        self.new_shortcut_panel.Hide()





def main():
    app = wx.App(False)

    #create an object of CalcFrame
    frame = Main(None)
    #show the frame
    frame.Show(True)
    #start the applications
    app.MainLoop()

if __name__ == '__main__':
    main()