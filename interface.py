import customtkinter

# Biblioteca para manipulação de imagens
from PIL import Image, ImageTk  

# Modulo para salvar as informacoes em arquivo .csv
from database import salvar_informacoes

# Módulo para interagir com câmeras RealSense
from camera_system import *  

# OpenCV para manipulação de vídeo e imagem
import cv2  

class MyFrameInfo(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=210, height=80)

        self.label = customtkinter.CTkLabel(self, font=("Arial",14), text="Distância:")
        self.label.place(x=12, y=10)

        global distancia_var
        distancia_var = customtkinter.StringVar()
        distancia_var.set("0 cm")

        self.distancia_display = customtkinter.CTkLabel(self, font=("Arial",14), textvariable=distancia_var)
        self.distancia_display.place(x=115, y=10)

        self.label = customtkinter.CTkLabel(self, font=("Arial",14), text="Área:")
        self.label.place(x=12, y=40)

        global area_var
        area_var = customtkinter.StringVar()
        area_var.set("0 cm²")

        self.area_display = customtkinter.CTkLabel(self, font=("Arial",14), textvariable=area_var)
        self.area_display.place(x=115, y=40)

    def update_distancia(self, distance):
        print("{:.2f} cm".format(distance))
        #distancia_var.set("{:.2f} cm".format(distance))

class MyFramePeso(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=210, height=50)

        self.label = customtkinter.CTkLabel(self, font=("Arial",14), text="Peso estimado:")
        self.label.place(x=12, y=10)
        
        global peso_var
        peso_var = customtkinter.StringVar()
        peso_var.set("0.0 kg")

        self.peso_display = customtkinter.CTkLabel(self, font=("Arial",14), textvariable=peso_var)
        self.peso_display.place(x=115, y=10)

class MyFrameConfig(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=250, height=500)

        self.label = customtkinter.CTkLabel(self, font=("Helvetica", 30), text="SPOT")
        self.label.place(x=80, y=10)

        self.image = customtkinter.CTkImage(light_image=Image.open("/home/tuca/Área de Trabalho/IT 2/SPOT (Sistema Peso Ovino Tridimensional)/SPOT_images/sheep_2.png"), dark_image=Image.open("/home/tuca/Área de Trabalho/IT 2/SPOT (Sistema Peso Ovino Tridimensional)/SPOT_images/sheep_2.png"), size=(150, 150))
        self.image_label = customtkinter.CTkLabel(self, image=self.image, text="")
        self.image_label.place(x=50, y=40) 

        self.my_frameInfo = MyFrameInfo(master=self)
        self.my_frameInfo.place(x=20, y=230)

        self.my_framePeso = MyFramePeso(master=self)
        self.my_framePeso.place(x=20, y=315)

        self.check_var = customtkinter.StringVar(value="Ligado")
        self.checkbox = customtkinter.CTkCheckBox(self, font=("Arial",14), fg_color="white", border_color="black", hover_color="gray", text="Utilizar sistema de predição", command=self.checkbox_Event, variable=self.check_var, onvalue="Ligado", offvalue="Desligado")
        self.checkbox.place(x=20, y=390)

        self.button = customtkinter.CTkButton(self, font=("Arial",16), text_color="black", fg_color="white", hover_color="gray", text="Registrar peso", command=self.registrar_Click, hover=True, width=210, height=60)
        self.button.place(x=20, y=430)

    def checkbox_Event(self):
        print("Caixa de seleção alterada, valor atual:", self.check_var.get())

    def registrar_Click(self):
        peso = peso_var.get()
        distancia = distancia_var.get()
        area = area_var.get()
        
        salvar_informacoes(peso, distancia, area)
        print('Informações salvas com sucesso!')

class MyFrameCamera(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=662, height=500)

        try:
            # Inicializa a câmera Intel RealSense
            self.dc = DepthCamera()
        except RuntimeError:
            print("Erro: Nenhum dispositivo conectado")
            exit()

        # Definição do ponto inicial do ponto de distância
        global point
        point = (330, 245)

        self.label = customtkinter.CTkLabel(self, text="")
        self.label.place(x=10, y=10)

        # Chama a função pela primeira vez para iniciar a exibição do vídeo
        self.update_video()
    
    def update_video(self):
        # Captura um frame da câmera RealSense
        ret, depth_frame, color_frame = self.dc.get_frame()

        # Calcula a distância do ponto de interesse à câmera usando o frame de profundidade
        distance = (depth_frame[point[1], point[0]]) / 10
        MyFrameInfo.update_distancia(self, distance)

        # Desenha um círculo no frame de cor no ponto de interesse
        cv2.circle(color_frame, point, 4, (255, 255, 255))

        # Converte o frame de cores para o formato RGB
        color_frame_rgb = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)

        # Converte o frame para um objeto Image do PIL
        img = Image.fromarray(color_frame_rgb)

        # Converte o objeto Image para o formato que pode ser exibido no Tkinter
        img_tk = ImageTk.PhotoImage(image=img)

        # Atualiza o rótulo Tkinter com o novo frame
        self.label.img = img_tk
        self.label.configure(image=img_tk)

        # Chama esta função novamente após 10 milissegundos para atualizar continuamente o feed de vídeo
        self.after(1, self.update_video)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("SPOT - Sistema Peso Ovino Tridimensional")
        self.geometry("960x540")
        self.resizable(False, False)

        # Corrigir isso pra adicionar o icon na pagina
        self.iconbitmap("@/home/tuca/Área de Trabalho/IT 2/SPOT (Sistema Peso Ovino Tridimensional)/SPOT_images/sheep_2.xbm")

        # Define o tema do programa como tema escuro
        customtkinter.set_appearance_mode("dark")  

        self.my_frameCamera = MyFrameCamera(master=self)
        self.my_frameCamera.place(x=20, y=20)

        self.my_frameConfig = MyFrameConfig(master=self)
        self.my_frameConfig.place(x=690, y=20)

app = App()
app.mainloop()