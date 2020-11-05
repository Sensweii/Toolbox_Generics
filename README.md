# UserApi
Simple Users API

## Endpoints

### /api/v1/users/
- [GET] returns list of users excluding superusers, deleted, or inactive
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
        "detail": <link to detail view>
    },
    {...}
]
```

### /api/v1/users/<id:int>/
- [GET] returns details of user, accepts integer url argument
- Content-Type: application/json
- Authorization: Bearer <oauth_token> `optional` returns more details when provided
- Response:
```
    {
        "id": int
        "email": str (with token)
        "first_name": str
        "last_name": str (with token)
        "list": <link to list view>
        "change_password": <link to change password>
    }
```

### /api/v1/users/register/
- [POST] creates user entry, will send e-mail to user email with activation code
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
}
```

### /api/v1/users/activate/
- [POST] activates user account, requires activation code from email
- Content-Type: application/json
- Authorization: <activation_code>
- Request Body:
```
{
    "email": str `required`
}
```
- Response:
```
{
    "email": str
    "first_name": str
    "last_name": str
    "registration_date": datetime str
    "is_activated": true
}
```

### /api/v1/users/login/
- [POST] requests login for user
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
    "token_type": "Bearer"
    "expires_on": datetime str
}
```

### /api/v1/users/<id:int>/change_password/
- [PATCH] updates user password
- Content-Type: application/json
- Authorization: Bearer <oauth_token> `required`
- Request Body:
```
{
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
}
```
