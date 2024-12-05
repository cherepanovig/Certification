import os
import csv
import time


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    # def load_prices(self, folder_path='docs'):
    def load_prices(self, folder_path=os.path.abspath("docs")):  # Абсолютный путь к "docs"
        """
        Загружает данные из CSV файлов в папке docs.
        Обрабатывает ошибки чтения файлов и неправильный формат данных.
        """
        for filename in os.listdir(folder_path):  # Перебираем файлы в папке
            if 'price' in filename.lower():  # Приводим имя файла к ниж.регистру и проверяем наличие 'price' в имени
                file_path = os.path.join(folder_path, filename)  # Полный путь к файлу
                try:  # Обработка ошибок при открытии и чтении файла
                    with open(file_path, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=',')  # Читаем CSV как словарь где ключи — это
                        # названия столбцов, а значения — это соответствующие данные из каждой строки
                        headers = reader.fieldnames  # Получаем названия столбцов
                        # print(headers)
                        product_col, price_col, weight_col = self._search_product_price_weight(
                            headers)  # Ищем нужные столбцы
                        if not all([product_col, price_col, weight_col]):  # Проверяем наличие всех нужных столбцов
                            print(f"Пропускаем файл {filename}: Отсутствуют необходимые столбцы.")
                            continue  # Переходим к следующему файлу
                        for row in reader:  # Перебираем строки в файле
                            try:  # Обработка ошибок в строке
                                product_name = row[product_col]  # Название продукта
                                price = float(row[price_col])  # Цена (преобразуем в число)
                                weight = float(row[weight_col])  # Вес (преобразуем в число)
                                price_per_kg = round(price / weight, 2)  # Цена за кг, округляем до 2 знаков
                                self.data.append({  # Добавляем данные в список
                                    'name': product_name,
                                    'price': price,
                                    'weight': weight,
                                    'file': filename,
                                    'price_per_kg': price_per_kg
                                })
                                # print(self.data)
                            except (ValueError, KeyError) as e:  # Обрабатываем ошибки типа данных и ключей
                                print(f"Ошибка обработки строки в {filename}: {e}. Пропускаем строку.")
                except Exception as e:  # Обрабатываем другие ошибки файла
                    print(f"Ошибка обработки файла {filename}: {e}")
        return self

    def _search_product_price_weight(self, headers):
        """
        Возвращает названия столбцов с названием продукта, ценой и весом.
        """
        product_col = None
        price_col = None
        weight_col = None

        product_names = ['товар', 'название', 'наименование', 'продукт']
        price_names = ['розница', 'цена']
        weight_names = ['вес', 'масса', 'фасовка']

        for header in headers:  # Перебираем названия столбцов
            if header.lower() in product_names:  # Ищем столбец с названием продукта
                product_col = header
            elif header.lower() in price_names:  # Ищем столбец с ценой
                price_col = header
            elif header.lower() in weight_names:  # Ищем столбец с весом
                weight_col = header

        return product_col, price_col, weight_col  # Возвращаем названия столбцов

    def export_to_html(self, fname='output.html'):
        """
        Экспортирует данные в HTML файл.
        """
        result = '''
<!DOCTYPE html>
<html>
<head>
    <title>Позиции продуктов</title>
</head>
<body>
    <table border="1">
        <tr>
            <th>Номер</th>
            <th>Название</th>
            <th>Цена</th>
            <th>Фасовка</th>
            <th>Файл</th>
            <th>Цена за кг.</th>
        </tr>
        '''
        for idx, item in enumerate(self.data, start=1):  # Перебираем данные и формируем строки таблицы
            result += f'''
                <tr>
                    <td>{idx}</td>
                    <td>{item['name']}</td>
                    <td>{item['price']}</td>
                    <td>{item['weight']}</td>
                    <td>{item['file']}</td>
                    <td>{item['price_per_kg']}</td>
                </tr>'''
        result += '''</table></body></html>'''

        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)
        return self

    def find_text(self, text):
        """
        Находит и выводит продукты, содержащие указанный текст, отсортированные по цене за кг.
        """
        filtered_data = [item for item in self.data if
                         text.lower() in item['name'].lower()]  # Фильтруем данные по тексту
        if not filtered_data:
            print(f"Продукты с текстом '{text}' не найдены!")
            return
        filtered_data.sort(key=lambda x: x['price_per_kg'])  # Сортируем по цене за кг

        print("№\tНаименование\tцена\tвес\tфайл\tцена за кг.")
        for idx, item in enumerate(filtered_data, start=1):
            print(f"{idx}\t{item['name']}\t{item['price']}\t{item['weight']}\t{item['file']}\t{item['price_per_kg']}")


pm = PriceMachine()
start_time = time.time()
pm.load_prices()
end_time = time.time()
execution_time = end_time - start_time
print(f'Загрузка данных закончена за {execution_time} сек.!')


while True:
    '''
    В бесконечном цикле пользователь вводит текст для поиска. Если введено exit, цикл завершается, и программа 
    заканчивает работу. Если введен другой текст, вызывается метод find_text, который выводит продукты, содержащие 
    заданный текст, отсортированные по цене за кг.
    '''
    user_input = input("Введите текст для поиска или 'exit' для выхода: ")
    if user_input.lower() == 'exit':
        print("Работа завершена.")
        break
    pm.find_text(user_input)

# pm.export_to_html()  # Экспортируем данные в HTML
# print("Данные экспортированы в output.html")
export_choice = input("Экспортировать данные в HTML? (да/нет): ")
if export_choice.lower() == "да":
    pm.export_to_html()  # Экспортируем данные в HTML
    print("Данные экспортированы в output.html")

print("Программа завершена.")
