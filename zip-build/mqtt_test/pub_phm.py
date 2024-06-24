import time
import json
import os
import awsiot.greengrasscoreipc.clientv2 as clientV2
from awsiot.greengrasscoreipc.model import QOS

#phm thing name 가져오기

# 첫번째 : 저장된 파일 경로에서 불러오기 

#Location for certification files
cert_path = "/root/"
data_path ="/greengrass/mqtt_test/"
#Thing name file(S/N)
ThingNameFile = cert_path + "ThingName"
result_file = data_path +"data.json"

def read_file(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            value = file.read()
            if value is not None:
                return value.strip()
    else:
            return NULL;
        
 # Thing Name 읽어오기
TSN = read_file(ThingNameFile)


# Define the topic, QoS, and payload
topic = f"MO/PHM/{TSN}/HDI/PHM_TEST/STATE-NOTIFIER/INFO"
qos = QOS.AT_LEAST_ONCE  # QoS 1
#payload = 'Hello, phm World'

# 파일이 있는지 30초 간격으로 확인하여 data load
while True:
    if os.path.exists(result_file):                
        with open(result_file, 'r') as json_file:
            data = json.load(json_file)    

        payload =json.dumps(data)

        # Create an IPC client
        ipc_client = clientV2.GreengrassCoreIPCClientV2()

        try:
            while True:
                # Publish the message
                try:
                    resp = ipc_client.publish_to_iot_core(
                        topic_name=topic,
                        qos=qos,
                        payload=payload
                    )
                    print(f"Sent `{payload}` to topic `{topic}`")
                except Exception as e:
                    print(f"Failed to publish message: {e}")
                
                # Wait for 30 minutes (30 * 60 seconds)
                time.sleep(1800)

        except KeyboardInterrupt:
            print("Exiting...")

        finally:
            # Close the IPC client
            ipc_client.close()
    
    else :
        print(f'File does not exist')
    
    time.sleep(30)