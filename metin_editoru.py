import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QColorDialog,
    QFontDialog, QToolBar, QLabel, QMessageBox, QComboBox
)
from PyQt5.QtGui import QTextCharFormat, QFont, QKeySequence
from PyQt5.QtCore import Qt

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metin Editörü")
        self.setGeometry(200, 200, 800, 600)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        self.status_bar = self.statusBar()
        self.char_count_label = QLabel("Karakter: 0")
        self.status_bar.addPermanentWidget(self.char_count_label)

        self.text_edit.textChanged.connect(self.update_char_count)

        self.create_menu()
        self.create_toolbar()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Dosya")

        new_action = QAction("Yeni", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Aç", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Kaydet", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        close_action = QAction("Kapat", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

    def create_toolbar(self):
        toolbar = QToolBar("Araç Çubuğu")
        self.addToolBar(toolbar)

        cut_action = QAction("Kes", self)
        cut_action.triggered.connect(self.text_edit.cut)
        toolbar.addAction(cut_action)

        copy_action = QAction("Kopyala", self)
        copy_action.triggered.connect(self.text_edit.copy)
        toolbar.addAction(copy_action)

        paste_action = QAction("Yapıştır", self)
        paste_action.triggered.connect(self.text_edit.paste)
        toolbar.addAction(paste_action)

        font_action = QAction("Yazı Tipi", self)
        font_action.triggered.connect(self.select_font)
        toolbar.addAction(font_action)

        color_action = QAction("Renk", self)
        color_action.triggered.connect(self.select_color)
    #    toolbar.addAction(color_action)

        bold_action = QAction("Kalın", self)
        bold_action.triggered.connect(self.set_bold)
        toolbar.addAction(bold_action)

        italic_action = QAction("İtalik", self)
        italic_action.triggered.connect(self.set_italic)
        toolbar.addAction(italic_action)

        size_label = QLabel(" Boyut: ")
        toolbar.addWidget(size_label)

        self.size_box = QComboBox()
        self.size_box.addItems([str(i) for i in range(8, 30)])
        self.size_box.setCurrentText("12")
        self.size_box.currentTextChanged.connect(self.set_font_size)
        toolbar.addWidget(self.size_box)

    def new_file(self):
        if self.text_edit.toPlainText():
            reply = QMessageBox.question(self, 'Yeni Dosya', "Değişiklikleri kaydetmeden yeni dosya açılsın mı?",QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
        self.text_edit.clear()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "Metin Dosyaları (*.txt)")
        if path:
            with open(path, 'r', encoding='utf-8') as file:
                self.text_edit.setText(file.read())

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Dosyayı Kaydet", "", "Metin Dosyaları (*.txt)")
        if path:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.toPlainText())
            self.status_bar.showMessage("Dosya başarıyla kaydedildi.", 3000)

    def select_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_edit.setCurrentFont(font)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            cursor = self.text_edit.textCursor()
            cursor.mergeCharFormat(fmt)

    def set_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold)
        self.text_edit.textCursor().mergeCharFormat(fmt)

    def set_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(True)
        self.text_edit.textCursor().mergeCharFormat(fmt)

    def set_font_size(self, size):
        fmt = QTextCharFormat()
        fmt.setFontPointSize(float(size))
        self.text_edit.textCursor().mergeCharFormat(fmt)

    def update_char_count(self):
        text = self.text_edit.toPlainText()
        self.char_count_label.setText(f"Karakter: {len(text)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec_())
