"""
Script para gerar executável do sistema de gestão de empresa
Usa PyInstaller para criar um arquivo .exe standalone
"""

import os
import sys
import subprocess

def build_executable():
    """Gera o executável usando PyInstaller"""
    
    print("Iniciando processo de geração do executável...")
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print("PyInstaller encontrado!")
    except ImportError:
        print("PyInstaller não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller instalado com sucesso!")
    
    # Parâmetros do PyInstaller
    pyinstaller_args = [
        "pyinstaller",
        "--onefile",                    # Gera um único arquivo executável
        "--windowed",                   # Sem console (apenas GUI)
        "--name=SistemaGestaoEmpresa",  # Nome do executável
        "--icon=NONE",                  # Sem ícone personalizado
        "--add-data=employees.json;.",  # Incluir arquivo de dados (se existir)
        "--add-data=departments.json;.", # Incluir arquivo de dados (se existir)
        "main.py"                       # Arquivo principal
    ]
    
    # Remover arquivos de dados se não existirem
    if not os.path.exists("employees.json"):
        pyinstaller_args = [arg for arg in pyinstaller_args if "employees.json" not in arg]
    
    if not os.path.exists("departments.json"):
        pyinstaller_args = [arg for arg in pyinstaller_args if "departments.json" not in arg]
    
    try:
        # Executar PyInstaller
        print("Executando PyInstaller...")
        subprocess.run(pyinstaller_args, check=True)
        
        print("\n" + "="*60)
        print("EXECUTÁVEL GERADO COM SUCESSO!")
        print("="*60)
        print(f"Localização: {os.path.join(os.getcwd(), 'dist', 'SistemaGestaoEmpresa.exe')}")
        print("\nO executável pode ser distribuído e executado em qualquer")
        print("computador Windows sem necessidade de instalação do Python.")
        print("\nArquivos de dados (employees.json e departments.json)")
        print("serão criados automaticamente na primeira execução.")
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao gerar executável: {e}")
        print("\nVerifique se todos os arquivos estão presentes:")
        print("- main.py")
        print("- models.py") 
        print("- data_manager.py")
        print("- gui_application.py")
        
    except Exception as e:
        print(f"Erro inesperado: {e}")

def clean_build_files():
    """Remove arquivos temporários da compilação"""
    import shutil
    
    temp_folders = ["build", "__pycache__"]
    temp_files = ["SistemaGestaoEmpresa.spec"]
    
    for folder in temp_folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Removido: {folder}/")
    
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removido: {file}")

if __name__ == "__main__":
    print("Sistema de Gestão de Empresa - Gerador de Executável")
    print("="*55)
    
    response = input("Deseja gerar o executável? (s/n): ").lower().strip()
    
    if response == 's':
        build_executable()
        
        clean_response = input("\nDeseja limpar arquivos temporários? (s/n): ").lower().strip()
        if clean_response == 's':
            clean_build_files()
            print("Limpeza concluída!")
    else:
        print("Operação cancelada.")
    
    input("\nPressione Enter para sair...")
