from customer import Customer

names = ['Maria',
         'Jose', 
         'Antonio',
         'Joao',
         'Francisco',
         'Ana',
         'Luiz',
         'Paulo',
         'Carlos',
         'Manoel',
         'Pedro',
         'Francisca',
         'Marcos',
         'Jorge',
         'Marcia']

cpfs = ['99214698198',
        '10149168870',
        '73573413307',
        '37766418274',
        '36063953450',
        '89118782787',
        '56158324280',
        '01326541307',
        '65182302665',
        '54832846310',
        '19418437783',
        '54436450309',
        '54945744742',
        '10183393376',
        '51535585250',]

data = '1985-05-17'

def populate():
    # Evitar tentar reescrever caso já exista (se existir o primeiro, quer dizer que já gravamos todos)
    if(Customer.get_customer_by_cpf(cpfs[0])):
       return False
    for i in range(0, 15):
        customer = Customer(name=names[i], cpf=cpfs[i], birthdate=data)
        Customer.add_customer(customer)
    return True