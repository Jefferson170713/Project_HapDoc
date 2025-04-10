import pandas as pd
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QFrame, QFileDialog, QMessageBox, QHBoxLayout, QCheckBox, QButtonGroup
from datetime import datetime
import os
from ProcedurePackageProcess import ProcedurePackageProcess

class WindowCenterClinic:
    def __init__(self, parent=None):
        self.parent = parent
        self.file_path = None
        self.output_path = None
        self.df = pd.DataFrame()
    
    def create_center_clinic_tab(self, center_clinic):
        layout_center_clinic = QVBoxLayout()

        # Layout horizontal para o QLabel e o botão "Limpar Status"
        status_layout = QHBoxLayout()

        # QLabel para exibir o status do arquivo
        self.label_status = QLabel("Nenhum arquivo carregado.")
        status_layout.addWidget(self.label_status)

        # Adiciona um espaço expansível para empurrar o botão para a direita
        status_layout.addStretch()

        # Botão para limpar o status
        btn_clear_status = QPushButton("Limpar Status")
        btn_clear_status.setFixedSize(150, 35)
        btn_clear_status.clicked.connect(self.clear_status)  # Conecta à função clear_status
        status_layout.addWidget(btn_clear_status)

        # Adiciona o layout horizontal ao layout vertical principal
        layout_center_clinic.addLayout(status_layout)

        # Adiciona os checkboxes para as opções
        checkbox_layout = QHBoxLayout()
        self.checkbox_group = QButtonGroup()
        self.checkbox_group.setExclusive(True)  # Apenas um pode ser selecionado

        self.checkbox_aditivo = QCheckBox("Aditivo")
        self.checkbox_aditivo.setChecked(True)  # Selecionado por padrão
        self.checkbox_group.addButton(self.checkbox_aditivo)
        checkbox_layout.addWidget(self.checkbox_aditivo)

        self.checkbox_contrato_medico = QCheckBox("Contrato Médico")
        self.checkbox_group.addButton(self.checkbox_contrato_medico)
        checkbox_layout.addWidget(self.checkbox_contrato_medico)

        self.checkbox_contratoterapia = QCheckBox("Contratoterapia")
        self.checkbox_group.addButton(self.checkbox_contratoterapia)
        checkbox_layout.addWidget(self.checkbox_contratoterapia)

        layout_center_clinic.addLayout(checkbox_layout)

        # Separador horizontal
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout_center_clinic.addWidget(separator)

        # Layout horizontal para os botões
        button_layout = QHBoxLayout()

        # Botão para pesquisar o arquivo principal
        btn_search = QPushButton("Pesquisar")
        btn_search.setFixedSize(150, 35)
        btn_search.clicked.connect(self.search_file)  # Função de pesquisa (a ser implementada)
        button_layout.addWidget(btn_search)

        # Adiciona um espaço expansível entre os botões
        button_layout.addStretch()

        # Botão para processar e salvar o arquivo
        btn_process_save = QPushButton("Salvar")
        btn_process_save.setFixedSize(150, 35)
        btn_process_save.clicked.connect(self.process_and_save)
        button_layout.addWidget(btn_process_save)

        # Adiciona o layout horizontal ao layout vertical principal
        layout_center_clinic.addLayout(button_layout)

        # Configurando o layout na aba
        center_clinic.setLayout(layout_center_clinic)
    
    # Função para pesquisar o arquivo principal
    def search_file(self):
        # Implementação futura
        pass

    # Função para processar e salvar o arquivo
    def process_and_save(self):
        if not self.file_path:
            QMessageBox.warning(self.parent, "Aviso", "Nenhum arquivo foi carregado!")
            return

        # Selecionar o local para salvar o arquivo processado
        save_path, _ = QFileDialog.getSaveFileName(self.parent, "Salvar Arquivo", "", "Arquivos Excel (*.xlsx)")
        if not save_path:
            return

        try:
            # Adiciona a extensão .xlsx se não estiver presente
            if not save_path.endswith(".xlsx"):
                save_path += ".xlsx"

            # Adiciona a data e hora ao nome do arquivo
            date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato: AAAA-MM-DD_HH-MM-SS
            base_name, ext = os.path.splitext(save_path)  # Divide o caminho em nome base e extensão
            save_path = f"{base_name}_{date}{ext}"  # Adiciona a data ao nome do arquivo

            # Processar o arquivo
            self.output_path = save_path

            # Verifica se o DataFrame self.df está carregado
            if self.df.empty:
                QMessageBox.warning(self.parent, "Aviso", "Os dados não foram carregados corretamente!")
                return

            # Criando o arquivo Excel com a aba principal
            with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                # Salvando a aba principal
                self.df.to_excel(writer, index=False, sheet_name='GERAL')

            QMessageBox.information(self.parent, "Sucesso", f"Arquivo processado e salvo em:\n{save_path}")

        except Exception as e:
            # Mensagem de erro detalhada
            QMessageBox.critical(self.parent, "Erro", f"Ocorreu um erro ao processar o arquivo:\n{str(e)}")
    
    # Função para limpar o status
    def clear_status(self):
        self.label_status.setText("Nenhum arquivo carregado.")