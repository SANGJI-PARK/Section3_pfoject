import os
import csv
import json
import requests

from flask import Blueprint, request
from mini_flask_app import CSV_FILEPATH, TMP_FILEPATH

user_bp = Blueprint('user', __name__)

# CSV 파일 경로와 임시 파일 경로입니다.
CSV_FILEPATH = os.path.join(os.getcwd(), 'mini_flask_app', 'users.csv')

@user_bp.route('/user')
def get_user():
    """
    get_user 함수는 `username` 을 키로 한 값을 쿼리 파라미터 값으로 넘겨주면 
    해당 값을 가진 유저를 리턴해야 합니다.

    요구사항:
      - HTTP Method: `GET`
      - Endpoint: `/api/user`

    상황별 요구사항:
      - `username` 값이 주어지지 않은 경우:
        - 리턴값: "No username given"
        - HTTP 상태코드: `400`
      - `username` 이 주어졌지만 해당되는 유저가 없는 경우:
        - 리턴값: "User '{ username }' doesn't exist"
        - HTTP 상태코드: `404`
      - 주어진 `username` 값으로 유저를 정상적으로 조회한 경우:
        - 리턴값: 'users.csv' 파일에 저장된 유저의 `id` 를 문자열로 변경한 값
        - HTTP 상태코드: `200`
    """

    if request.args.get('cityname') is None:
      return "No cityname given", 400
    
    # 쿼리 파라미터로 데이터를 받아올 때 : request.args.get()
    cityname = request.args.get('cityname')
    city = None

    with open(CSV_FILEPATH, 'r') as f :
      csv_reader = csv.DictReader(f)

      for row in csv_reader :
        if row['cityname'] == cityname:
          city = row
    
    if city is None :
      return f"City '{ cityname }' doesn't exist", 404
    
    return city['weather'], 200


@user_bp.route('/user', methods=['PATCH'])
def update_user():
    """
    
    """
    cityname = request.args.get('cityname')
    new_cityname = request.args.get('new_cityname')

    if not cityname or not new_cityname :
      return "No cityname/new_cityname given", 400
    else :
      cityname = cityname
      new_cityname = new_cityname

    #username이 존재하는지 확인
    city = None

    with open(CSV_FILEPATH, 'r') as f :
      csv_reader = csv.DictReader(f)

      for row in csv_reader :
        if row['cityname'] == cityname:
          city = row
    
    if city is None :
      return f"City '{ cityname }' doesn't exist", 404

    #new_username이 사용중인지 확인
    
    with open (CSV_FILEPATH,'r') as f:
      csv_reader = csv.DictWriter(f)

      for row in csv_reader:
        if row['cityname'] == new_cityname:
          city = row
    
    if city :
      return f"Cityname '{ new_cityname }' is in use", 400

    

@user_bp.route('/user', methods=['POST'])
def create_user():
    """
    도시 이름이 없는 경우 : 새로 날씨를 찾아서 업데이트하기
    create_user 함수에서는 JSON 으로 전달되는 데이터로 
    새로운 유저를 'users.csv' 파일에 추가해야 합니다. 이 때 추가되는 유저의 아이디
    값은 파일에 존재하는 가장 높은 아이디 값에 1 을 추가한 값입니다.

    요구사항:
      - HTTP Method: `POST`
      - Endpoint: `api/user`
      - 받는 JSON 데이터 형식 예시:
            ```json
            {
                "username":"유저 이름"
            }
            ```

    상황별 요구사항:
      - 주어진 JSON 데이터에 `username` 키가 없는 경우:
        - 리턴값: "No username given"
        - HTTP 상태코드: `400`
      - 주어진 JSON 데이터의 `username` 을 사용하는 유저가 이미 'users.csv' 파일에 존재하는 경우:
        - 리턴값: "User '{ username }' already exists"
        - HTTP 상태코드: `40
      - 주어진 JSON 데이터의 `username` 으로 정상적으로 생성한 경우:
        - 리턴값: "Created user '{ username }'"
        - HTTP 상태코드: `200`
    """
    request_data = request.get_json()
    '''   
    if request_data is None :
      return "No cityname given", 400
    else :
      return request_data["cityname"], 200
    '''
    try :
      cityname = request_data["cityname"]
    except :
      cityname = None
 
    if cityname is None :
      return "No cityname given", 400
      
    city=None
    with open (CSV_FILEPATH,'r') as f:
      csv_reader = csv.DictReader(f)

      for row in csv_reader:
        if row['cityname'] == cityname:
         city = row
      if city :
        return f"Cityname '{ cityname }' is in use", 400
      else :
        API_URL = f'https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid=999579ae24c9a2798ddc5f0cef792ce5'
        resp = requests.get(API_URL)
        json_resp = json.loads(resp.text)
        weather = json_resp['weather'][0]['main']

        with open(CSV_FILEPATH,'r') as inFile, open(TMP_FILEPATH, 'w')as outFile:
          fieldnames = ['id','cityname','weather']

          csv_reader = csv.DictReader(inFile)
          csv_writer = csv.DictWriter(outFile, fieldnames=fieldnames)

          csv_writer.writeheader()

          last_id_num = 0
          for row in csv_reader:
            last_id_num = row['id']
            csv_writer.writerow(row)
            #csv_reader
      
          csv_writer.writerow({
            'id':int(last_id_num)+1,
            'cityname': cityname,
            'weather' : weather
          })
      
    os.replace(TMP_FILEPATH,CSV_FILEPATH)

    return f"Created the weather of '{ cityname }'", 200

@user_bp.route('/user', methods=['DELETE'])
def delete_user():
    if request.args.get('cityname') is None:
      return "No cityname given", 400
    
    # DELETE 할 때도 request.args.get()를 통해서 받아올 수 있다.
    cityname = request.args.get('cityname')
    city = None

    with open(CSV_FILEPATH, 'r') as f :
      csv_reader = csv.DictReader(f)

      for row in csv_reader :
        if row['cityname'] == cityname:
          city = row
    
    if city is None :
      return f"City '{ cityname }' doesn't exist", 404
    
    ## csv 파일에 있는 user 데이터 지워주기
    with open(CSV_FILEPATH,'r') as inFile, open(TMP_FILEPATH, 'w')as outFile:
      fieldnames = ['id','cityname','weather']

      csv_reader = csv.DictReader(inFile)
      csv_writer = csv.DictWriter(outFile, fieldnames=fieldnames)

      csv_writer.writeheader()

      for row in csv_reader :
        id_match = (row['id'] == city['id'])
        
        if id_match == True : 
          continue

        csv_writer.writerow(row)
    
    os.replace(TMP_FILEPATH, CSV_FILEPATH)

    return f'Deleted {cityname}.', 200