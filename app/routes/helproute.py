from flask import Blueprint, render_template

helpBP = Blueprint("help_support", __name__)


@helpBP.route('/help_support', methods=['GET', 'POST'])
def help_support():
    

    return render_template("user/help_support.html")