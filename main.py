import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QWidget,
    QHBoxLayout,
    QSplitter,
    QTextEdit,
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory


# Function to generate complement and reverse complement of DNA sequence
def complement(sequence):
    complement_map = str.maketrans("ATCG", "TAGC")
    return sequence.translate(complement_map)


def reverse(sequence):
    return sequence[::-1]


def reverse_complement(sequence):
    return reverse(complement(sequence))


def gc_content(sequence):
    gc_count = sequence.count("G") + sequence.count("C")
    return (gc_count / len(sequence)) * 100 if len(sequence) > 0 else 0


class DNAProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DNA Sequence Processor")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Left panel for table and buttons
        self.left_panel = QVBoxLayout()
        self.main_layout.addLayout(self.left_panel)

        # Right panel for statistics and visualization
        self.right_panel = QVBoxLayout()
        self.main_layout.addLayout(self.right_panel)

        # App Title
        self.app_title = QLabel("DNA Sequence Processor")
        self.app_title.setFont(QFont("Arial", 18, QFont.Bold))
        self.app_title.setAlignment(Qt.AlignCenter)
        self.left_panel.addWidget(self.app_title)

        # File Label
        self.file_label = QLabel("No file uploaded.")
        self.file_label.setFont(QFont("Arial", 12))
        self.file_label.setAlignment(Qt.AlignCenter)
        self.left_panel.addWidget(self.file_label)

        # Button Layout
        self.button_layout = QHBoxLayout()
        self.left_panel.addLayout(self.button_layout)

        # Upload Button
        self.upload_button = QPushButton("Upload CSV")
        self.upload_button.setFont(QFont("Arial", 12))
        self.upload_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px; } QPushButton:hover { background-color: #45a049; }"
        )
        self.upload_button.clicked.connect(self.process_csv)
        self.button_layout.addWidget(self.upload_button)

        # Save Button
        self.save_button = QPushButton("Save Processed CSV")
        self.save_button.setFont(QFont("Arial", 12))
        self.save_button.setStyleSheet(
            "QPushButton { background-color: #2196F3; color: white; border-radius: 10px; padding: 10px; } QPushButton:hover { background-color: #0b7dda; }"
        )
        self.save_button.clicked.connect(self.save_csv)
        self.save_button.setEnabled(False)
        self.button_layout.addWidget(self.save_button)

        # Table Widget
        self.table_widget = QTableWidget()
        self.left_panel.addWidget(self.table_widget)
        self.table_widget.cellClicked.connect(self.display_sequence_statistics)

        # Statistics Label
        self.statistics_label = QLabel("Statistics:")
        self.statistics_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.right_panel.addWidget(self.statistics_label)

        # Statistics Text
        self.statistics_text = QTextEdit()
        self.statistics_text.setReadOnly(True)
        self.right_panel.addWidget(self.statistics_text)

        # Visualization Widget
        self.visualization_label = QLabel("")
        self.visualization_label.setAlignment(Qt.AlignCenter)
        self.right_panel.addWidget(self.visualization_label)

        # Dataframe placeholder
        self.df = None

    def process_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return

        try:
            # Read the CSV file
            self.df = pd.read_csv(file_path)

            if "DNA_Sequence" not in self.df.columns:
                QMessageBox.critical(
                    self, "Error", "The CSV file must contain a 'DNA_Sequence' column."
                )
                return

            # Process DNA sequences
            self.df["Reverse"] = self.df["DNA_Sequence"].apply(reverse)
            self.df["Complement"] = self.df["DNA_Sequence"].apply(complement)
            self.df["Reverse_Complement"] = self.df["DNA_Sequence"].apply(
                reverse_complement
            )

            # Update the table
            self.update_table(self.df)
            self.save_button.setEnabled(True)
            self.file_label.setText(f"Uploaded File: {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process the CSV file.\n{e}")

    def update_table(self, df):
        self.table_widget.clear()
        self.table_widget.setRowCount(len(df))
        self.table_widget.setColumnCount(len(df.columns))
        self.table_widget.setHorizontalHeaderLabels(df.columns)

        for row_index, row in df.iterrows():
            for col_index, value in enumerate(row):
                self.table_widget.setItem(
                    row_index, col_index, QTableWidgetItem(str(value))
                )

    def save_csv(self):
        if self.df is None:
            QMessageBox.warning(self, "Warning", "No data to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            try:
                self.df.to_csv(file_path, index=False)
                QMessageBox.information(self, "Success", "File saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save the file.\n{e}")

    def display_sequence_statistics(self, row, column):
        if self.df is not None and "DNA_Sequence" in self.df.columns:
            sequence = self.df.iloc[row]["DNA_Sequence"]
            self.display_statistics_and_plot(sequence)

    def display_statistics_and_plot(self, sequence):
        # Statistics
        gc = gc_content(sequence)
        gc_count = sequence.count("G") + sequence.count("C")
        at_count = sequence.count("A") + sequence.count("T")
        total_length = len(sequence)

        stats_text = (
            f"GC Content: {gc:.2f}%\n"
            f"GC Count: {gc_count}\n"
            f"AT Count: {at_count}\n"
            f"Total Length: {total_length}"
        )

        self.statistics_text.setText(stats_text)

        # Visualization
        counts = {
            "A": sequence.count("A"),
            "T": sequence.count("T"),
            "C": sequence.count("C"),
            "G": sequence.count("G"),
        }

        plt.figure(figsize=(5, 4))
        plt.bar(
            counts.keys(), counts.values(), color=["blue", "red", "green", "orange"]
        )
        plt.title("Nucleotide Distribution")
        plt.xlabel("Nucleotides")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig("nucleotide_distribution.png")
        plt.close()

        # Update UI
        pixmap = QPixmap("nucleotide_distribution.png")
        self.visualization_label.setPixmap(pixmap)


if __name__ == "__main__":
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    app = QApplication(sys.argv)
    window = DNAProcessorApp()
    window.show()
    sys.exit(app.exec_())
