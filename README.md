# Auth Challenge



### Verifying User Phone Number
#### getting an OTP code (fake one)
```http
POST /api/v1/auth/login/verify/
```


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `phone_number` | `string` | **required** the user phone number |


### Register New Account
#### registering new account without any info just phone number
```http
POST /api/v1/auth/register/
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `phone_number` | `string` | **required** user phone number |
| `code`         | `string` | **required** OTP code |

### Updating User Info
#### after user signed up a form should appear that can add more info's to their account
```http
PUT /api/v1/auth/register/update-info/
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `first_name` | `string` | **required** user first name |
| `last_name`         | `string` | **required** user last name |
| `email` | `string` | **required** user email address |
| `password`         | `string` | **required** user password |

### Login To Account
```http
GET /api/v1/auth/login/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `phone_number` | `string` | **required** user phone number |
| `password`         | `string` | **required** user password |
