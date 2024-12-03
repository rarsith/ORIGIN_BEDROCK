def match_color_scheme(status_input):
    states = {
        "WIP": "background-color: #ffff00; color: black;",
        "IN PROGRESS": "background-color: #94c4ff; color: black;",
        "PENDING REVIEW": "background-color: #98eeff; color: black;",
        "TWEAK": "background-color: #c898ff; color: black;",
        "IGNORE": "background-color: #d1d1d1; color: #595959;",
        "REJECTED": "background-color: #ff2020; color: #ffffff;",
        "INTERNAL APPROVED": "background-color: #00ff46; color: #404040;",
        "CLIENT APPROVED": "background-color: #009c2b; color: #ffffff;",
        "READY TO DELIVER": "background-color: #00802b; color: #333333;",
        "TEMP APPROVED": "background-color: #b0ffb2; color: #0d0d0d;",

        'READY TO START': 'background-color: #ffbd00;',
        'COMPLETED': 'background-color: #148300; color: #ffffff;',
        'OMITTED': 'background-color: #936E94; color: black;',
        'ON HOLD': 'background-color: #A41A1A; color: black;',
        'NOT STARTED': 'background-color: #636363; color: #A8A8A8;',

        "LOW": "background-color: #ADC01E; color: black;",
        "MEDIUM": "background-color: #20A8C9; color: black;",
        "HIGH": "background-color: #C12020; color: black;",
        "NORMAL": "background-color: #8D8D8D; color: black;",
        "CRITICAL": "background-color: #880000; color: #FFFFFF;"
    }
    return states.get(status_input)
