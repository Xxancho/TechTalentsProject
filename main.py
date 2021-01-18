import time
import tkinter as tk
import bisect
import math
from tkinter import ALL, HORIZONTAL, VERTICAL
from tkinter.font import Font


def find_lis(a):
    n = len(a)

    #Массив элементов, которые мы меняем с помощью бин поиска
    results = [math.inf] * (n+1)
    results[0] = -math.inf

    #Массив позиций элементов, которые мы ставим в массиве results
    positions = [0] * (n+1)
    positions[0] = -1

    #Массив предыдущих элементов для элементов, которые мы ставим в массиве results
    previous = [0] * n

    #Пошаговая карта всех изменений в массиве results
    #Каждый элемент состоит из трех элементов: индекс меняемого элемента, новое значение и прошлое значение
    results_array_canvas_map = []

    # Пошаговая карта всех изменений в массиве positions
    # Каждый элемент состоит из трех элементов: индекс меняемого элемента, новое значение и прошлое значение
    positions_array_canvas_map = []

    # Пошаговая карта всех изменений в массиве previous
    # Каждый элемент состоит из трех элементов: индекс меняемого элемента, новое значение и прошлое значение
    previous_array_canvas_map = []

    #Длина максимальной подпоследовательности
    length = 0

    #Массив, содержащий все варианты НВП  по ходу выполнения программы
    answer_list = []



    for i in range(n):
        #Ищем позицию для вставки элемента в массив results
        j = bisect.bisect_left(results, a[i])

        #Если мы можем вставить элемент(он меньше найденой позиции и больше левой)
        if results[j - 1] < a[i] < results[j]:

            results_array_canvas_map.append((j, a[i], results[j]))          #Добавление элемента в пошаговую карту изменений массива результатов
            positions_array_canvas_map.append((j, i, positions[j]))         #Добавление элемента в пошаговую карту изменений массива текущих позиций
            previous_array_canvas_map.append((i, positions[j - 1], previous[i]))  #Добавление элемента в пошаговую карту изменений массива предыдущих элементов

            results[j] = a[i]                   #Релаксируем элемент в массиве result
            positions[j] = i                    #Добавляем его позицию в массив позиций
            previous[i] = positions[j - 1]      #Добавляем позицию предыдущего элемента
            length = max(length, j)             #Релаксируем максимальную длину НВП

            answer = []                         #Создаем массив для текущей НВП
            p = positions[length]               #Индекс элемента для начала создания - длина текущей НВП
            while p != -1:                      #Пока данный индекс будет больше 0 - выполняем цикл
                answer.append(a[p])             #Добавляем к ответу элемент основного массива по текущему индексу
                p = previous[p]                 #Заменяем текущий индекс на индекс предыдущего элемента
            answer.reverse()                    #Разворачиваем ответ
            answer_list.append(answer)          #Добавляем ответ в массив всех НВП, найденных в ходе выполнения программы
        else:
            results_array_canvas_map.append((j, -1, -1))    #Добавляем в список результатов элемент, означающий, что
                                                        #шаг нужно пропустить, не меняя элементов и окрашивать только первые два массива
            positions_array_canvas_map.append((j, -1, -1))
            previous_array_canvas_map.append((i, -1, -1))
            answer_list.append(answer_list[i-1])


    return (answer_list, results_array_canvas_map, positions_array_canvas_map, previous_array_canvas_map)


sequence = []           #Массив элементов основной последовательности
find_lis_result = ()    #Кортеж массивов: массив ответов, карты изменений массивов результатов, теккущих элементов, предыдущих элементов
map_list = []           #Массив, содержащий 4 массива: каждый содержит айди элементов текста своего массива
current_step = -1

longest_element = 0

answer_map = []

#Получение наидлинейшего элемента в основном массиве
def get_longest_element():
    global longest_element
    longest_element = 0
    for i in range(len(sequence)):
        if len(str(sequence[i])) > longest_element:
            longest_element = len(str(sequence[i]))

FONT_SIZE = 30

def create_map_list():
    canvas_arrays.delete(ALL)                                                       #Очищаем весь canvas
    global map_list                                         #Объявляем глобальную переменную - массив айди элементов canvas
    global answer_map                                       #Массив canvas элементов ответа
    map_list = [[], [], [], []]

    canvas_arrays.create_text(20, FONT_SIZE, text = 'A:', fill = 'green',font=("Arial", FONT_SIZE))
    canvas_arrays.create_text(20, FONT_SIZE*2+FONT_SIZE//4, text='D:', fill='green', font=("Arial", FONT_SIZE))
    canvas_arrays.create_text(20+FONT_SIZE*9/4, FONT_SIZE*3+FONT_SIZE//2, text='Positions:', fill='green', font=("Arial", FONT_SIZE))
    canvas_arrays.create_text(20+FONT_SIZE*8/4, FONT_SIZE*5, text='Previous:', fill='green', font=("Arial", FONT_SIZE))

    #Задаем массиву айди элементов canvas его вид
    distance = FONT_SIZE * 9
    map_list[1].append(canvas_arrays.create_text(distance, FONT_SIZE*2+FONT_SIZE//4,                            #Добавляем в canvas первый элемент массива результатов(- бесконечность)
                                text='-∞', fill='white', font=("Arial", FONT_SIZE)))
    map_list[2].append(canvas_arrays.create_text(distance, FONT_SIZE*3+FONT_SIZE//2,                            #Добавляем в canvas первый элемент массива позиций(0)
                                text='0', fill='white', font=("Arial", FONT_SIZE)))
    map_list[3].append(canvas_arrays.create_text(longest_element * FONT_SIZE +distance, FONT_SIZE*5,    #Добавляем в canvas первый элемент массива позиций(-1). Он имеет позицию  longest_element * 16 + 20
                                text='-1', fill='white', font=("Arial", FONT_SIZE)))
    distance = distance + longest_element * FONT_SIZE                                          #Необходимое начальное расстояние. longest_element * 16 - это требуемое расстояние между двумя элементами
    for i in range(len(sequence)):


        map_list[0].append(canvas_arrays.create_text(distance, FONT_SIZE,                  #Добавляем в canvas элемент массива результатов.
                                text = str(sequence[i]),
                                fill = 'white', font=("Arial", FONT_SIZE)))


        map_list[1].append(canvas_arrays.create_text(distance, FONT_SIZE*2+FONT_SIZE//4,                   #Добавляем в canvas элемент массива результатов.
                                text = '∞', fill = 'white', font=("Arial", FONT_SIZE)))
        map_list[2].append(canvas_arrays.create_text(distance, FONT_SIZE*3+FONT_SIZE//2,                   #Добавляем в canvas элемент массива результатов.
                                text = '0', fill = 'white', font=("Arial", FONT_SIZE)))
        if i != len(sequence) - 1:                                                   #Не позволи твыйти за пределы массива предыдущих элементов, так как цикл идет n+1 раз, а в нем всего n элементов
            map_list[3].append(canvas_arrays.create_text(distance +                  #Добавляем в canvas элемент массива результатов.
                                longest_element * FONT_SIZE, FONT_SIZE*5,
                                text='0', fill='white', font=("Arial", FONT_SIZE)))
        distance = distance + longest_element * FONT_SIZE


    canvas_arrays.create_line(0, FONT_SIZE*1.6, distance, FONT_SIZE*1.6, fill = 'white')

    canvas_arrays.create_line(0, FONT_SIZE*2.6+FONT_SIZE//4, distance, FONT_SIZE*2.6+FONT_SIZE//4, fill='white')

    canvas_arrays.create_line(0, FONT_SIZE*3.7+FONT_SIZE//2, distance, FONT_SIZE*3.7+FONT_SIZE//2,
                              fill='white')

    canvas_arrays.create_line(0, FONT_SIZE*5.6, distance, FONT_SIZE*5.6,
                              fill='#d89600')

    canvas_arrays.create_line(FONT_SIZE*8, 0,  FONT_SIZE*8, FONT_SIZE*5+FONT_SIZE//2,
                              fill='green')

    for i in range(len(sequence)):
        answer_map.append(canvas_arrays.create_text(FONT_SIZE * i*longest_element+20, FONT_SIZE*6+FONT_SIZE, text = '0', fil = 'gray15', font=("Arial", FONT_SIZE)))

    canvas_arrays.config(scrollregion=[0, 0, distance - longest_element * FONT_SIZE/2, FONT_SIZE*8 ])

    #Задаем поле для прокрутки


def clean_all():
    global sequence
    global find_lis_result
    global map_list
    global current_step
    global answer_map
    sequence = []  # Массив элементов основной последовательности
    find_lis_result = ()  # Кортеж массивов: массив ответов, карты изменений массивов результатов, теккущих элементов, предыдущих элементов
    map_list = []  # Массив, содержащий 4 массива: каждый содержит айди элементов текста своего массива
    current_step = -1
    answer_map = []


def submit_button_clicked():
    global sequence
    global find_lis_result
    global map_list
    clean_all()                                                         #Очищаем все массивы
    sequence = [x for x in field.get('1.0', tk.END).split()]
    for i in range(len(sequence)):
        if not str(sequence[i]).isdigit():
            clean_all()
            field.config(bg = 'red')
            return
        else:
            sequence[i] = int(sequence[i])
            field.config(bg='white')

    #Считываем последовательность
    get_longest_element()                                               #Получаем самый длинный элемент последовательности
    #print(sequence)
    find_lis_result = find_lis(sequence)                                #Получаем результат работы алгоритма: массив ответов, три массива пошагового изменения массивов
    #print(find_lis_result[0])
    #print(find_lis_result[1])
    #print(find_lis_result[2])
    #print(find_lis_result[3])
    create_map_list()                                                   #Создаем элементы текста в canvas, а так же записываем их айди в матрицу айдишников

    #print(map_list)

prev_step_result = 0        #Предыдущий элемент в массиве result
prev_step_positions = 0     #Предыдущий элемент в массиве positions
prev_step_prev = 0          #Предыдущий элемент в массиве previous
def next_step_button_clicked():
    global  current_step
    global prev_step_result
    global prev_step_positions
    global prev_step_prev
    global answer_map

    if current_step+1 < len(find_lis_result[1]):

        current_step = current_step + 1




        array_index = find_lis_result[1][current_step][0]
        new_value = find_lis_result[1][current_step][
            1]
        id = map_list[1][array_index]


        for i in range(len(find_lis_result[0][current_step])):

            canvas_arrays.itemconfig(answer_map[i], fill = 'white', text=  str(find_lis_result[0][current_step][i]))


        if new_value != -1:


            canvas_arrays.itemconfig(id, text = str(new_value), fill = 'yellow')



            #canvas_arrays.itemconfig(prev_step_positions, fill = 'white')     #Красим предыдущий элемент обратно в белый
            array_index = find_lis_result[2][current_step][0]  # Переменная, в которую заносим индекс изменяемого элемента в массива positions
            new_value = find_lis_result[2][current_step][1]  # Переменная, в которую заносим новое занчение элемента массива positions
            id = map_list[2][array_index]  # Получаем id элемента canvas соответствующего нужному элементу массива positions
            canvas_arrays.itemconfig(id, text=str(new_value), fill = 'yellow')  # Изменяем отображение элемента positions

            #prev_step_positions = map_list[2][array_index]    #Записываем в переменную предыдущего шага по данному массиву предыдущий элемент



            #canvas_arrays.itemconfig(prev_step_prev, fill='white')
            if current_step != 0:
                array_index = find_lis_result[3][current_step][0]  # Переменная, в которую заносим индекс изменяемого элемента в массива previous
                new_value = find_lis_result[3][current_step][1]
                id = map_list[3][array_index]
                canvas_arrays.itemconfig(id, text=str(new_value), fill = 'yellow')
               # prev_step_prev = map_list[3][array_index]

            #Условие необходимо для того, что бы в случае, когда мы меняем уже существующий элемент, он не красился в белый, а оставался желтым
            if find_lis_result[1][current_step - 1][0] != find_lis_result[1][current_step][0]:
                prev_array_index = find_lis_result[1][current_step - 1][0]
                prev_id = map_list[1][prev_array_index]
                canvas_arrays.itemconfig(prev_id, fill='white')

                prev_array_index = find_lis_result[2][current_step - 1][0]
                prev_id = map_list[2][prev_array_index]
                canvas_arrays.itemconfig(prev_id, fill='white')

            prev_array_index = find_lis_result[3][current_step - 1][0]
            prev_id = map_list[3][prev_array_index]
            canvas_arrays.itemconfig(prev_id, fill='white')

        else:
            array_index = find_lis_result[1][current_step-1][0]
            id = map_list[1][array_index]
            canvas_arrays.itemconfig(id, fill='white')

            array_index = find_lis_result[2][current_step-1][0]
            id = map_list[2][array_index]
            canvas_arrays.itemconfig(id, fill='white')

            array_index = find_lis_result[3][current_step-1][0]
            id = map_list[3][array_index]
            canvas_arrays.itemconfig(id, fill='white')


        id = map_list[0][current_step]
        canvas_arrays.itemconfig(id, fill='yellow')
        prev_id = map_list[0][current_step-1]
        canvas_arrays.itemconfig(prev_id, fill='white')






def prev_step_button_clicked():
    global current_step
    global answer_map

    #Переменная текущего шага
    if current_step  >= 0:                                      #Выполняем, если текущий шаг больше нуля


        id = map_list[0][current_step]
        canvas_arrays.itemconfig(id, fill='white')


        for i in range(len(answer_map)):
            canvas_arrays.itemconfig(answer_map[i], fill='gray15')

        for i in range(len(find_lis_result[0][current_step])-1):

            canvas_arrays.itemconfig(answer_map[i], fill = 'white', text=  str(find_lis_result[0][current_step][i]))

        array_index = find_lis_result[1][current_step][0]  # Переменная, в которую заносим индекс изменяемого элемента в массива result
        new_value = find_lis_result[1][current_step][2]  # Переменная, в которую заносим новое занчение элемента массива result
        id = map_list[1][array_index]


        print(find_lis_result[1][current_step][2])
        if  find_lis_result[1][current_step][2] != -1:
            if new_value == math.inf:
                canvas_arrays.itemconfig(id, text='∞', fill = 'white')
            else:
                canvas_arrays.itemconfig(id, text=str(new_value), fill = 'white')




            array_index = find_lis_result[2][current_step][
            0]  # Переменная, в которую заносим индекс изменяемого элемента в массива positions
            new_value = find_lis_result[2][current_step][
            2]  # Переменная, в которую заносим новое занчение элемента массива positions
            id = map_list[2][array_index]  # Получаем id элемента canvas соответствующего нужному элементу массива positions
            canvas_arrays.itemconfig(id, text=str(new_value), fill = 'white')  # Изменяем отображение элемента positions

            if current_step != 0:
                array_index = find_lis_result[3][current_step][0]  # Переменная, в которую заносим индекс изменяемого элемента в массива positions
                new_value = find_lis_result[3][current_step][2]  # Переменная, в которую заносим новое занчение элемента массива positions
                id = map_list[3][array_index]  # Получаем id элемента canvas соответствующего нужному элементу массива positions
                canvas_arrays.itemconfig(id, text=str(new_value), fill = 'white')  # Изменяем отображение элемента positions

            if current_step > 0 and find_lis_result[1][current_step - 1][2] != -1:
                prev_array_index = find_lis_result[1][current_step - 1][0]
                prev_id = map_list[1][prev_array_index]
                canvas_arrays.itemconfig(prev_id, fill='yellow')

                prev_array_index = find_lis_result[2][current_step - 1][0]
                prev_id = map_list[2][prev_array_index]
                canvas_arrays.itemconfig(prev_id, fill='yellow')

                prev_array_index = find_lis_result[3][current_step - 1][0]
                prev_id = map_list[3][prev_array_index]
                canvas_arrays.itemconfig(prev_id, fill='yellow')
        else:
            if find_lis_result[1][current_step - 1][2] != -1:
                if current_step > 0:
                    prev_array_index = find_lis_result[1][current_step - 1][0]
                    prev_id = map_list[1][prev_array_index]
                    canvas_arrays.itemconfig(prev_id, fill='yellow')

                    prev_array_index = find_lis_result[2][current_step - 1][0]
                    prev_id = map_list[2][prev_array_index]
                    canvas_arrays.itemconfig(prev_id, fill='yellow')

                    prev_array_index = find_lis_result[3][current_step - 1][0]
                    prev_id = map_list[3][prev_array_index]
                    canvas_arrays.itemconfig(prev_id, fill='yellow')


        if current_step > 0:
            id = map_list[0][current_step - 1]
            canvas_arrays.itemconfig(id, fill='yellow')

        if current_step < len(find_lis_result[1])-1:
            id = map_list[3][current_step +1]
            canvas_arrays.itemconfig(id, fill='white')

        if current_step == 0:
            prev_array_index = find_lis_result[3][current_step][0]
            prev_id = map_list[3][prev_array_index]
            canvas_arrays.itemconfig(prev_id, fill='white')

        current_step = current_step - 1

def size_button_clicked():
    if not str(size_entry.get()).isdigit():
        size_entry.config(bg = 'red')
        return
    else:
        if int(size_entry.get()) < 1:
            size_entry.config(bg = 'red')
            return
        else:
            size_entry.config(bg = 'white')

    global FONT_SIZE
    global map_list
    global answer_map
    global current_step
    map_list = []
    answer_map = []
    FONT_SIZE = int(size_entry.get())
    t = current_step
    submit_button_clicked()
    for i in range(t+1):
        next_step_button_clicked()



root = tk.Tk()
root.geometry('800x800+200+100')



top_frame = tk.Frame(root, bg = 'gray10')
top_frame.place(relwidth = 1, relheight = 0.3)

main_frame = tk.Frame(root, bg = 'gray10')
main_frame.place(rely = 0.3, relx = 0, relwidth = 1, relheight = .7)

label = tk.Label(top_frame, text = 'Введите последовательнотельность чисел через пробел',
                 bg = '#d89600', font=("Arial", 16))
label.place(rely = 0.1, relx = 0.1, relwidth = 0.8, relheight = .15)

field = tk.Text(top_frame, font=("Arial", 16))
field.place(rely = 0.3, relx = 0.1, relwidth = 0.8, relheight = .4)

scroll = tk.Scrollbar(top_frame, command = field.yview(), orient=tk.VERTICAL)
scroll.place(rely = 0.3, relx = 0.875, relwidth = 0.025, relheight = .4)
field.config(yscrollcommand = scroll.set)

submit_button = tk.Button(top_frame, text = 'Подтвердить', bg = '#d89600',
                          font=("Arial", 16), command = submit_button_clicked)
submit_button.place(rely = 0.75, relx = 0.35,  relwidth = 0.3, relheight = 0.2)

canvas_arrays = tk.Canvas(main_frame, bg = 'gray15')
canvas_arrays.place(rely = 0.05, relx = 0.05,  relwidth = 0.9, relheight = 0.5)
#canvas_arrays.place(rely = 0.05, relx = 0.05,  width = 200, height = 100)


next_step_button = tk.Button(main_frame, text = 'Следующий шаг', bg = '#d89600',
                          font=("Arial", 16), command = next_step_button_clicked)
next_step_button.place(rely = 0.65, relx = 0.4,  relwidth = 0.3, relheight = 0.2)

prev_step_button = tk.Button(main_frame, text = 'Предыдущий шаг', bg = '#d89600',
                          font=("Arial", 16), command = prev_step_button_clicked)
prev_step_button.place(rely = 0.65, relx = 0.05,  relwidth = 0.3, relheight = 0.2)

canvas_horizontal_scrollbar = tk.Scrollbar(main_frame, orient=HORIZONTAL, command=canvas_arrays.xview)
canvas_horizontal_scrollbar.place(rely = 0.55, relx = 0.05, relwidth = 0.9, relheight = 0.025)



canvas_vectical_scrollbar = tk.Scrollbar(main_frame, orient=VERTICAL, command=canvas_arrays.yview)
canvas_vectical_scrollbar.place(rely = 0.05, relx = 0.95, relwidth = 0.025, relheight = .5)

canvas_arrays.config(xscrollcommand=canvas_horizontal_scrollbar.set, yscrollcommand=canvas_vectical_scrollbar.set)


size_label = tk.Label(main_frame,text = 'Введите размер шрифта')
size_label.place(rely = 0.65, relx = 0.8125,  relwidth = 0.17, relheight = 0.05)

size_entry = tk.Entry(main_frame)
size_entry.place(rely = 0.7, relx = 0.85,  relwidth = 0.1, relheight = 0.1)

size_button = tk.Button(main_frame, text=  'Подтвердить', bg = '#d89600',
                          font=("Arial", 12), command = size_button_clicked)
size_button.place(rely = 0.8, relx = 0.8125,  relwidth = 0.17, relheight = 0.05)




root.mainloop()
