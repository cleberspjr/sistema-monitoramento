#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime
import schedule
import time
import os
import re
import subprocess
import pandas as pd
from pathlib import Path
import time
import threading


# In[24]:


#save only 1 record per termal_zone
def thermal_zone():
    t_zone = [os.path.join(thermal, m.group(0)) for m in [re.search('thermal_zone[0-9]+', d) for d in os.listdir(thermal)] if m] 
    #t_zone = [filename for filename in os.listdir(thermal) if filename.startswith("thermal_zone")]
    return t_zone

def value(valor):
    val = (subprocess.check_output(['cat', valor]))
    return val

def thermal_temperature(zona):
    zona_temp = ([int(value(os.path.join(p, 'temp'))) for p in zona])

    return zona_temp

#save only 1 record per termal_zone
def save_thermal_temperature(zona, file):
    q = open(file, 'w')
    zona_temp = ([int(value(os.path.join(p, 'temp'))) for p in zona])
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
    label = ""
    label = str("day")+";"+str("time")
    record = ""
    record = str(now).split(" ")[0]+";"+str(now).split(" ")[1]
    i=0
    for p in zona: 
        label += ";"+str(p.split("/")[-1])
        record +=";"+str(zona_temp[i])
        i+=1        
    record +=str('\n')
    q.write(str(label)+"\n")
    q.write(record)    
    q.close()

def save_thermal_temperature(zona, file, intervalo, duracao):
    tempo_inicial = time.time()

    while True:
        q = open(file, 'a')
        zona_temp = ([int(value(os.path.join(p, 'temp'))) for p in zona])    
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
        label = ""
        label = str("day")+";"+str("time")
        record = ""
        record = str(now).split(" ")[0]+";"+str(now).split(" ")[1]
        i=0
        for p in zona: 
            label += ";"+str(p.split("/")[-1])
            record +=";"+str(zona_temp[i])
            i+=1        
        record +=str('\n')
        q.write(str(label)+"\n")
        q.write(record)    
        q.close()

        time.sleep(intervalo)

        tempo_atual = time.time()
        if tempo_atual - tempo_inicial >= duracao:
            print("Condição de parada atingida. Encerrando a coleta de dados.")
            break
                
zona = ['/sys/class/thermal/thermal_zone0', '/sys/class/thermal/thermal_zone1']
file = 'temperaturas.csv'
coletar_dados_thermal_zones(zona, file, intervalo=10, duracao=60)

# to do: implementar condicao de parada
    # condicao de parada: setar o intervalo (segundos entre uma coleta e outra) e a duração
# to do: verificar se eh facil incluir uma opcao de encerrar o programa

def save_info_proc_file(name_file ='info_proc.txt'):
    informacoes = {}
    
    with open('/proc/cpuinfo', 'r') as file:
        linhas = file.readlines()

    for linha in linhas:
        # Separa a linha em chave e valor
        partes = linha.strip().split(':')
        if len(partes) == 2:
            chave = partes[0].strip()
            valor = partes[1].strip()
            informacoes[chave] = valor

    with open(name_file, 'w') as file:
        for chave, valor in informacoes.items():
            file.write(f'{chave}: {valor}\n')

    print(f'Informações do processador salvas em {name_file}')

# Exemplo de uso
save_info_proc_file()

def save_thermal_temperature_por_segundo(zona, file, interval):
        q = open(file, 'a')
        count = 1
        while (True):
            save_thermal_temperature(zona, file)
            print("Records saved:", count)
            count += 1
            time.sleep(30)
        # to do
        # if count x interval == duration sai do programa
        
    
        print(zona_temp)
#funcao nova

def save_processor_info():
   # p = open(file, 'w')
    #cpu_file = '/proc/cpuinfo'
    
    with open('/proc/cpuinfo', 'r') as cpu_info_file:
        cpu_info = cpu_info_file.read()
    print(cpu_info)    


def print_several_temps_all_zones(file):
    df = pd.read_csv(file, sep=";", header=None)
    
    time_list = df[df.columns[1]].values.tolist()[1:]
    zones_dict = {}    
    all_zones_in_a_dictionary(zones_dict, df)
    print(zones_dict)
    zonesdict = zones_dict
    
    df = pd.DataFrame(data=zonesdict)
    df.index = time_list
    lines = df.plot.line(figsize=(10, 4))
    
#funcao nova
def all_zones_in_a_dictionary(zones_dict, df):

    for i in range(2, df.shape[1]):
        print("accessing position:", i)
        zone_name = df[df.columns[i]].values.tolist()[0]
        temp_list = df[df.columns[i]].values.tolist()[1:]
        temp_list_2 = [float(element) for element in temp_list]

        zones_dict[str(zone_name)] = temp_list_2
    return zones_dict


# In[3]:


thermal = '/sys/class/thermal/'

def main():    
    output_file_unico = "temp_database.csv"
    output_file_varios = "temp_database_all.csv" 
    output_file_varios_teste = "temp_database_all.csv" 
    output_processor_info = "processor_info.csv"
    #Especifica a zona termal que se quer medir
    zona = thermal_zone()    
    #print(zona)
    #Salva as temperaturas de cada zona (1 unica vez)
    #save_thermal_temperature(zona, output_file_unico)
    
    # No futuro esta funcao vai ser chamada por 1 thread isolada    
    
    # Salvar as informacoes do processador
    thread1 = threading.Thread(target=save_processor_info, args=())
    thread1.start()
    
    # Salva as temperaturas de cada zona (1 registro por intervalo=segundo)
   # thread2 = threading.Thread(target=save_thermal_temperature_por_segundo, args=(zona, output_file_varios_teste, 10))
   # thread2.start()
    
    
    
    print("master doing thing 1")
    print("master doing thing 2")
    print("master doing thing 3")
    
    #save_thermal_temperature_por_segundo(zona, output_file_varios_teste,10)    # exemplo - save_thermal_temperature_por_segundo(zona, output_file_unico,10)
    
#     Printa grafico de linhas que exibe 1 temperatura por zona (arquivo output_file_unico)
#     chamada da funcao aqui
#     ex. print_single_temp(zona, output_file_unico)
#    print_single_temp(zona, output_file_unico)

#     # Printa grafico de linhas que exibe 10 temperaturas para cada zona termal (de 1 em 1)
#     # no intervalo de tempo especificado (usar o arquivo output_file_varios e printar os 10 ultimos minutos)
#     # chamada da funcao aqui
#     # ex. print_several_temps(output_file_unico, interval=10)
    
   # print_several_temps_all_zones(output_file_varios)
    
    
    
if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:




