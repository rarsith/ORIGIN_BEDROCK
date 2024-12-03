from PySide2.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PySide2.QtCore import QTimer
from pxr import Usd, UsdImagingGL, Sdf, Gf
import sys

class HydraViewport(QOpenGLWidget):
    def __init__(self, usd_file):
        super(HydraViewport, self).__init__()
        self.usd_file = usd_file
        self.engine = None
        self.stage = None
        self.cameraPath = None

    def initializeGL(self):
        from OpenGL.GL import glEnable, GL_DEPTH_TEST

        self.stage = Usd.Stage.Open(self.usd_file)
        self.engine = UsdImagingGL.Engine()
        self.engine.SetRendererPlugin('HdEmbreeRendererPlugin')  # Optional: Set preferred renderer

        glEnable(GL_DEPTH_TEST)  # Enable depth testing

        # Camera setup (optional custom position)
        self.cameraPath = '/camera'
        self.engine.SetCameraPath(self.cameraPath)
        self.engine.SetRenderViewport((0, 0, self.width(), self.height()))

    def resizeGL(self, width, height):
        self.engine.SetRenderViewport((0, 0, width, height))

    def paintGL(self):
        self.engine.Render(self.stage.GetPseudoRoot(), UsdImagingGL.GL.RenderParams())
        self.update()  # Trigger continuous updates

class MainWindow(QMainWindow):
    def __init__(self, usd_file):
        super().__init__()
        self.setWindowTitle("Hydra Viewport in PySide2")
        self.setGeometry(100, 100, 800, 600)
        self.viewport = HydraViewport(usd_file)
        self.setCentralWidget(self.viewport)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("D:\\__SANDBOX\\USD\\emily_lookdev_v001.usda")
    window.show()
    sys.exit(app.exec_())
