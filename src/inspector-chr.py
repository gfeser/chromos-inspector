
from inspector import Inspector

#INSPECTOR_URL_API='http://inspector.has.ru/api/'
INSPECTOR_URL_API='http://john.feser.ru/api/'



insp=Inspector(INSPECTOR_URL_API)
insp.read(0)
insp.sendChr()
insp.read(1)
insp.sendChr()

for i in range(2,10):

    insp.read(i)
    insp.sendChr()
    text="Проверьте комбинацию "+str(i-2)+str(i-1)+str(i)+" и нажмиле Enter..."
    input(text)



