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
        # Assuming `animal_id` is a variable containing the dynamic animal ID
            cursor.execute("""
                SELECT ai.animal_id, ai.name, ai.species, ai.breed, ai.age, ai.sex, ai.characteristics, 
                    ai.health_status, ai.arrival_date, ai.adoption_status, ai.special_needs, ai.adoption_date, 
                    ai.birthday, ai.notes, ai.size, ai.location_rescued, ai.description, ai.is_desexed, 
                    COALESCE(amh.vacc_id, NULL) AS vacc_id, 
                    COALESCE(amh.vacc_type, NULL) AS vacc_type, 
                    COALESCE(amh.vacc_date, NULL) AS vacc_date, 
                    COALESCE(amh.vacc_dose, NULL) AS vacc_dose 
                FROM animal_information ai 
                LEFT JOIN animal_med_history amh ON ai.animal_id = amh.animal_id
                WHERE ai.animal_id = %s
            """, (animal_id,))
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

    # Validate the required fields (those that must always have a value)
    required_fields = ['name', 'species', 'breed', 'age', 'sex', 'characteristics', 'health_status',
                       'arrival_date', 'adoption_status', 'special_needs', 'birthday',
                       'notes', 'size', 'location_rescued', 'description', 'is_desexed']

    # Optional fields, such as 'adoption_date', can be empty
    optional_fields = ['adoption_date', 'vactype', 'vacdose', 'vacdate']

    # Check for missing required fields
    missing_fields = [field for field in required_fields if field not in animal_data or not animal_data[field]]

    # If there are missing required fields, set them to None (will be NULL in the DB)
    for field in required_fields:
        if field not in animal_data or not animal_data[field]:
            animal_data[field] = None

    # If any required fields are missing, return an error
    if missing_fields:
        return jsonify({"error": f"Missing or empty fields: {', '.join(missing_fields)}"}), 400

    # Check for missing but optional fields (and set to None if empty)
    for field in optional_fields:
        if field not in animal_data or not animal_data[field]:
            animal_data[field] = None
    vac = False
    if 'vactype' in animal_data:
        if animal_data['vactype'] and len(animal_data['vactype']) > 0:
            vac = True

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

            # Save vaccine data if vaccine is in form
            if vac:
                sql = """INSERT INTO animal_med_history (
                    vacc_type,
                    vacc_date,
                    vacc_dose,
                    animal_id
                ) VALUES (
                    %s, %s, %s, %s
                )"""
                cursor.execute(sql, (animal_data['vactype'], animal_data['vacdate'], animal_data['vacdose'], animal_id))
                connection.commit()


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


@app.route('/api/animals/<int:animal_id>', methods=['PUT'])
def update_animal(animal_id):
    """Update an animal's information by animal_id."""
    # Get the incoming request data
    data = request.form.to_dict()
    print(data)

    # Validate the required fields (those that must always have a value)
    required_fields = ['name', 'species', 'breed', 'age', 'sex', 'characteristics', 'health_status',
                       'arrival_date', 'adoption_status', 'special_needs', 'birthday',
                       'notes', 'size', 'location_rescued', 'description', 'is_desexed']

    # Optional fields, such as 'adoption_date', can be empty
    optional_fields = ['adoption_date', 'vactype', 'vacdose', 'vacdate']

    # Check for missing required fields
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    # If there are missing required fields, set them to None (will be NULL in the DB)
    for field in required_fields:
        if field not in data or not data[field]:
            data[field] = None

    # If any required fields are missing, return an error
    if missing_fields:
        return jsonify({"error": f"Missing or empty fields: {', '.join(missing_fields)}"}), 400

    # Check for missing but optional fields (and set to None if empty)
    for field in optional_fields:
        if field not in data or not data[field]:
           data[field] = None
    vac = False
    if 'vactype' in data:
        if data['vactype'] and len(data['vactype']) > 0:
            vac = True

    # Connect to the database
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor() as cursor:
            # Check if the image is part of the request
            if 'image' in request.files:
                image = request.files['image']

                # Check if the image has a valid file extension using allowed_file()
                if image and allowed_file(image.filename):
                    # Create a folder path for the animal if it doesn't exist
                    animal_folder_path = os.path.join(app.config['UPLOAD_PATH'], str(animal_id))
                    if not os.path.exists(animal_folder_path):
                        os.makedirs(animal_folder_path)

                    # Save the new image as 'profile.jpeg'
                    profile_filename = 'profile.jpeg'
                    image_path = os.path.join(animal_folder_path, profile_filename)
                    image.save(image_path)  # Overwrite the existing image

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

            # Commit the transaction to save the data
            connection.commit()


            # Save vaccine data if vaccine is in form
            if vac:
                # Check if data['vacid'] has a value (meaning it's an update request)
                if 'vacid' in data and data['vacid']:
                    # If vacid has a value, perform the UPDATE
                    sql = """UPDATE animal_med_history
                            SET vacc_type = %s, vacc_date = %s, vacc_dose = %s, animal_id = %s
                            WHERE vacc_id = %s"""
                    cursor.execute(sql, (data['vactype'], data['vacdate'], data['vacdose'], animal_id, data['vacid']))
                    connection.commit()
                else:
                    # If vacid is not provided or has no value, perform the INSERT
                    sql = """INSERT INTO animal_med_history (vacc_type, vacc_date, vacc_dose, animal_id)
                            VALUES (%s, %s, %s, %s)"""
                    cursor.execute(sql, (data['vactype'], data['vacdate'], data['vacdose'], animal_id))
                    connection.commit()

        # Return success response
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
            if stored_password == try_password:
            #if bcrypt.checkpw(try_password.encode('utf-8'), stored_password.encode('utf-8')):
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

@app.route('/api/animal-about', methods=['GET'])
def get_animals_about():
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
            cursor.execute("SELECT * FROM animal_information WHERE adoption_status = 'Adopted'")
            rows = cursor.fetchall()

        # Return the results as JSON
        return jsonify(rows)
    finally:
        # Close the database connection
        connection.close()

@app.route('/species-distribution', methods=['GET'])
def species_distribution():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with connection.cursor() as cursor:
            # Query to count species occurrences
            cursor.execute("""
                SELECT species, COUNT(*) as count
                FROM animal_information
                GROUP BY species
            """)
            results = cursor.fetchall()

        # Convert to JSON format
        data = {
            "labels": [row[0] for row in results],
            "values": [row[1] for row in results]
        }
        return jsonify(data)

    finally:
        connection.close()



@app.route('/adoption-status', methods=['GET'])
def adoption_status():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    try:
        with connection.cursor() as cursor:
            # Query to count adoption statuses
            cursor.execute("""
                SELECT adoption_status, COUNT(*) as count
                FROM animal_information
                GROUP BY adoption_status
            """)
            results = cursor.fetchall()

        # Convert to JSON format
        data = {
            "labels": [row[0] for row in results],
            "values": [row[1] for row in results]
        }
        return jsonify(data)

    finally:
        connection.close()


@app.route('/age-distribution', methods=['GET'])
def age_distribution():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    try:
        with connection.cursor() as cursor:
            # Query to categorize animals into age groups
            cursor.execute("""
                SELECT
                    CASE
                        WHEN age < 1 THEN 'Under 1 Year'
                        WHEN age BETWEEN 1 AND 3 THEN '1-3 Years'
                        WHEN age BETWEEN 4 AND 7 THEN '4-7 Years'
                        ELSE '8+ Years'
                    END as age_group,
                    COUNT(*) as count
                FROM animal_information
                GROUP BY age_group
            """)
            results = cursor.fetchall()

        # Convert to JSON format
        data = {
            "labels": [row[0] for row in results],
            "values": [row[1] for row in results]
        }
        return jsonify(data)

    finally:
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)
