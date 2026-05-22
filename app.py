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

    # Create student object
    student = Student(
        first_name=data['first_name'],
        class_name=data['class_name'],
        email=data['email']
    )

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
# Run application
if __name__ == '__main__':

    # Create database and tables
    with app.app_context():
        db.create_all()

    # Run on custom port
    app.run(debug=True, port=8000)