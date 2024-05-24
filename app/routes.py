from flask import Blueprint, render_template
from flask import request, redirect, url_for
from .models import db, Item, Service
from datetime import datetime, timedelta
from flask import jsonify
from sqlalchemy import and_
import pyperclip as pc
from .fonction_all import *


bp = Blueprint('main', __name__)


@bp.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        task = request.form['task']
        project = request.form['project']
        status = request.form['status']
        date_livraison = request.form['date_livraison']
        importance = request.form['importance']
        risque = request.form['risque']
        commentaire = request.form['commentaire']
        new_item = Item(task=task, project=project,status=status, date_livraison=date_livraison,risque=risque, importance=importance,commentaire=commentaire )

        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main.hello_html'))
    return render_template('add_task.html')

@bp.route('/')
def hello_html():
    tasks_retard = Item.query.filter(and_(Item.status == "En retard", Item.status != "Terminée")).all()
    tasks_cours = Item.query.filter(and_(Item.status == "En cours", (Item.status != "Terminée"))).all()
    tasks_importante = Item.query.filter(and_(((Item.importance == "Critique") | (Item.importance == "Élevée")),(Item.status != "Terminée"))).all()
    tasks_attente = Item.query.filter(and_(Item.status == "En attente" , (Item.status != "Terminée"))).all()
    return render_template('index.html',tasks_retard=tasks_retard,tasks_cours=tasks_cours,tasks_importante=tasks_importante,tasks_attente=tasks_attente)

@bp.route('/day')
def day():
    current_date = str(datetime.now().strftime('%Y-%m-%d'))
    tasks = Item.query.filter(Item.date_livraison == current_date).all()
    return render_template('day.html', tasks=tasks, current_date=current_date)

@bp.route('/all')
def all_task():
    tasks = Item.query.all()  # Assurez-vous que Item a une méthode all() pour récupérer toutes les tâches
    return render_template('task_all.html', tasks=tasks)

@bp.route('/week')
def week():
    current_date = datetime.now()
    debut_semaine = current_date - timedelta(days=current_date.weekday())
    jours_semaine = []
    all_task = []
    for i in range(5):
        x=(debut_semaine + timedelta(days=i)).strftime("%Y-%m-%d")
        jours_semaine.append(x)
        tasks = Item.query.filter(Item.date_livraison == x).all()
        all_task.append(tasks)
    data = list(zip(jours_semaine, all_task))
    return render_template('week.html',data=data)

@bp.route('/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'La tâche a été supprimée avec succès'}), 200

@bp.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.status = request.form['status']
        item.date_livraison = request.form['date_livraison']
        item.importance = request.form['importance']
        item.risque = request.form['risque']
        item.commentaire = request.form['commentaire']
        db.session.commit()
        return redirect(url_for('main.day'))
    return render_template('edit_item.html', item=item)

@bp.route('/update_task_status/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    task = Item.query.get_or_404(task_id)
    new_status = request.json.get('new_status')

    if new_status not in ['Terminée', 'pending']:
        return jsonify({'error': 'Statut invalide'}), 400

    task.status = new_status
    db.session.commit()
    return jsonify({'message': 'Statut de la tâche mis à jour avec succès'}), 200

@bp.route('/check_tasks', methods=['GET'])
def check_tasks_route():
    check_tasks()
    return '', 204

@bp.route('/PM')
def PM():
    services = Service.query.all() 
    return render_template('htmlPM.html',services=services)


@bp.route('/addPM', methods=['GET', 'POST'])
def addPM():
    if request.method == 'POST':
        serviceName = request.form['serviceName']
        serviceIP = request.form['serviceIP']
        serviceUsername = request.form['serviceUsername']
        password = request.form['password']
        common_password = request.form['commonPassword']
        
        encrypted_password = encrypt_password(password, common_password)
        
        new_service = Service(name=serviceName, ip=serviceIP,user=serviceUsername, password=encrypted_password,key=generate_key(common_password))
        db.session.add(new_service)
        db.session.commit()  
        return redirect(url_for('main.PM'))
    return render_template('add_mdp.html')



@bp.route('/update_variable', methods=['POST'])
def update_variable():
    global your_variable
    service_id = request.form['service_id']
    magic = request.form['magic']
    service = Service.query.filter(Service.id == service_id).first()
    if service:  # Vérifiez si le service existe
        # Si le service existe, décryptez le mot de passe avec la fonction decrypt_password
        password = decrypt_password(service.password, magic)
        return jsonify({'password': password}), 200
    else:
        # Si le service n'existe pas, renvoyez un message d'erreur approprié
        return 'Service not found', 404

@bp.route('/delete_service', methods=['POST'])
def delete_service():
    service_id = request.form.get('service_id')
    if service_id:
        service = Service.query.get(service_id)
        if service:
            db.session.delete(service)
            db.session.commit()
            return jsonify({'success': True})
    return jsonify({'success': False})