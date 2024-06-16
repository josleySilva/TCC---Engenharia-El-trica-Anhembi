import time
time.sleep(20)

import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np
import paho.mqtt.client as mqtt
import datetime

from_db = []
q1 = """SELECT * FROM SensorData;"""
m1 = """SELECT * FROM MT1;"""
m2 = """SELECT * FROM MT2;"""
m3 = """SELECT * FROM MT3;"""
m4 = """SELECT * FROM MT4;"""
m5 = """SELECT * FROM MT5;"""
teste_sql = """SELECT * FROM RESULT_ANALIZE;"""
delete = """DELETE FROM SensorData"""
index_reiniciar = """ALTER TABLE SensorData AUTO_INCREMENT=0"""

read_line = False

# Define as credenciais do broker MQTT
broker_address = "localhost"  # Endereço do broker MQTT
#broker_address = "192.168.0.103"  # Endereço do broker MQTT
broker_port = 1883  # Porta do broker MQTT

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    from_db = []
    try:
        cursor.execute(query)
        result = cursor.fetchall()

        for variavel in result:
            variavel = list(variavel)
            from_db.append(variavel)

        columns = ["id", "type", "Location", "Valor x", "Valor y", "Valor z", "date"]
        df = pd.DataFrame(from_db, columns=columns)

        df["Valor x"] = df["Valor x"].astype(float)
        df["Valor y"] = df["Valor y"].astype(float)
        df["Valor z"] = df["Valor z"].astype(float)

        return df
    except Error as err:
        print(f"Error: '{err}'")

def read_querymotors(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()

        for variavel in result:
            variavel = list(variavel)
            from_db.append(variavel)

        columns = ["id", "SENSOR", "LOCATION", "EIXO_X", "EIXO_Y", "EIXO_Z", "timer", "READING_TIME", "DATE_READING"]
        df = pd.DataFrame(from_db, columns=columns)
        df["EIXO_X"] = df["EIXO_X"].astype(float)
        df["EIXO_Y"] = df["EIXO_Y"].astype(float)
        df["EIXO_Z"] = df["EIXO_Z"].astype(float)


        return df
    except Error as err:
        print(f"Error: '{err}'")

def insert_data(connection, data):
    cursor = connection.cursor()
    try:
        for row in data:
            cursor.execute("INSERT INTO RESULT_ANALIZE (Sensor, Location, EIXO_X, EIXO_Y, EIXO_Z, timer, DATE_READING) VALUES (%s, %s, %s, %s, %s, %s, %s)", row)
        connection.commit()
        print("Data inserted successfully")
    except Error as err:
        print(f"Error: '{err}'")

def insert_data_mt1(connection, data):
    cursor = connection.cursor()
    try:
        for row in data:
            cursor.execute("INSERT INTO MT1 (Sensor, Location, EIXO_X, EIXO_Y, EIXO_Z, timer, DATE_READING) VALUES (%s, %s, %s, %s, %s, %s, %s)", row)
        connection.commit()
        print("Data inserted successfully")
    except Error as err:
        print(f"Error: '{err}'")

def insert_data_mt2(connection, data):
    cursor = connection.cursor()
    try:
        for row in data:
            cursor.execute("INSERT INTO MT2 (Sensor, Location, EIXO_X, EIXO_Y, EIXO_Z, timer, DATE_READING) VALUES (%s, %s, %s, %s, %s, %s, %s)", row)
        connection.commit()
        print("Data inserted successfully")
    except Error as err:
        print(f"Error: '{err}'")

def insert_data_mt3(connection, data):
    cursor = connection.cursor()
    try:
        for row in data:
            cursor.execute("INSERT INTO MT3 (Sensor, Location, EIXO_X, EIXO_Y, EIXO_Z, timer, DATE_READING) VALUES (%s, %s, %s, %s, %s, %s, %s)", row)
        connection.commit()
        print("Data inserted successfully")
    except Error as err:
        print(f"Error: '{err}'")

def insert_data_mt4(connection, data):
    cursor = connection.cursor()
    try:
        for row in data:
            cursor.execute("INSERT INTO MT4 (Sensor, Location, EIXO_X, EIXO_Y, EIXO_Z, timer, DATE_READING) VALUES (%s, %s, %s, %s, %s, %s, %s)", row)
        connection.commit()
        print("Data inserted successfully")
    except Error as err:
        print(f"Error: '{err}'")

def insert_data_mt5(connection, data):
    cursor = connection.cursor()
    try:
        for row in data:
            cursor.execute("INSERT INTO MT5 (Sensor, Location, EIXO_X, EIXO_Y, EIXO_Z, timer, DATE_READING) VALUES (%s, %s, %s, %s, %s, %s, %s)", row)
        connection.commit()
        print("Data inserted successfully")
    except Error as err:
        print(f"Error: '{err}'")

def semaforo(dados,setpoint):
    nivel = setpoint
    df = dados
    ultimas_leituras = df.tail(2)
    alarm_x = ultimas_leituras['EIXO_X'] > nivel
    alarm_y = ultimas_leituras['EIXO_Y'] > nivel
    alarm_z = ultimas_leituras['EIXO_Z'] > nivel

    if alarm_x.sum() >= 2 :
        result_color = "VERMELHO"
    if alarm_y.sum() == 1:
        result_color = "AMARELO"
    if alarm_z.sum() == 0:
        result_color = "VERDE"

    return result_color

def insert_datasensor(connection, data):
    cursor = connection.cursor()
    try:
        for row in data:
            cursor.execute("INSERT INTO SensorData (sensor, location, value1, value2, value3) VALUES (%s, %s, %s, %s, %s)", row)
        connection.commit()
        #print("Data inserted successfully")
    except Error as err:
        print(f"Error MySQL: '{err}'")

def calculo_rms(valores):

    dados = valores

    # transformando a string que vem do banco SQL em datetime
    dados["date"] = pd.to_datetime(dados["date"])

    # subtraindo o primeiro pelo segundo no datetime
    dados["diferenca"] = dados["date"].diff()

    # transformando em milissegundos
    dados['microssegundos'] = dados['diferenca'].apply((lambda x: x.microseconds // 1000))
    dados['microssegundos'] = dados['microssegundos'] / 1000

    # dados["VX(m/s)"] = (dados["Valor x"] * dados["microssegundos"]) #desconsiderado pq a variação na leitura aumenta muito o resultado, a media de tempo e 94 ms

    # Tirando a media do tempo que as leituras foram realizadas
    media_leitura = dados['microssegundos'].mean().round(3)

    # Vetor das tres dimencoes
    # Saindo de m/s^2 para m/s usando a media do tempo de leitura das medições
    dados["Delta X (m/s2)"] = (dados["Valor x"].diff())
    dados["Delta Y (m/s2)"] = (dados["Valor y"].diff())
    dados["Delta Z (m/s2)"] = (dados["Valor z"].diff())

    # Transformando em milimetros / segundos
    dados["Vvelocidade X (m/s)"] = ((dados["Delta X (m/s2)"]) * media_leitura)
    dados["Vvelocidade Y (m/s)"] = ((dados["Delta Y (m/s2)"]) * media_leitura)
    dados["Vvelocidade Z (m/s)"] = ((dados["Delta Z (m/s2)"]) * media_leitura)

    # Calculo da diferenca do primeiro para o segundo
    dados["Velocidade X (mm/s)"] = ((dados["Vvelocidade X (m/s)"]) * 1000)
    dados["Velocidade Y (mm/s)"] = (dados["Vvelocidade Y (m/s)"] * 1000)
    dados["Velocidade Z (mm/s)"] = (dados["Vvelocidade Z (m/s)"] * 1000)
    # print(dados["Velocidade Z (mm/s)"])

    # Intensidade da Velocidade VETOR
    dados["Intensidade da Velocidade"] = np.sqrt(
    dados['Velocidade X (mm/s)'] ** 2 + dados['Velocidade Y (mm/s)'] ** 2 + dados['Velocidade Z (mm/s)'] ** 2)

    # Eleve cada valor ao quadrado
    dados['quadrados dos valores'] = dados['Intensidade da Velocidade'] ** 2
    # print(dados['quadrados dos valores'])

    # Calcule a média dos quadrados
    media_quadrados = dados['quadrados dos valores'].mean()

    # Calcule a raiz quadrada da média
    media_rms = (np.sqrt(media_quadrados)).round(2)

    name_sensor = dados["type"][10]
    name_location = dados["Location"][10]

    x = datetime.datetime.now()
    dia_atual = x.strftime("%d/%m")

    result_rms = [(str(name_sensor), str(name_location), media_rms, media_rms, media_rms, media_leitura, str(dia_atual))]
    #print(result_rms)
    return result_rms


# Callback que é chamada quando a conexão com o broker é estabelecida
def on_connect(client, userdata, flags, rc):
    print("Conectado com o código de resultado: " + str(rc))
    # Inscreva-se no tópico 'python/execute' para receber mensagens
    client.subscribe("python/exec")
    client.subscribe("python/accel")
    client.subscribe("python/node")
# Callback que é chamada quando uma mensagem é recebida no tópico inscrito
def on_message(client, userdata, msg):
    #print("Mensagem recebida no tópico '" + msg.topic + "': " + str(msg.payload.decode()))

    # Aqui você pode adicionar o código para tratar as mensagens recebidas
    # Por exemplo, verificar se a mensagem é 'ligar' ou 'desligar'

    if msg.topic == "python/accel":

        input_string = msg.payload.decode()
        valores = [tuple(str(valor) for valor in input_string.split(','))]
        insert_datasensor(connection_db, valores)


    if msg.payload.decode() == "verify":

        dadosm1 = read_querymotors(connection_db, m1)
        dadosm2 = read_querymotors(connection_db, m2)
        dadosm3 = read_querymotors(connection_db, m3)
        dadosm4 = read_querymotors(connection_db, m4)
        dadosm5 = read_querymotors(connection_db, m5)
        dadosteste = read_querymotors(connection_db, teste_sql)

        if len(dadosm1) > 2 :
            semaforo_node = semaforo(dadosm1, 5)
            client.publish('python/led_m1', semaforo_node)

        if len(dadosm2) > 2:
            semaforo_node = semaforo(dadosm2, 5)
            client.publish('python/led_m2', semaforo_node)

        if len(dadosm3) > 2:
            semaforo_node = semaforo(dadosm3, 5)
            client.publish('python/led_m3', semaforo_node)

        if len(dadosm4) > 2:
            semaforo_node = semaforo(dadosm4, 5)
            client.publish('python/led_m4', semaforo_node)

        if len(dadosm5) > 2:
            semaforo_node = semaforo(dadosm5, 5)
            client.publish('python/led_m5', semaforo_node)

        if len(dadosteste) > 2:
            print("entrou na outra rotina")
            semaforo_node = semaforo(dadosteste, 5)
            client.publish('python/led_teste', semaforo_node)

    if msg.payload.decode() == "read_dados":
        # Código para lidar com a mensagem 'ligar'
        print("Comando executado")

        #---------------------------- Colocar aqui oq tem q ser feito --------------
        #read_line = True
        # Cria a canexcao no banco de dados e transforma em dataframe, os valores vem originais em m/s^2

        dados = read_query(connection_db, q1)

        hora_csv = datetime.datetime.now().strftime("%d-%m_%H-%M-%S")
        nome = dados["Location"][10]
        csv_name = f"{nome}_{hora_csv}.csv"
        dados.to_csv(csv_name, index=False)
        # Pega os dados da read_query que vem do banco de dados e transforma em mm/s
        valor_calculado = calculo_rms(dados)
        #print(valor_calculado)
        #print(type(valor_calculado))
        # Inserir informaçoes na tabela final
        read_query(connection_db, delete)
        read_query(connection_db, index_reiniciar)
        if valor_calculado[0][1] == 'MT1':
            insert_data_mt1(connection_db, valor_calculado)
        if valor_calculado[0][1] == 'MT2':
            insert_data_mt2(connection_db, valor_calculado)
        if valor_calculado[0][1] == 'MT3':
            insert_data_mt3(connection_db, valor_calculado)
        if valor_calculado[0][1] == 'MT4':
            insert_data_mt4(connection_db, valor_calculado)
        if valor_calculado[0][1] == 'MT5':
            insert_data_mt5(connection_db, valor_calculado)
        if valor_calculado[0][1] == 'teste':
            insert_data(connection_db, valor_calculado)
        #read_query(connection_db,delete)

    if msg.payload.decode() == "read_export":
        # Código para lidar com a mensagem 'desligar'
        print("Comando executado")

        hora_csv = datetime.datetime.now().strftime("%d-%m_%H-%M-%S")

        # Cria a canexcao no banco de dados e transforma em dataframe, os valores vem originais em m/s^2
        dados = read_query(connection_db, q1)

        nome = dados["Location"][10]
        csv_name = f"{nome}_{hora_csv}.csv"
        dados.to_csv(csv_name, index=False)
        # Pega os dados da read_query que vem do banco de dados e transforma em mm/s
        valor_calculado = calculo_rms(dados)
        #print(valor_calculado)
        # Inserir informaçoes na tabela final
        read_query(connection_db, delete)
        insert_data(connection_db, valor_calculado)




        # ---------------------------- Colocar aqui oq tem q ser feito --------------






#------------------------------------- ficar rodando com o main --------------------------------
#print("teste")

# Informacoes para conectar no banco de dados e data base acompanhar o read_query
connection_db = create_db_connection("localhost", "phpmyadmin", "admin","esp32_vibration")


# Cria a canexcao no banco de dados e transforma em dataframe, os valores vem originais em m/s^2
#dados = read_query(connection_db, q1)
#print(dados)
# Pega os dados da read_query que vem do banco de dados e transforma em mm/s
#valor_calculado = calculo_rms(dados)

#read_line = False

#-----------------------------------------------------------------------------------------------------
# Cria um cliente MQTT
client = mqtt.Client()

# Define as funções de callback
client.on_connect = on_connect
client.on_message = on_message

# Conecta-se ao broker MQTT
client.connect(broker_address, broker_port, 60)

# Inicia o loop para manter a conexão e processar as mensagens recebidas
client.loop_forever()

#------------------------------------------------------------------------------------------------



#print(valor_calculado)

# Inserir informaçoes na tabela final
#insert_data(connection_db, valor_calculado)

#dados.to_csv('bom.csv')
#print(df)
#print(dados)

#dados.to_excel("bom.xlsx", index=False)

#pd.ExcelWriter("motor27.xlsx", engine = "xlsxwriter")
#writer = pd.ExcelWriter("motor27.xlsx", engine = "xlsxwriter")
#df.to_excel(writer, sheet_name= "Sheet1")
#writer.save()

#print(df)


