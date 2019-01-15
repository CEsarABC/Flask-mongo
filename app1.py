import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb://admin:Temper11@ds251804.mlab.com:51804/task_manager'

mongo = PyMongo(app)


''' Brings all the tasks to the main page '''
@app.route('/')
@app.route('/test_get_tasks')
def get_tasks():
    return render_template("t_tasks.html", 
    nests=mongo.db.nesting.find())
    
''' brings the categories to addtask.html '''
@app.route('/add_task')
def add_task():
    return render_template('t_addtask.html',
    categories=mongo.db.categories.find())
    
    
''' inserts one dictionary when the form in addtask.html is submited '''
@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks =  mongo.db.nesting
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


''' brings all the information to the form in edittask.html '''
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.nesting.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('t_edittask.html', task=the_task, categories=all_categories)
    
    
''' updates all the fields in the entry after form is submited '''
@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.nesting
    tasks.update( {'_id': ObjectId(task_id)},{
        'task_name':request.form.get['task_name'],
        'category_name':request.form.get['category_name'],
        'task_description': request.form.get['task_description'],
        'due_date': request.form.get['due_date'],
        'is_urgent':request.form.get['is_urgent']
    })
    tasks.update_one({'_id': ObjectId(task_id)},{'$set':{"alergen":[{"diary":request.form.get['diary']}]}})
    return redirect(url_for('get_tasks'))
    
    
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.nesting.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))
    
''' displays all categories menu   '''

@app.route('/get_categories')
def get_categories():
    return render_template('t_categories.html',
    categories=mongo.db.categories.find())
    
''' link to edit button, brigs a new page with a form to 
edit the chosen category '''

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('t_editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))

''' this function is a form action for edit category  '''
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form['category_name']})
    return redirect(url_for('get_categories'))

  

@app.route('/delete_category/<category_id>')  
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for("get_categories"))
    

@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))
    

@app.route('/new_category')
def new_category():
    return render_template('t_addcategory.html')
    
    
'''TESTING'''

@app.route('/addtest')
def test():
    return render_template('test.html',
    categories=mongo.db.categories.find())
    

@app.route('/testedit_task/<task_id>')
def testedit_task(task_id):
    the_task =  mongo.db.nesting.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('testedittask.html', task=the_task, categories=all_categories)


@app.route('/update_nesting/<task_id>', methods=["POST"])
def update_nesting(task_id):
    nesting = mongo.db.nesting
    nesting.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get['task_name'],
        'category_name':request.form.get['category_name'],
        'task_description': request.form.get['task_description'],
        'due_date': request.form.get['due_date'],
        'is_urgent':request.form.get['is_urgent'],
        'alergen': [
            {'diary': request.form.get['diary']}
            ]
    })
    return redirect(url_for('get_tasks'))
   
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
debug=True)