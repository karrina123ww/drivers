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
        self.pushButton_filter.clicked.connect(self.filter_data)  # Новая кнопка фильтрации
        
        self.pushButton_load.setStyleSheet("background-color: #ADD8E6;")
        self.pushButton_sort.setStyleSheet("background-color: #D8BFD8;")
        self.pushButton_delete.setStyleSheet("background-color: #ff9999;") 
        self.pushButton_edit.setStyleSheet("background-color: #ffff99;")   
        self.pushButton_save.setStyleSheet("background-color: #99ff99;")  
        self.pushButton_add.setStyleSheet("background-color: #ffcc99;")
        self.pushButton_filter.setStyleSheet("background-color: #c2c2f0;")  # Стиль для кнопки фильтрации
        
        # Инициализируем список для хранения данных
        self.drivers_data = []
        self.filtered_data = None  # Для хранения отфильтрованных данных
        
    def load_data(self):
        try:
            with open('drivers.txt', 'r', encoding='utf-8') as file:
                self.drivers_data = [line.strip().split(';') for line in file.readlines()]
            self.filtered_data = None  # Сбрасываем фильтр при загрузке новых данных
            self.update_table()
            QMessageBox.information(self, 'Успех', 'Данные успешно загружены!')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {str(e)}')
    
    def update_table(self):
        data = self.filtered_data if self.filtered_data is not None else self.drivers_data
        self.tableWidget.setRowCount(len(data))
        for row, driver in enumerate(data):
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
            data_to_sort = self.filtered_data if self.filtered_data is not None else self.drivers_data
            data_to_sort.sort(key=lambda x: x[col])
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
            if self.filtered_data is not None:
                # Удаляем из основного списка, найдя соответствующую запись
                filtered_item = self.filtered_data[selected_row]
                for i, item in enumerate(self.drivers_data):
                    if item == filtered_item:
                        del self.drivers_data[i]
                        break
                self.filtered_data.remove(filtered_item)
            else:
                del self.drivers_data[selected_row]
            self.update_table()
    
    def edit_data(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите строку для редактирования!')
            return
        
        data_source = self.filtered_data if self.filtered_data is not None else self.drivers_data
        driver = data_source[selected_row]
        items = ['ФИО', 'Год рождения', 'Марка авто', 'Год выпуска', 'Госномер']
        item, ok = QInputDialog.getItem(self, 'Редактирование', 'Выберите поле для редактирования:', items, 0, False)
        
        if ok and item:
            col = items.index(item)
            new_value, ok = QInputDialog.getText(self, 'Редактирование', 
                                               f'Введите новое значение для "{items[col]}":', 
                                               QLineEdit.Normal, driver[col])
            if ok and new_value:
                # Обновляем данные в основном списке, если работаем с отфильтрованными данными
                if self.filtered_data is not None:
                    for i, item in enumerate(self.drivers_data):
                        if item == driver:
                            self.drivers_data[i][col] = new_value
                            break
                    self.filtered_data[selected_row][col] = new_value
                else:
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
        self.filtered_data = None  # Сбрасываем фильтр при добавлении новых данных
        self.update_table()
    
    def filter_data(self):
        if not self.drivers_data:
            QMessageBox.warning(self, 'Предупреждение', 'Нет данных для фильтрации!')
            return
        
        items = ['ФИО', 'Год рождения', 'Марка авто', 'Год выпуска', 'Госномер']
        item, ok = QInputDialog.getItem(self, 'Фильтрация', 'Выберите поле для фильтрации:', items, 0, False)
        
        if ok and item:
            col = items.index(item)
            filter_value, ok = QInputDialog.getText(self, 'Фильтрация', 
                                                  f'Введите значение для фильтрации по "{items[col]}":')
            if ok:
                if filter_value:
                    self.filtered_data = [driver for driver in self.drivers_data 
                                        if filter_value.lower() in driver[col].lower()]
                    self.update_table()
                    QMessageBox.information(self, 'Фильтрация', 
                                         f'Найдено {len(self.filtered_data)} записей.')
                else:
                    self.filtered_data = None
                    self.update_table()
                    QMessageBox.information(self, 'Фильтрация', 'Фильтр сброшен.')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DriversApp()
    window.show()
    sys.exit(app.exec_())