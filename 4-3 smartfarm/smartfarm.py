# ================================
# 스마트 팜 센서 시스템 (최종 완성본)
# ================================

print("START")

# ===== 라이브러리 =====
import random
import threading
import time
from datetime import datetime
from queue import Queue

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


# ================================
# 1. 센서 클래스
# ================================
class ParmSensor:
    def __init__(self, name):
        self.name = name
        self.temperature = 0
        self.light = 0
        self.humidity = 0

    def SetData(self):
        self.temperature = random.randint(20, 30)
        self.light = random.randint(5000, 10000)
        self.humidity = random.randint(40, 70)

    def GetData(self):
        return self.temperature, self.light, self.humidity


# ================================
# 2. 전역 Queue
# ================================
sensor_queue = Queue()


# ================================
# 3. MySQL 연결
# ================================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0000",   # 본인 비밀번호
    database="smartfarm"
)

cursor = conn.cursor()


# ================================
# 4. DB INSERT 함수
# ================================
def insert_sensor_data(data):
    sql = """
    INSERT INTO parm_data (sensor_name, input_time, temperature, light, humidity)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, data)
    conn.commit()


# ================================
# 5. 센서 쓰레드 (Producer)
# ================================
def sensor_worker(sensor):
    print(f"{sensor.name} thread started")  # 디버그용

    while True:
        sensor.SetData()
        temp, light, humi = sensor.GetData()

        now = datetime.now()

        print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} "
              f"{sensor.name} — temp {temp}, light {light}, humi {humi}")

        # Queue에 저장
        sensor_queue.put((sensor.name, now, temp, light, humi))

        time.sleep(10)


# ================================
# 6. DB 쓰레드 (Consumer)
# ================================
def db_worker():
    print("DB thread started")  # 디버그용

    while True:
        if not sensor_queue.empty():
            data = sensor_queue.get()
            insert_sensor_data(data)

        time.sleep(1)


# ================================
# 7. 데이터 조회
# ================================
def get_sensor_data():
    cursor.execute("SELECT * FROM parm_data")
    return cursor.fetchall()


# ================================
# 8. 그래프
# ================================
def plot_temperature():
    data = get_sensor_data()

    df = pd.DataFrame(data, columns=[
        "id", "sensor", "time", "temp", "light", "humi"
    ])

    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    result = df.groupby("sensor")['temp'].resample('1H').mean()

    result.unstack(0).plot()

    # 습도 90 이상 표시
    high_humi = df[df['humi'] > 90]
    plt.scatter(high_humi.index, high_humi['temp'], marker='*')

    plt.title("Sensor Temperature Average")
    plt.xlabel("Time")
    plt.ylabel("Temperature")

    plt.show()


# ================================
# 9. 메인 실행
# ================================
if __name__ == "__main__":

    print("MAIN START")

    # 센서 5개 생성
    sensors = [ParmSensor(f"Parm-{i}") for i in range(1, 6)]

    # 센서 쓰레드 실행
    for s in sensors:
        t = threading.Thread(target=sensor_worker, args=(s,))
        t.daemon = True
        t.start()

    # DB 쓰레드 실행
    db_thread = threading.Thread(target=db_worker)
    db_thread.daemon = True
    db_thread.start()

    # 프로그램 유지
    while True:
        time.sleep(1)
