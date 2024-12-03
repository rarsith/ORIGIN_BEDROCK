def match_color_scheme(status_input):
    states = {
        'WIP': '''
            QPushButton {
                background-color: #BBCB0F;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8; 
            }
        ''',
        'IN PROGRESS': '''
            QPushButton {
                background-color: #80ccff;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'PENDING REVIEW': '''
            QPushButton {
                background-color: #ffc266;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'TWEAK': '''
            QPushButton {
                background-color: #db70b8;
                color: black;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'IGNORE': '''
            QPushButton {
                background-color: #bfbfbf;
                color: #595959;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'REJECTED': '''
            QPushButton {
                background-color: #c86851;
                color: #d9d9d9;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'INTERNAL APPROVED': '''
            QPushButton {
                background-color: #99cc00;
                color: #404040;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        ''',
        'CLIENT APPROVED': '''
            QPushButton {
                background-color: #00802b;
                color: #333333;
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
                background-color: #e6e600;
                color: #0d0d0d;
            }
            QPushButton:checked {
                border: 3px solid #a6fff8;
            }
        '''
    }

    return states.get(status_input)
