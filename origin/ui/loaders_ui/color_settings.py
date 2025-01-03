import os


def match_color_scheme(status_input):
    states = {
        'WIP': '''
            QPushButton {
                background-color: #ffff00;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8; 
            }
        ''',
        'IN PROGRESS': '''
            QPushButton {
                background-color: #94c4ff;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'PENDING REVIEW': '''
            QPushButton {
                background-color: #98eeff;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'TWEAK': '''
            QPushButton {
                background-color: #c898ff;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'IGNORE': '''
            QPushButton {
                background-color: #d1d1d1;
                color: #595959;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'REJECTED': '''
            QPushButton {
                background-color: #ff2020;
                color: #ffffff;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'INTERNAL APPROVED': '''
            QPushButton {
                background-color: #00ff46;
                color: #404040;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'CLIENT APPROVED': '''
            QPushButton {
                background-color: #009c2b;
                color: #ffffff;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'READY TO DELIVER': '''
            QPushButton {
                background-color: #00802b;
                color: #333333;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'TEMP APPROVED': '''
            QPushButton {
                background-color: #b0ffb2;
                color: #0d0d0d;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        '''
    }

    return states.get(status_input)


def match_color_status_scheme(widget_type, status_input):
    states = {
        'WIP': '''
            QPushButton {
                background-color: #ffff00;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8; 
            }
        ''',
        'IN PROGRESS': '''
            QPushButton {
                background-color: #94c4ff;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'PENDING REVIEW': '''
            QPushButton {
                background-color: #98eeff;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'TWEAK': '''
            QPushButton {
                background-color: #c898ff;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'IGNORE': '''
            QPushButton {
                background-color: #d1d1d1;
                color: #595959;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'REJECTED': '''
            QPushButton {
                background-color: #ff2020;
                color: #ffffff;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'INTERNAL APPROVED': '''
            QPushButton {
                background-color: #00ff46;
                color: #404040;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'CLIENT APPROVED': '''
            QPushButton {
                background-color: #009c2b;
                color: #ffffff;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'READY TO DELIVER': '''
            QPushButton {
                background-color: #00802b;
                color: #333333;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'TEMP APPROVED': '''
            QPushButton {
                background-color: #b0ffb2;
                color: #0d0d0d;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        '''
    }

    selected_style = states.get(status_input)
    widget_update = selected_style.replace("QPushButton", widget_type)

    return widget_update


def match_icon_status_scheme(status_input):
    get_dev_path = os.getenv("ORIGIN_ROOT")
    status_icons_path = os.path.join(get_dev_path, "origin/icons/statuses_icons")
    normalized_path = os.path.normpath(status_icons_path)

    states = {'WIP': 'wip','INTERNAL APPROVED': 'internal_approved','PENDING REVIEW': 'pending_review'}

    selected_icon = states.get(status_input)
    icon_full_path = os.path.join(normalized_path, f"{selected_icon}.png")

    return icon_full_path
