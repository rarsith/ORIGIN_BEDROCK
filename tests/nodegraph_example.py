import sys
from PySide2.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsPathItem, QMainWindow, QVBoxLayout, QWidget
from PySide2.QtGui import QPainterPath, QPainter, QColor, QPen
from PySide2.QtCore import Qt, QPointF

class Node(QGraphicsEllipseItem):
    def __init__(self, x, y):
        super().__init__(-30, -15, 60, 30)
        self.setPos(x, y)
        self.setBrush(Qt.lightGray)
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
        self.input_ports = []
        self.output_ports = []
        self.connections = []

    def add_input_port(self):
        port = Port(self, is_input=True)
        self.input_ports.append(port)
        self.update_ports()

    def add_output_port(self):
        port = Port(self, is_input=False)
        self.output_ports.append(port)
        self.update_ports()

    def update_ports(self):
        total_ports = len(self.input_ports) + len(self.output_ports)
        port_spacing = 30
        y_offset = -((total_ports - 1) * port_spacing) / 2

        for port in self.input_ports:
            port.setPos(-30, y_offset)
            y_offset += port_spacing

        for port in self.output_ports:
            port.setPos(30, y_offset)
            y_offset += port_spacing

class Port(QGraphicsEllipseItem):
    def __init__(self, node, is_input):
        super().__init__(-5, -5, 10, 10, node)
        self.node = node
        self.is_input = is_input
        self.setBrush(Qt.blue if self.is_input else Qt.red)
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, False)

class NodeGraph(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Node Graph")
        self.setGeometry(100, 100, 800, 600)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(0, 0, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.nodes = []

        node_a = Node(100, 100)
        node_b = Node(300, 200)

        node_a.add_input_port()
        node_a.add_output_port()
        node_b.add_input_port()
        node_b.add_output_port()

        self.nodes.extend([node_a, node_b])
        self.scene.addItem(node_a)
        self.scene.addItem(node_b)

        self.view.setScene(self.scene)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NodeGraph()
    window.show()
    sys.exit(app.exec_())
