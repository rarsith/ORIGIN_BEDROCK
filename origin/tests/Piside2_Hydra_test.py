import sys
from PySide2 import QtWidgets, QtCore
from pxr import Usd, UsdGeom, UsdAppUtils, UsdImagingGL

class HydraViewportWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super(HydraViewportWidget, self).__init__(parent)
        self._renderer = UsdImagingGL.Engine()
        self._stage = None

    def initializeGL(self):
        """Initialize OpenGL context."""
        self.context = UsdAppUtils.AppController(self.context())
        self.context.InitializeRenderer()

    def paintGL(self):
        """Paint the USD stage using Hydra."""
        if self._stage:
            self._renderer.Render(self._stage, UsdGeom.Camera(self._stage.GetDefaultPrim()))

    def load_usd_file(self, file_path):
        """Load a .usd or .abc file and set the stage."""
        self._stage = Usd.Stage.Open(file_path)
        self.update()  # Trigger a repaint

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create the central widget (Hydra viewport)
        self.viewport = HydraViewportWidget(self)
        self.setCentralWidget(self.viewport)

        # Menu for loading .usd or .abc files
        load_action = QtWidgets.QAction("Load File", self)
        load_action.triggered.connect(self.load_file)

        menu = self.menuBar().addMenu("File")
        menu.addAction(load_action)

    def load_file(self):
        """Open file dialog to select a .usd or .abc file."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "USD Files (*.usd *.usda *.usdc *.abc)")
        if file_path:
            self.viewport.load_usd_file(file_path)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())
