import json
import os
from typing import List, Dict
from models import Employee, Department

class DataManager:
    def __init__(self, employees_file="employees.json", departments_file="departments.json"):
        """
        Inicializa o gerenciador de dados
        """
        self.employees_file = employees_file
        self.departments_file = departments_file
    
    def save_employees(self, employees: List[Employee]) -> bool:
        """
        Salva a lista de empregados no arquivo JSON
        """
        try:
            data = [emp.to_dict() for emp in employees]
            with open(self.employees_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar empregados: {e}")
            return False
    
    def load_employees(self) -> List[Employee]:
        """
        Carrega a lista de empregados do arquivo JSON
        """
        try:
            if not os.path.exists(self.employees_file):
                return []
            
            with open(self.employees_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            employees = []
            for emp_data in data:
                employees.append(Employee.from_dict(emp_data))
            
            return employees
        except Exception as e:
            print(f"Erro ao carregar empregados: {e}")
            return []
    
    def save_departments(self, departments: List[Department]) -> bool:
        """
        Salva a lista de setores no arquivo JSON
        """
        try:
            data = [dept.to_dict() for dept in departments]
            with open(self.departments_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar setores: {e}")
            return False
    
    def load_departments(self, employees_dict: Dict[int, Employee]) -> List[Department]:
        """
        Carrega a lista de setores do arquivo JSON
        """
        try:
            if not os.path.exists(self.departments_file):
                return []
            
            with open(self.departments_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            departments = []
            for dept_data in data:
                departments.append(Department.from_dict(dept_data, employees_dict))
            
            return departments
        except Exception as e:
            print(f"Erro ao carregar setores: {e}")
            return []
    
    def save_all_data(self, employees: List[Employee], departments: List[Department]) -> bool:
        """
        Salva todos os dados (empregados e setores)
        """
        employees_saved = self.save_employees(employees)
        departments_saved = self.save_departments(departments)
        return employees_saved and departments_saved
    
    def load_all_data(self) -> tuple:
        """
        Carrega todos os dados (empregados e setores)
        """
        employees = self.load_employees()
        employees_dict = {emp.id: emp for emp in employees}
        departments = self.load_departments(employees_dict)
        
        return employees, departments
