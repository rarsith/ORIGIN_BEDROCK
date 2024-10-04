hover_orange = """
           QPushButton {
               border: none;
               background: transparent;
           }
           QPushButton:pressed {
               background: 8px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
           }
           QPushButton:hover {
               border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
               background: transparent;
           }
       """