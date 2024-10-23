## README.md

```markdown
# SPOT - Sistema Peso Ovino Tridimensional

O projeto SPOT é um sistema desenvolvido para capturar informações tridimensionais de ovinos, com o objetivo de auxiliar na predição de peso e outras métricas relevantes na pecuária. O sistema utiliza a câmera Intel RealSense D455 para capturar imagens coloridas e de profundidade, permitindo a análise e armazenamento de dados para futuras implementações de machine learning.

## Funcionalidades

- **Captura de Dados**: Coleta de imagens coloridas e de profundidade, medição de distância e cálculo de área.
- **Entrada de Peso**: Permite que o usuário insira o peso do ovino manualmente.
- **Armazenamento de Dados**: Salva todas as informações em um banco de dados SQLite, incluindo as imagens capturadas.
- **Visualização de Dados**: Possibilidade de visualizar os dados armazenados anteriormente.
- **Interface Amigável**: Interface gráfica intuitiva utilizando o `customtkinter`.
- **Detecção de Câmera**: Sistema aguarda a conexão da câmera antes de iniciar ou permite visualizar dados anteriores.

## Requisitos

- Python 3.6 ou superior.
- Câmera Intel RealSense D455.
- Bibliotecas Python listadas em `requirements.txt`.

## Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/Arthur1220/SPOT.git
   cd SPOT
   ```

2. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Instale o Intel RealSense SDK 2.0**:

   - **Para Ubuntu**:

     ```bash
     sudo apt-key adv --keyserver keys.gnupg.net --recv-key 49EFB2CF
     sudo add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo focal main" -u
     sudo apt-get install librealsense2-dkms librealsense2-utils librealsense2-dev librealsense2-dbg
     ```

   - **Para Windows**:

     Baixe o SDK em [Intel RealSense SDK 2.0 Releases](https://github.com/IntelRealSense/librealsense/releases) e siga as instruções do instalador.

## Uso

1. **Conecte a câmera Intel RealSense D455** ao computador.

2. **Execute o aplicativo**:

   ```bash
   python interface.py
   ```

3. **Na tela inicial**, você pode:

   - **Iniciar o sistema**: Se a câmera estiver conectada, o sistema iniciará.
   - **Visualizar informações**: Ver os dados armazenados até o momento.

## Estrutura do Projeto

- `camera_system.py`: Módulo responsável pela interação com a câmera Intel RealSense.
- `database.py`: Módulo para interação com o banco de dados SQLite.
- `interface.py`: Aplicação principal com a interface gráfica.
- `requirements.txt`: Lista das dependências necessárias.
- `README.md`: Este arquivo, contendo informações sobre o projeto.