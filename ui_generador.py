from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)

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

        form.addRow("Semilla (x0)", self.e_x0)
        form.addRow("a", self.e_a)
        form.addRow("c", self.e_c)
        form.addRow("m", self.e_m)
        form.addRow("Cantidad (n)", self.e_n)

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
            self.callback(numeros)

            QMessageBox.information(self, "Éxito", f"{n} números generados")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
