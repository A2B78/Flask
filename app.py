from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Remplacez ces informations par celles de votre base de données RDS PostgreSQL
DATABASE_HOST = "mark.cfas4wq4cb4x.eu-west-3.rds.amazonaws.com"
DATABASE_PORT = "5432"
DATABASE_NAME = "postgres"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "CGKKM4JejXYQ5PIRgC8a"

def create_connection():
    connection = psycopg2.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD
    )
    return connection

@app.route('/')
def index():
    connection = create_connection()
    cursor = connection.cursor()

    # Récupérer et afficher toutes les données de la table app_student
    retrieve_app_student_query = '''
        SELECT * FROM app_student;
    '''
    cursor.execute(retrieve_app_student_query)
    app_student_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('index.html', app_student_data=app_student_data)

@app.route('/add_student', methods=['POST'])
def add_student():
    connection = create_connection()
    cursor = connection.cursor()

    # Récupérer les données du formulaire
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    score = request.form['score']

    # Insérer les nouvelles données dans la table app_student
    insert_student_query = '''
        INSERT INTO app_student (first_name, last_name, score) VALUES (%s, %s, %s);
    '''
    cursor.execute(insert_student_query, (first_name, last_name, score))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/')

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    connection = create_connection()
    cursor = connection.cursor()

    # Supprimer l'étudiant spécifié par son ID
    delete_student_query = '''
        DELETE FROM app_student WHERE id = %s;
    '''
    cursor.execute(delete_student_query, (student_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/')

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    connection = create_connection()
    cursor = connection.cursor()

    if request.method == 'GET':
        # Récupérer les données de l'étudiant pour pré-remplir le formulaire
        retrieve_student_query = '''
            SELECT * FROM app_student WHERE id = %s;
        '''
        cursor.execute(retrieve_student_query, (student_id,))
        student_data = cursor.fetchone()

        cursor.close()
        connection.close()

        return render_template('edit_student.html', student_data=student_data)

    elif request.method == 'POST':
        # Récupérer les nouvelles données du formulaire
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']
        new_score = request.form['score']

        # Mettre à jour les données de l'étudiant
        update_student_query = '''
            UPDATE app_student SET first_name = %s, last_name = %s, score = %s WHERE id = %s;
        '''
        cursor.execute(update_student_query, (new_first_name, new_last_name, new_score, student_id))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
