import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                               QTextEdit, QMessageBox, QFrame, QStackedWidget)
from PySide6.QtCore import Qt, QTimer, QDateTime, QSize
from PySide6.QtGui import QIcon, QPixmap, QFontDatabase, QFont

class KlippekGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Klippek v0.0.1")
        self.setGeometry(50, 50, 1200, 800)
        
        font_id = QFontDatabase.addApplicationFont("LexendDecaFont.ttf")
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                self.custom_font_family = font_families[0]
        else:
            self.custom_font_family = "Arial"  
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #181820;")
        
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 10, 0, 10)
        self.main_layout.setSpacing(4)
        

        top_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_pixmap = QPixmap("mainlogo.png")
        scaled_logo = logo_pixmap.scaled(255, 255, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_logo)
        logo_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        logo_label.setStyleSheet("margin-left: 14px;")
        top_layout.addWidget(logo_label)
        
        top_layout.addStretch()
        top_layout.setAlignment(Qt.AlignVCenter)
        
        self.datetime_label = QLabel()
        self.datetime_label.setStyleSheet(f"color: #FFC24D; font-size: 32px; margin-right: 14px; font-family: '{self.custom_font_family}';")
        self.datetime_label.setContentsMargins(0, 0, 0, 0)
        self.datetime_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_layout.addWidget(self.datetime_label)
        self.main_layout.addLayout(top_layout)
        self.update_datetime()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: white;")
        line.setFixedHeight(4)
        self.main_layout.addWidget(line)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        
        sidebar = QWidget()
        sidebar.setStyleSheet("background-color: #181820;")
        sidebar.setFixedWidth(115)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 50, 10, 50)
        sidebar_layout.setSpacing(25)
        sidebar_layout.setAlignment(Qt.AlignHCenter)
       
        button_style = """
            QPushButton {
                background-color: #181820;
                border: 2px solid #181820;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #3a3a44;
                border: 2px solid #4a4a54;
            }
            QPushButton:pressed {
                background-color: #1c1c24;
            }
        """

        self.home_button = QPushButton()
        self.home_button.setIcon(QIcon("homebutton.png"))
        self.home_button.setIconSize(QSize(75, 75))
        self.home_button.setFixedSize(75, 75)
        self.home_button.setStyleSheet(button_style)
        self.home_button.clicked.connect(self.show_home_page)
        sidebar_layout.addWidget(self.home_button)
        
        clip_button = QPushButton()
        clip_button.setIcon(QIcon("clipbutton.png"))
        clip_button.setIconSize(QSize(75, 75))
        clip_button.setFixedSize(75, 75)
        clip_button.setStyleSheet(button_style)
        clip_button.clicked.connect(self.button_clicked)
        sidebar_layout.addWidget(clip_button)
        
        button3 = QPushButton()
        button3.setIcon(QIcon("rewardbutton.png"))
        button3.setIconSize(QSize(75, 75))
        button3.setFixedSize(75, 75)
        button3.setStyleSheet(button_style)
        button3.clicked.connect(self.button_clicked)
        sidebar_layout.addWidget(button3)
        
        button4 = QPushButton()
        button4.setIcon(QIcon("statsbutton.png"))
        button4.setIconSize(QSize(75, 75))
        button4.setFixedSize(75, 75)
        button4.setStyleSheet(button_style)
        button4.clicked.connect(self.button_clicked)
        sidebar_layout.addWidget(button4)
        
        button5 = QPushButton()
        button5.setIcon(QIcon("socialbutton.png"))
        button5.setIconSize(QSize(75, 75))
        button5.setFixedSize(75, 75)
        button5.setStyleSheet(button_style)
        button5.clicked.connect(self.button_clicked)
        sidebar_layout.addWidget(button5)
        
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon("settingsbutton.png"))
        self.settings_button.setIconSize(QSize(75, 75))
        self.settings_button.setFixedSize(75, 75)
        self.settings_button.setStyleSheet(button_style)
        self.settings_button.clicked.connect(self.show_settings_page)
        sidebar_layout.addWidget(self.settings_button)
        
        sidebar_layout.addStretch()
        content_layout.addWidget(sidebar)
        
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #181820;")
        
        
        self.home_page = self.create_home_page()
        self.stacked_widget.addWidget(self.home_page)
        
        
        self.settings_page = self.create_settings_page()
        self.stacked_widget.addWidget(self.settings_page)
        
        content_layout.addWidget(self.stacked_widget)
        self.main_layout.addLayout(content_layout)
    
    def create_home_page(self):
        main_content = QWidget()
        main_content.setStyleSheet("background-color: #181820;")
        main_content_layout = QHBoxLayout(main_content)
        main_content_layout.setContentsMargins(20, 20, 20, 20)
        main_content_layout.setSpacing(20)
        
        box_style = """
            QFrame {
                background-color: #2a2a34;
                border: 2px solid #3a3a44;
                border-radius: 15px;
            }
        """
        
        
        box1 = QFrame()
        box1.setStyleSheet(box_style)
        box1_layout = QVBoxLayout(box1)
        box1_layout.setContentsMargins(20, 20, 20, 20)
        
        box1_label = QLabel("Activity")
        box1_label.setStyleSheet(f"color: white; font-size: 29px; font-weight: bold; font-family: '{self.custom_font_family}'; background-color: transparent; border: none;")
        box1_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        box1_layout.addWidget(box1_label)
        box1_layout.addStretch()
        box1_button = QPushButton("Add More Friends!")
        box1_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #665b6a;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                font-family: '{self.custom_font_family}';
            }}
            QPushButton:hover {{
                background-color: #FFD580;
            }}
            QPushButton:pressed {{
                background-color: #E6A020;
            }}
        """)
        box1_button.setFixedWidth(200)
        box1_button.clicked.connect(self.button_clicked)
        box1_layout.addWidget(box1_button, alignment=Qt.AlignCenter)
        
        
        box2 = QFrame()
        box2.setStyleSheet(box_style)
        box2_layout = QVBoxLayout(box2)
        box2_layout.setContentsMargins(20, 20, 20, 20)
        
        box2_label = QLabel("Recent Clips")
        box2_label.setStyleSheet(f"color: white; font-size: 29px; font-weight: bold; font-family: '{self.custom_font_family}'; background-color: transparent; border: none;")
        box2_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        box2_layout.addWidget(box2_label)
        for i in range(10):
            row = QFrame()
            if i % 2 == 0:
                row.setStyleSheet("background-color: #3a3a44; border: none; border-radius: 0px;")
            else:
                row.setStyleSheet("background-color: #4c4551; border: none; border-radius: 0px;")
            row.setFixedHeight(50)
            box2_layout.addWidget(row)
            box2_layout.setSpacing(0)
        box2_layout.addStretch()
        
        box2_button = QPushButton("See all clips")
        box2_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #665b6a;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                font-family: '{self.custom_font_family}';
            }}
            QPushButton:hover {{
                background-color: #FFD580;
            }}
            QPushButton:pressed {{
                background-color: #E6A020;
            }}
        """)
        box2_button.setFixedWidth(200)
        box2_button.clicked.connect(self.button_clicked)
        box2_layout.addWidget(box2_button, alignment=Qt.AlignCenter)
        
        main_content_layout.addWidget(box1, 35)  
        main_content_layout.addWidget(box2, 65)  
        
        return main_content
    
    def create_settings_page(self):
        settings_widget = QWidget()
        settings_widget.setStyleSheet("background-color: #181820;")
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setContentsMargins(40, 40, 40, 40)
        settings_layout.setSpacing(30)
        
    

        box_style = """
            QFrame {
                background-color: #2a2a34;
                border: 2px solid #3a3a44;
                border-radius: 15px;
            }
        """
        main_box = QFrame()
        main_box.setStyleSheet(box_style)
        main_box_layout = QVBoxLayout(main_box)
        main_box_layout.setContentsMargins(30, 30, 30, 30)
        main_box_layout.setSpacing(30)

        main_box_layout.addStretch()
        
        settings_layout.addWidget(main_box)
        return settings_widget


    
    def show_home_page(self):
        self.stacked_widget.setCurrentIndex(0)
        print("Home Button Pressed")
    
    def show_settings_page(self):
        self.stacked_widget.setCurrentIndex(1)
        print("Settings Button Pressed")
    
    def button_clicked(self):
        print("Button Pressed")
    
    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime() 
        formatted_time = current_datetime.toString("HH:mm - d/MM/yyyy")
        self.datetime_label.setText(formatted_time)

def main():
    app = QApplication(sys.argv)
    window = KlippekGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()