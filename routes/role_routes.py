from flask import Blueprint, request, jsonify, render_template
from db import get_db_connection

role_bp = Blueprint("role", __name__)

@role_bp.route('/roles', methods=['POST'])
def create_role():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "As credenciais são obrigatórias."}), 400

    # name, email, password = data["name"], data["email"], data["password"]
    name, access = data["name"], data["access"]
    conn = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO roles (name, access)
                VALUES (%s, %s)
                RETURNING role_id, name, access, created_at, is_active""",
            (name, access)
        )
        new_item = cur.fetchone()
        conn.commit()
        return jsonify({
            "role_id": new_item[0],
            "name": new_item[1],
            "access": new_item[2],
            "created_at": new_item[3].isoformat(),
            "is_active": new_item[4]
        }), 201
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@role_bp.route('/roles', methods=['GET'])
def get_roles():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT role_id, name, access, created_at, is_active FROM roles ORDER BY created_at DESC")
        roles = cur.fetchall()
        return jsonify([
            {
                "role_id": role[0],
                "name": role[1],
                "access": role[2],
                "created_at": role[3].isoformat(),
                "is_active": role[4]
            } for role in roles
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()
