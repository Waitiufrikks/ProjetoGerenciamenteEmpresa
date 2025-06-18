"""
Modelos de dados para o sistema de gestão de empresa
Contém as classes Employee e Department com suas funcionalidades
"""

class Employee:
    """Classe que representa um empregado da empresa"""
    
    counter_id = 1
    
    def __init__(self, name, cpf, phone, address, department="Nenhum", employee_id=None):
        """
        Inicializa um novo empregado
        
        Args:
            name (str): Nome do empregado
            cpf (str): CPF do empregado
            phone (str): Telefone do empregado
            address (str): Endereço do empregado
            department (str): Setor do empregado
            employee_id (int): ID específico (usado ao carregar dados)
        """
        if employee_id is not None:
            self.id = employee_id
            # Atualiza o contador para evitar conflitos
            if employee_id >= Employee.counter_id:
                Employee.counter_id = employee_id + 1
        else:
            self.id = Employee.counter_id
            Employee.counter_id += 1
        
        self.name = name
        self.cpf = cpf
        self.phone = phone
        self.address = address
        self.department = department
    
    def update_data(self, name=None, phone=None, address=None):
        """
        Atualiza os dados do empregado
        
        Args:
            name (str): Novo nome (opcional)
            phone (str): Novo telefone (opcional)
            address (str): Novo endereço (opcional)
        """
        if name is not None:
            self.name = name
        if phone is not None:
            self.phone = phone
        if address is not None:
            self.address = address
    
    def to_dict(self):
        """Converte o empregado para dicionário para serialização JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'cpf': self.cpf,
            'phone': self.phone,
            'address': self.address,
            'department': self.department
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria um empregado a partir de um dicionário"""
        return cls(
            name=data['name'],
            cpf=data['cpf'],
            phone=data['phone'],
            address=data['address'],
            department=data['department'],
            employee_id=data['id']
        )


class Department:
    """Classe que representa um setor da empresa"""
    
    def __init__(self, name):
        """
        Inicializa um novo setor
        
        Args:
            name (str): Nome do setor
        """
        self.name = name
        self.team = []
    
    def add_employee(self, employee):
        """
        Adiciona um empregado ao setor
        
        Args:
            employee (Employee): Empregado a ser adicionado
        """
        if employee not in self.team:
            self.team.append(employee)
    
    def remove_employee(self, employee):
        """
        Remove um empregado do setor
        
        Args:
            employee (Employee): Empregado a ser removido
        """
        if employee in self.team:
            self.team.remove(employee)
    
    def to_dict(self):
        """Converte o setor para dicionário para serialização JSON"""
        return {
            'name': self.name,
            'team_ids': [emp.id for emp in self.team]
        }
    
    @classmethod
    def from_dict(cls, data, employees_dict):
        """
        Cria um setor a partir de um dicionário
        
        Args:
            data (dict): Dados do setor
            employees_dict (dict): Dicionário de empregados por ID
        """
        department = cls(data['name'])
        for emp_id in data.get('team_ids', []):
            if emp_id in employees_dict:
                department.add_employee(employees_dict[emp_id])
        return department
