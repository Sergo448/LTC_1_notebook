# LTC_1_notebook/notebooks/FinderData.ipynb
# importing some libraries
import pandas as pd
import re


def OpenerCouneterRows(path):
    """
    path: str Путь до файла .xlsx
    rerurn: data_exel DataFrame
            ncols list

    Функция возвращает нам DataFrame в виде
    исходного DataFrame с конкретными номерами
    столбцов, т.к. у исходного их нет
    """
    data_excel_head = pd.read_excel(path, nrows=50)
    ncols_data = data_excel_head.shape[1]
    ncols = []
    for col in range(ncols_data):
        ncols.append('Col{}'.format(col))

    data_excel = pd.read_excel(path, names=ncols)

    return data_excel, ncols


path = '/home/sergey/PycharmProjects/LTC_1_notebook/exel_data/Chapter_1_buildibgs.xlsx'

data_excel, ncols = OpenerCouneterRows(path=path)


def searcher_row_razdel(data):
    """
        data: dataframe
        return: row (int)

        Функция ищет строчку, в которой находится №пп для того,
        чтобы потом взять эту строчку и вытянуть из нее необходимую
        шапку для будующей таблицы
    """

    global n_row
    razdel_array = []

    for row, column in data.iterrows():
        # first
        for i in range(len(column)):
            # print(row, column[i])
            if re.search(r'\bРаздел\b', str(column[i])):
                razdel_array.append(column[i])
                # return row
                n_row = row

        # second
    return razdel_array, n_row


row_razdel, start_row = searcher_row_razdel(data_excel)


def make_rows(data, start_row):
    """

    :param data:
    :param start_row:
    :return:
    """
    Row_list = []

    for index, rows in data[start_row + 1:].iterrows():
        my_list = [rows.Col0, rows.Col1, rows.Col2, rows.Col3,
                   rows.Col4, rows.Col5, rows.Col6, rows.Col7,
                   rows.Col8, rows.Col9, rows.Col10, rows.Col11,
                   rows.Col12, rows.Col13, rows.Col14, rows.Col15,
                   rows.Col16, rows.Col17, rows.Col8, rows.Col19,
                   rows.Col20]

        Row_list.append(my_list)

    return Row_list


rows_ = make_rows(data=data_excel, start_row=start_row)

# Создаем списки данных для будущего иерархического списка
list_of_razdel_nn = []
list_of_shifrs = []
list_of_works_janeral = []

# (rows_[i][4])

for i in range(len(rows_)):
    # Составляем список подразделов
    if str(rows_[i][0]).isdigit():
        list_of_razdel_nn.append((rows_[i][0]))
    # Составляем список шифров
    if str(rows_[i][2]) != 'nan':
        list_of_shifrs.append(str(rows_[i][2]))
    if str(rows_[i][0]) != 'nan' and str(rows_[i][2]) != 'nan' and str(rows_[i][4]) != 'nan':
        list_of_works_janeral.append(str(rows_[i][4]))

list_of_works_parts = [[], [], [], []]

# Дополняем данные
for i in range(len(rows_)):

    if (str(rows_[i][0]) == 'nan' and
            str(rows_[i][1]) == 'nan' and
            str(rows_[i][2]) == 'nan' and
            str(rows_[i][3]) == 'nan' and
            str(rows_[i][4]) != 'nan'):

        # Заполняем список частей разработки
        list_of_works_parts[0].append(rows_[i][4])

        # Заполняем спиок единиц измерений частей разработки, если nan, то 'Безразмерная'
        # Для ЗТР если nan то берем клетку по диагонали вверх
        if str(rows_[i][4]) == 'ЗТР':
            list_of_works_parts[1].append(rows_[i - 1][6])
        elif str(rows_[i][6]) == 'nan' and str(rows_[i][4]) != 'ЗТР':
            list_of_works_parts[1].append('Безразмерная')
        else:
            list_of_works_parts[1].append(rows_[i][6])

        # Заполняем список кол-ва единиц, если nan, то 1
        # Для ЗТР если nan то берем клетку по диагонали вверх
        if str(rows_[i][4]) == 'ЗТР':
            list_of_works_parts[2].append(rows_[i - 1][7])
        elif str(rows_[i][7]) == 'nan':
            list_of_works_parts[2].append(1)
        else:
            list_of_works_parts[2].append(rows_[i][7])

        # Заполняем список затрат
        if str(rows_[i][4]) == 'ЗТР':
            list_of_works_parts[3].append(rows_[i - 1][19])
        else:
            list_of_works_parts[3].append(rows_[i][16])
        # Для ЗТР если nan то берем клетку по диагонали вверх

    else:
        continue

    if str(rows_[i][4]) == 'ЗТР':
        # Point - метка для разрыва и перехода к другому нормативному документу
        list_of_works_parts[0].append('Point')
        list_of_works_parts[1].append('Point')
        list_of_works_parts[2].append('Point')
        list_of_works_parts[3].append('Point')

# №пп, Шифр, Наименование работы

array_for_dict_1 = list(zip(list(list_of_razdel_nn),  # №пп
                            list(list_of_shifrs),  # Шифр
                            list(list_of_works_janeral)))  # Наименование работы

array_for_dict_2 = list(zip(list(list_of_works_parts[0]),  # Наименование работ
                            list(list_of_works_parts[1]),  # Единицы измерений
                            list(list_of_works_parts[2]),  # Количество
                            list(list_of_works_parts[3])))  # Стоимость


# Создаем упорядоченный список для array_for_dict_2 без точек разрыва
half_final = []
lil = []

# for i in range(len(array_for_dict_2)):
for i in range(len(array_for_dict_2)):

    if 'Point' not in list(array_for_dict_2[i]):
        lil.append(array_for_dict_2[i])

    elif 'Point' in list(array_for_dict_2[i]):
        # print(lil)
        # print(len(lil))
        half_final.append(lil)
        lil = []
    else:
        continue

result_list = list(zip(list(array_for_dict_1), list(half_final)))

print(result_list)