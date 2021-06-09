light = """
            QWidget {
                background: none;
            }
             QPushButton {
                background-color: #ff4f00;
                color: black;
                font-family:"Times";
              font-weight: 600;
            }
             QLineEdit{
                 background-color: none; 
                 font-family:"Times";
              font-weight: 600;
            }
            QHeaderView::section{
            color:black;
            font-family:"Times";
              font-weight: 600;
            }
             QTableWidget{
                 background-color:None;
                 color: black;
                 font-family:"Times";
              font-weight: 600;
             }
             QTableWidgetItem{color: none;
             font-family:"Times";
              font-weight: 600;}
             QListWidget{color: none;
             font-family:"Times";
              font-weight: 600;}
             QGroupBox{color: none;
             font-family:"Times";
              font-weight: 600;}
             QTabWidget{
                color: black;
                transform:rotate(90deg);
                height:200;
                font-family:"Times";
              font-weight: 600;
             }
             QLabel{color: none;
             font-family:"Times";
              font-weight: 600;}
             QTabBar{color: none;font-size: 200%;
             font-family:"Times";
              font-weight: 600;}
             QComboBox{color: none;
             font-family:"Times";
              font-weight: 600;}
             """

dark = """QMenu {
            border: 1px solid #a5a5a5;
            color:#a5a5a5;
        }
        QMenuBar{color:#a5a5a5;
            background-color: #ff4f00;}
        QWidget {
            background: #2c3337;
        }
        QPushButton {
            background-color: #ff4f00;
            color: #181513;
        }
        QLineEdit{
            background-color: white;
            font-family:"Times";
              font-weight: 600; 
        }
        QTableWidget{
            background-color:#2c3337;
            color: #a5a5a5;
            font-family:"Times";
              font-weight: 600;
        }
        QHeaderView::section{
            color: #a5a5a5;
            font-family:"Times";
              font-weight: 600;
        }
        QTableWidgetItem{color: #a5a5a5;
            font-family:"Times";
              font-weight: 600;}
        QListWidget{color: #a5a5a5;
            font-family:"Times";
              font-weight: 600;}
        QGroupBox{color: #a5a5a5;}
        QTabWidget{
            border: 1px solid #a5a5a5;
            color: #a5a5a5;
            font-family:"Times";
              font-weight: 600;
        }
        QLabel{color:#a5a5a5}
        QTabBar{color: #a5a5a5;
            width: 400px;
            height: 1000px;
            font-family:"Times";
              font-weight: 600;}
        QComboBox{color:#a5a5a5;
            font-family:"Times";
              font-weight: 600;} 
        QPushButton {
              height: 50;
              font-family:"Times";
              font-weight: 600;
          }
           QLineEdit{
               height: 40;
               margin-top:1;
              margin-bottom:1;
          }
          QLabel{
              color:#a5a5a5;
              margin-left:9;
              margin-top:0;
              margin-bottom:0;
              font-size: 200%;
          }
           """


def color_theme():
    arr = []
    for line in open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt'):
        arr.append(line)
    theme = arr[8].split()
    if theme[2] == 'dark':
        set_theme = dark
    if theme[2] == 'light':
        set_theme = light
    return set_theme


def update_color_theme(value):
    arr = []
    for line in open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt'):
        arr.append(line)
    with open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt', 'r') as f:
        old_data = f.read()
    new_data = old_data.replace(arr[8], 'Color-theme = ' + value + '\n')
    with open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt', 'w') as f:
        f.write(new_data)
    return 0


def auto_input():
    arr = []
    for line in open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt'):
        arr.append(line)
    wt = arr[3].split()
    return wt[2]


def auto_output(value):
    arr = []
    for line in open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt'):
        arr.append(line)
    with open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt', 'r') as f:
        old_data = f.read()
    new_data = old_data.replace(arr[3], 'auto_in = ' + str(value) + '\n')
    with open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt', 'w') as f:
        f.write(new_data)
    return 0

def start_set():
    arr = []
    for line in open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt'):
        arr.append(line)
    index = arr[9].split()
    return int(index[2])

def update_start_set(value):
    arr = []
    for line in open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt'):
        arr.append(line)
    with open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt', 'r') as f:
        old_data = f.read()
    new_data = old_data.replace(arr[4], 'address = ' + value[0] + '\n')
    with open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt', 'w') as f:
        f.write(new_data)

    for line in open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt'):
        arr.append(line)
    with open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt', 'r') as f:
        old_data = f.read()
    new_data_1 = old_data.replace(arr[5], 'address = ' + value[1] + '\n')
    with open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt', 'w') as f:
        f.write(new_data_1)

    for line in open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt'):
        arr.append(line)
    with open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt', 'r') as f:
        old_data = f.read()
    new_data_2 = old_data.replace(arr[6], 'address = ' + value[2] + '\n')
    with open('C:/Users/HP-15/Desktop/Project_kurs/settings/config.txt', 'w') as f:
        f.write(new_data_2)
    return 0
