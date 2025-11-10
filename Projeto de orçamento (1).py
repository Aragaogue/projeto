import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import csv
import io

# =============================================================================
# CLASSES DE DOMÍNIO (Back-end de Cálculo - POO)
# Mantidas para encapsular as regras de negócio de forma robusta.
# =============================================================================

class Imovel:
    """Classe base para todos os tipos de imóveis, com regras de cálculo base."""
    def __init__(self, tipo_imovel, valor_base, possui_garagem=False):
        self.tipo_imovel = tipo_imovel
        self.valor_base = valor_base
        self.possui_garagem = possui_garagem
        self.mensalidade_adicionais = 0.0

    def calcular_adicionais(self):
        """Polimorfismo: Onde as subclasses definirão seus adicionais."""
        raise NotImplementedError("Subclasses devem implementar este método.")

    def calcular_aluguel_mensal(self):
        """Calcula o valor base mais os adicionais."""
        return self.valor_base + self.mensalidade_adicionais

class Apartamento(Imovel):
    """Implementa as regras de cálculo para Apartamentos."""
    def __init__(self, num_quartos, possui_garagem, sem_criancas):
        super().__init__("Apartamento", 700.00, possui_garagem)
        self.num_quartos = num_quartos
        self.sem_criancas = sem_criancas
        self.desconto_aplicado = 0.0
        self.calcular_adicionais()

    def calcular_adicionais(self):
        """Regras de Adicional: Quartos e Garagem."""
        adicional = 0.0
        if self.num_quartos == 2:
            adicional += 200.00 # Regra c
        if self.possui_garagem:
            adicional += 300.00 # Regra e
        self.mensalidade_adicionais = adicional

    def calcular_aluguel_mensal(self):
        """Aplica o desconto de 5% se sem_criancas for True (Regra g)."""
        aluguel_bruto = self.valor_base + self.mensalidade_adicionais
        
        if self.sem_criancas:
            self.desconto_aplicado = aluguel_bruto * 0.05
            return aluguel_bruto - self.desconto_aplicado
        return aluguel_bruto

class Casa(Imovel):
    """Implementa as regras de cálculo para Casas."""
    def __init__(self, num_quartos, possui_garagem):
        super().__init__("Casa", 900.00, possui_garagem)
        self.num_quartos = num_quartos
        self.calcular_adicionais()

    def calcular_adicionais(self):
        """Regras de Adicional: Quartos e Garagem."""
        adicional = 0.0
        if self.num_quartos == 2:
            adicional += 250.00 # Regra d
        if self.possui_garagem:
            adicional += 300.00 # Regra e
        self.mensalidade_adicionais = adicional

class Estudio(Imovel):
    """Implementa as regras de cálculo para Estúdios."""
    def __init__(self, num_vagas):
        # Garagem é True se houver pelo menos 1 vaga
        super().__init__("Estúdio", 1200.00, num_vagas > 0) 
        self.num_vagas = num_vagas
        self.calcular_adicionais()

    def calcular_adicionais(self):
        """Regra f: Cálculo de vagas para Estúdio."""
        adicional = 0.0
        if self.num_vagas > 0:
            adicional += 250.00 # Valor base de vagas (até 2)
            if self.num_vagas > 2:
                adicional += (self.num_vagas - 2) * 60.00 # +R$ 60 cada extra
        self.mensalidade_adicionais = adicional

class OrcamentoGenerator:
    """Gerencia o cálculo do contrato e a geração do conteúdo CSV."""
    VALOR_CONTRATO = 2000.00
    MAX_PARCELAS_CONTRATO = 5

    def __init__(self, imovel_selecionado):
        self.imovel = imovel_selecionado
        self.aluguel_mensal = self.imovel.calcular_aluguel_mensal()
        self.parcela_contrato = self.VALOR_CONTRATO / self.MAX_PARCELAS_CONTRATO
        self.parcelas = self._gerar_parcelas()

    def _gerar_parcelas(self):
        """Algoritmo de geração das 12 parcelas (Contrato nos 5 primeiros meses)."""
        parcelas = []
        for mes in range(1, 13):
            parcela_contrato_mensal = 0.0
            
            if mes <= self.MAX_PARCELAS_CONTRATO:
                parcela_contrato_mensal = self.parcela_contrato
            
            valor_total_mensal = self.aluguel_mensal + parcela_contrato_mensal
            
            parcelas.append({
                'mes': mes,
                'aluguel': self.aluguel_mensal,
                'contrato': parcela_contrato_mensal,
                'total': valor_total_mensal
            })
        return parcelas

    def gerar_csv_string(self):
        """Gera o conteúdo do CSV como uma string para visualização ou cópia."""
        output = io.StringIO()
        # Usa ';' para compatibilidade com Excel em PT-BR
        writer = csv.writer(output, delimiter=';') 

        # Cabeçalho
        writer.writerow(["Mês", "Parcela Aluguel", "Parcela Contrato", "Valor Total Mensal"])

        # Dados
        for p in self.parcelas:
            writer.writerow([
                p['mes'],
                f"{p['aluguel']:.2f}",
                f"{p['contrato']:.2f}",
                f"{p['total']:.2f}"
            ])
        return output.getvalue()

# =============================================================================
# INTERFACE GRÁFICA (Front-end - Tkinter)
# =============================================================================

class App(tk.Tk):
    """Classe principal da aplicação Tkinter."""
    def __init__(self):
        super().__init__()
        self.title("Orçamento de Aluguel R.M. - Calculadora Simples")
        self.geometry("750x450")
        self.resizable(False, False)
        
        self.current_orcamento = None
        self._setup_styles()
        self._setup_vars()
        self._setup_ui()
        self.atualizar_opcoes_dinamicas() # Inicializa as opções

    def _setup_vars(self):
        """Inicializa as variáveis de controle da GUI."""
        self.tipo_imovel = tk.StringVar(value="Apartamento")
        self.num_quartos = tk.IntVar(value=1)
        self.possui_garagem = tk.BooleanVar(value=False)
        self.sem_criancas = tk.BooleanVar(value=False)
        self.num_vagas_estudio = tk.IntVar(value=0)
        
        self.aluguel_result = tk.StringVar(value="R$ 0,00")
        self.contrato_result = tk.StringVar(value="R$ 0,00")
        self.total_result = tk.StringVar(value="R$ 0,00")

    def _setup_styles(self):
        """Configura os estilos visuais."""
        s = ttk.Style()
        s.configure('TFrame', background='#f0f4f8')
        s.configure('TLabel', background='#f0f4f8', font=('Inter', 10))
        s.configure('Title.TLabel', font=('Inter', 16, 'bold'), foreground='#1e40af')
        s.configure('Subtitle.TLabel', font=('Inter', 12, 'bold'), foreground='#3b82f6')
        s.configure('Result.TLabel', font=('Inter', 18, 'bold'), foreground='#047857')
        s.configure('Accent.TButton', background='#059669', foreground='white', font=('Inter', 10, 'bold'))

    def _setup_ui(self):
        """Configura a estrutura visual da aplicação usando grid."""
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="R.M. Imobiliária", style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky='n')
        ttk.Label(main_frame, text="Gerador de Orçamento de Aluguel Mensal", style='Subtitle.TLabel').grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky='n')

        # ------------------- Frame de Inputs -------------------
        input_frame = ttk.LabelFrame(main_frame, text="1. Configuração do Imóvel", padding="15 15 15 15")
        input_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        input_frame.grid_columnconfigure(0, weight=1)

        # Seleção do Tipo de Imóvel
        ttk.Label(input_frame, text="Tipo de Locação:", font=('Inter', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=(0, 5))
        tipos = ["Apartamento", "Casa", "Estúdio"]
        self.tipo_select = ttk.Combobox(input_frame, textvariable=self.tipo_imovel, values=tipos, state='readonly', width=25)
        self.tipo_select.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        self.tipo_select.bind("<<ComboboxSelected>>", self.atualizar_opcoes_dinamicas)

        # Frame para as opções dinâmicas
        self.dynamic_options_frame = ttk.Frame(input_frame, padding="5 0 5 0")
        self.dynamic_options_frame.grid(row=2, column=0, sticky='ew', pady=(5, 15))
        self.dynamic_options_frame.grid_columnconfigure(0, weight=1)
        
        # Botão Calcular
        ttk.Button(input_frame, text="Calcular Orçamento", command=self.calcular_orcamento, style='Accent.TButton').grid(row=3, column=0, sticky='ew', pady=(10, 0))

        # ------------------- Frame de Resultados -------------------
        output_frame = ttk.LabelFrame(main_frame, text="2. Resumo da 1ª Parcela (Valor Total Mensal)", padding="15 15 15 15")
        output_frame.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
        output_frame.grid_columnconfigure(0, weight=1)

        # Labels de Resultados
        self._create_result_label(output_frame, "Aluguel Líquido:", self.aluguel_result, 0)
        self._create_result_label(output_frame, "Parcela Contrato (5x):", self.contrato_result, 1)
        
        ttk.Separator(output_frame, orient='horizontal').grid(row=2, column=0, sticky='ew', pady=10)
        
        self._create_result_label(output_frame, "TOTAL Mensal (Primeiros 5 Meses):", self.total_result, 3, style='Result.TLabel')

        # Botão Gerar CSV (Regra i)
        self.csv_button = ttk.Button(output_frame, text="Ver Orçamento Detalhado (12 Meses)", command=self.gerar_csv_output, state=tk.DISABLED, style='Accent.TButton')
        self.csv_button.grid(row=4, column=0, sticky='ew', pady=(15, 0))
    
    def _create_result_label(self, parent, label_text, var, row, style='Subtitle.TLabel'):
        """Função auxiliar para criar rótulos de resultado com alinhamento."""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky='ew', pady=2)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text=label_text, style='TLabel').grid(row=0, column=0, sticky='w')
        ttk.Label(frame, textvariable=var, style=style, foreground='#047857').grid(row=0, column=1, sticky='e')


    def limpar_frame(self, frame):
        """Função auxiliar para limpar widgets do frame dinâmico."""
        for widget in frame.winfo_children():
            widget.destroy()

    def atualizar_opcoes_dinamicas(self, event=None):
        """Atualiza os inputs disponíveis com base no tipo de imóvel selecionado."""
        tipo = self.tipo_imovel.get()
        self.limpar_frame(self.dynamic_options_frame)
        
        # Mapeamento dinâmico para evitar longos if/elif aninhados
        config = {
            "Apartamento": {
                "adicional_quartos": "R$ 200,00",
                "show_children_option": True
            },
            "Casa": {
                "adicional_quartos": "R$ 250,00",
                "show_children_option": False
            }
        }
        
        # ------------------- Configuração para Apartamento/Casa -------------------
        if tipo in ["Apartamento", "Casa"]:
            config_data = config[tipo]
            
            # 1. Opção de Quartos
            ttk.Label(self.dynamic_options_frame, text="Configuração de Quartos:").grid(row=0, column=0, sticky='w', pady=(0, 5))
            ttk.Radiobutton(self.dynamic_options_frame, text="1 Quarto (Base)", variable=self.num_quartos, value=1).grid(row=1, column=0, sticky='w')
            ttk.Radiobutton(self.dynamic_options_frame, text=f"2 Quartos (+{config_data['adicional_quartos']})", variable=self.num_quartos, value=2).grid(row=2, column=0, sticky='w', pady=(0, 10))

            # 2. Opção de Garagem
            ttk.Checkbutton(self.dynamic_options_frame, text="Vaga de Garagem (+R$ 300,00)", variable=self.possui_garagem).grid(row=3, column=0, sticky='w', pady=5)

            # 3. Opção de Desconto (Apenas Apartamento)
            if config_data["show_children_option"]:
                ttk.Checkbutton(self.dynamic_options_frame, text="Sem Crianças (Desconto 5%)", variable=self.sem_criancas).grid(row=4, column=0, sticky='w', pady=5)
            
            # Reseta a variável de vagas do Estúdio
            self.num_vagas_estudio.set(0)

        # ------------------- Configuração para Estúdio -------------------
        elif tipo == "Estúdio":
            # 1. Opção de Vagas para Estúdio
            ttk.Label(self.dynamic_options_frame, text="Nº de Vagas Estacionamento:").grid(row=0, column=0, sticky='w', pady=(0, 5))
            
            vaga_input_frame = ttk.Frame(self.dynamic_options_frame)
            vaga_input_frame.grid(row=1, column=0, sticky='ew')
            vaga_input_frame.grid_columnconfigure(0, weight=1)
            
            ttk.Entry(vaga_input_frame, textvariable=self.num_vagas_estudio, width=5).grid(row=0, column=0, sticky='w')
            ttk.Label(vaga_input_frame, text="R$ 250 (até 2), +R$ 60 (extra)").grid(row=0, column=1, sticky='w', padx=10)
            
            # Reseta as variáveis de Apartamento/Casa
            self.num_quartos.set(1)
            self.possui_garagem.set(False)
            self.sem_criancas.set(False)

    def calcular_orcamento(self):
        """Cria os objetos de domínio e atualiza os resultados na GUI."""
        try:
            tipo = self.tipo_imovel.get()
            imovel = None

            if tipo == "Apartamento":
                imovel = Apartamento(
                    num_quartos=self.num_quartos.get(),
                    possui_garagem=self.possui_garagem.get(),
                    sem_criancas=self.sem_criancas.get()
                )
            elif tipo == "Casa":
                imovel = Casa(
                    num_quartos=self.num_quartos.get(),
                    possui_garagem=self.possui_garagem.get()
                )
            elif tipo == "Estúdio":
                # Garante que o número de vagas é válido (não negativo)
                vagas = max(0, self.num_vagas_estudio.get())
                imovel = Estudio(num_vagas=vagas)
            
            # Cria o Gerador de Orçamento
            self.current_orcamento = OrcamentoGenerator(imovel)
            
            # Atualiza os resultados na GUI
            aluguel = self.current_orcamento.aluguel_mensal
            contrato = self.current_orcamento.parcela_contrato
            total = aluguel + contrato
            
            self.aluguel_result.set(f"R$ {aluguel:.2f}")
            self.contrato_result.set(f"R$ {contrato:.2f}")
            self.total_result.set(f"R$ {total:.2f}")
            
            # Habilita o botão de CSV
            self.csv_button.config(state=tk.NORMAL)
            
        except Exception as e:
            # Em caso de erro (ex: input inválido), limpa os resultados e notifica
            self.aluguel_result.set("R$ 0,00")
            self.contrato_result.set("R$ 0,00")
            self.total_result.set("R$ 0,00")
            self.csv_button.config(state=tk.DISABLED)
            self.current_orcamento = None
            messagebox.showerror("Erro de Cálculo", f"Verifique os dados de entrada. Detalhe: {e}")

    def gerar_csv_output(self):
        """Exibe o conteúdo do CSV em uma nova janela de visualização."""
        if not self.current_orcamento:
            messagebox.showwarning("Atenção", "Por favor, calcule o orçamento primeiro.")
            return

        # 1. Gerar o conteúdo CSV como string
        csv_data = self.current_orcamento.gerar_csv_string()

        # 2. Criar uma nova janela (Toplevel) para visualização
        csv_window = tk.Toplevel(self)
        csv_window.title("Orçamento Detalhado (12 Meses)")
        csv_window.geometry("500x350")

        ttk.Label(csv_window, text="Detalhes do Orçamento Anual (Mês/Valor Total):", font=('Inter', 12, 'bold')).pack(pady=10)

        # 3. Usar ScrolledText para exibir o conteúdo do CSV
        text_area = scrolledtext.ScrolledText(csv_window, wrap=tk.WORD, width=60, height=15)
        text_area.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Inserir o conteúdo
        text_area.insert(tk.END, csv_data)
        text_area.config(state=tk.DISABLED) # Torna o texto somente leitura

        # Botão para fechar
        ttk.Button(csv_window, text="Fechar", command=csv_window.destroy, style='Accent.TButton').pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
