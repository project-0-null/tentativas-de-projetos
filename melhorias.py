import cv2
import torch

try:
    # Carrega o modelo YOLOv5 nano (correto)
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
except Exception as e:
    print(f"Erro ao carregar o modelo YOLO: {e}")
    print("Certifique-se de que a biblioteca 'ultralytics' está instalada corretamente e há conexão com a internet para baixar o modelo na primeira vez.")
    exit()

urlstream = 'http://172.16.30.124/stream'
wcam = cv2.VideoCapture(urlstream, cv2.CAP_FFMPEG)

if not wcam.isOpened():
    print("Erro: não foi possível abrir a webcam")
    exit()

frame_counter = 0
last_annotated_frame = None

while True:
    ret, frame = wcam.read()
    
    if not ret:
        print("Erro ao capturar o frame")
        break

    frame_counter += 1
    
    # Processa a cada 10 frames para melhor performance
    if frame_counter % 10 == 0:
        # Converte BGR para RGB (YOLO espera RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(rgb_frame)
        
        # Verifica se há pessoas detectadas
        person_detected = False
        for det in results.pred[0]:
            class_id = int(det[5])
            class_name = model.names[class_id]
            
            if class_name == 'person':
                person_detected = True
                # Não break aqui para detectar múltiplas pessoas
                
        if person_detected:
            print("Pessoa detectada!")
        
        # Renderiza as anotações
        annotated_frame = results.render()[0]
        # Converte de volta para BGR para exibição no OpenCV
        last_annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

    # Exibe o frame (anotado ou original)
    display_frame = last_annotated_frame if last_annotated_frame is not None else frame
    cv2.imshow('Stream ESP32-CAM com YOLOv5', display_frame)

    # Verifica se o usuário quer sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Encerrando...")
wcam.release()
cv2.destroyAllWindows()