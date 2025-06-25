import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QInputDialog, QLineEdit


class DriversApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(DriversApp, self).__init__()
        uic.loadUi('drivers.ui', self)
        
        # Подключаем кнопки к функциям
        self.pushButton_load.clicked.connect(self.load_data)
        self.pushButton_sort.clicked.connect(self.sort_data)
        self.pushButton_delete.clicked.connect(self.delete_data)
        self.pushButton_edit.clicked.connect(self.edit_data)
        self.pushButton_save.clicked.connect(self.save_data)
        self.pushButton_add.clicked.connect(self.add_data)
        
        self.pushButton_load.setStyleSheet("background-color: #ADD8E6;")
        self.pushButton_sort.setStyleSheet("background-color: #D8BFD8;")
        self.pushButton_delete.setStyleSheet("background-color: #ff9999;") 
        self.pushButton_edit.setStyleSheet("background-color: #ffff99;")   
        self.pushButton_save.setStyleSheet("background-color: #99ff99;")  
        self.pushButton_add.setStyleSheet("background-color: #ffcc99;")  
        # Инициализируем список для хранения данных
        self.drivers_data = []
        
    def load_data(self):
        try:
            with open('drivers.txt', 'r', encoding='utf-8') as file:
                self.drivers_data = [line.strip().split(';') for line in file.readlines()]
            self.update_table()
            QMessageBox.information(self, 'Успех', 'Данные успешно загружены!')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {str(e)}')
    
    def update_table(self):
        self.tableWidget.setRowCount(len(self.drivers_data))
        for row, driver in enumerate(self.drivers_data):
            for col, value in enumerate(driver):
                self.tableWidget.setItem(row, col, QTableWidgetItem(value))
    
    def sort_data(self):
        if not self.drivers_data:
            QMessageBox.warning(self, 'Предупреждение', 'Нет данных для сортировки!')
            return
        
        items = ['ФИО', 'Год рождения', 'Марка авто', 'Год выпуска', 'Госномер']
        item, ok = QInputDialog.getItem(self, 'Сортировка', 'Выберите поле для сортировки:', items, 0, False)
        
        if ok and item:
            col = items.index(item)
            self.drivers_data.sort(key=lambda x: x[col])
            self.update_table()
    
    def delete_data(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите строку для удаления!')
            return
        
        reply = QMessageBox.question(self, 'Подтверждение', 
                                    'Вы уверены, что хотите удалить эту запись?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            del self.drivers_data[selected_row]
            self.update_table()
    
    def edit_data(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите строку для редактирования!')
            return
        
        driver = self.drivers_data[selected_row]
        items = ['ФИО', 'Год рождения', 'Марка авто', 'Год выпуска', 'Госномер']
        item, ok = QInputDialog.getItem(self, 'Редактирование', 'Выберите поле для редактирования:', items, 0, False)
        
        if ok and item:
            col = items.index(item)
            new_value, ok = QInputDialog.getText(self, 'Редактирование', 
                                               f'Введите новое значение для "{items[col]}":', 
                                               QLineEdit.Normal, driver[col])
            if ok and new_value:
                self.drivers_data[selected_row][col] = new_value
                self.update_table()
    
    def save_data(self):
        try:
            with open('drivers.txt', 'w', encoding='utf-8') as file:
                for driver in self.drivers_data:
                    file.write(';'.join(driver) + '\n')
            QMessageBox.information(self, 'Успех', 'Данные успешно сохранены!')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить данные: {str(e)}')
    
    def add_data(self):
        fio, ok = QInputDialog.getText(self, 'Добавление', 'Введите ФИО:')
        if not ok or not fio:
            return
        
        birth_year, ok = QInputDialog.getText(self, 'Добавление', 'Введите год рождения:')
        if not ok or not birth_year:
            return
        
        car_brand, ok = QInputDialog.getText(self, 'Добавление', 'Введите марку авто:')
        if not ok or not car_brand:
            return
        
        car_year, ok = QInputDialog.getText(self, 'Добавление', 'Введите год выпуска авто:')
        if not ok or not car_year:
            return
        
        license_plate, ok = QInputDialog.getText(self, 'Добавление', 'Введите госномер:')
        if not ok or not license_plate:
            return
        
        self.drivers_data.append([fio, birth_year, car_brand, car_year, license_plate])
        self.update_table()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DriversApp()
    window.show()
    sys.exit(app.exec_())