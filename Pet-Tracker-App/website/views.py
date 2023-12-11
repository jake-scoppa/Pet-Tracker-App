from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
from .models import User, Pet

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    pets = Pet.query.all()
    if request.method == 'POST':
        user_id = current_user.id
        name = request.form['name']
        feeding_schedule = request.form['feeding_schedule']
        weight = request.form['weight']
        notes = request.form['notes']
        new_pet = Pet(user_id=user_id, name=name, feeding_schedule=feeding_schedule, weight=weight, notes=notes)
        db.session.add(new_pet)
        db.session.commit()

        flash('Pet added successfully!', 'success')
    return render_template('home.html', user=current_user, pets=pets)

@views.route('/delete-pet', methods=['POST'])
def delete_pet():  
    pet = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    petId = pet['petId']
    pet = Pet.query.get(petId)
    if pet:
        if pet.user_id == current_user.id:
            db.session.delete(pet)
            db.session.commit()

    return jsonify({})

@views.route('/edit_pet/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    # Fetch the pet from the database based on pet_id
    pet = Pet.query.get_or_404(pet_id)

    if request.method == 'POST':
        # Update pet details based on the form submission
        pet.name = request.form['name']
        pet.feeding_schedule = request.form['feeding_schedule']
        pet.weight = request.form['weight']
        pet.notes = request.form['notes']

        # Commit changes to the database
        db.session.commit()

        # Redirect to the home page after editing
        return redirect(url_for('views.home'))

    return render_template('edit_pet.html', pet=pet, user=current_user)