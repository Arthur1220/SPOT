Claro! A seguir, apresento uma versão atualizada do seu arquivo `README.md`, incorporando as etapas detalhadas que você forneceu para resolver os problemas com o repositório RealSense e a compilação do SDK a partir do código-fonte.

---

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

- **Sistema Operacional**: Ubuntu 22.04 (Jammy) ou superior.
- **Câmera**: Intel RealSense D455.
- **Python**: Versão 3.6 ou superior.
- **Bibliotecas Python**: Listadas em `requirements.txt`.

## Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/SPOT.git
cd SPOT
```

### 2. Configure o Ambiente Virtual (Recomendado)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalando as Dependências Necessárias

Para compilar o Librealsense corretamente, precisamos garantir que todas as dependências estejam instaladas, incluindo aquelas que fornecem o arquivo `GL/glu.h`.

#### Passos:

1. **Atualize a Lista de Pacotes:**

   ```bash
   sudo apt-get update
   ```

2. **Instale as Dependências:**

   ```bash
   sudo apt-get install -y git cmake libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev
   ```

   **Descrição das Dependências:**

   - `git`: Ferramenta de controle de versão para clonar repositórios.
   - `cmake`: Ferramenta de automação de compilação.
   - `libssl-dev`: Bibliotecas de desenvolvimento para SSL.
   - `libusb-1.0-0-dev`: Bibliotecas de desenvolvimento para USB.
   - `pkg-config`: Ferramenta para gerenciar pacotes.
   - `libgtk-3-dev`: Bibliotecas de desenvolvimento para GTK+ 3.
   - `libglfw3-dev`: Bibliotecas de desenvolvimento para GLFW (biblioteca OpenGL).
   - `libgl1-mesa-dev`: Bibliotecas de desenvolvimento para OpenGL.
   - `libglu1-mesa-dev`: Bibliotecas de desenvolvimento para GLU (OpenGL Utility Library).

3. **Verifique se o Arquivo `glu.h` Está Presente:**

   ```bash
   ls /usr/include/GL/glu.h
   ```

   Você deve ver o caminho para o arquivo sem erros. Se não estiver presente, tente reinstalar o pacote:

   ```bash
   sudo apt-get install --reinstall libglu1-mesa-dev
   ```

### 4. Compilando o SDK da Intel RealSense a Partir do Código-Fonte

Como o repositório oficial estava inacessível, a melhor alternativa é compilar o SDK a partir do código-fonte.

#### Passos:

1. **Clone o Repositório do Librealsense:**

   ```bash
   git clone https://github.com/IntelRealSense/librealsense.git
   cd librealsense
   ```

2. **Verifique a Versão Estável Mais Recente (Opcional):**

   ```bash
   git checkout $(git tag | grep ^v | sort -V | tail -1)
   ```

3. **Crie um Diretório de Compilação e Entre Nele:**

   ```bash
   mkdir build && cd build
   ```

4. **Configure a Compilação com CMake:**

   ```bash
   cmake .. -DBUILD_EXAMPLES=true
   ```

   **Nota:** A opção `-DBUILD_EXAMPLES=true` compila os exemplos fornecidos pelo SDK. Se você não precisar dos exemplos, pode omitir essa opção.

5. **Compile o SDK:**

   ```bash
   make -j$(nproc)
   ```

   **Explicação:**

   - `-j$(nproc)`: Utiliza todos os núcleos disponíveis do processador para acelerar a compilação.

6. **Instale o SDK Compilado:**

   ```bash
   sudo make install
   ```

7. **Atualize o Cache de Bibliotecas:**

   ```bash
   sudo ldconfig
   ```

### 5. Instalando a Biblioteca Python `pyrealsense2`

Agora que o SDK está instalado, precisamos garantir que a biblioteca Python `pyrealsense2` esteja disponível para o seu projeto.

#### Passos:

1. **Instale a Biblioteca Usando `pip`:**

   ```bash
   pip install pyrealsense2 --user
   ```

   **Nota:** O parâmetro `--user` instala o pacote para o usuário atual, evitando a necessidade de permissões de superusuário.

2. **Alternativa (Usando Ambiente Virtual):**

   É altamente recomendável usar ambientes virtuais para gerenciar as dependências do seu projeto isoladamente.

   ```bash
   # Crie um ambiente virtual chamado 'venv' (se ainda não tiver criado)
   python3 -m venv venv

   # Ative o ambiente virtual
   source venv/bin/activate

   # Instale as dependências dentro do ambiente virtual
   pip install -r requirements.txt
   ```

### 6. Executando o Aplicativo

Com todas as dependências e o SDK instalados, você está pronto para executar o aplicativo.

```bash
python interface.py
```

## Uso

1. **Conecte a câmera Intel RealSense D455** ao computador.
2. **Execute o aplicativo** conforme o passo acima.
3. **Na tela inicial**, você pode:
   - **Iniciar o sistema**: Se a câmera estiver conectada, o sistema iniciará.
   - **Visualizar informações**: Ver os dados armazenados até o momento.

## Estrutura do Projeto

- `camera_system.py`: Módulo responsável pela interação com a câmera Intel RealSense.
- `database.py`: Módulo para interação com o banco de dados SQLite.
- `interface.py`: Aplicação principal com a interface gráfica.
- `requirements.txt`: Lista das dependências necessárias.
- `README.md`: Este arquivo, contendo informações sobre o projeto.