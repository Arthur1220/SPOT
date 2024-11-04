import customtkinter
from PIL import Image, ImageTk  
from database import salvar_informacoes, initialize_database, fetch_all_records
from camera_system import DepthCamera
import cv2  
import numpy as np
import tkinter as tk
from tkinter import messagebox  # Importa o messagebox
import sqlite3

class InitialScreen(customtkinter.CTk):
    """Tela inicial que aguarda a conexão da câmera ou permite visualizar dados armazenados."""
    def __init__(self):
        super().__init__()
        self.title("SPOT - Sistema Peso Ovino Tridimensional")
        self.geometry("400x400")
        self.resizable(False, False)
        customtkinter.set_appearance_mode("dark")  

        try:
            logo_image = customtkinter.CTkImage(
                light_image=Image.open("SPOT_images/sheep_2.png"), 
                dark_image=Image.open("SPOT_images/sheep_2.png"), 
                size=(200, 200)  
            )
            self.logo_label = customtkinter.CTkLabel(self, image=logo_image, text="")
            self.logo_label.image = logo_image  # Mantém uma referência para evitar coleta de lixo
            self.logo_label.pack(pady=10)
        except Exception as e:
            print(f"Erro ao carregar o logotipo: {e}")

        self.label = customtkinter.CTkLabel(self, text="Bem-vindo ao SPOT", font=("Helvetica", 20))
        self.label.pack(pady=20)

        self.status_label = customtkinter.CTkLabel(self, text="Verificando conexão da câmera...", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.pack(pady=20)

        self.start_button = customtkinter.CTkButton(
            self.button_frame, text="Iniciar Sistema", command=self.start_system
        )
        self.start_button.pack(side="left", padx=10)

        self.view_button = customtkinter.CTkButton(
            self.button_frame, text="Visualizar Informações", command=self.view_data
        )
        self.view_button.pack(side="right", padx=10)

        self.check_camera_connection()

    def check_camera_connection(self):
        """Verifica se a câmera está conectada."""
        try:
            self.dc = DepthCamera()
            self.status_label.configure(text="Câmera conectada.")
            self.start_button.configure(state="normal")
        except RuntimeError:
            self.status_label.configure(text="Câmera não encontrada.")
            self.start_button.configure(state="disabled")
        # Sempre fecha a conexão para evitar conflitos
        try:
            self.dc.release()
        except:
            pass

    def start_system(self):
        """Inicia o sistema principal."""
        self.destroy()
        app = App()
        app.mainloop()

    def view_data(self):
        """Abre a janela de visualização de dados."""
        self.destroy()
        viewer = DataViewer()
        viewer.mainloop()

class DataViewer(customtkinter.CTk):
    """Janela para visualizar os dados armazenados."""
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Dados - SPOT")
        self.geometry("800x600")
        self.resizable(False, False)
        customtkinter.set_appearance_mode("dark")  

        self.label = customtkinter.CTkLabel(self, text="Dados Armazenados", font=("Helvetica", 20))
        self.label.pack(pady=10)

        # Tabela para exibir os registros
        self.table_frame = customtkinter.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_data()

    def load_data(self):
        """Carrega os dados do banco de dados e exibe na tabela."""
        records = fetch_all_records()
        if not records:
            no_data_label = customtkinter.CTkLabel(self.table_frame, text="Nenhum dado armazenado.")
            no_data_label.pack()
            return

        # Cabeçalhos da tabela
        headers = ["ID", "Peso (kg)", "Área (cm²)", "Distância (cm)", "Data e Hora"]
        for col, header in enumerate(headers):
            header_label = customtkinter.CTkLabel(self.table_frame, text=header, font=("Arial", 12, "bold"))
            header_label.grid(row=0, column=col, padx=5, pady=5)

        # Linhas da tabela
        for row_num, record in enumerate(records, start=1):
            for col_num, value in enumerate(record[:5]):
                cell = customtkinter.CTkLabel(self.table_frame, text=str(value))
                cell.grid(row=row_num, column=col_num, padx=5, pady=5)

            # Botão para visualizar as imagens
            view_button = customtkinter.CTkButton(
                self.table_frame, text="Ver Imagens", command=lambda r=record: self.show_images(r)
            )
            view_button.grid(row=row_num, column=len(headers), padx=5, pady=5)

    def show_images(self, record):
        """Exibe as imagens armazenadas de um registro específico."""
        image_window = customtkinter.CTkToplevel(self)
        image_window.title(f"Imagens do Registro {record[0]}")
        image_window.geometry("700x500")

        # Converte os bytes de imagem de volta para imagens
        imagem_color_bytes = record[5]
        imagem_depth_bytes = record[6]

        color_array = cv2.imdecode(np.frombuffer(imagem_color_bytes, np.uint8), cv2.IMREAD_COLOR)
        depth_array = cv2.imdecode(np.frombuffer(imagem_depth_bytes, np.uint8), cv2.IMREAD_COLOR)

        # Converte para RGB
        color_frame_rgb = cv2.cvtColor(color_array, cv2.COLOR_BGR2RGB)
        img_color = Image.fromarray(color_frame_rgb)
        img_color_tk = ImageTk.PhotoImage(image=img_color)

        img_depth = Image.fromarray(depth_array)
        img_depth_tk = ImageTk.PhotoImage(image=img_depth)

        # Exibe as imagens
        label_color = customtkinter.CTkLabel(image_window, image=img_color_tk)
        label_color.image = img_color_tk
        label_color.pack(side="left")

        label_depth = customtkinter.CTkLabel(image_window, image=img_depth_tk)
        label_depth.image = img_depth_tk
        label_depth.pack(side="right")

class MyFrameInfo(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=210, height=80)
        """Frame para exibir distância e área."""

        self.label_distancia = customtkinter.CTkLabel(self, font=("Arial",14), text="Distância:")
        self.label_distancia.place(x=12, y=10)

        self.distancia_var = customtkinter.StringVar()
        self.distancia_var.set("0 cm")

        self.distancia_display = customtkinter.CTkLabel(self, font=("Arial",14), textvariable=self.distancia_var)
        self.distancia_display.place(x=115, y=10)

        self.label_area = customtkinter.CTkLabel(self, font=("Arial",14), text="Área:")
        self.label_area.place(x=12, y=40)

        self.area_var = customtkinter.StringVar()
        self.area_var.set("0 cm²")

        self.area_display = customtkinter.CTkLabel(self, font=("Arial",14), textvariable=self.area_var)
        self.area_display.place(x=115, y=40)
    
    def update_distancia(self, distance):
        """Atualiza a exibição da distância."""
        self.distancia_var.set("{:.2f} cm".format(distance))
    
    def update_area(self, area):
        """Atualiza a exibição da área."""
        self.area_var.set("{:.2f} cm²".format(area))

class MyFramePeso(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=210, height=80)
        """Frame para entrada e exibição do peso."""

        self.label_peso = customtkinter.CTkLabel(self, font=("Arial",14), text="Peso estimado:")
        self.label_peso.place(x=12, y=10)
        
        # Campo de entrada para o usuário inserir o peso
        self.peso_entry = customtkinter.CTkEntry(self, font=("Arial",14), width=80)
        self.peso_entry.place(x=115, y=10)
        
        # Variável para exibir o peso
        self.peso_var = customtkinter.StringVar()
        self.peso_var.set("0.0 kg")

        self.peso_display = customtkinter.CTkLabel(self, font=("Arial",14), textvariable=self.peso_var)
        self.peso_display.place(x=115, y=40)

class MyFrameConfig(customtkinter.CTkFrame):
    def __init__(self, master, camera_frame=None, **kwargs):
        super().__init__(master, **kwargs, width=250, height=500)
        """Frame principal de configuração."""
        self.camera_frame = camera_frame

        self.label_title = customtkinter.CTkLabel(self, font=("Helvetica", 30), text="SPOT")
        self.label_title.place(x=80, y=10)

        self.image = customtkinter.CTkImage(
            light_image=Image.open("SPOT_images/sheep_2.png"), 
            dark_image=Image.open("SPOT_images/sheep_2.png"), 
            size=(150, 150)
        )
        self.image_label = customtkinter.CTkLabel(self, image=self.image, text="")
        self.image_label.place(x=50, y=40) 

        # Instâncias dos frames de informação e peso
        self.my_frameInfo = MyFrameInfo(master=self)
        self.my_frameInfo.place(x=20, y=230)

        self.my_framePeso = MyFramePeso(master=self)
        self.my_framePeso.place(x=20, y=315)

        self.check_var = customtkinter.StringVar(value="Ligado")
        self.checkbox = customtkinter.CTkCheckBox(
            self, font=("Arial",14), fg_color="white", border_color="black", hover_color="gray",
            text="Utilizar sistema de predição", command=self.checkbox_Event, variable=self.check_var,
            onvalue="Ligado", offvalue="Desligado"
        )
        self.checkbox.place(x=20, y=390)

        self.button = customtkinter.CTkButton(
            self, font=("Arial",16), text_color="black", fg_color="white", hover_color="gray",
            text="Registrar peso", command=self.registrar_Click, hover=True, width=210, height=60
        )
        self.button.place(x=20, y=430)

    def checkbox_Event(self):
        """Evento ao alterar a caixa de seleção."""
        print("Caixa de seleção alterada, valor atual:", self.check_var.get())

    def registrar_Click(self):
        """Evento ao clicar no botão 'Registrar peso'."""
        # Obtém o peso inserido pelo usuário
        peso_text = self.my_framePeso.peso_entry.get()
        if not peso_text:
            messagebox.showwarning("Aviso", "Por favor, insira o peso.")
            return
        try:
            peso_float = float(peso_text)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico para o peso.")
            return

        distancia_text = self.my_frameInfo.distancia_var.get().replace(" cm", "")
        area_text = self.my_frameInfo.area_var.get().replace(" cm²", "")

        try:
            distancia_float = float(distancia_text)
            area_float = float(area_text)
        except ValueError:
            messagebox.showerror("Erro", "Erro ao converter distância ou área.")
            return

        # Obtém os frames mais recentes da câmera
        color_frame = self.camera_frame.latest_color_frame
        depth_frame = self.camera_frame.latest_depth_frame

        if color_frame is None or depth_frame is None:
            messagebox.showerror("Erro", "Não foi possível obter os frames da câmera.")
            return

        # Processa o frame de profundidade para criar uma imagem colorida (padrão de temperatura)
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_frame, alpha=0.03), cv2.COLORMAP_JET
        )

        # Converte as imagens para bytes
        _, buffer_color = cv2.imencode('.jpg', color_frame)
        imagem_color_bytes = buffer_color.tobytes()

        _, buffer_depth = cv2.imencode('.jpg', depth_colormap)
        imagem_depth_bytes = buffer_depth.tobytes()

        # Salva os dados no banco de dados
        salvar_informacoes(peso_float, distancia_float, area_float, imagem_color_bytes, imagem_depth_bytes)

        # Exibe um popup de confirmação
        messagebox.showinfo("Sucesso", "Informações salvas com sucesso!")

        # Exibe as imagens capturadas
        #self.display_captured_images(color_frame, depth_colormap)

        # Opcional: Limpar o campo de entrada após salvar
        self.my_framePeso.peso_entry.delete(0, tk.END)

    def display_captured_images(self, color_frame, depth_colormap):
        """Exibe as imagens capturadas em uma nova janela."""
        # Cria uma nova janela Toplevel
        image_window = customtkinter.CTkToplevel(self)
        image_window.title("Imagens Capturadas")
        image_window.geometry("700x500")

        # Converte o frame de cor para RGB e cria uma imagem Tkinter
        color_frame_rgb = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)
        img_color = Image.fromarray(color_frame_rgb)
        img_color_tk = ImageTk.PhotoImage(image=img_color)

        # Converte o colormap de profundidade para imagem Tkinter
        img_depth = Image.fromarray(depth_colormap)
        img_depth_tk = ImageTk.PhotoImage(image=img_depth)

        # Cria labels para exibir as imagens
        label_color = customtkinter.CTkLabel(image_window, image=img_color_tk)
        label_color.image = img_color_tk  # Mantém uma referência
        label_color.pack(side="left")

        label_depth = customtkinter.CTkLabel(image_window, image=img_depth_tk)
        label_depth.image = img_depth_tk  # Mantém uma referência
        label_depth.pack(side="right")

class MyFrameCamera(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=662, height=500)
        """Frame que exibe o vídeo da câmera."""
        self.master = master
        try:
            # Inicializa a câmera Intel RealSense
            self.dc = DepthCamera()
        except RuntimeError:
            print("Erro: Nenhum dispositivo conectado")
            exit()

        # Coordenadas para o ponto de medição de distância
        self.point = (330, 245)

        self.label = customtkinter.CTkLabel(self, text="")
        self.label.place(x=10, y=10)

        self.latest_color_frame = None
        self.latest_depth_frame = None

        # Inicia o loop de atualização de vídeo
        self.update_video()
    
    def update_video(self):
        """Atualiza o vídeo exibido no frame."""
        # Captura um frame da câmera RealSense
        ret, depth_frame, color_frame = self.dc.get_frame()
        if ret:
            self.latest_color_frame = color_frame
            self.latest_depth_frame = depth_frame

            # Calcula a distância do ponto de interesse à câmera usando o frame de profundidade
            distance = depth_frame[self.point[1], self.point[0]] / 10.0  # Converte para cm

            # Atualiza a exibição da distância
            self.master.my_frameConfig.my_frameInfo.update_distancia(distance)

            # Calcula a área do objeto em frente à câmera
            area = self.calculate_area(depth_frame)
            self.master.my_frameConfig.my_frameInfo.update_area(area)

            # Desenha um círculo no frame de cor no ponto de interesse
            cv2.circle(color_frame, self.point, 4, (255, 255, 255))

            # Converte o frame de cores para o formato RGB
            color_frame_rgb = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)

            # Converte o frame para um objeto Image do PIL
            img = Image.fromarray(color_frame_rgb)

            # Converte o objeto Image para o formato que pode ser exibido no Tkinter
            img_tk = ImageTk.PhotoImage(image=img)

            # Atualiza o rótulo Tkinter com o novo frame
            self.label.imgtk = img_tk
            self.label.configure(image=img_tk)

        # Agenda esta função para ser chamada novamente após 10 milissegundos
        self.after(10, self.update_video)

    def calculate_area(self, depth_frame):
        """Calcula a área do objeto principal na imagem de profundidade."""
        # Define um limiar de profundidade para segmentação
        depth_threshold = 1000  # Ajuste conforme necessário
        _, depth_thresh = cv2.threshold(depth_frame, depth_threshold, 65535, cv2.THRESH_BINARY_INV)
        
        # Converte para imagem de 8 bits
        depth_thresh_8u = cv2.convertScaleAbs(depth_thresh, alpha=255.0/65535.0)

        # Encontra contornos na imagem limiar
        contours, _ = cv2.findContours(depth_thresh_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Assume que o maior contorno é o objeto de interesse
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            # Opcional: desenha o contorno no frame de cor
            # cv2.drawContours(self.latest_color_frame, [largest_contour], -1, (0, 255, 0), 2)
        else:
            area = 0.0
        return area

class App(customtkinter.CTk):
    """Aplicação principal."""
    def __init__(self):
        super().__init__()
        self.title("SPOT - Sistema Peso Ovino Tridimensional")
        self.geometry("960x540")
        self.resizable(False, False)
        customtkinter.set_appearance_mode("dark")  

        self.my_frameConfig = MyFrameConfig(master=self)
        self.my_frameConfig.place(x=690, y=20)

        self.my_frameCamera = MyFrameCamera(master=self)
        self.my_frameCamera.place(x=20, y=20)

        self.my_frameConfig.camera_frame = self.my_frameCamera

    def view_data(self):
        """Abre a janela de visualização de dados a partir da tela principal."""
        viewer = DataViewer()
        viewer.mainloop()

if __name__ == "__main__":
    initialize_database()
    initial_screen = InitialScreen()
    initial_screen.mainloop()