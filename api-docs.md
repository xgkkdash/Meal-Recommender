# Meal-Recommender

## frontend website
www.meal-recommender.com

## api doc website
api.meal-recommender.com/v1/docs

## Base Url
api.meal-recommender.com/v1

## Models

### User
- account_id
- password
- email
- name
- age
- gender
- height
- weight

### Food
- name
- type (meat, vegetable, egg, ...)
- energy  (cals)
- nutrition (dict, keys: {protein, fat, sugar, ...})
- deliver_time
- price

### Plan
- plan_id
- user_id
- breakfast (Food)
- lunch (Food)
- dinner (Food)

## Endpoints:
(all endpoint requires authentication except register and login)
#### Authentication
pass your access_token into Headers as {"token": access_token}

### Register
POST http://api.meal-recommender.com/v1/register
- create a new user

#### Request
- Headers: Content-Type:application/json
- Body: json of model User with required params: account_id, password, email

#### Response
- status code: 201 for success and 409 for failed with duplicate account_id
- Headers: Content-Type:application/json
- Body: json of model User

### Login
POST http://api.meal-recommender.com/v1/login
- endpoint for created user to get access token

#### Request
- Headers: Content-Type:application/x-www-form-urlencoded
- Body: fill username and password in field data

#### Response
- status code: 200 for success, 404 for user not found, 401 for failed with wrong id/password
- Headers: Content-Type:application/json
- Body: json of a dict {"access_token": access_token}

### Get user profile
GET http://api.meal-recommender.com/v1/profile
- get profile for current user identified by auth token

#### Request

#### Response
- status code: 200 for success and 401 for failed with Unauthorized
- Headers: Content-Type:application/json
- Body: json of model User, the current user found by

### Update user profile
PUT http://api.meal-recommender.com/v1/profile
- update profile for current user identified by auth token

#### Request
- Headers: Content-Type:application/json
- Body: json of model User

#### Response
- status code: 200 for success, 404 for user not found, 401 for failed with Unauthorized
- Headers: Content-Type:application/json
- Body: json of model User, representing the updated user

### Get all foods
GET http://api.meal-recommender.com/v1/foods
- get all alternative foods stored in database

#### Request

#### Response
- status code: 200 for success and 401 for failed with Unauthorized
- Headers: Content-Type:application/json
- Body: json encoded list, each member of the list is an instance of model Food

### Get food by name
GET http://api.meal-recommender.com/v1/foods/{name}
- get detail of a specified food by its name 

#### Request

#### Response
- status code: 200 for success, 404 for food not found, 401 for failed with Unauthorized
- Headers: Content-Type:application/json
- Body: json of model Food

### Insert food
POST http://api.meal-recommender.com/v1/foods
- insert a food into server's database

#### Request
- Headers: Content-Type:application/json
- Body: json of model Food

#### Response
- status code: 201 for success and 401 for failed with Unauthorized
- Headers: Content-Type:application/json
- Body: json of model Food

### Update food
PUT http://api.meal-recommender.com/v1/foods/{name}
- update a food detail by its name

#### Request
- Headers: Content-Type:application/json
- Body: json of model Food

#### Response
- status code: 200 for success, 404 for food not found, 401 for failed with Unauthorized
- Headers: Content-Type:application/json
- Body: json of model Food

### Delete food
DELETE http://api.meal-recommender.com/v1/foods/{name}
- delete a food by name

#### Request

#### Response
- status code: 200 for success, 404 for food not found, 401 for failed with Unauthorized
- Headers: Content-Type:application/json
- Body: json of a dict {"success": a boolean result}

### Generate a plan
POST http://api.meal-recommender.com/v1/plans
- get a plan by a given user (detected by auth token) and some given food conditions

#### Request
- Headers: Content-Type:application/json
- Body: json of a dict, including all food conditions, format like mongodb search phrase,
example: {name: {chicken, beef, bread}, max_price: 50, max_deliver_time: 40, ...}

#### Response
- status code: 200 for success, 401 for failed with Unauthorized
- Headers: Content-Type:application/json
- Body: json of model Plan

### Get plans by user_id
GET http://api.meal-recommender.com/v1/plans?user=xxxx
- get all plans of a given user

#### Request

#### Response
- status code: 200 for success, 404 for plan not found, 401 for failed with Unauthorized
- Headers: Content-Type:application/json
- Body: json encoded list, each member of the list is an instance of model Plan
