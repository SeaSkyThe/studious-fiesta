try:
    from app import app
    import unittest
except Exception as e:
    print(f"Some modules are missing {e} ")


class APITest(unittest.TestCase):
    # Verifica se a resposta das GET requests para todas as rotas é 200.
    def test_index_route(self):
        response = app.test_client(self).get('/')
        self.assertEqual(response.status_code, 200)
    
    
    # TESTES PARA ROTA DE ADICIONAR CUSTOMERS
    def test_add_route(self):
        response = app.test_client(self).get('/add')
        self.assertEqual(response.status_code, 200)
    
    # Testa o caso em que é passado um CPF válido no formulário
    def test_add_route_when_submitting_valid_cpf(self):
        import datetime
        date = datetime.datetime.strptime('1999-02-06', '%Y-%m-%d').date()
        response = app.test_client(self).post('/add', data={'customer_name': "Customer1", 'customer_birthdate': date, 
                                                               'customer_cpf': '111.444.777-35'})
        # Pode retornar 201 caso seja criado um novo registro ou 400, quando já existe um registro com esse cpf.
        self.assertTrue(response.status_code == 201 or response.status_code == 400) 
    
    # Testa o caso em que é passado um cpf inválido
    def test_add_route_when_submitting_invalid_cpf(self):
        import datetime
        date = datetime.datetime.strptime('1999-02-06', '%Y-%m-%d').date()
        response = app.test_client(self).post('/add', data={'customer_name': "Customer1", 'customer_birthdate': date, 
                                                               'customer_cpf': '111.444.777-05'})
        # Verifica se a resposta é 422
        self.assertEqual(response.status_code, 422)
        
    # Testa o caso em que é passado um cpf vazio
    def test_add_route_when_submitting_empty_cpf(self):
        import datetime
        date = datetime.datetime.strptime('1999-02-06', '%Y-%m-%d').date()
        response = app.test_client(self).post('/add', data={'customer_name': "Customer1", 'customer_birthdate': date, 
                                                               'customer_cpf': ''})
        self.assertEqual(response.status_code, 422)
    
    # Testa o caso em que é passado um não númerico
    def test_add_route_when_submitting_wrong_cpf(self):
        import datetime
        date = datetime.datetime.strptime('1999-02-06', '%Y-%m-%d').date()
        response = app.test_client(self).post('/add', data={'customer_name': "Customer1", 'customer_birthdate': date, 
                                                               'customer_cpf': 'aaaabcdd'})
        self.assertEqual(response.status_code, 422)
    
    # TESTES PARA ROTA DE PESQUISAR CUSTOMERS
    def test_search_route(self):
        response = app.test_client(self).get('/search')
        self.assertEqual(response.status_code, 200)
    
    def test_search_route_when_submitting_valid_cpf(self):
        response = app.test_client(self).post('/search', data={'customer_cpf': '111.444.777-35'})
        self.assertEqual(response.status_code, 200)
        
    def test_search_route_when_submitting_non_existant_cpf(self):
        response = app.test_client(self).post('/search', data={'customer_cpf': '11111111111'})
        self.assertEqual(response.status_code, 200)
    
    # TESTES PARA ROTA DE LISTAR CUSTOMERS
    def test_show_route(self):
        response = app.test_client(self).get('/show')
        self.assertEqual(response.status_code, 200) 


if __name__ == '__main__':
    unittest.main()