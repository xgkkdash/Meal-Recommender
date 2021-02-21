# Design and Specification

## Business critical components
Data source and destination, compute, storage, rules and exception.
- HTTP server to listen for sync request from user
- Database to store user info and foods
- Rest Client to get food choices
- Algorithm to generate meal plan based on user info and food choices
- Rest Client to order take-out food from 3rd-party platform


## Interface
### Web Server with UI rest call
- `sign_up`
- `sign_in`
- `profile`
- `get_plan`

## Language, Frameworks and tools
- Python 3.8
- Flask/Django for web_server
- MongoDB for database


## Metrics and logs
### Metrics
- Total number of users
- Total number of foods
- others TBD

### Logs
- General logs
- Exception log for failed rest request/response


## Component Specification
#### Models
- User
- Food
- Plan

See `models.py` for details.

#### HTTP server
- Define Flask/Django web server and it'd listen at localhost:
- On `sign_up` request, provide a view to let user create his account and password, save new user to DB and send a confirm email to user
- On `sign_in` request, provide a view to let user input his account and password, verify according to DB record
- On `profile` request, could be requested after user sign_in, provide a view to let user update his info.
- On `get_plan` request, check DB first, if there is not any plan for this user, generate a weekly meal plan for him, and save this plan to DB

#### Rest client
- Timer `get_foods` to rest get foods from 3rd-party platform, update DB.foods by latest results
- Timer `auto_order` to rest order meal from 3rd-party platform, according plans saved in DB

#### Recommender (algorithm)
- `decider`: generate a weekly meal plan based on given user_info and food_choices

#### Database
- Connect to MongoDB at start
- Check existing collections and create one if missing
- User's password should be encoded before saving into DB
- Define `create_user` for saving new user; throw error if account_id isn't unique.
- Define `read_user` for getting a user by account_id; return None if it doesn't exist.
- Define `update_user` for update user info by account_id; create a new user if account_id is not exist.
- Define `create_food` for saving a food; throw error if id isn't unique.
- Define `read_food` for getting a food by id; return None if it doesn't exist.
- Define `update_food` for update food info by id; create a new food if id is not exist.
- Define `delete_food` for delete a food by id, do nothing if it doesn't exist.
- Define `create_plan` for saving a plan; throw error if id isn't unique.
- Define `read_plan` for getting a plan by id; return None if it doesn't exist.
- Define `update_plan` for update plan detail by id; create a new plan if id is not exist.
- Define `delete_plan` for delete a plan by id, do nothing if it doesn't exist.


## Technical Challenges

### Get data from app
- many food info are from app but not website, should use proper way to get these 

### Auto payment
- needs to find out what framework is required to implement auto payment

### Sync of foods
- local food choices may not be exactly the same with remote
 