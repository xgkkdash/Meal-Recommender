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
- role

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

### Login
POST http://api.meal-recommender.com/v1/login
- endpoint for created user to get access token

### Get user profile
GET http://api.meal-recommender.com/v1/profile
- get profile for current user identified by auth token

### Update user profile
PUT http://api.meal-recommender.com/v1/profile
- update profile for current user identified by auth token

### Get all foods
GET http://api.meal-recommender.com/v1/foods
- get all alternative foods stored in database

### Get food by name
GET http://api.meal-recommender.com/v1/foods/{name}
- get detail of a specified food by its name 

### Insert food
POST http://api.meal-recommender.com/v1/foods
- insert a food into server's database
- only user with role admin can do this

### Update food
PUT http://api.meal-recommender.com/v1/foods/{name}
- update a food detail by its name
- only user with role admin can do this

### Delete food
DELETE http://api.meal-recommender.com/v1/foods/{name}
- delete a food by name
- only user with role admin can do this

### Generate a plan
POST http://api.meal-recommender.com/v1/plans
- get a plan by a given user (detected by auth token) and some given food conditions
- conditions should be put into request.json, with format like mongodb search phrase,
  example: {name: {chicken, beef, bread}, max_price: 50, max_deliver_time: 40, ...}

### Get plans by user_id
GET http://api.meal-recommender.com/v1/plans
- get all plans by a given user (detected by auth token)
- a user can only get his own plans, cannot get others' plan

### Get all users
GET http://api.meal-recommender.com/v1/users
- get all registered users from database
- only user with role admin can do this

### Get user by account_id
GET http://api.meal-recommender.com/v1/users/{account_id}
- get a specified user by his account_id
- only user with role admin can do this

### Delete user
DELETE http://api.meal-recommender.com/v1/users/{account_id}
- delete a user by his account_id
- only user with role admin can do this
