from datetime import datetime
from app import db
import sqlalchemy

# association table
ds_algo_association = db.Table('ds_algo_association',
    db.Column('datastructure_id', db.Integer, db.ForeignKey('data_structure.id')),
    db.Column('algorithm_id', db.Integer, db.ForeignKey('algorithm.id'))
)

# User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    # relationships
    data_structures = db.relationship('DataStructure', backref='user', lazy=True)
    algorithms = db.relationship('Algorithm', backref='user', lazy=True)

# DataStructure
class DataStructure(db.Model):
    __tablename__ = 'data_structure'
    id = db.Column(db.Integer, primary_key=True, server_default=sqlalchemy.text("nextval('shared_id_seq')"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ds_name = db.Column(db.String(120), unique=True, nullable=False)
    time_complexity = db.Column(db.Text, nullable=True) 
    mem_complexity = db.Column(db.Text, nullable=True)  
    type = db.Column(db.Text, nullable=True)            
    description = db.Column(db.Text, nullable=False)   
    code_example = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    related_algorithms = db.relationship('Algorithm', secondary=ds_algo_association, back_populates='related_datastructures')

    def __repr__(self):
        return f"<DataStructure {self.ds_name}>"

# Algorithm
class Algorithm(db.Model):
    __tablename__ = 'algorithm'
    id = db.Column(db.Integer, primary_key=True, server_default=sqlalchemy.text("nextval('shared_id_seq')"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    algo_name = db.Column(db.String(120), unique=True, nullable=False)
    time_complexity = db.Column(db.Text, nullable=True)  
    mem_complexity = db.Column(db.Text, nullable=True)  
    version = db.Column(db.Text, nullable=True)         
    description = db.Column(db.Text, nullable=False)     
    code_example = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    related_datastructures = db.relationship('DataStructure', secondary=ds_algo_association, back_populates='related_algorithms')

    def __repr__(self):
        return f"<Algorithm {self.algo_name}>"
