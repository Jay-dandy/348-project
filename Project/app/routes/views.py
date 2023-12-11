from flask import render_template, request, redirect, url_for, current_app as app
from flask import Blueprint, session, flash
from app import db
import sqlalchemy
# create a new blueprint
views = Blueprint('views', __name__)

@views.route('/login', methods=['GET', 'POST'])
def login():
    from app.models.models import User
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('views.dashboard'))  # Redirect to dashboard
        else:
            return 'Invalid username or password'
    return render_template('login.html')

# @views.route('/dashboard')
# def dashboard():
#     from app.models.models import DataStructure, Algorithm
#     if 'user_id' not in session:
#         return redirect(url_for('views.login'))
    
#     user_id = session['user_id']
#     data_structures = DataStructure.query.filter_by(user_id=user_id).all()
#     algorithms = Algorithm.query.filter_by(user_id=user_id).all()
#     return render_template('dashboard.html', data_structures=data_structures, algorithms=algorithms)

@views.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))
    return render_template('dashboard.html')

@views.route('/library')
def library():
    from app.models.models import DataStructure, Algorithm
    if 'user_id' not in session:
        return redirect(url_for('views.login'))
    user_id = session['user_id']
    data_structures = DataStructure.query.filter_by(user_id=user_id).all()
    algorithms = Algorithm.query.filter_by(user_id=user_id).all()
    return render_template('library.html', data_structures=data_structures, algorithms=algorithms)


@views.route('/register', methods=['GET', 'POST'])
def register():
    from app.models.models import User

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In a real app, you should hash the password
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.login'))
        else:
            return 'Username already exists'
    return render_template('register.html')


@views.route('/details/<int:id>')
def details(id):
    from app.models.models import DataStructure, Algorithm
    user_id = session.get('user_id')

    # Check DataStructures first
    item = DataStructure.query.filter_by(id=id, user_id=user_id).first()
    if not item:
        # If not found, check Algorithms
        item = Algorithm.query.filter_by(id=id, user_id=user_id).first()
    
    if not item:
        flash('Item not found or you do not have access to this item.', 'error')
        return redirect(url_for('views.library'))
    
    return render_template('details.html', item=item)


@views.route('/', methods=['GET'])
def index():
    return redirect(url_for('views.login'))

@views.route('/add_data_structure', methods=['GET', 'POST'])
def add_data_structure():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    if request.method == 'POST':
        user_id = session['user_id']
        ds_name = request.form.get('ds_name')
        time_complexity = request.form.get('time_complexity')
        mem_complexity = request.form.get('mem_complexity')
        type = request.form.get('type')
        description = request.form.get('description')
        code_example = request.form.get('code_example')

        try:
            db.session.execute(sqlalchemy.text("CALL create_data_structure_proc(:user_id, :ds_name, :time_complexity, :mem_complexity, :type, :description, :example_code)"), 
                              {
                                'user_id': user_id, 
                                'ds_name': ds_name, 
                                'time_complexity': time_complexity, 
                                'mem_complexity': mem_complexity, 
                                'type': type, 
                                'description': description, 
                                'example_code': code_example
                              })
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('An error occurred while adding the data structure.', 'error')
            return redirect(url_for('views.add_data_structure'))

        return redirect(url_for('views.dashboard'))

    return render_template('add_data_structure.html')

@views.route('/add_algorithm', methods=['GET', 'POST'])
def add_algorithm():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    if request.method == 'POST':
        user_id = session['user_id']
        algo_name = request.form.get('algo_name')
        time_complexity = request.form.get('time_complexity')
        mem_complexity = request.form.get('mem_complexity')
        version = request.form.get('version')
        description = request.form.get('description')
        code_example = request.form.get('code_example')

        try:
            db.session.execute(sqlalchemy.text("CALL create_algorithm_proc(:user_id, :algo_name, :time_complexity, :mem_complexity, :version, :description, :example_code)"), 
                              {
                                'user_id': user_id, 
                                'algo_name': algo_name, 
                                'time_complexity': time_complexity, 
                                'mem_complexity': mem_complexity, 
                                'version': version, 
                                'description': description, 
                                'example_code': code_example
                              })
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('An error occurred while adding the algorithm.', 'error')
            return redirect(url_for('views.add_algorithm'))

        return redirect(url_for('views.dashboard'))

    return render_template('add_algorithm.html')



@views.route('/edit_data_structure/<int:id>', methods=['GET', 'POST'])
def edit_data_structure(id):
    from app.models.models import DataStructure

    ds = DataStructure.query.get_or_404(id)
    if request.method == 'POST':
        ds_name = request.form['ds_name']
        time_complexity = request.form['time_complexity']
        mem_complexity = request.form['mem_complexity']
        type = request.form['type']
        description = request.form['description']
        code_example = request.form['code_example']

        try:
            db.session.execute(sqlalchemy.text("CALL update_data_structure_proc(:id, :ds_name, :time_complexity, :mem_complexity, :type, :description, :example_code)"), 
                              {
                                'id': id,
                                'ds_name': ds_name, 
                                'time_complexity': time_complexity, 
                                'mem_complexity': mem_complexity, 
                                'type': type, 
                                'description': description, 
                                'example_code': code_example
                              })
            db.session.commit()
            flash('Data structure updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred: ' + str(e), 'error')
            return redirect(url_for('views.edit_data_structure', id=id))

        return redirect(url_for('views.details', id=id))

    return render_template('edit_data_structure.html', ds=ds)



@views.route('/delete_data_structure/<int:id>')
def delete_data_structure(id):
    from app.models.models import DataStructure

    ds = DataStructure.query.get_or_404(id)
    db.session.delete(ds)
    db.session.commit()
    return redirect(url_for('views.dashboard'))


@views.route('/edit_algorithm/<int:id>', methods=['GET', 'POST'])
def edit_algorithm(id):
    from app.models.models import Algorithm

    algo = Algorithm.query.get_or_404(id)
    if request.method == 'POST':
        algo_name = request.form['algo_name']
        time_complexity = request.form['time_complexity']
        mem_complexity = request.form['mem_complexity']
        version = request.form['version']
        description = request.form['description']
        code_example = request.form['code_example']

        try:
            db.session.execute(sqlalchemy.text("CALL update_algorithm_proc(:id, :algo_name, :time_complexity, :mem_complexity, :version, :description, :example_code)"), 
                              {
                                'id': id,
                                'algo_name': algo_name, 
                                'time_complexity': time_complexity, 
                                'mem_complexity': mem_complexity, 
                                'version': version, 
                                'description': description, 
                                'example_code': code_example
                              })
            db.session.commit()
            flash('Algorithm updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred: ' + str(e), 'error')
            return redirect(url_for('views.edit_algorithm', id=id))

        return redirect(url_for('views.details', id=id))

    return render_template('edit_algorithm.html', algo=algo)


@views.route('/delete_algorithm/<int:id>')
def delete_algorithm(id):
    from app.models.models import Algorithm

    algo = Algorithm.query.get_or_404(id)
    db.session.delete(algo)
    db.session.commit()
    return redirect(url_for('views.dashboard'))

######### search #######
@views.route('/search', methods=['POST'])
def search():
    from app.models.models import Algorithm, DataStructure
    if 'user_id' not in session:
        return redirect(url_for('views.login'))

    user_id = session['user_id']
    search_query = request.form.get('search_query', '')

    # perform search on both DataStructures and Algorithms tables
    data_structures = DataStructure.query.filter(DataStructure.user_id == user_id, DataStructure.ds_name.contains(search_query)).all()
    algorithms = Algorithm.query.filter(Algorithm.user_id == user_id, Algorithm.algo_name.contains(search_query)).all()

    # ender search results page
    return render_template('search_results.html', data_structures=data_structures, algorithms=algorithms, search_query=search_query)

@views.route('/logout')
def logout():
    # Clear the user session
    session.clear()
    return redirect(url_for('views.login'))
