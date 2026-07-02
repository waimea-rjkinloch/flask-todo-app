#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Home Page
#-----------------------------------------------------------
@app.get("/")
def show_welcome():
    with connect_db() as db:
        sql = """
            SELECT id, name, priority, complete
            FROM TasksToDo
        """
        params = ()
        TasksToDo = db.execute(sql, params).fetchall()
        return render_template("pages/home.jinja", TasksToDo=TasksToDo)


#-----------------------------------------------------------
# Handle The Task Form Data
#-----------------------------------------------------------
@app.post("/Task/new")
def process_creature_form():
    # Get the form data
    species = request.form.get("species", "unknown").strip()
    name = request.form.get("name", "unknown").strip()

    # Connect to the db
    with connect_db() as db:

        sql = """

                INSERT INTO creatures (species,name)
                VALUES (?, ?)

        """
        params = (species, name)

        #  Run the query
        db.execute(sql, params)

        flash(f"Creature {name} added successfully")

        # We're done, so back to the list
        return redirect("/creatures")

#-----------------------------------------------------------
# Help page - Show some help
#-----------------------------------------------------------
@app.get("/help")
def show_help():

    flash("Flash test message")
    flash("Flash test message with a longer bit of text")
    flash("Success test message", "success")
    flash("Error test message", "error")

    return render_template("pages/help.jinja")


#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

