import csv

from flask import Blueprint, render_template
from mini_flask_app import CSV_FILEPATH

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    user_list = []

    with open(CSV_FILEPATH, 'r') as f:
      csv_reader = csv.DictReader(f)

      for row in csv_reader :
        user_list.append(row)

    return render_template('index.html',user_list=user_list) , 200
    # 렌더링을 하면 'template'폴더에 있는 html 문서에 데이터를 전달해준다.
