from flask import Blueprint, request, jsonify, render_template
from db import get_db_connection

role_bp = Blueprint("role", __name__)

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

@role_bp.route('/roles', methods=['POST'])
def create_roles():
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

@role_bp.route('/roles/<int:role_id>', methods=['PUT'])
def update_roles(role_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados para atualização são obrigatórios."}), 400
    
    name, access, is_active = data["name"], data["access"], data["is_active"]

    if name is None and access is None and is_active is None:
        return jsonify({"error": "Pelo menos um campo (name, access ou is_active) deve ser fornecido para atualização."}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        update_fields = []
        values = []

        if name is not None:
            update_fields.append("name = %s")
            values.append(name)
        if access is not None:
            update_fields.append("access = %s")
            values.append(access)
        if is_active is not None:
            update_fields.append("is_active = %s")
            values.append(is_active)
        
        values.append(role_id)

        query = f"UPDATE roles SET {', '.join(update_fields)} WHERE role_id = %s RETURNING role_id, name, access, created_at, is_active"
        
        cur.execute(query, values)
        updated_role = cur.fetchone()

        if updated_role is None:
            return jsonify({"error": "Cargo não encontrado."}), 404
        
        conn.commit()
        return jsonify({
            "clinic_id": updated_role[0],
            "name": updated_role[1],
            "access": updated_role[2],
            "created_at": updated_role[3].isoformat(),
            "is_active": updated_role[4]
        }), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@role_bp.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_roles(role_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT role_id FROM roles WHERE role_id = %s", (role_id,))
        role = cur.fetchone()

        if role is None:
            return jsonify({"error": "Cargo não encontrado."}), 404
        
        cur.execute("DELETE FROM roles WHERE role_id = %s", (role_id,))
        conn.commit()

        return jsonify({"message": "Cargo deletado com sucesso."}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()