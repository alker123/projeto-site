print("Testando importação do meuapp...")
try:
    import meuapp
    print("Importação bem-sucedida!")
except Exception as e:
    print(f"Erro ao importar meuapp: {e}")
