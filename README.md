# UserApi
Simple Users API

## Endpoints

### /api/v1/users/
- [GET] returns list of users excluding superusers, deleted, or inactive

### /api/v1/users/register
- [POST] creates user entry, will send e-mail to user email with activation code
- Content-Type: application/json
- Body:
```
      {
        "email": str `required`
        "first_name": str `optional`
        "last_name": str `optional`
        "password": str `required`
      }
``` 
