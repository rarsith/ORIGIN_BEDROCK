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
