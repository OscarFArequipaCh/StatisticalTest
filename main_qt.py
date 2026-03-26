import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QTextEdit, QLabel,
    QComboBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QLineEdit, QMenuBar
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
        self.combo_metodo.addItems(["Poker", "Corridas", "Kolmogorov-Smirnov"])

        self.input_gl = QLineEdit()
        self.input_gl.setPlaceholderText("GL (opcional)")

        self.btn_ejecutar = QPushButton("Ejecutar prueba")
        self.btn_ejecutar.clicked.connect(self.ejecutar_prueba)

        self.btn_graficar = QPushButton("Mostrar gráficas")
        self.btn_graficar.clicked.connect(self.mostrar_graficas)

        opciones_layout.addWidget(QLabel("Opciones"))
        opciones_layout.addWidget(self.combo_metodo)
        opciones_layout.addWidget(self.input_gl)
        opciones_layout.addWidget(self.btn_ejecutar)
        opciones_layout.addWidget(self.btn_graficar)

        left_panel.addLayout(opciones_layout, 1)

        # ---------------- PANEL CENTRAL (GRÁFICAS) ----------------
        self.graph_container = QWidget()
        graph_layout = QHBoxLayout()

        self.hist_canvas = FigureCanvas(g.histograma([], show=False))
        self.disp_canvas = FigureCanvas(g.dispersion([], show=False))

        graph_layout.addWidget(self.hist_canvas)
        graph_layout.addWidget(self.disp_canvas)
        self.graph_container.setLayout(graph_layout)

        # ---------------- PANEL INFERIOR (TAB RESULTS + TABLA) ----------------
        self.tabs = QTabWidget()
        self.tab_resultados = QTextEdit()
        self.tab_tabla = QTableWidget()

        self.tabs.addTab(self.tab_resultados, "Resultados")
        self.tabs.addTab(self.tab_tabla, "Tabla")

        right_panel = QVBoxLayout()
        right_panel.addWidget(self.graph_container, 2)
        right_panel.addWidget(self.tabs, 1)

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

    def actualizar_graficas(self):
        if not self.numeros:
            return

        hist_fig = g.histograma(self.numeros, show=False)
        disp_fig = g.dispersion(self.numeros, show=False)

        self.hist_canvas.figure = hist_fig
        self.hist_canvas.draw()

        self.disp_canvas.figure = disp_fig
        self.disp_canvas.draw()

    def obtener_gl(self, tabla):
        texto = self.input_gl.text().strip()
        if texto:
            return int(texto)
        return len(tabla) - 1

    def ejecutar_prueba(self):
        if not self.numeros:
            return

        metodo = self.combo_metodo.currentText()
        self.tab_resultados.clear()

        if metodo == "Poker":
            frec = p.contar_frecuencias(self.numeros)
            tabla = p.generar_tabla(frec, len(self.numeros))

            tabla_agrupada = p.agrupar_categorias(tabla)
            chi = p.chi_cuadrado_agrupado(tabla_agrupada)

            self.mostrar_tabla(tabla_agrupada)

            gl = self.obtener_gl(tabla_agrupada)
            chi_critico = p.obtener_chi_critico(gl)

            self.tab_resultados.append(f"Chi = {chi:.4f}")
            self.tab_resultados.append(f"GL = {gl}")
            self.tab_resultados.append(f"Chi crítico = {chi_critico}")

        elif metodo == "Corridas":
            binaria = p.generar_binaria(self.numeros)
            corr = p.obtener_corridas(binaria)
            FO = p.frecuencia_corridas(corr)

            n = len(self.numeros)
            max_long = max(FO.keys())
            FE = p.frecuencia_esperada_corridas(n, max_long)

            tabla = p.tabla_corridas(FO, FE)
            tabla_agrupada = p.agrupar_categorias(tabla)

            chi = p.chi_cuadrado_agrupado(tabla_agrupada)

            self.mostrar_tabla(tabla_agrupada)

            gl = self.obtener_gl(tabla_agrupada)
            chi_critico = p.obtener_chi_critico(gl)

            self.tab_resultados.append(f"Chi = {chi:.4f}")
            self.tab_resultados.append(f"GL = {gl}")
            self.tab_resultados.append(f"Chi crítico = {chi_critico}")

        elif metodo == "Kolmogorov-Smirnov":
            D, Dp, Dm = p.kolmogorov_smirnov(self.numeros)
            self.tab_resultados.append(f"D = {D:.4f}")

    def mostrar_tabla(self, tabla):
        self.tab_tabla.setRowCount(len(tabla))
        self.tab_tabla.setColumnCount(3)
        self.tab_tabla.setHorizontalHeaderLabels(["Categoría", "FO", "FE"])

        for i, (cat, fo, fe) in enumerate(tabla):
            self.tab_tabla.setItem(i, 0, QTableWidgetItem(cat))
            self.tab_tabla.setItem(i, 1, QTableWidgetItem(str(fo)))
            self.tab_tabla.setItem(i, 2, QTableWidgetItem(f"{fe:.4f}"))

    def mostrar_graficas(self):
        import graficas as g

        if not self.numeros:
            return

        metodo = self.combo_metodo.currentText()

        if metodo == "Poker":
            frec = p.contar_frecuencias(self.numeros)
            g.graficar_poker(p.generar_tabla(frec, len(self.numeros)))

        elif metodo == "Corridas":
            corr = p.obtener_corridas(p.generar_binaria(self.numeros))
            g.graficar_corridas(p.frecuencia_corridas(corr))

        elif metodo == "Kolmogorov-Smirnov":
            g.graficar_ks(self.numeros)

        g.histograma(self.numeros)
        g.dispersion(self.numeros)


# ---------------- EJECUCIÓN ----------------

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())