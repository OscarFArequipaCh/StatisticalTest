import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QTextEdit, QLabel,
    QComboBox, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QLineEdit, QSizePolicy,
    QGroupBox, QMessageBox
)
from PySide6.QtGui import QAction
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

import graficas as g

import pandas as pd

import pruebas as p
from ui_generador import abrir_generador


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador de Números Aleatorios")
        self.setGeometry(100, 100, 900, 600)

        self.numeros = []

        # Layout principal
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # ---------------- PANEL IZQUIERDO ----------------
        left_panel = QVBoxLayout()

        # Tabla de datos dentro del panel izquierdo
        self.tab_datos = QTableWidget()
        self.tab_datos.setColumnCount(1)
        self.tab_datos.setHorizontalHeaderLabels(["Número"])
        left_panel.addWidget(self.tab_datos, 3)

        # Opciones en la parte inferior del panel izquierdo
        opciones_layout = QVBoxLayout()

        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Poker", "Corridas", "Kolmogorov-Smirnov", "Frecuencias", "Distancias", "Promedios", "Series"])

        self.input_gl = QLineEdit()
        self.input_gl.setPlaceholderText("GL (opcional)")

        self.btn_ejecutar = QPushButton("Ejecutar prueba")
        self.btn_ejecutar.clicked.connect(self.ejecutar_prueba)

        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.setStyleSheet("background-color: #ff6b6b; color: white;")
        self.btn_limpiar.clicked.connect(self.limpiar_datos)

        opciones_layout.addWidget(self.combo_metodo)
        opciones_layout.addWidget(self.input_gl)
        opciones_layout.addWidget(self.btn_ejecutar)
        opciones_layout.addWidget(self.btn_limpiar)

        self.options_group = QGroupBox("Opciones de prueba")
        self.options_group.setLayout(opciones_layout)

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.options_group.setSizePolicy(size_policy)
        self.options_group.setFixedHeight(230)
        self.options_group.setVisible(False)

        left_panel.addWidget(self.options_group)

        # ---------------- PANEL CENTRAL (GRÁFICAS) ----------------
        self.graph_container = QWidget()
        graph_layout = QHBoxLayout()

        self.hist_canvas = FigureCanvas(g.histograma([], show=False))
        self.disp_canvas = FigureCanvas(g.dispersion([], show=False))

        graph_layout.addWidget(self.hist_canvas)
        graph_layout.addWidget(self.disp_canvas)
        self.graph_container.setLayout(graph_layout)

        # ---------------- PANEL INFERIOR (RESULTADOS + TABLA) ----------------
        self.tab_resultados = QTextEdit()
        self.tab_resultados.setReadOnly(True)
        self.tab_resultados.setFontFamily("Courier New")
        self.tab_resultados.setStyleSheet("background-color: #f4f4f4; color: #1f1f1f; font-size: 11pt;")

        self.tab_tabla = QTableWidget()

        bottom_panel = QHBoxLayout()
        
        # Panel izquierdo del inferior (Resultados)
        resultados_container = QVBoxLayout()
        resultados_container.addWidget(QLabel("Resultados"))
        resultados_container.addWidget(self.tab_resultados)
        
        # Panel derecho del inferior (Tabla)
        tabla_container = QVBoxLayout()
        tabla_container.addWidget(QLabel("Tabla de categorías"))
        tabla_container.addWidget(self.tab_tabla)
        
        bottom_panel.addLayout(resultados_container)
        bottom_panel.addLayout(tabla_container)

        right_panel = QVBoxLayout()
        right_panel.addWidget(self.graph_container, 2)
        right_panel.addLayout(bottom_panel, 1)

        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 3)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.crear_menu()

    # ---------------- FUNCIONES ----------------

    def crear_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")
        input_menu = menu_bar.addMenu("Input")
        view_menu = menu_bar.addMenu("View")
        tools_menu = menu_bar.addMenu("Tools")
        help_menu = menu_bar.addMenu("Help")

        cargar_excel_action = QAction("Cargar Excel", self)
        cargar_excel_action.triggered.connect(self.cargar_datos)

        generar_numeros_action = QAction("Generar números", self)
        generar_numeros_action.triggered.connect(self.generar_numeros)

        input_menu.addAction(cargar_excel_action)
        input_menu.addAction(generar_numeros_action)

    def cargar_datos(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Abrir Excel", "", "Excel (*.xlsx *.xls)")
        if not archivo:
            return

        df = pd.read_excel(archivo)
        self.numeros = df[df.columns[0]].dropna().tolist()

        self.mostrar_datos_tabla()
        self.actualizar_graficas()
        self.options_group.setVisible(True)

    def mostrar_datos_tabla(self):
        self.tab_datos.setRowCount(len(self.numeros))
        self.tab_datos.setColumnCount(1)
        self.tab_datos.setHorizontalHeaderLabels(["Número"])

        for i, val in enumerate(self.numeros):
            self.tab_datos.setItem(i, 0, QTableWidgetItem(str(val)))

    def generar_numeros(self):
        abrir_generador(self.set_numeros)

    def set_numeros(self, numeros):
        self.numeros = numeros
        self.mostrar_datos_tabla()
        self.actualizar_graficas()
        self.options_group.setVisible(True)

    def actualizar_graficas(self):
        if not self.numeros:
            return

        hist_fig = g.histograma(self.numeros, show=False)
        disp_fig = g.dispersion(self.numeros, show=False)

        self.hist_canvas.figure = hist_fig
        self.hist_canvas.draw()

        self.disp_canvas.figure = disp_fig
        self.disp_canvas.draw()

    def obtener_gl(self):
        texto = self.input_gl.text().strip()
        if texto:
            try:
                valor = int(texto)
                return valor
            except ValueError:
                return None
        return None

    def validar_numeros(self):
        if not self.numeros:
            return False, "No hay datos para evaluar."

        for v in self.numeros:
            try:
                x = float(v)
            except (ValueError, TypeError):
                return False, f"Valor no numérico detectado: {v}"

            if x < 0 or x > 1:
                return False, f"Número fuera de rango [0,1]: {v}"

        return True, ""

    def limpiar_datos(self):
        self.numeros = []
        self.tab_datos.setRowCount(0)
        self.tab_resultados.clear()
        self.tab_tabla.clear()
        self.tab_tabla.setRowCount(0)
        self.tab_tabla.setColumnCount(0)
        self.input_gl.clear()
        self.hist_canvas.figure = g.histograma([], show=False)
        self.hist_canvas.draw()
        self.disp_canvas.figure = g.dispersion([], show=False)
        self.disp_canvas.draw()
        self.options_group.setVisible(False)

    def ejecutar_prueba(self):
        if not self.numeros:
            QMessageBox.warning(self, "Validación", "Aún no hay datos cargados o generados.")
            return

        valido, mensaje = self.validar_numeros()
        if not valido:
            QMessageBox.warning(self, "Validación", mensaje)
            return

        metodo = self.combo_metodo.currentText()
        self.tab_resultados.clear()
        self.tab_tabla.clear()
        self.tab_tabla.setRowCount(0)
        self.tab_tabla.setColumnCount(0)

        gl = self.obtener_gl()

        if metodo == "Poker":
            resultado = p.prueba_poker(self.numeros, gl=gl)
        elif metodo == "Corridas":
            resultado = p.prueba_corridas(self.numeros, gl=gl)
        elif metodo == "Kolmogorov-Smirnov":
            resultado = p.prueba_ks(self.numeros)
        elif metodo == "Frecuencias":
            resultado = p.prueba_frecuencias(self.numeros, gl=gl)
        elif metodo == "Distancias":
            resultado = p.prueba_distancias(self.numeros)
        elif metodo == "Promedios":
            resultado = p.prueba_promedios(self.numeros)
        elif metodo == "Series":
            resultado = p.prueba_series(self.numeros, gl=gl)

        if not resultado:
            self.tab_resultados.setPlainText("No se pudo ejecutar la prueba. Verifique los datos.")
            return

        texto = []
        texto.append(f"Prueba: {resultado['metodo']}")
        texto.append("------------------------------")

        if resultado['metodo'] in ['Poker', 'Corridas', 'Frecuencias', 'Distancias', 'Series']:
            texto.append(f"Chi = {resultado['chi']:.6f}")
            texto.append(f"GL = {resultado['gl']}")
            texto.append(f"Chi crítico (0.05) = {resultado['chi_critico']}")
            texto.append(f"Decisión = {resultado['decision']}")
            self.mostrar_tabla(resultado['tabla_agrupada'])
        elif resultado['metodo'] == 'Promedios':
            texto.append(f"Media = {resultado['media']:.6f}")
            texto.append(f"Z = {resultado['Z']:.6f}")
            texto.append(f"Z crítico (0.05) = ±{resultado['Z_critico']:.2f}")
            texto.append(f"Decisión = {resultado['decision']}")
        else:
            texto.append(f"D = {resultado['D']:.6f}")
            texto.append(f"Dp = {resultado['Dp']:.6f}")
            texto.append(f"Dm = {resultado['Dm']:.6f}")
            texto.append(f"D crítico (0.05) = {resultado['D_critico']:.6f}")
            texto.append(f"Decisión = {resultado['decision']}")

        self.tab_resultados.setPlainText("\n".join(texto))

    def mostrar_tabla(self, tabla):
        self.tab_tabla.setRowCount(len(tabla))
        self.tab_tabla.setColumnCount(3)
        self.tab_tabla.setHorizontalHeaderLabels(["Categoría", "FO", "FE"])

        for i, (cat, fo, fe) in enumerate(tabla):
            self.tab_tabla.setItem(i, 0, QTableWidgetItem(cat))
            self.tab_tabla.setItem(i, 1, QTableWidgetItem(str(fo)))
            self.tab_tabla.setItem(i, 2, QTableWidgetItem(f"{fe:.4f}"))

# ---------------- EJECUCIÓN ----------------

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())