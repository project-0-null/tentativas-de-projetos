import importlib
import subprocess
import sys

def check_python_package(package_name):
    try:
        importlib.import_module(package_name)
        print(f"✓ {package_name} está instalado")
        return True
    except ImportError:
        print(f"✗ {package_name} NÃO está instalado")
        return False

def check_system_dependency(command):
    try:
        result = subprocess.run(['which', command], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {command} está instalado")
            return True
        else:
            print(f"✗ {command} NÃO está instalado")
            return False
    except Exception as e:
        print(f"Erro ao verificar {command}: {e}")
        return False

print("=== VERIFICANDO DEPENDÊNCIAS DO SISTEMA ===")
check_system_dependency('ffmpeg')
check_system_dependency('python3')
check_system_dependency('pip3')

print("\n=== VERIFICANDO BIBLIOTECAS PYTHON ===")
packages = ['cv2', 'torch', 'torchvision']
for package in packages:
    check_python_package(package)

print("\n=== VERIFICANDO YOLOv5 ===")
try:
    import torch
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True, skip_validation=True)
    print("✓ YOLOv5 carregado com sucesso")
except Exception as e:
    print(f"✗ Erro ao carregar YOLOv5: {e}")

print("\nVerificação concluída!")