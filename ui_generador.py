from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QComboBox
)

import distribuciones as d
from generador import LCG

DEFAULTS = {
    "x0": 111,
    "a": 1103515245,
    "c": 12345,
    "m": 2**32
}


def abrir_generador(callback, parent=None):
    dialog = GeneradorDialog(callback, parent)
    dialog.exec()


class GeneradorDialog(QDialog):
    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generador LCG")
        self.callback = callback

        form = QFormLayout()

        self.e_x0 = QLineEdit(str(DEFAULTS["x0"]))
        self.e_a = QLineEdit(str(DEFAULTS["a"]))
        self.e_c = QLineEdit(str(DEFAULTS["c"]))
        self.e_m = QLineEdit(str(DEFAULTS["m"]))
        self.e_n = QLineEdit()

        self.combo_distribucion = QComboBox()
        self.combo_distribucion.addItems(["Uniforme", "Exponencial", "Normal", "Binomial", "Poisson"])
        self.combo_distribucion.currentIndexChanged.connect(self.actualizar_parametros_distribucion)

        self.label_lambda = QLabel("λ")
        self.input_lambda = QLineEdit("1.0")
        self.input_lambda.setPlaceholderText("λ")

        self.label_mu = QLabel("μ")
        self.input_mu = QLineEdit("0.0")
        self.input_mu.setPlaceholderText("μ")

        self.label_sigma = QLabel("σ")
        self.input_sigma = QLineEdit("1.0")
        self.input_sigma.setPlaceholderText("σ")

        self.label_n_binomial = QLabel("n")
        self.input_n_binomial = QLineEdit("10")
        self.input_n_binomial.setPlaceholderText("n")

        self.label_p_binomial = QLabel("p")
        self.input_p_binomial = QLineEdit("0.5")
        self.input_p_binomial.setPlaceholderText("p")

        form.addRow("Semilla (x0)", self.e_x0)
        form.addRow("a", self.e_a)
        form.addRow("c", self.e_c)
        form.addRow("m", self.e_m)
        form.addRow("Cantidad (n)", self.e_n)
        form.addRow("Distribución", self.combo_distribucion)
        form.addRow(self.label_lambda, self.input_lambda)
        form.addRow(self.label_mu, self.input_mu)
        form.addRow(self.label_sigma, self.input_sigma)
        form.addRow(self.label_n_binomial, self.input_n_binomial)
        form.addRow(self.label_p_binomial, self.input_p_binomial)

        self.actualizar_parametros_distribucion()

        self.btn_generar = QPushButton("Generar")
        self.btn_generar.clicked.connect(self.generar)

        container = QVBoxLayout()
        container.addLayout(form)
        container.addWidget(self.btn_generar)

        self.setLayout(container)

    def generar(self):
        try:
            x0 = int(self.e_x0.text().strip())
            a = int(self.e_a.text().strip())
            c = int(self.e_c.text().strip())
            m = int(self.e_m.text().strip())
            n_text = self.e_n.text().strip()

            if not n_text:
                raise ValueError("Ingrese la cantidad de números (n)")

            n = int(n_text)
            if n <= 0:
                raise ValueError("n debe ser un número entero positivo")

            gen = LCG(x0, a, c, m)
            numeros = gen.generar_numeros(n)
            transformados = self.transformar_distribucion(numeros)
            resultado = self.callback(transformados)

            if resultado is False:
                return

            QMessageBox.information(self, "Éxito", f"{n} números generados")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def transformar_distribucion(self, uniformes):
        distribucion = self.combo_distribucion.currentText()

        if distribucion == "Uniforme":
            return uniformes
        if distribucion == "Exponencial":
            lam = self.obtener_float(self.input_lambda.text().strip(), "λ")
            return d.exponencial(uniformes, lam=lam)
        if distribucion == "Normal":
            mu = self.obtener_float(self.input_mu.text().strip(), "μ")
            sigma = self.obtener_float(self.input_sigma.text().strip(), "σ")
            return d.normal_box_muller(uniformes, mu=mu, sigma=sigma)
        if distribucion == "Binomial":
            n = self.obtener_int(self.input_n_binomial.text().strip(), "n")
            p = self.obtener_float(self.input_p_binomial.text().strip(), "p")
            return d.binomial(uniformes, n=n, p=p)
        if distribucion == "Poisson":
            lam = self.obtener_float(self.input_lambda.text().strip(), "λ")
            return d.poisson_inversion(uniformes, lam=lam)

        raise ValueError("Distribución desconocida.")

    def obtener_float(self, texto, nombre):
        try:
            return float(texto)
        except ValueError:
            raise ValueError(f"El parámetro {nombre} debe ser numérico.")

    def obtener_int(self, texto, nombre):
        try:
            return int(texto)
        except ValueError:
            raise ValueError(f"El parámetro {nombre} debe ser un entero.")

    def actualizar_parametros_distribucion(self):
        distribucion = self.combo_distribucion.currentText()

        exponencial_poisson = distribucion in ["Exponencial", "Poisson"]
        normal = distribucion == "Normal"
        binomial = distribucion == "Binomial"

        self.label_lambda.setVisible(exponencial_poisson)
        self.input_lambda.setVisible(exponencial_poisson)

        self.label_mu.setVisible(normal)
        self.input_mu.setVisible(normal)
        self.label_sigma.setVisible(normal)
        self.input_sigma.setVisible(normal)

        self.label_n_binomial.setVisible(binomial)
        self.input_n_binomial.setVisible(binomial)
        self.label_p_binomial.setVisible(binomial)
        self.input_p_binomial.setVisible(binomial)
