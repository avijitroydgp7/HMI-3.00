from PyQt6.QtGui import QAction
import qtawesome as qta

class CommonMenu:
    """
    Creates the 'Common' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        common_menu = menu_bar.addMenu("&Common")

        # Environment Submenu
        environment_icon = qta.icon('fa5s.cogs', options=[{'color':'#5f6368'}])
        environment_menu = common_menu.addMenu(environment_icon, "Environment")
        environment_menu.addAction(QAction(qta.icon('fa5s.exchange-alt'), "Screen Switching", main_window))
        environment_menu.addAction(QAction(qta.icon('fa5s.window-restore'), "Dialog Window", main_window))
        environment_menu.addAction(QAction(qta.icon('fa5s.info-circle'), "System Information", main_window))
        environment_menu.addAction(QAction(qta.icon('fa5s.user-shield'), "Security", main_window))

        ethernet_icon = qta.icon('fa5s.network-wired', options=[{'color':'#4285f4'}])
        controller_icon = qta.icon('fa5s.gamepad', options=[{'color':'#5f6368'}])
        common_menu.addAction(QAction(ethernet_icon, "Ethernet", main_window))
        common_menu.addAction(QAction(controller_icon, "Controller Setting", main_window))

        # Peripheral Device Submenu
        peripheral_device_icon = qta.icon('fa5s.plug', options=[{'color':'#34a853'}])
        peripheral_device_menu = common_menu.addMenu(peripheral_device_icon, "Peripheral Device")
        peripheral_device_menu.addAction(QAction(qta.icon('fa5s.barcode'), "Barcode", main_window))
        peripheral_device_menu.addAction(QAction(qta.icon('fa5s.broadcast-tower'), "RFID", main_window))
        peripheral_device_menu.addAction(QAction(qta.icon('mdi6.axis-arrow'), "Servo", main_window))
        peripheral_device_menu.addAction(QAction(qta.icon('fa5s.robot'), "Robot", main_window))
        peripheral_device_menu.addAction(QAction(qta.icon('fa5s.camera-retro'), "Camera", main_window))

        common_menu.addSeparator()

        # Tags Submenu
        tags_icon = qta.icon('fa5s.tags', options=[{'color':'#34a853'}])
        tags_menu = common_menu.addMenu(tags_icon, "Tags")
        tags_menu.addAction(QAction(qta.icon('fa5s.folder-open'), "Open", main_window))
        tags_menu.addAction(QAction(qta.icon('fa5s.plus-circle'), "New", main_window))
        tags_menu.addAction(QAction(qta.icon('fa5s.plus'), "Add", main_window))
        tags_menu.addAction(QAction(qta.icon('fa5s.edit'), "Edit", main_window))
        tags_menu.addAction(QAction(qta.icon('fa5s.minus-circle'), "Remove", main_window))
        tags_menu.addAction(QAction(qta.icon('fa5s.file-import'), "Import", main_window))
        tags_menu.addAction(QAction(qta.icon('fa5s.file-export'), "Export", main_window))

        # Comment Submenu
        comment_icon = qta.icon('fa5s.comment-dots', options=[{'color':'#fbbc05'}])
        comment_menu = common_menu.addMenu(comment_icon, "Comment")
        comment_menu.addAction(QAction(qta.icon('fa5s.folder-open'), "Open", main_window))
        comment_menu.addAction(QAction(qta.icon('fa5s.plus-circle'), "New", main_window))
        comment_menu.addSeparator()
        comment_menu.addAction(QAction(qta.icon('mdi6.table-column-plus-after'), "Add Column", main_window))
        comment_menu.addAction(QAction(qta.icon('mdi6.table-row-plus-after'), "Add Row", main_window))
        comment_menu.addAction(QAction(qta.icon('mdi6.table-column-remove'), "Remove Column", main_window))
        comment_menu.addAction(QAction(qta.icon('mdi6.table-row-remove'), "Remove Row", main_window))
        comment_menu.addSeparator()
        comment_menu.addAction(QAction(qta.icon('fa5s.search'), "Find", main_window))
        style_submenu = comment_menu.addMenu(qta.icon('fa5s.paint-brush'), "Style")
        style_submenu.addAction(QAction(qta.icon('fa5s.bold'), "Bold", main_window))
        style_submenu.addAction(QAction(qta.icon('fa5s.italic'), "Italic", main_window))
        style_submenu.addAction(QAction(qta.icon('fa5s.underline'), "Underline", main_window))
        style_submenu.addAction(QAction(qta.icon('fa5s.fill-drip'), "Fill", main_window))

        # Alarm Submenu
        alarm_icon = qta.icon('fa5s.bell', options=[{'color':'#ea4335'}])
        alarm_menu_common = common_menu.addMenu(alarm_icon, "Alarm")
        alarm_menu_common.addAction(QAction(qta.icon('fa5s.user-clock'), "User Alarm", main_window))
        alarm_menu_common.addAction(QAction(qta.icon('fa5s.cog'), "System Alarm", main_window))
        alarm_menu_common.addAction(QAction(qta.icon('fa5s.window-restore'), "Popup Alarm", main_window))

        logging_icon = qta.icon('fa5s.file-medical-alt', options=[{'color':'#4285f4'}])
        common_menu.addAction(QAction(logging_icon, "Logging..", main_window))
        common_menu.addSeparator()
        script_icon = qta.icon('fa5s.code', options=[{'color':'#5f6368'}])
        tags_data_transfer_icon = qta.icon('fa5s.exchange-alt', options=[{'color':'#4285f4'}])
        trigger_action_icon = qta.icon('fa5s.bolt', options=[{'color':'#fbbc05'}])
        time_action_icon = qta.icon('fa5s.clock', options=[{'color':'#4285f4'}])
        common_menu.addAction(QAction(script_icon, "Script", main_window))
        common_menu.addAction(QAction(tags_data_transfer_icon, "Tags Data Transfer", main_window))
        common_menu.addAction(QAction(trigger_action_icon, "Trigger Action..", main_window))
        common_menu.addAction(QAction(time_action_icon, "Time Action..", main_window))

