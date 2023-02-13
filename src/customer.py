import sqlite3
import sys

# Customer Model
class Customer:
    def __init__(self, name, cpf, birthdate):
        self.name = name
        self.cpf = Customer.normalize_cpf(cpf)
        self.birthdate = birthdate
        
    def __str__(self):
        return f"Name: {self.name} \nCPF: {self.cpf} \nBirthdate: {self.birthdate}\n"
    
    def is_cpf_valid(self):
        
        # Transforma os 9 primeiros digitos do cpf em inteiros e inverte a sua ordem, multiplicar pelos multiplicadores
        # 2, 3, 4, 5, 6, 7, 8, 9, 10
        nine_first_digits = list(self.cpf[0:9])
        try:
            nine_first_digits = [int(x) for x in nine_first_digits]
        except ValueError:
            return False
    
        nine_first_digits.reverse()
        total_sum = 0
        
        # Calculo do primeiro dígito
        for multiplier in range(2, 11):
            try:
                total_sum += nine_first_digits[multiplier-2]*multiplier
            except IndexError:
                return False
        remainder = total_sum%11 # Resto da divisão da soma por 11
        
        if(remainder < 2): # Se o resto for menor que 2, o dígito é 0
            digit = 0
        else: # Se for maior ou igual a 2, o dígito é 11 - resto
            digit = 11 - remainder 
        
        # Calculo do segundo dígito - semelhante, porém adicionamos o digito calculado no final do nosso cpf (nesse caso, no começo, pq ele está invertido)
        ten_first_digits = [digit] + nine_first_digits
        total_sum = 0
        for multiplier in range(2, 12):
            total_sum += ten_first_digits[multiplier-2]*multiplier
        
        remainder = total_sum%11 # Resto da divisão da soma por 11
        
        if(remainder < 2): # Se o resto for menor que 2, o dígito é 0
            digit2 = 0
        else: # Se for maior ou igual a 2, o dígito é 11 - resto
            digit2 = 11 - remainder 
        
        # Transformano o cpf calculado em string novamente
        calculated_cpf = [digit2] + ten_first_digits
        calculated_cpf.reverse()
        calculated_cpf = ''.join([str(x) for x in calculated_cpf])
        
        # Comparando e verificando se o cpf calculao é igual ao original
        if(calculated_cpf == self.cpf):
            return True
        
        return False
        
    
    # Cria a tabela CUSTOMERS no banco de dados.
    @staticmethod
    def create_database_table():
        try:
            c = sqlite3.connect("./database/customers.db").cursor()
            c.execute("CREATE TABLE IF NOT EXISTS CUSTOMERS(name TEXT, cpf TEXT, birthdate DATE)")
            c.connection.close()
            return True
        except Exception as e:
            print("\nErro ao criar tabela no banco de dados: ", e, "\n", file=sys.stderr)
            return False
    
    # Adiciona um CUSTOMER no banco de dados, utilizando um objeto Customer.
    @staticmethod
    def add_customer(customer_object):
        name = customer_object.name
        cpf = customer_object.cpf
        birthdate = customer_object.birthdate

        # Caso ja exista um CPF igual cadastrado, não cadastramos um novo.
        if(Customer.get_customer_by_cpf(cpf)):
            print("\nErro ao adicionar cliente no banco de dados - Já existe um cadastro com esse CPF: ", cpf," \n", file=sys.stderr)
            return False

        try:
            c = sqlite3.connect("./database/customers.db").cursor()
            c.execute("INSERT INTO CUSTOMERS (name, cpf, birthdate) VALUES (?, ?, ?)", (name, cpf, birthdate))
            c.connection.commit()
            c.connection.close()
            return True
        except Exception as e:
            print("Erro ao adicionar cliente no banco de dados: ", e, "\n", file=sys.stderr)
            return False
    
    # Resgata todos os CUSTOMERS do banco de dados
    @staticmethod
    def get_customers(limit=None, offset=None):
        result = []
        try:
            c = sqlite3.connect("./database/customers.db").cursor()
            if(limit and offset):
                c.execute("SELECT * FROM CUSTOMERS LIMIT ? OFFSET ?", (limit, offset))
            else:
                c.execute("SELECT * FROM CUSTOMERS")
            result = c.fetchall()
            c.connection.close()
        except Exception as e:
            print("Erro ao recuperar clientes do banco de dados: ", e, "\n", file=sys.stderr)
            return False
        
        return result
    
    # Restaga o CUSTOMER com um CPF específico.
    @staticmethod
    def get_customer_by_cpf(cpf):
        result = []
        cpf = Customer.normalize_cpf(cpf)
        try:
            c = sqlite3.connect("./database/customers.db").cursor()
            c.execute("SELECT * FROM CUSTOMERS WHERE CPF = (?)", (cpf,))
            result = c.fetchone()
            c.connection.close()
        except Exception as e:
            print("Erro ao recuperar clientes do banco de dados: ", e, "\n", file=sys.stderr)
            return False
        
        return result
    
    # Normaliza o CPF (remove a mascara)
    @staticmethod
    def normalize_cpf(cpf):
        return cpf.replace(".", "").replace("-", "")
        