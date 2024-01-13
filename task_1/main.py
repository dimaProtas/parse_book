from collections import Counter


# Открываем фаил с данными и преобразуем в список словарей
with open("table.csv", "r") as f:
    lines = f.readlines()
    data = []
    for line in lines:
        el = line.strip().split(',')
        element = {
            'id': el[1],
            'text': el[0]
        }
        data.append(element)

    # Получаем количество повторений каждого id
    id_counts = Counter([item['id'] for item in data])
    # print(id_counts)

    # Получаем только те id которые встречаються 3 раза
    for item in data:
        if id_counts[item['id']] == 3:
            print(item['id'])
