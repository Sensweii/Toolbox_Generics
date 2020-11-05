# UserApi
Simple Users API

Endpoints

/api/v1/users/
  - [GET] returns list of users excluding superusers, deleted, or inactive

/api/v1/users/register
  - [POST] creates user entry
    Content-Type: application/json
    Body:
      {
        "email": string, `required`
        "first_name": string, `optional`
        "last_name": string, `optional`
        "password": string, `required`
      }
 
