ICO = 'beauty_logo.ico'
# ICO_UI = '../beauty_logo.ico'

WINDOW_STYLE_ID = 'win'
MAIN_STYLE = '''
        #win{
        background-color:white;
        }
        QPushButton{
            height:45px;
            width: 100%;
            background-color: rgb(225, 228, 255);
            font-size: 25px;
            border-radius:20px;
            font-weight:bold;
            font-style:'Tahoma'
        }
        QPushButton:hover{
            color: white;;
            background-color: rgb(255, 74, 109);
        }
         QPushButton:pressed{
            color:black;
        }
        '''
RADIO_STYLE = '''
           QRadioButton::indicator {
               width:10px;
               height:10px;
               border: 1 px solid red;
               border-radius: 7px;
           }

           QRadioButton::indicator:checked {
               background-color:blue;
               border:2px solid blue;     
           }

           QRadioButton::indicator:unchecked {
               background-color:gray; 
               border: 2px solid gray; 
           }'''
