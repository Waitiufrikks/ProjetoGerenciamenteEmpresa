"""
Interface gráfica principal do sistema de gestão de empresa
Implementa todas as funcionalidades usando Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models import Employee, Department
from data_manager import DataManager

class EmployeeManagementApp:
    """Aplicação principal com interface gráfica"""
    
    def __init__(self, root):
        """
        Inicializa a aplicação GUI
        
        Args:
            root: Janela principal do Tkinter
        """
        self.root = root
        self.root.title("Sistema de Gestão de Empresa")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Inicializar gerenciador de dados
        self.data_manager = DataManager()
        
        # Carregar dados existentes
        self.employees, self.departments = self.data_manager.load_all_data()
        
        # Configurar interface
        self.setup_ui()
        
        # Atualizar exibições
        self.refresh_all_displays()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Sistema de Gestão de Empresa", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de botões (lado esquerdo)
        buttons_frame = ttk.LabelFrame(main_frame, text="Operações", padding="10")
        buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Botões principais
        ttk.Button(buttons_frame, text="Cadastrar Empregado", 
                  command=self.register_employee_dialog).pack(fill=tk.X, pady=2)
        
        ttk.Button(buttons_frame, text="Editar Empregado", 
                  command=self.edit_employee_dialog).pack(fill=tk.X, pady=2)
        
        ttk.Button(buttons_frame, text="Excluir Empregado", 
                  command=self.delete_employee_dialog).pack(fill=tk.X, pady=2)
        
        ttk.Separator(buttons_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Gerenciar Setores", 
                  command=self.manage_departments_dialog).pack(fill=tk.X, pady=2)
        
        ttk.Button(buttons_frame, text="Realocar Empregado", 
                  command=self.reallocate_employee_dialog).pack(fill=tk.X, pady=2)
        
        ttk.Separator(buttons_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Atualizar Exibição", 
                  command=self.refresh_all_displays).pack(fill=tk.X, pady=2)
        
        # Frame de exibição (lado direito)
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        display_frame.rowconfigure(1, weight=1)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(display_frame)
        self.notebook.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Aba de empregados
        self.employees_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.employees_frame, text="Empregados")
        
        # Aba de setores
        self.departments_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.departments_frame, text="Setores")
        
        # Configurar conteúdo das abas
        self.setup_employees_tab()
        self.setup_departments_tab()
    
    def setup_employees_tab(self):
        """Configura a aba de empregados"""
        # Treeview para empregados
        columns = ('ID', 'Nome', 'CPF', 'Telefone', 'Endereço', 'Setor')
        self.employees_tree = ttk.Treeview(self.employees_frame, columns=columns, show='headings')
        
        # Configurar colunas
        for col in columns:
            self.employees_tree.heading(col, text=col)
            if col == 'ID':
                self.employees_tree.column(col, width=50)
            elif col in ['CPF', 'Telefone']:
                self.employees_tree.column(col, width=100)
            else:
                self.employees_tree.column(col, width=120)
        
        # Scrollbars
        emp_scrollbar_y = ttk.Scrollbar(self.employees_frame, orient=tk.VERTICAL, command=self.employees_tree.yview)
        emp_scrollbar_x = ttk.Scrollbar(self.employees_frame, orient=tk.HORIZONTAL, command=self.employees_tree.xview)
        self.employees_tree.configure(yscrollcommand=emp_scrollbar_y.set, xscrollcommand=emp_scrollbar_x.set)
        
        # Grid
        self.employees_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        emp_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        emp_scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configurar grid weights
        self.employees_frame.columnconfigure(0, weight=1)
        self.employees_frame.rowconfigure(0, weight=1)
    
    def setup_departments_tab(self):
        """Configura a aba de setores"""
        # Treeview para setores
        self.departments_tree = ttk.Treeview(self.departments_frame, columns=('Empregados',), show='tree headings')
        self.departments_tree.heading('#0', text='Setor')
        self.departments_tree.heading('Empregados', text='Empregados')
        
        # Scrollbar
        dept_scrollbar = ttk.Scrollbar(self.departments_frame, orient=tk.VERTICAL, command=self.departments_tree.yview)
        self.departments_tree.configure(yscrollcommand=dept_scrollbar.set)
        
        # Grid
        self.departments_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        dept_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar grid weights
        self.departments_frame.columnconfigure(0, weight=1)
        self.departments_frame.rowconfigure(0, weight=1)
    
    def refresh_all_displays(self):
        """Atualiza todas as exibições"""
        self.refresh_employees_display()
        self.refresh_departments_display()
    
    def refresh_employees_display(self):
        """Atualiza a exibição de empregados"""
        # Limpar treeview
        for item in self.employees_tree.get_children():
            self.employees_tree.delete(item)
        
        # Adicionar empregados
        for emp in self.employees:
            self.employees_tree.insert('', 'end', values=(
                emp.id, emp.name, emp.cpf, emp.phone, emp.address, emp.department
            ))
    
    def refresh_departments_display(self):
        """Atualiza a exibição de setores"""
        # Limpar treeview
        for item in self.departments_tree.get_children():
            self.departments_tree.delete(item)
        
        # Adicionar setores e seus empregados
        for dept in self.departments:
            dept_item = self.departments_tree.insert('', 'end', text=dept.name, 
                                                     values=(f"{len(dept.team)} empregados",))
            
            for emp in dept.team:
                self.departments_tree.insert(dept_item, 'end', text=f"  → {emp.name}", 
                                           values=(f"CPF: {emp.cpf}",))
    
    def register_employee_dialog(self):
        """Abre diálogo para cadastrar empregado"""
        dialog = EmployeeDialog(self.root, "Cadastrar Empregado", self.departments)
        if dialog.result:
            emp_data = dialog.result
            
            # Verificar se CPF já existe
            if any(emp.cpf == emp_data['cpf'] for emp in self.employees):
                messagebox.showerror("Erro", "CPF já cadastrado!")
                return
            
            # Criar empregado
            employee = Employee(
                name=emp_data['name'],
                cpf=emp_data['cpf'],
                phone=emp_data['phone'],
                address=emp_data['address'],
                department=emp_data['department']
            )
            
            self.employees.append(employee)
            
            # Adicionar ao setor se necessário
            if emp_data['department'] != "Nenhum":
                dept = self.find_department_by_name(emp_data['department'])
                if dept:
                    dept.add_employee(employee)
            
            # Salvar dados
            self.save_data()
            self.refresh_all_displays()
            
            messagebox.showinfo("Sucesso", "Empregado cadastrado com sucesso!")
    
    def edit_employee_dialog(self):
        """Abre diálogo para editar empregado"""
        if not self.employees:
            messagebox.showwarning("Aviso", "Não há empregados cadastrados!")
            return
        
        # Selecionar empregado
        employee = self.select_employee_dialog("Selecionar empregado para editar:")
        if not employee:
            return
        
        # Abrir diálogo de edição
        dialog = EmployeeDialog(self.root, "Editar Empregado", self.departments, employee)
        if dialog.result:
            emp_data = dialog.result
            
            # Verificar se CPF já existe (exceto o próprio empregado)
            if any(emp.cpf == emp_data['cpf'] and emp.id != employee.id for emp in self.employees):
                messagebox.showerror("Erro", "CPF já cadastrado por outro empregado!")
                return
            
            # Atualizar dados
            old_department = employee.department
            employee.update_data(emp_data['name'], emp_data['phone'], emp_data['address'])
            employee.cpf = emp_data['cpf']
            employee.department = emp_data['department']
            
            # Atualizar setores
            if old_department != emp_data['department']:
                # Remover do setor antigo
                if old_department != "Nenhum":
                    old_dept = self.find_department_by_name(old_department)
                    if old_dept:
                        old_dept.remove_employee(employee)
                
                # Adicionar ao novo setor
                if emp_data['department'] != "Nenhum":
                    new_dept = self.find_department_by_name(emp_data['department'])
                    if new_dept:
                        new_dept.add_employee(employee)
            
            # Salvar dados
            self.save_data()
            self.refresh_all_displays()
            
            messagebox.showinfo("Sucesso", "Empregado editado com sucesso!")
    
    def delete_employee_dialog(self):
        """Abre diálogo para excluir empregado"""
        if not self.employees:
            messagebox.showwarning("Aviso", "Não há empregados cadastrados!")
            return
        
        # Selecionar empregado
        employee = self.select_employee_dialog("Selecionar empregado para excluir:")
        if not employee:
            return
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir {employee.name}?"):
            # Remover do setor
            if employee.department != "Nenhum":
                dept = self.find_department_by_name(employee.department)
                if dept:
                    dept.remove_employee(employee)
            
            # Remover da lista
            self.employees.remove(employee)
            
            # Salvar dados
            self.save_data()
            self.refresh_all_displays()
            
            messagebox.showinfo("Sucesso", "Empregado excluído com sucesso!")
    
    def manage_departments_dialog(self):
        """Abre diálogo para gerenciar setores"""
        dialog = DepartmentManagementDialog(self.root, self.departments)
        if dialog.changes_made:
            # Atualizar referências de empregados
            self.update_employee_department_references()
            
            # Salvar dados
            self.save_data()
            self.refresh_all_displays()
    
    def reallocate_employee_dialog(self):
        """Abre diálogo para realocar empregado"""
        if not self.employees:
            messagebox.showwarning("Aviso", "Não há empregados cadastrados!")
            return
        
        if not self.departments:
            messagebox.showwarning("Aviso", "Não há setores cadastrados!")
            return
        
        # Selecionar empregado
        employee = self.select_employee_dialog("Selecionar empregado para realocar:")
        if not employee:
            return
        
        # Selecionar novo setor
        dept_names = [dept.name for dept in self.departments]
        dialog = DepartmentSelectionDialog(self.root, dept_names, 
                                         f"Realocar {employee.name}\nSetor atual: {employee.department}")
        
        if dialog.result:
            new_dept_name = dialog.result
            
            # Remover do setor atual
            if employee.department != "Nenhum":
                old_dept = self.find_department_by_name(employee.department)
                if old_dept:
                    old_dept.remove_employee(employee)
            
            # Adicionar ao novo setor
            new_dept = self.find_department_by_name(new_dept_name)
            if new_dept:
                new_dept.add_employee(employee)
                employee.department = new_dept_name
            
            # Salvar dados
            self.save_data()
            self.refresh_all_displays()
            
            messagebox.showinfo("Sucesso", f"Empregado realocado para {new_dept_name}!")
    
    def select_employee_dialog(self, message):
        """Abre diálogo para seleção de empregado"""
        dialog = EmployeeSelectionDialog(self.root, self.employees, message)
        return dialog.result
    
    def find_department_by_name(self, name):
        """Encontra setor pelo nome"""
        return next((dept for dept in self.departments if dept.name == name), None)
    
    def update_employee_department_references(self):
        """Atualiza referências de setores nos empregados"""
        dept_names = {dept.name for dept in self.departments}
        for emp in self.employees:
            if emp.department not in dept_names and emp.department != "Nenhum":
                emp.department = "Nenhum"
    
    def save_data(self):
        """Salva todos os dados"""
        if not self.data_manager.save_all_data(self.employees, self.departments):
            messagebox.showerror("Erro", "Falha ao salvar dados!")


class EmployeeDialog:
    """Diálogo para cadastro/edição de empregado"""
    
    def __init__(self, parent, title, departments, employee=None):
        self.result = None
        
        # Criar janela
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos
        ttk.Label(main_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar(value=employee.name if employee else "")
        ttk.Entry(main_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(main_frame, text="CPF:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cpf_var = tk.StringVar(value=employee.cpf if employee else "")
        ttk.Entry(main_frame, textvariable=self.cpf_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="Telefone:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.phone_var = tk.StringVar(value=employee.phone if employee else "")
        ttk.Entry(main_frame, textvariable=self.phone_var, width=30).grid(row=2, column=1, pady=5)
        
        ttk.Label(main_frame, text="Endereço:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.address_var = tk.StringVar(value=employee.address if employee else "")
        ttk.Entry(main_frame, textvariable=self.address_var, width=30).grid(row=3, column=1, pady=5)
        
        ttk.Label(main_frame, text="Setor:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.dept_var = tk.StringVar(value=employee.department if employee else "Nenhum")
        dept_values = ["Nenhum"] + [dept.name for dept in departments]
        ttk.Combobox(main_frame, textvariable=self.dept_var, values=dept_values, 
                    state="readonly", width=27).grid(row=4, column=1, pady=5)
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Salvar", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
        # Centralizar janela
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Aguardar resultado
        self.dialog.wait_window()
    
    def save(self):
        # Validar campos
        if not all([self.name_var.get().strip(), self.cpf_var.get().strip(), 
                   self.phone_var.get().strip(), self.address_var.get().strip()]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        # Validar CPF (apenas números)
        if not self.cpf_var.get().isdigit():
            messagebox.showerror("Erro", "CPF deve conter apenas números!")
            return
        
        # Validar telefone (apenas números)
        if not self.phone_var.get().isdigit():
            messagebox.showerror("Erro", "Telefone deve conter apenas números!")
            return
        
        self.result = {
            'name': self.name_var.get().strip(),
            'cpf': self.cpf_var.get().strip(),
            'phone': self.phone_var.get().strip(),
            'address': self.address_var.get().strip(),
            'department': self.dept_var.get()
        }
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()


class EmployeeSelectionDialog:
    """Diálogo para seleção de empregado"""
    
    def __init__(self, parent, employees, message):
        self.result = None
        
        # Criar janela
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Selecionar Empregado")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mensagem
        ttk.Label(main_frame, text=message).pack(pady=(0, 10))
        
        # Lista de empregados
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.listbox = tk.Listbox(listbox_frame)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Preencher lista
        for emp in employees:
            self.listbox.insert(tk.END, f"{emp.id} - {emp.name} - {emp.department}")
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Selecionar", command=self.select).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
        # Bind duplo clique
        self.listbox.bind('<Double-1>', lambda e: self.select())
        
        self.employees = employees
        
        # Centralizar janela
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Aguardar resultado
        self.dialog.wait_window()
    
    def select(self):
        selection = self.listbox.curselection()
        if selection:
            self.result = self.employees[selection[0]]
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()


class DepartmentSelectionDialog:
    """Diálogo para seleção de setor"""
    
    def __init__(self, parent, departments, message):
        self.result = None
        
        # Criar janela
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Selecionar Setor")
        self.dialog.geometry("300x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mensagem
        ttk.Label(main_frame, text=message).pack(pady=(0, 10))
        
        # Lista de setores
        self.listbox = tk.Listbox(main_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        for dept in departments:
            self.listbox.insert(tk.END, dept)
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack()
        
        ttk.Button(buttons_frame, text="Selecionar", command=self.select).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
        # Bind duplo clique
        self.listbox.bind('<Double-1>', lambda e: self.select())
        
        self.departments = departments
        
        # Centralizar janela
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Aguardar resultado
        self.dialog.wait_window()
    
    def select(self):
        selection = self.listbox.curselection()
        if selection:
            self.result = self.departments[selection[0]]
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()


class DepartmentManagementDialog:
    """Diálogo para gerenciamento de setores"""
    
    def __init__(self, parent, departments):
        self.departments = departments
        self.changes_made = False
        
        # Criar janela
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Gerenciar Setores")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista de setores
        list_frame = ttk.LabelFrame(main_frame, text="Setores Cadastrados", padding="5")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.listbox = tk.Listbox(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="Criar Setor", command=self.create_department).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Editar Setor", command=self.edit_department).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Excluir Setor", command=self.delete_department).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Fechar", command=self.close).pack(side=tk.RIGHT, padx=2)
        
        # Atualizar lista
        self.refresh_list()
        
        # Centralizar janela
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Aguardar resultado
        self.dialog.wait_window()
    
    def refresh_list(self):
        """Atualiza a lista de setores"""
        self.listbox.delete(0, tk.END)
        for dept in self.departments:
            self.listbox.insert(tk.END, f"{dept.name} ({len(dept.team)} empregados)")
    
    def create_department(self):
        """Cria novo setor"""
        name = simpledialog.askstring("Criar Setor", "Nome do novo setor:")
        if name:
            name = name.strip()
            if any(dept.name == name for dept in self.departments):
                messagebox.showerror("Erro", "Setor já existe!")
            else:
                self.departments.append(Department(name))
                self.changes_made = True
                self.refresh_list()
                messagebox.showinfo("Sucesso", "Setor criado com sucesso!")
    
    def edit_department(self):
        """Edita setor selecionado"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um setor para editar!")
            return
        
        dept = self.departments[selection[0]]
        new_name = simpledialog.askstring("Editar Setor", f"Novo nome para '{dept.name}':", 
                                         initialvalue=dept.name)
        
        if new_name:
            new_name = new_name.strip()
            if any(d.name == new_name for d in self.departments if d != dept):
                messagebox.showerror("Erro", "Já existe um setor com esse nome!")
            else:
                # Atualizar nome nos empregados
                for emp in dept.team:
                    emp.department = new_name
                dept.name = new_name
                self.changes_made = True
                self.refresh_list()
                messagebox.showinfo("Sucesso", "Setor editado com sucesso!")
    
    def delete_department(self):
        """Exclui setor selecionado"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um setor para excluir!")
            return
        
        dept = self.departments[selection[0]]
        
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o setor '{dept.name}'?\n"
                              f"Os {len(dept.team)} empregados serão movidos para 'Nenhum'."):
            # Mover empregados para "Nenhum"
            for emp in dept.team:
                emp.department = "Nenhum"
            
            self.departments.remove(dept)
            self.changes_made = True
            self.refresh_list()
            messagebox.showinfo("Sucesso", "Setor excluído com sucesso!")
    
    def close(self):
        """Fecha o diálogo"""
        self.dialog.destroy()
