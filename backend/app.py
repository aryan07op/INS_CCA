# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
# Ensure this import path matches your folder structure
from utils.password_handler import PasswordHandler

app = Flask(__name__)
CORS(app)

# --- Endpoint for Step 1: Unsalted Hashes & Rainbow Tables ---
@app.route('/api/step1/unsalted', methods=['POST'])
def step1_unsalted_demo():
    data = request.get_json()
    password = data.get('password')
    if not password:
        return jsonify({'error': 'Password is required'}), 400

    # 1. Generate the insecure, unsalted hash
    unsalted_hash = PasswordHandler.hash_without_salt(password)
    
    # 2. Simulate a rainbow table attack against it
    attack_result = PasswordHandler.simulate_rainbow_table_attack(unsalted_hash)

    return jsonify({
        'password': password,
        'hash': unsalted_hash,
        'attack': attack_result
    })

# --- Endpoint for Step 2: Salted Hash Comparison ---
@app.route('/api/step2/salted-comparison', methods=['POST'])
def step2_salted_demo():
    data = request.get_json()
    password_a = data.get('passwordA')
    password_b = data.get('passwordB')
    use_same_salt = data.get('useSameSalt', False)

    if not password_a or not password_b:
        return jsonify({'error': 'Both passwords are required'}), 400

    salt_a_hex = None
    salt_b_hex = None
    
    # Logic for salting
    if use_same_salt:
        # Using the *same* salt for both (less secure, demonstrates a concept)
        common_salt_hex = PasswordHandler.generate_salt()
        hash_a = PasswordHandler.hash_with_given_salt(password_a, common_salt_hex)
        hash_b = PasswordHandler.hash_with_given_salt(password_b, common_salt_hex)
        salt_a_hex = common_salt_hex
        salt_b_hex = common_salt_hex
    else:
        # Using *unique* salts for each (the correct way)
        salted_a = PasswordHandler.hash_with_custom_salt(password_a)
        salted_b = PasswordHandler.hash_with_custom_salt(password_b)
        hash_a = salted_a['hash']
        hash_b = salted_b['hash']
        salt_a_hex = salted_a['salt']
        salt_b_hex = salted_b['salt']

    return jsonify({
        'passwordA': {'pass': password_a, 'salt': salt_a_hex, 'hash': hash_a},
        'passwordB': {'pass': password_b, 'salt': salt_b_hex, 'hash': hash_b},
        'usingSameSalt': use_same_salt
    })

# --- Endpoint for Step 3: Modern Standard (Bcrypt) ---
@app.route('/api/step3/bcrypt', methods=['POST'])
def step3_bcrypt_demo():
    data = request.get_json()
    password = data.get('password')
    if not password:
        return jsonify({'error': 'Password is required'}), 400

    # 1. Hash the password
    bcrypt_hash_obj_1 = PasswordHandler.hash_with_bcrypt(password)
    
    # 2. Hash the *same* password again to show the hash is different
    bcrypt_hash_obj_2 = PasswordHandler.hash_with_bcrypt(password)

    # 3. Verify the original password against both hashes
    is_valid_1 = PasswordHandler.verify_bcrypt(password, bcrypt_hash_obj_1['hash'])
    is_valid_2 = PasswordHandler.verify_bcrypt(password, bcrypt_hash_obj_2['hash'])

    return jsonify({
        'password': password,
        'hash1': bcrypt_hash_obj_1['hash'],
        'hash2': bcrypt_hash_obj_2['hash'],
        'verification': {
            'hash1_valid': is_valid_1,
            'hash2_valid': is_valid_2
        }
    })


if __name__ == '__main__':
    app.run(debug=True)
