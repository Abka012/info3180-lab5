import os

from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField, StringField, TextAreaField
from wtforms.validators import DataRequired, Optional


def allowed_file(filename, allowed_extensions={"png", "jpg", "jpeg", "gif"}):
    """Check if the file has an allowed image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


class MovieForm(FlaskForm):
    """Form for creating or editing a movie entry."""

    title = StringField(
        "Title", validators=[DataRequired(message="Movie title is required")]
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired(
                message="A brief description or summary of the movie is required"
            )
        ],
    )

    poster = FileField("Poster", validators=[Optional()])

    def validate_poster(self, field):
        """Custom validator to check if the uploaded file is a valid image."""
        if field.data:
            filename = secure_filename(field.data.filename)
            if not allowed_file(filename):
                raise ValueError(
                    "Invalid file type. Only image files (PNG, JPG, JPEG, GIF) are allowed."
                )
