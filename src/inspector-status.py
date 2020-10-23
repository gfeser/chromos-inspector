from inspector import Inspector
from time import sleep

#INSPECTOR_URL_API='http://inspector.has.ru/api/'
INSPECTOR_URL_API='http://john.feser.ru/api/'

statuses = {2:"Подготовка",5:"Готов",6:"Анализ",19:"Ошибка"}

insp=Inspector(INSPECTOR_URL_API)

while True:
    for s in statuses:
        print("\nНовый статус:",statuses[s])
        insp.sendStatus(s)
        sleep(15)


