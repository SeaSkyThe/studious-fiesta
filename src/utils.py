from flask import *

# Utils for /add view
def add_build_responses(is_json):
    if(is_json):
        positive_response = make_response(jsonify({'success': True, 'message': "Cliente cadastrado com sucesso!"}), 200)
        invalid_cpf_response = make_response(jsonify({'success': False, 'message': "CPF Invalido"}), 422)
        existant_cpf_response = make_response(jsonify({'success': False, 'message': "Um cliente com esse CPF ja existe"}), 400)
    else:
        positive_response = make_response(render_template('add_customer_success.html'), 201)
        invalid_cpf_response = make_response(render_template('add_customer_fail.html'), 422)
        existant_cpf_response = make_response(render_template('add_customer_fail.html'), 400)
    
    return positive_response, invalid_cpf_response, existant_cpf_response

def add_gather_data(data):
    customer_name = data['customer_name']
    customer_cpf = data['customer_cpf']
    customer_birthdate = data['customer_birthdate']
    
    return customer_name, customer_cpf, customer_birthdate

# Utils for /search view
def search_build_response(is_json, customer):
    if(is_json):
        response = make_response(jsonify({'success': False, 'cliente': {}}), 200)
        if(customer):
            response = make_response(jsonify({'success': True, 'cliente': {'customer_name': customer[0], 'customer_cpf': customer[1], 'customer_birthdate': customer[2]}}), 200)        
    else:
        response = make_response(render_template('search_customer.html', customer=customer), 200)
    return response

def search_gather_data(data):
    cpf = data['customer_cpf']
    return cpf