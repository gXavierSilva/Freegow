from flask import Blueprint, request, jsonify, render_template
from db import get_db_connection

user_bp = Blueprint("user", __name__)

@user_bp.route('/')
def hello():
    return jsonify({"message": "Bem-vindo à API PostgreSQL"})

# Rota para criar um novo usuário
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "As credenciais são obrigatórias."}), 400

    name, email, password = data["name"], data["email"], data["password"]
    conn = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, password, created_at, is_active""",
            (name, email, password)
        )
        new_item = cur.fetchone()
        conn.commit()
        return jsonify({
            "id": new_item[0],
            "name": new_item[1],
            "email": new_item[2],
            "password": new_item[3],
            "created_at": new_item[4].isoformat(),
            "is_active": new_item[5]
        }), 201
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

# Rota para listar todos os usuários
@user_bp.route('/users', methods=['GET'])
def get_users():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password, created_at, is_active FROM users ORDER BY created_at DESC")
        users = cur.fetchall()
        return jsonify([
            {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "password": user[3],
                "created_at": user[4].isoformat(),
                "is_active": user[5]
            } for user in users
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

# Consulta o banco de dados buscando um usuário
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get("email"), data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({"success": True, "redirect": "/dashboard"})
    else:
        return jsonify({"success": False, "message": "Credenciais inválidas"}), 401
