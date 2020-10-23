
import requests
import re

#INSPECTOR_URL_API='http://inspector.has.ru/api/'
INSPECTOR_URL_API='http://john.feser.ru/api/'


class Inspector:
    
    lastid=1

    def __init__(self):
    
        self.areas = {}
        self.method=""
        self.analyse_date=''
    
    # Чтение файла по номеру
    def read(self,number):
        
        filename="export/{}_export.txt".format(number) 
        with open(filename, "rt", encoding="cp1251") as f:
            lines = f.readlines()
            
            # данные из паспорта
            for line in lines:
                if re.search('\[Peaks\]', line):
                    break
                
                sch=re.search('AnalyseTime=(.*)', line) #2020.10.21 17:51:06
                if sch:
                    self.analyse_date=sch.group(1).replace(' ','T')+'+03:00'

                sch=re.search('Method=(.*)', line) #2020.10.21 17:51:06
                if sch:
                    self.method=sch.group(1)

            print("\n=== Хроматограмма:{}    Метод:{}   Дата:{} ===".format(number,self.method,self.analyse_date))
            
            self.areas = {}
            
            # площади пиков
            peaks_flag=False
            for line in lines:
                if not peaks_flag:
                    if re.search('\[Peaks\]', line):
                        peaks_flag=True
                    continue


                if re.search('\[Groups\]', line):
                    break
                
                params=line.split(',')
                if len(params)<5:
                    continue
                if float(params[4])==0: # в паспорте ГСО этих компонентов нет
                    continue
                
                comp_name=params[5].replace('"','').replace('\n','').strip()
                comp_area=float(params[3])
                
                self.areas[comp_name]=comp_area
                #print('{:10s} {:10.5f}'.format(comp_name,comp_area))
                
    def sendChr(self):
        
        headers = {'Content-Type':'application/json'}
        
        json_chr_template = """{"jsonrpc": "2.0", "method": "chr", "params": {
         "dt": "{{analysedate}}",
         "devid":"4b13d19e-4bf4-43a5-91fa-4334718f0539",
         "type": 1,
         "operator": "Иванов Я.Ф.",
         "method": "{{methodname}}",
         "components": [
            {{componentlist}} ]
            }   , "id": {{id}}  }"""
        
        jdata=json_chr_template
        jdata=jdata.replace('{{analysedate}}',self.analyse_date)
        jdata=jdata.replace('{{methodname}}',self.method)
        jdata=jdata.replace('{{id}}',str(Inspector.lastid))
        Inspector.lastid+=1
        
        components=""
        
        firstflag=True
        for cname in self.areas:
            if firstflag:
                firstflag=False
            else:
                components+=','
            components+='{ "name":"'+cname+'", "area":'+str(self.areas[cname])+' }'
        jdata=jdata.replace('{{componentlist}}',components)
        
        #print(jdata)
        
        post_call = requests.post(INSPECTOR_URL_API, data=jdata.encode('utf-8'), headers = headers)

        print('Ответ: ',post_call.content.decode('utf-8'))
        print()


chr=Inspector()
chr.read(0)
chr.sendChr()
chr.read(1)
chr.sendChr()

for i in range(2,10):

    chr.read(i)
    chr.sendChr()
    text="Проверьте комбинацию "+str(i-2)+str(i-1)+str(i)+" и нажмиле Enter..."
    input(text)



