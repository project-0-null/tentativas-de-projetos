import cv2
import torch
from datetime import datetime, timezone # <-- NOVO
import json                         # <-- NOVO

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU device: {torch.cuda.get_device_name(0)}")
    print(f"CUDA version: {torch.version.cuda}")

try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True).cuda() if torch.cuda.is_available() else torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
except Exception as e:
    print(f"Erro ao carregar o modelo YOLO: {e}")
    exit()

urlstream = 'http://172.16.30.124/stream'
wcam = cv2.VideoCapture(0)

if not wcam.isOpened():
    print("error nao foi possivel abrir a webcam")
    exit()

frame_counter = 0
last_annotated_frame = None

while True:
    ret, frame = wcam.read()
    if not ret:
        print("erro ao capturar o frame")
        break

    frame_counter += 1
    if frame_counter % 10 == 0:
        results = model(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        for det in results.pred[0]:
            class_id = int(det[5])
            class_name = model.names[class_id]

            if class_name == 'person':
                # --- INÍCIO DO BLOCO FIWARE --- # <-- NOVO
                
                # 1. Obter o horário atual no formato padrão (ISO 8601 UTC)
                timestamp_utc = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                
                # 2. Criar um ID único para cada evento de detecção
                detection_id = f"urn:ngsi-ld:PersonDetection:{timestamp_utc}"

                # 3. Construir o dicionário Python no modelo FIWARE NGSI-LD
                fiware_entity = {
                    "id": detection_id,
                    "type": "PersonDetection",
                    "status": {
                        "type": "Property",
                        "value": "detected",
                        "observedAt": timestamp_utc
                    },
                    # "location": { # Futuramente, o local virá aqui
                    #     "type": "GeoProperty",
                    #     "value": {
                    #         "type": "Point",
                    #         "coordinates": [ x, y ] 
                    #     }
                    # },
                    "@context": [
                        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context-v1.3.jsonld"
                    ]
                }
                
                # 4. Imprimir o dicionário formatado como um JSON no console
                print("\n--- Entidade FIWARE Gerada ---")
                print(json.dumps(fiware_entity, indent=4))
                print("----------------------------\n")

                # --- FIM DO BLOCO FIWARE --- #
                break # Interrompe o loop 'for' pois já achamos uma pessoa neste frame
        
        annotated_frame = results.render()[0]
        # Linha correta
        last_annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

    if last_annotated_frame is not None:
        cv2.imshow('Stream ESP32-CAM com YOLOv5', last_annotated_frame)
    else:
        cv2.imshow('Stream ESP32-CAM com YOLOv5', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("encerrando...")
wcam.release()
cv2.destroyAllWindows()