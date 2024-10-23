import pyrealsense2 as rs
import numpy as np

class DepthCamera:
    def __init__(self):
        """Inicializa a câmera Intel RealSense."""
        # Configura os streams de profundidade e cor
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Obtém a linha de produto do dispositivo para definir uma resolução suportada
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Inicia o streaming
        self.pipeline.start(config)

    def get_frame(self):
        """Captura um frame da câmera."""
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            return False, None, None

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        return True, depth_image, color_image

    def release(self):
        """Para o streaming da câmera."""
        self.pipeline.stop()