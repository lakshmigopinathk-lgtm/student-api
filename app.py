from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Create Flask application
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect database with Flask
db = SQLAlchemy(app)

# Create Student table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


# Create POST API
@app.route('/student', methods=['POST'])
def add_student():

    # Receive JSON data from Postman
    data = request.get_json()
    
    # Check duplicate email
    existing_student = Student.query.filter_by(email=data['email']).first()

    if existing_student:
        return {
            "message": "already registered"
        }

    # Create student object
    student = Student(
        first_name=data['first_name'],
        class_name=data['class_name'],
        email=data['email']
    )
    if student.id:
        existing_student = Student.query.get(student.id)

        if not existing_student:
            return jsonify({
                "message": "Student not found"
            }), 404
        existing_student.first_name=student.first_name
        existing_student.class_name=student.class_name
        existing_student.email=student.email
    
        student=existing_student


    # Save into database
    db.session.add(student)
    db.session.commit()

    # Send response
    return jsonify({
        "message": "Student added successfully ",
        "id":student.id
    })
#finding student details by id
@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):

    # Find student by id
    student = Student.query.get(id)

    # If student not found
    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404
    

    # Return student details
    return jsonify({
        "id": student.id,
        "first_name": student.first_name,
        "class_name": student.class_name,
        "email": student.email
    })
@app.route('/students', methods=['GET'])
def get_all_students():

    # Get all students
    students = Student.query.all()

    # Convert objects into list
    student_list = []

    for student in students:
        student_list.append({
            "id": student.id,
            "first_name": student.first_name,
            "class_name": student.class_name,
            "email": student.email
        })

    # Return list
    return jsonify(student_list)
@app.route('/students/filter', methods=['GET'])
def filter_students():

    # Get request parameters
    class_name = request.args.get('class_name')
    first_name = request.args.get('first_name')

    # Start query
    query = Student.query

    # Apply filters
    if class_name:
        query = query.filter_by(class_name=class_name)

    if first_name:
        query = query.filter_by(first_name=first_name)

    # Get filtered students
    students = query.all()

    # Convert to list
    student_list = []

    for student in students:
        student_list.append({
            "id": student.id,
            "first_name": student.first_name,
            "class_name": student.class_name,
            "email": student.email
        })

    return jsonify(student_list)
#deleting
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_student(id):

    student = Student.query.get(id)

    if student:
        db.session.delete(student)
        db.session.commit()

        return {
            "message": "Student deleted successfully"
        }

    return {
        "message": "Student not found"
    }
#finding student based on their names 
@app.route('/search', methods=['GET'])
def search_student():

    name = request.args.get('name')

    students = Student.query.filter(
        Student.first_name.like(f'{name}%')
    ).all()

    student_list = []

    for student in students:
        student_list.append({
            "id": student.id,
            "first_name": student.first_name,
            "class_name": student.class_name,
            "email": student.email
        })

    return jsonify(student_list)
# Run application
if __name__ == '__main__':

    # Create database and tables
    with app.app_context():
        db.create_all()

    # Run on custom port
    app.run(debug=True, port=8000)