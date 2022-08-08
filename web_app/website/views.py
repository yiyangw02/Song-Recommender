from flask import Blueprint, render_template, request, flash, jsonify,  redirect, url_for
from flask_login import login_required, current_user
from .models import Mood, User
from . import db
import json
from textblob import TextBlob

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        mood = request.form.get('description')
        score = request.form.get('score')
        polarity = TextBlob(str(mood)).sentiment.polarity
        if len(mood) < 1:
            flash('Not enough context. Please provide more info!', category='error')
        elif polarity == 0.0:
            flash("Please try to enter something else for better evaluation!")
        else:
            newMood = Mood(textData=mood, score=score, userId=current_user.id)
            db.session.add(newMood)
            db.session.commit()
            return song()
    return render_template("home.html", user=current_user)


@views.route('/song', methods=['GET', 'POST'])
@login_required
def song():
    polarity = TextBlob(
        str(request.form.get('description'))).sentiment.polarity
    score = request.form.get('score')
    # product is in the range [-100, 100]
    product = int(score) * polarity
    if product < -66:
        flash("your predicted mood is irritable")
        return redirect("https://open.spotify.com/playlist/1WJSCv94LinHIjb0kLx5a6?si=930f3296a26c4e32")
    elif product >= -66 and product < -33:
        flash("your predicted mood is anxious")
        return redirect("https://open.spotify.com/playlist/3iUYZJLVK1MiFe8DkBL9tK?si=6846975cd6c84f64")
    elif product >= -33 and product < -0:
        flash("your predicted mood is tired")
        return redirect("https://open.spotify.com/playlist/3iUYZJLVK1MiFe8DkBL9tK?si=c976997eab2a4f31")
    elif product > 0 and product < 50:
        flash("your predicted mood is happy")
        return redirect("https://open.spotify.com/playlist/0RH319xCjeU8VyTSqCF6M4?si=d1944bfed72243d3")
    else:
        flash("your predicted mood is exciting!!")
        return redirect("https://open.spotify.com/playlist/1dDG8jhP519bSR1cjSMp45?si=65050a043c6d4c88")
    return render_template("song.html", user=current_user)
