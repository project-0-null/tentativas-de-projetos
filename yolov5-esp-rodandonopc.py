import cv2
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU device: {torch.cuda.get_device_name(0)}")
    print(f"CUDA version: {torch.version.cuda}")

try:
   # model =  torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True).cuda() if torch.cuda.is_available() else torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
except Exception as e:
    print(f"Erro ao carregar o modelo YOLO: {e}")
    print("Certifique-se de que a biblioteca 'ultralytics' está instalada corretamente e há conexão com a internet para baixar o modelo na primeira vez.")
    exit()
    #carrega o modelo YOLOv8 nano

urlstream = 'http://172.16.30.124/stream'
#mudar conforme o ip do esp32 mostrado na ide



#wcam = cv2.VideoCapture(urlstream)
wcam = cv2.VideoCapture(0)

#pra colocar o esp32 é só trocar o 0 pelo ip do video stream do esp32

if not wcam.isOpened():
    print("error nao foi possivel abrir a webcam")
    exit()

frame_counter = 0
last_annotated_frame = None

while True:
    ret,frame = wcam.read()
    #ret é um booleano que indica se o frame foi lido com sucesso
    # frame é o próprio quadro da imagem capturada

    if not ret:
        print("erro ao capturar o frame")
        break
    #cv2.imshow('yolou', frame)

    frame_counter += 1
    if frame_counter % 10 == 0:

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        results = model(frame)
        #realiza a detecção de objetos no frame capturado

        results = model(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        person_detected = False
        for det in results.pred[0]:
            class_id = int(det[5])
            class_name = model.names[class_id]

            if class_name =='person':
                person_detected = True
                break
            
            if person_detected:
                print("Pessoa detectada!")
                

        if person_detected:
            print("Pessoa detectada!")

        annotated_frame = results.render()[0]
        #desenha as caixinhas e os nomes dos obj dectados

        last_annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
        #volta pra BGR pro opencv
    if last_annotated_frame is not None:
        cv2.imshow('Stream ESP32-CAM com YOLOv5', last_annotated_frame)
    else:
        cv2.imshow('Stream ESP32-CAM com YOLOv5', frame)
    #exibe o frame com todos os desenhos bonitinhos


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("encerrando...")
wcam.release()
cv2.destroyAllWindows()