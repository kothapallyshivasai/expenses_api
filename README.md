# Installation
============================================================

## Create a virtual environment or install these normally
----------------------------------------------------------
### cd expenses_api
### pip install -r requirements.txt
----------------------------------------------------------

## Creating virtual environment (Optional)
----------------------------------------------------------
### python -m venv venv
### .\venv\Scripts\activate
### cd expenses_api
### pip install -r requirements.txt
----------------------------------------------------------

# Description & URLS
============================================================
### I have created a Django RestAPI for the expenses spent by users who are registered in this website, One can register in this and can through this url.
-----------------------------------------------------------------------------------------------------------------------------------------
# Registration & Login
-----------------------------------------------------------------------------------------------------------------------------------------


## http://127.0.0.1:8000/api/register/ - POST Method (You can test this in Thunderclient or Postman), This returns access token and refresh token, Save the access token for later use. It also has validations you can feel free to test.

## The data in Body Json should be similar to this 
{
    "username": "tester",
    "first_name": "Test",
    "last_name": "Er",
    "password": "securepassword",
    "email": "tester@gmail.com",
    "mobile_number": "7889406035"
}

## Try to create more users or use the existing users with the user id's 1, 2, 4 which i already added previously
-----------------------------------------------------------------------------------------------------------------------------------------

## http://127.0.0.1:8000/api/token/ - POST Method 

## The data should be like this
{
  "username": "test2",
  "password": "securepassword"
}

## This returns refresh and access tokens, Save the access token for future use.
-----------------------------------------------------------------------------------------------------------------------------------------
# Expenses
-----------------------------------------------------------------------------------------------------------------------------------------
## http://127.0.0.1:8000/api/expenses/ - POST Method 

## Also put previously stored access token in (Auth -> Bearer -> Bearer YOUR_ACCESS_TOKEN) inside ThunderClient

## The data should be like this
{
    "payer": 2,
    "participants": [1, 2, 4],
    "amount": 2000,
    "description": "Party",
    "split_method": "PERCENTAGE",
    "percentage_shares": {
        "1": 50,
        "2": 25,
        "4": 25
    }
}
-----------------------------------------------------------------------------------------------------------------------------------------
# Balance Sheet
-----------------------------------------------------------------------------------------------------------------------------------------
## http://127.0.0.1:8000/api/download_balance_sheet_user/ - GET Method

## This is for getting all transactions done by the expense created by the user

## Also put previously stored access token in (Auth -> Bearer -> Bearer YOUR_ACCESS_TOKEN) inside ThunderClient

## The output will be given similar to a csv file in the thunderclient, But when you try to use it in browser or frontend applications it will download. 
-----------------------------------------------------------------------------------------------------------------------------------------
## http://127.0.0.1:8000/api/download_balance_sheet_user_individual/ - GET Method 

## This is for getting all transactions done by the user created by the anyone

## Also put previously stored access token in (Auth -> Bearer -> Bearer YOUR_ACCESS_TOKEN) inside ThunderClient

## The output will be given similar to a csv file in the thunderclient, But when you try to use it in browser or frontend applications it will download.
-----------------------------------------------------------------------------------------------------------------------------------------
# Bonus Points
-----------------------------------------------------------------------------------------------------------------------------------------
## Authentication
### I have used jwt tokens which we can use in any frontend applications for authentication, And also i made the application to use refresh and access token, Access token expires every 1 hr and refresh token expires every 90 days, Refresh token is used for refreshing access token and resetting it's timer. Through this applications can have a good and flexible authentication.

## Validation
### I have used Django's built-in validation for all the fields in the models, And also used manual inputs for checking for errors

## Testing
### I have used unit testing inside this application which can be viewed at tests.py inside api app

## Large Data Handling
### I have used Django's built-in ORM for handling large data