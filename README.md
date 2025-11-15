# 🚭 Detector de Fumantes - Visão Computacional

Sistema de detecção de fumantes em áreas restritas utilizando YOLOv8 e Python.

![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10+-blue.svg)
![YOLO](https://img.shields.io/badge/YOLOv8-8.0+-purple.svg)
## 📖 Sobre o Projeto

Sistema de visão computacional desenvolvido com intensivos treinamentos utilizando datasets customizados no Roboflow. O projeto visa reforçar a saúde e segurança ocupacional em áreas onde fumar é proibido. O detector identifica fumantes em tempo real através de câmeras, registra evidências e gera alertas para os responsáveis, respeitando os princípios da ISO 31000.

### 🎯 Funcionalidades Principais

-  **Detecção em tempo real** de pessoas, cigarros e gestos de fumar.
-  **Sistema de alerta** com cooldown para evitar spam.
-  **Captura de evidências** com imagens anotadas.
-  **Registro automático** em planilha CSV com data-hora, local e caminho para o registro em imagem.
-  **Interface visual** com feedback em tempo real.
-  **Multiplataforma** Windows, Linux, Mac (exceto pelo envio de e-mail, que no momento é exclusivo para windows).

## 🛠️ Tecnologias e Bibliotecas Utilizadas

- **Visão Computacional**: [OpenCV](https://opencv.org/), [YOLOv8 (Ultralytics)](https://docs.ultralytics.com/pt/models/yolov8/)
- **Machine Learning**: [PyTorch](https://pytorch.org/)
- **Análise de Dados**: [Pandas](https://pandas.pydata.org/)
- **Gerenciamento de Arquivos**: [os](https://docs.python.org/3/library/os.html), [Pathlib](https://docs.python.org/3/library/pathlib.html)
- **Desenvolvimento**: [Python 3.8+](https://www.python.org/)

## 💻 Como Executar
 1. Clone o repositório.
```bash
    git clone https://github.com/TAMSnow/Smoke_Detector.git
```
2. Instale as dependências.
```
    pip install -r requirements.txt
```
 3. Execute em seu computador (é necessário ter uma câmera conectada).
```
    python detectorPrincipal.py
```

## ☀️ Possíveis Futuros
- Integração com câmeras IP.
- Analise estatística de horarios de pico e locais com mais registros.


## 👥 Autores
- [Gabriel Felipe](https://github.com/gabrielf-elipe)
- [Tales Artur](https://github.com/TAMSnow)
- [Henrique Maia](https://github.com/hmr-25)

