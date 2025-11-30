from cadastrar import *
cadastrar_conta("test123@gmail.com", "senha123", "Test User", "123456789")
print(verificar_login("test123@gmail.com", "senha123", "Test User", "123456789"))