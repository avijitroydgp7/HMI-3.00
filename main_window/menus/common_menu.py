# main_window\menus\common_menu.py
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QSpinBox
from ..services.icon_service import IconService

class CommonMenu:
    """
    Creates the 'Common' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        common_menu = menu_bar.addMenu("&Common")

        # Environment Submenu
        environment_icon = IconService.get_icon('common-environment')
        environment_menu = common_menu.addMenu(environment_icon, "Environment")
        environment_menu.addAction(QAction(IconService.get_icon('common-screen-switching'), "Screen Switching", main_window))
        environment_menu.addAction(QAction(IconService.get_icon('common-dialog-window'), "Dialog Window", main_window))
        environment_menu.addAction(QAction(IconService.get_icon('common-system-information'), "System Information", main_window))
        environment_menu.addAction(QAction(IconService.get_icon('common-security'), "Security", main_window))

        ethernet_icon = IconService.get_icon('common-ethernet')
        controller_icon = IconService.get_icon('common-controller-setting')
        common_menu.addAction(QAction(ethernet_icon, "Ethernet", main_window))
        common_menu.addAction(QAction(controller_icon, "Controller Setting", main_window))

        # Peripheral Device Submenu
        peripheral_device_icon = IconService.get_icon('common-peripheral-device')
        peripheral_device_menu = common_menu.addMenu(peripheral_device_icon, "Peripheral Device")
        peripheral_device_menu.addAction(QAction(IconService.get_icon('common-barcode'), "Barcode", main_window))
        peripheral_device_menu.addAction(QAction(IconService.get_icon('common-rfid'), "RFID", main_window))
        peripheral_device_menu.addAction(QAction(IconService.get_icon('common-servo'), "Servo", main_window))
        peripheral_device_menu.addAction(QAction(IconService.get_icon('common-robot'), "Robot", main_window))
        peripheral_device_menu.addAction(QAction(IconService.get_icon('common-camera'), "Camera", main_window))

        common_menu.addSeparator()

        # Tags Submenu
        tags_icon = IconService.get_icon('common-tags')
        tags_menu = common_menu.addMenu(tags_icon, "Tags")
        tags_menu.addAction(QAction(IconService.get_icon('common-folder-open'), "Open", main_window))
        tags_menu.addAction(QAction(IconService.get_icon('common-new'), "New", main_window))
        tags_menu.addAction(QAction(IconService.get_icon('common-add'), "Add", main_window))
        tags_menu.addAction(QAction(IconService.get_icon('common-edit'), "Edit", main_window))
        tags_menu.addAction(QAction(IconService.get_icon('common-remove'), "Remove", main_window))
        tags_menu.addAction(QAction(IconService.get_icon('common-import'), "Import", main_window))
        tags_menu.addAction(QAction(IconService.get_icon('common-export'), "Export", main_window))

        # Comment Submenu
        comment_icon = IconService.get_icon('common-comment')
        self.comment_menu = common_menu.addMenu(comment_icon, "Comment")
        self.comment_menu.addAction(QAction(IconService.get_icon('common-folder-open'), "Open", main_window))
        self.comment_menu.addAction(QAction(IconService.get_icon('common-new'), "New", main_window))
        self.comment_menu.addAction(QAction(IconService.get_icon('common-import'), "Import", main_window))
        self.comment_menu.addAction(QAction(IconService.get_icon('common-export'), "Export", main_window))
        self.comment_menu.addSeparator()

        self.add_column_action = QAction(IconService.get_icon('common-add-column'), "Add Column", main_window)
        self.comment_menu.addAction(self.add_column_action)
        self.add_row_action = QAction(IconService.get_icon('common-add-row'), "Add Row", main_window)
        self.comment_menu.addAction(self.add_row_action)
        self.remove_column_action = QAction(IconService.get_icon('common-remove-column'), "Remove Column", main_window)
        self.comment_menu.addAction(self.remove_column_action)
        self.remove_row_action = QAction(IconService.get_icon('common-remove-row'), "Remove Row", main_window)
        self.comment_menu.addAction(self.remove_row_action)

        self.comment_menu.addSeparator()
        self.find_action = QAction(IconService.get_icon('common-find'), "Find", main_window)
        self.comment_menu.addAction(self.find_action)

        style_submenu = self.comment_menu.addMenu(IconService.get_icon('common-style'), "Style")
        self.bold_action = QAction(IconService.get_icon('common-bold'), "Bold", main_window)
        self.italic_action = QAction(IconService.get_icon('common-italic'), "Italic", main_window)
        self.underline_action = QAction(IconService.get_icon('common-underline'), "Underline", main_window)
        self.fill_text_action = QAction(IconService.get_icon('common-edit'), "Fill Text", main_window)
        self.fill_background_action = QAction(IconService.get_icon('common-fill'), "Fill Background", main_window)
        style_submenu.addAction(self.bold_action)
        style_submenu.addAction(self.italic_action)
        style_submenu.addAction(self.underline_action)
        style_submenu.addAction(self.fill_text_action)
        style_submenu.addAction(self.fill_background_action)


        # Alarm Submenu
        alarm_icon = IconService.get_icon('common-alarm')
        alarm_menu_common = common_menu.addMenu(alarm_icon, "Alarm")
        alarm_menu_common.addAction(QAction(IconService.get_icon('common-user-alarm'), "User Alarm", main_window))
        alarm_menu_common.addAction(QAction(IconService.get_icon('common-system-alarm'), "System Alarm", main_window))
        alarm_menu_common.addAction(QAction(IconService.get_icon('common-popup-alarm'), "Popup Alarm", main_window))

        logging_icon = IconService.get_icon('common-logging')
        common_menu.addAction(QAction(logging_icon, "Logging..", main_window))
        common_menu.addSeparator()
        script_icon = IconService.get_icon('common-script')
        tags_data_transfer_icon = IconService.get_icon('common-tags-data-transfer')
        trigger_action_icon = IconService.get_icon('common-trigger-action')
        time_action_icon = IconService.get_icon('common-time-action')
        common_menu.addAction(QAction(script_icon, "Script", main_window))
        common_menu.addAction(QAction(tags_data_transfer_icon, "Tags Data Transfer", main_window))
        common_menu.addAction(QAction(trigger_action_icon, "Trigger Action..", main_window))
        common_menu.addAction(QAction(time_action_icon, "Time Action..", main_window))