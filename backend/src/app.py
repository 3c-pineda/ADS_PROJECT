from flask import Flask, jsonify, request
import pymysql.cursors
import os
import bcrypt
import shutil

app = Flask(__name__)

HOST = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
app.config['UPLOAD_PATH'] = "../../pet_shelter_sys/public/images/pet_images/"

# Database connection
DB_HOST = 'localhost'
DB_USER = 'admin'
DB_PASSWORD = 'adminpass'
DB_NAME = 'animal_shelter'

### ANIMAL INFORMATION API ENDPOINTS

# Get all the rows

@app.route('/api/animals', methods=['GET'])
def get_all_animals():
    """Fetch all rows from the animal_information table and return as JSON."""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Query to fetch all rows
            cursor.execute("SELECT * FROM animal_information")
            rows = cursor.fetchall()

        # Return the results as JSON
        return jsonify(rows)
    finally:
        # Close the database connection
        connection.close()

# Get a specific row using the animal_id

@app.route('/api/animals/<int:animal_id>', methods=['GET'])
def get_animal_by_id(animal_id):
    """Fetch a specific animal by its primary key (animal_id) and return as JSON."""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Query to fetch a specific animal by animal_id
            cursor.execute("SELECT * FROM animal_information WHERE animal_id = %s", (animal_id,))
            row = cursor.fetchone()  # fetchone to get a single result

        if row:
            # Return the specific animal data as JSON
            return jsonify(row)
        else:
            # Return a 404 error if the animal with the given ID is not found
            abort(404, description="Animal not found")

    finally:
        # Close the database connection
        connection.close()

# Get all rows with specific species
@app.route('/api/animals/<string:species>', methods=['GET'])
def get_animal_by_species(species):
    """Fetch all animals of a specific species and return as JSON."""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Query to fetch all animals by species
            cursor.execute("SELECT * FROM animal_information WHERE species = %s", (species,))
            rows = cursor.fetchall()  # fetchall to get all matching results

        if rows:
            # Return the animal data as JSON
            return jsonify(rows)
        else:
            # Return a 404 error if no animals of the given species are found
            abort(404, description="No animals found for the specified species")

    finally:
        # Close the database connection
        connection.close()

# Utility function to check allowed file extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['jpeg','jpg','png']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/animals', methods=['POST'])
def create_animal():
    """Add a new animal to the database and store the uploaded image."""
    
    # Check if an image was uploaded
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']
    
    # Check if the image has a valid filename and extension
    if image and allowed_file(image.filename):
        filename = image.filename  # Use original filename
    else:
        return jsonify({"error": "Invalid file type. Only PNG, JPG, JPEG, GIF are allowed."}), 400
    
    # Parse the form data (animal details)
    animal_data = request.form.to_dict()

    # Validate the required fields
    required_fields = ['name', 'species', 'breed', 'age', 'sex', 'characteristics', 'health_status',
                       'arrival_date', 'adoption_status', 'special_needs', 'adoption_date', 'birthday',
                       'notes', 'size', 'location_rescued', 'description', 'is_desexed']
    
    missing_fields = [field for field in required_fields if field not in animal_data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor() as cursor:
            # Insert the animal data into the database
            sql = """
                INSERT INTO animal_information (
                    name, species, breed, age, sex, characteristics, health_status, arrival_date,
                    adoption_status, special_needs, adoption_date, birthday, notes, size, location_rescued,
                    description, is_desexed
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            cursor.execute(sql, (
                animal_data['name'], animal_data['species'], animal_data['breed'], animal_data['age'],
                animal_data['sex'], animal_data['characteristics'], animal_data['health_status'],
                animal_data['arrival_date'], animal_data['adoption_status'], animal_data['special_needs'],
                animal_data['adoption_date'], animal_data['birthday'], animal_data['notes'], animal_data['size'],
                animal_data['location_rescued'], animal_data['description'], animal_data['is_desexed']
            ))

            # Commit the transaction to save the data
            connection.commit()

            # Get the newly inserted animal's ID (primary key)
            animal_id = cursor.lastrowid

            # Create a folder named after the animal ID
            animal_folder_path = os.path.join(app.config['UPLOAD_PATH'], str(animal_id))

            if not os.path.exists(animal_folder_path):
                os.makedirs(animal_folder_path)

            # Save the image as 'profile.<original_extension>'
            profile_filename = f"profile.jpeg"
            image_path = os.path.join(animal_folder_path, profile_filename)
            image.save(image_path)

            # Return a success response with the new animal ID
            return jsonify({
                "message": "Animal created successfully",
                "animal_id": animal_id,
                "image_path": image_path
            }), 201

    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500

    finally:
        connection.close()




# Update animal information using animal_id with 'PUT' method

@app.route('/api/animals/<int:animal_id>', methods=['PUT'])
def update_animal(animal_id):
    """Update an animal's information by animal_id."""
    data = request.get_json()

    # Check if the required fields are in the request
    required_fields = ['name', 'species', 'breed', 'age', 'sex', 'characteristics', 'health_status', 'arrival_date', 'adoption_status', 'special_needs', 'adoption_date', 'birthday', 'notes', 'size', 'location_rescued', 'description', 'is_desexed']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor() as cursor:
            # SQL query to update animal information
            query = """
                UPDATE animal_information
                SET name = %s, species = %s, breed = %s, age = %s, sex = %s,
                    characteristics = %s, health_status = %s, arrival_date = %s,
                    adoption_status = %s, special_needs = %s, adoption_date = %s,
                    birthday = %s, notes = %s, size = %s, location_rescued = %s,
                    description = %s, is_desexed = %s
                WHERE animal_id = %s
            """
            cursor.execute(query, (
                data['name'], data['species'], data['breed'], data['age'], data['sex'],
                data['characteristics'], data['health_status'], data['arrival_date'],
                data['adoption_status'], data['special_needs'], data['adoption_date'],
                data['birthday'], data['notes'], data['size'], data['location_rescued'],
                data['description'], data['is_desexed'], animal_id
            ))

            connection.commit()

        return jsonify({'message': 'Animal updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()

# Delete row using animal_id with 'DELETE' method

@app.route('/api/animals/<int:animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    """Delete an animal's information by animal_id."""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor() as cursor:
            # SQL query to delete animal information
            query = "DELETE FROM animal_information WHERE animal_id = %s"
            cursor.execute(query, (animal_id,))

            if cursor.rowcount == 0:  # No rows were deleted
                return jsonify({'error': 'Animal not found'}), 404

            connection.commit()

            # delete folder images

            animal_image_folder = os.path.join(app.config['UPLOAD_PATH'], str(animal_id))
            if os.path.exists(animal_image_folder):
                shutil.rmtree(animal_image_folder)

        return jsonify({'message': 'Animal deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()


### ANIMAL MEDICAL HISTORY API ENDPOINTS

# Get all records

@app.route('/api/animal_med_history', methods=['GET'])
def get_all_med_history():
    """Get all medical history records."""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = "SELECT * FROM animal_med_history"
            cursor.execute(query)
            result = cursor.fetchall()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()

# Get specific record using vacc_id

@app.route('/api/animal_med_history/<int:vacc_id>', methods=['GET'])
def get_med_history(vacc_id):
    """Get a specific medical history record by vacc_id."""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = "SELECT * FROM animal_med_history WHERE vacc_id = %s"
            cursor.execute(query, (vacc_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({'error': 'Record not found'}), 404

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()

# Create a record
@app.route('/api/animal_med_history', methods=['POST'])
def create_animal_med_history():
    """Add a new medical history record for an animal."""
    # Parse the JSON data from the request
    data = request.json

    # Validate input data
    required_fields = ['vacc_type', 'vacc_date', 'vacc_dose', 'animal_id']

    # Ensure all required fields are present
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor() as cursor:
            # SQL query to insert a new record into the animal_med_history table
            sql = """
                INSERT INTO animal_med_history (
                    vacc_type, vacc_date, vacc_dose, animal_id
                )
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data['vacc_type'], data['vacc_date'],
                data['vacc_dose'], data['animal_id']
            ))

            # Commit the transaction
            connection.commit()

            # Return a success response with the new record ID
            return jsonify({
                "message": "Medical history record created successfully",
                "med_history_id": cursor.lastrowid
            }), 201

    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500

    finally:
        connection.close()


# Update specific record using vacc_id with 'PUT' method

@app.route('/api/animal_med_history/<int:vacc_id>', methods=['PUT'])
def update_med_history(vacc_id):
    """Update a medical history record for an animal by vacc_id."""
    data = request.get_json()

    required_fields = ['vacc_type', 'vacc_date', 'vacc_dose', 'animal_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor() as cursor:
            # Check if the animal_id exists in the animal_information table
            check_animal_query = "SELECT 1 FROM animal_information WHERE animal_id = %s"
            cursor.execute(check_animal_query, (data['animal_id'],))
            animal_exists = cursor.fetchone()

            if not animal_exists:
                return jsonify({'error': 'Animal ID does not exist'}), 400

            # SQL query to update the medical history record
            query = """
                UPDATE animal_med_history
                SET vacc_type = %s, vacc_date = %s, vacc_dose = %s, animal_id = %s
                WHERE vacc_id = %s
            """
            cursor.execute(query, (
                data['vacc_type'], data['vacc_date'], data['vacc_dose'], data['animal_id'], vacc_id
            ))

            if cursor.rowcount == 0:  # No rows were updated
                return jsonify({'error': 'Medical history not found'}), 404

            connection.commit()

        return jsonify({'message': 'Medical history updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()

# Delete specific record using vacc_id with 'DELETE' method

@app.route('/api/animal_med_history/<int:vacc_id>', methods=['DELETE'])
def delete_med_history(vacc_id):
    """Delete a medical history record by vacc_id."""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor() as cursor:
            # SQL query to delete the medical history record
            query = "DELETE FROM animal_med_history WHERE vacc_id = %s"
            cursor.execute(query, (vacc_id,))

            if cursor.rowcount == 0:
                return jsonify({'error': 'Medical history record not found'}), 404

            connection.commit()

        return jsonify({'message': 'Medical history record deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()

# Admin api goes here

@app.route("/api/login", methods=["POST"])
def login_admin():
    """Try to authenticate admin"""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor

    )
    data = request.get_json()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM admin WHERE username = %s"
            cursor.execute(query, (data['username'],))
            if cursor.rowcount == 0:
                return jsonify({'error': 'Username or password incorrect.'}), 401

            # This is where it goes it username has been found.
            admin = cursor.fetchone()
            stored_password = admin['password']
            try_password = data['password']
            if bcrypt.checkpw(try_password.encode('utf-8'), stored_password.encode('utf-8')):
                return jsonify({'message': 'Login successful'}), 200
            return jsonify({'error': 'Username or password incorrect.'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()

# Contact us post api end point
@app.route("/api/contact-us", methods=["POST"])
def save_email():
    data = request.get_json()
    print(data)
    # Validate input data
    required_fields = ['name', 'email', 'subject', 'reason', 'description']

    # Ensure all required fields are present
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    filename = f"./emails/{data['email']}.txt"

    # Prepare the content to write to the file (e.g., format it as a string)
    content = f"Name: {data['name']}\nEmail: {data['email']}\nSubject: {data['subject']}\nReason: {data['reason']}\nDescription: {data['description']}\n\n"

    # Write to the file
    with open(filename, 'a') as file:
        file.write(content)

    return jsonify({"message": "Email saved successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
