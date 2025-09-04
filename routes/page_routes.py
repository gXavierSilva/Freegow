from flask import Blueprint, render_template, jsonify

page_bp = Blueprint("pages", __name__)

# Rotas que renderizam páginas de Registro/Login
@page_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@page_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@page_bp.route('/recovery', methods=['GET'])
def recovery_page():
    return render_template('recuperação.html')

# Rotas que renderizam páginas do Dashboard
@page_bp.route('/dashboard', methods=['GET'])
def dashboard_page():
    return render_template('dashboard.html')

@page_bp.route('/schedule', methods=['GET'])
def schedule_page():
    return render_template('agendadash.html')

@page_bp.route('/patients', methods=['GET'])
def patients_page():
    return render_template('pacientes.html')

@page_bp.route('/financial', methods=['GET'])
def financial_page():
    return render_template('financeiro.html')

@page_bp.route('/reports', methods=['GET'])
def reports_page():
    return render_template('relatorios.html')

@page_bp.route('/marketing', methods=['GET'])
def marketing_page():
    return render_template('marketing.html')

@page_bp.route('/management', methods=['GET'])
def management_page():
    return render_template('gerencia.html')

@page_bp.route('/help', methods=['GET'])
def help_page():
    return render_template('ajuda.html')

@page_bp.route('/settings', methods=['GET'])
def settings_page():
    return render_template('configuracao.html')

@page_bp.route('/myprofile', methods=['GET'])
def myprofile_page():
    return render_template('meuperfil.html')
