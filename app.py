import sys
import os

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QFileDialog, QMessageBox
)
from PyQt6.QtGui import QFont

import analyzer_logic as logic

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.prg_filepath = ""
        self.last_g_factor = self.load_last_g_factor()
        self.animation = None

        self.setWindowTitle("Aerosol Jet PRG Analyzer")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()
        file_layout = QHBoxLayout()
        run_layout = QHBoxLayout()

        self.file_button = QPushButton("Select .prg File")
        self.file_label = QLabel("No file selected")
        self.file_label.setFont(QFont("Arial", 12))

        self.g_factor_label = QLabel("G-Factor:")
        self.g_factor_entry = QLineEdit()
        self.g_factor_entry.setPlaceholderText("e.g., 0.5")
        self.g_factor_entry.setText(str(self.last_g_factor))

        self.run_button = QPushButton("Run Analysis")
        self.run_button.setStyleSheet("background-color: #3474eb; color: white; font-weight: bold;")

        self.output_textbox = QTextEdit()
        self.output_textbox.setReadOnly(True)
        self.output_textbox.setFont(QFont("Monaco", 12))

        file_layout.addWidget(self.file_button)
        file_layout.addWidget(self.file_label, 1)

        run_layout.addWidget(self.g_factor_label)
        run_layout.addWidget(self.g_factor_entry)
        run_layout.addWidget(self.run_button)

        main_layout.addLayout(file_layout)
        main_layout.addLayout(run_layout)
        main_layout.addWidget(self.output_textbox)

        self.setLayout(main_layout)

        self.file_button.clicked.connect(self.select_file)
        self.run_button.clicked.connect(self.run_full_analysis)

    def load_last_g_factor(self):
        import configparser
        config = configparser.ConfigParser()
        config_path = logic.get_config_path()
        if os.path.exists(config_path):
            config.read(config_path)
            return config.getfloat('Parameters', 'g_factor', fallback=0.5)
        return 0.5

    def save_g_factor(self, g_factor):
        import configparser
        config = configparser.ConfigParser()
        config_path = logic.get_config_path()
        config['Parameters'] = {'g_factor': str(g_factor)}
        with open(config_path, 'w') as configfile:
            config.write(configfile)

    def select_file(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select the .prg file to analyze",
            "",
            "Aerosol Jet Program (*.prg);;All files (*.*)"
        )
        if filepath:
            self.prg_filepath = filepath
            self.file_label.setText(os.path.basename(filepath))

    def run_full_analysis(self):
        if not self.prg_filepath:
            QMessageBox.critical(self, "Error", "Please select a .prg file first.")
            return

        try:
            g_factor = float(self.g_factor_entry.text())
            if g_factor <= 0:
                QMessageBox.critical(self, "Error", "G-Factor must be a positive number.")
                return
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid G-Factor. Please enter a number.")
            return

        self.save_g_factor(g_factor)

        self.output_textbox.setText("Running analysis...\n\nPlease wait.")
        QApplication.processEvents()

        parsed_segments = logic.parse_prg_file(self.prg_filepath)
        if not parsed_segments:
            QMessageBox.warning(self, "Warning", "Could not parse any segments for analysis.")
            self.output_textbox.setText("Analysis failed: No segments found.")
            return

        limiting_speed, stress_events, arc_info, limiting_arc_details = logic.run_path_stress_analysis(
            parsed_segments, g_factor)

        report_string = logic.generate_analysis_report(limiting_speed, stress_events, g_factor, limiting_arc_details)
        self.output_textbox.setText(report_string)

        base_name = os.path.basename(self.prg_filepath)
        base, ext = os.path.splitext(base_name)
        annotated_filename = os.path.join(os.path.dirname(self.prg_filepath), f"{base}_annotated{ext}")

        logic.create_annotated_prg_file(self.prg_filepath, annotated_filename, limiting_speed, stress_events,
                                        arc_info, g_factor, limiting_arc_details)

        QMessageBox.information(self, "Success", f"Analysis complete.\nAnnotated file saved as:\n{annotated_filename}")

        self.animation = logic.animate_printer(self.prg_filepath, limiting_speed)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())