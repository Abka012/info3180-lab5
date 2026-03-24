"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
import time

from flask import jsonify, render_template
from werkzeug.utils import secure_filename

from app import app, db
from app.forms import MovieForm
from app.models import Movie

###
# Routing for your application.
###


@app.route("/")
def index():
    return jsonify(message="This is the beginning of our API")


@app.route("/api/v1/movies", methods=["POST"])
def movies():
    """Handle movie creation with file upload."""
    form = MovieForm()

    if form.validate_on_submit():
        # Get the uploaded file
        poster_file = form.poster.data

        # Process poster upload
        poster_filename = None
        if poster_file and hasattr(poster_file, "filename"):
            # Get the original filename and secure it
            original_filename = secure_filename(poster_file.filename)
            if original_filename:
                # Generate a unique filename by adding timestamp prefix
                poster_filename = f"{int(time.time())}_{original_filename}"
                # Save the file to the uploads folder
                upload_path = os.path.join(app.config["UPLOAD_FOLDER"], poster_filename)
                poster_file.save(upload_path)

        # Create and save the movie
        movie = Movie()
        movie.title = form.title.data
        movie.description = form.description.data
        movie.poster = poster_filename
        db.session.add(movie)
        db.session.commit()

        return jsonify(
            message="Movie Successfully added",
            title=form.title.data,
            poster=poster_filename,
            description=form.description.data,
        )

    # Return validation errors
    return jsonify(errors=form_errors(form)), 400


###
# The functions below should be applicable to all Flask apps.
###


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = "Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error,
            )
            error_messages.append(message)

    return error_messages


@app.route("/<file_name>.txt")
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + ".txt"
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers["X-UA-Compatible"] = "IE=Edge,chrome=1"
    response.headers["Cache-Control"] = "public, max-age=0"
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template("404.html"), 404
