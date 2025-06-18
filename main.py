import tkinter as tk
from gui_application import EmployeeManagementApp

def main():
    """Função principal que inicializa a aplicação GUI"""
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
