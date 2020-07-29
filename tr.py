import requests
import sys
  
# Данные авторизации в API Trello  
auth_params = {    
    'key': "0bb746d2fa55f2aaaef0ad66a00ad646",    
    'token': "5b0ddff2c978e46d525544ef515d13e6aa8e589674d75e768e8ed2938fa0bf14", }  
  
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"
board_id = "ZB9KiSWJ"
idBoard = "5f1eb5164ccef86d198cc1d3"

def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        task_kol = 0
        for task in task_data:      
            task_kol += 1
        print(column['name'] + ': ' + str(task_kol))
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        i = 1
        for task in task_data:      
            print('\t', i, task['name'], 'id:' , task['id'])  
            i += 1

def create(name, column_name):
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке
            print('ok')
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})      
            break

def create_с(column_name):
    requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': idBoard, **auth_params}) 
    print('Список "' + column_name + '" добавлен.')

def move(name, column_name):
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    tasks_move = {}
    task_id = None
    i = 1
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        i2 = 1
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                tasks_move[str(i)] = [column['name'], task_id, i2]
                i += 1
            i2 += 1

    if len(tasks_move) == 1:
        # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
        # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
        for column in column_data:
            if column['name'] == column_name:
                # И выполним запрос к API для перемещения задачи в нужную колонку    
                requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
                break
    elif len(tasks_move) > 1:
        print('Задача с названием:', name, 'содержится в следующих списках:')
        for el in tasks_move:
            print(str(el) + '. ' + str(tasks_move[el][0]) + ' (Номер задачи в списке: ' + str(tasks_move[el][2]) + ')')
        task_num = input ("Выберите нужный вариант: ")
        for column in column_data:
            if column['name'] == column_name:
                # И выполним запрос к API для перемещения задачи в нужную колонку    
                requests.put(base_url.format('cards') + '/' + tasks_move[task_num][1] + '/idList', data={'value': column['id'], **auth_params})
                print('Перенос выполнен.')
                break
       
if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif len(sys.argv) == 3:
        create_с(sys.argv[2])
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])