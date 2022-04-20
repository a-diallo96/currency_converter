from PySide2 import QtWidgets
import currency_converter


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devise")
        self.setup_ui()
        self.set_defaultValues()
        self.setup_connections()
        self.resize(800,100)


    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)  # type: ignore créeationde layout
       
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox()
        self.btn_inverser = QtWidgets.QPushButton(" *** Inverser Devises *** ")
        self.btn_changeMode = QtWidgets.QPushButton(" mode sombre ")


        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)
        self.layout.addWidget(self.btn_changeMode)

    def set_defaultValues(self):

        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))  # type: ignore
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))  # type: ignore
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("EUR")
        self.spn_montant.setRange(1,1000000)
        self.spn_montantConverti.setRange(1,1000000)

        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)

    def setup_connections(self):
        self.cbb_devisesFrom.activated.connect(self.compute)  # type: ignore
        self.cbb_devisesTo.activated.connect(self.compute)  # type: ignore
        self.spn_montant.valueChanged.connect(self.compute)   # type: ignore
        self.btn_inverser.clicked.connect(self.inversDevises)  # type: ignore
        self.btn_changeMode.clicked.connect(self.change_mode)  # type: ignore


    def compute(self):
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()
        try:
            resultat = self.c.convert(montant,devise_from,devise_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("la conversion n'a pas fonctionné")

        else:
            self.spn_montantConverti.setValue(resultat)

    
    def inversDevises(self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        self.cbb_devisesTo.setCurrentText(devise_from)
        self.cbb_devisesFrom.setCurrentText(devise_to)

        self.compute()

    def change_mode(self):
        if self.btn_changeMode.text() ==  " mode sombre ":
            self.setStyleSheet("""
            background-color:rgb(30,30,30);
            color:rgb(240,240,240);
            """)
            self.btn_inverser.setStyleSheet("background-color:blue")
            self.btn_changeMode.setText("mode clair")
        else:
            self.setStyleSheet("")
            self.btn_inverser.setStyleSheet("")
            self.btn_changeMode.setText(" mode sombre ")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    win = App()
    win.show() 
    app.exec_()