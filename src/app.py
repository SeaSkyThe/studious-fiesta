import sqlite3
from flask import *
import json
from customer import Customer
from populate_db import populate
import sys
from flask_paginate import Pagination, get_page_parameter


app = Flask(__name__)
app.static_folder = 'static'

Customer.create_database_table()
populate()

# HOMEPAGE - Contém Links para todos os outros ENDPOINTS 
@app.route('/', methods=['GET'])
def home():
    return render_template('homepage.html'), 200

# /ADD - Endpoint para adicionar um novo CUSTOMER
@app.route('/add', methods=['POST', 'GET'])
def add_customers():
    if(request.method == 'GET'):
        return render_template('add_customer.html'), 200
    
    elif(request.method == 'POST'):
        if(request.data): # Se for Via JSON
            json = request.get_json()
            if(json):
                # Dados do CUSTOMER vindos do json
                customer_name = json['customer_name']
                customer_cpf = json['customer_cpf']
                customer_birthdate = json['customer_birthdate']
                
                positive_response = make_response(jsonify({'success': True, 'message': "Cliente cadastrado com sucesso!"}), 200)
                invalid_cpf_response = make_response(jsonify({'success': False, 'message': "CPF Invalido"}), 422)
                existant_cpf_response = make_response(jsonify({'success': False, 'message': "Um cliente com esse CPF ja existe"}), 400)

        else: # Se for Via form
            # Dados do CUSTOMER vindos do form.
            customer_name = request.form['customer_name']
            customer_cpf = request.form['customer_cpf']
            customer_birthdate = request.form['customer_birthdate']
            
            positive_response = make_response(render_template('add_customer_success.html'), 201)
            invalid_cpf_response = make_response(render_template('add_customer_fail.html'), 422)
            existant_cpf_response = make_response(render_template('add_customer_fail.html'), 400)

        # Cria o objeto CUSTOMER
        customer = Customer(name=customer_name, cpf=customer_cpf, birthdate=customer_birthdate)
        
        # Se o CPF não passar na verificação, manda um 422
        if(not customer.is_cpf_valid()):
            return invalid_cpf_response
        
        # Se já existir um usuário cadastrado com esse CPF, 400
        if(not Customer.add_customer(customer)):
            return existant_cpf_response
        
        # Se não, sucesso.
        return positive_response
                
@app.route('/show', methods=['GET'])
def show_customers():
    current_page = request.args.get(get_page_parameter(), type=int, default=1)
    page_size = 10
    
    offset = request.args.get('offset', None)
    limit = request.args.get('limit', None)
    
    # Recuperando os clientes do banco de dados
    customers = Customer.get_customers(limit, offset)

    if(limit and offset):
        response = {"success": True, "clientes": []}
        
        for customer in customers:
            response['clientes'].append(
                {'customer_name': customer[0],
                 'customer_cpf': customer[1],
                 'customer_birthdate': customer[2]}
            )
    else:
        if(not customers):
            response = make_response(render_template('list_customers.html'))
        
        else:
            # Dividindo a lista de clientes em chunks de tamanho 10, cada chunk será exibido em uma página
            customers_pages = [customers[i:i+page_size] for i in range(0, len(customers), page_size)]

            pagination = Pagination(page=current_page, total=len(customers), search=False, record_name='customers')
            
            
            response = make_response(render_template('list_customers.html', customers=customers_pages[current_page-1], pagination=pagination), 200)
    
    

    return response
    
@app.route('/search', methods=['GET', 'POST'])
def search_customers():
    if(request.method == 'GET'):
        return render_template('search_customer.html'), 200
    
    elif(request.method == 'POST'):
        if(request.data): # Se for Via JSON
            json = request.get_json()
            cpf = json['customer_cpf']
        else: # Se for via FORM
            cpf = request.form['customer_cpf']
        
        customer = []
        customer = Customer.get_customer_by_cpf(cpf)
        
        # Montando a resposta
        if(request.data):
            response = make_response(jsonify({'success': True, 'cliente': {'customer_name': customer[0], 'customer_cpf': customer[1], 'customer_birthdate': customer[2]}}), 200)
        else:
            response = make_response(render_template('search_customer.html', customer=customer), 200)
        
        return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)