# ToolboxGenerics
A simple generic API. Currently, only contains a User API that offers basic CRUD on User resource.
Offers a login endpoint that responds with OAuth token for authenticating requests.

### Installation requirements
- It is recommended to create a virtual environment to isolate local installations
- Python 3.9.0
- pip
- other packages: pip install -r requirements.txt

### Secrets.json
- For local setup, create a copy of secrets_template.json and populate the fields.

### Email Sending
- The app currently uses Google SMTP as a free email sending service.
- To enable email sending for EMAIL_HOST_USER (defined in settings), go to gmail account settings > security settings > and turn `ON` access of non-secure apps. For security purposes, developers may want to use a dummy gmail account when testing.

### For developer setup
- python manage.py runserver --settings=toolbox_generics.settings.dev


## Endpoints

### /api/v1/users/
__________________
#### [GET]
- returns list of users excluding superusers
- Content-Type: application/json
- Authorization: Bearer <oauth_token> `optional` returns more details when provided
- Response: List of users
```
[
    {
        "id": int
        "email": str (with token)
        "first_name": str
        "last_name": str (with token)
        "url": <link to resource>
    },
    {...}
]
```
#### [POST]
- creates user entry, will send e-mail to user email with activation code
- Content-Type: application/json
- Request Body:
```
{
    "email": str `required`
    "first_name": str `optional`
    "last_name": str `optional`
    "password": str `required`
}
```
- Response:
```
{
    "id": int
    "email": str
    "first_name": str
    "last_name": str
    "url": <link to resource>
}
```


### /api/v1/users/<id:int>/
___________________________
#### [GET] 
- returns details of user, accepts integer argument
- Content-Type: application/json
- Authorization: Bearer <oauth_token> `optional` returns more details when provided
- Response:
```
{
    "id": int
    "email": str (with token)
    "first_name": str
    "last_name": str (with token)
    "url": <link to resource>
}
```
#### [PATCH]
- updates details of user, accepts integer argument
- Content-Type: application/json
- Authorization: Bearer <oauth_token> `required`
- Request Body: Can accept several parameters. Updating `is_activated` field on this endpoint has no effect.
```
{
    "password": str
}
```
- Response:
```
{
    "id": int
    "email": str
    "first_name": str
    "last_name": str
    "is_activated": bool
    "url": <link to resource>
}
```

### /api/v1/users/<id:int>/status
_________________________________
#### [PATCH]
- Updates `is_activated` field of user (activation step), accepts integer argument
- Content-Type: application/json
- Authorization: <activation_code> `from email`
- Request Body:
```
{
    "is_activated": true `required`
}
```
- Response:
```
{
    "id": int
    "email": str
    "first_name": str
    "last_name": str
    "is_activated": bool
    "url": <link to resource>
}
```


### /api/v1/login/
__________________
#### [POST] 
- requests login for user
- Content-Type: application/json
- Request Body:
```
  {
    "email": str `required`
    "password": str `required`
  }
``` 
- Response:
```
{
    "access_token": str
    "expires_in": int (seconds)
    "token_type": str
    "scope": str
    "refresh_token": str
}
```
