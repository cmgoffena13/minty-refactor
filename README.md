# Minty localhost Application

## Application Setup
1. You need Postgres. Uses specific Postgres syntax alongside stored procedures and functions.
2. If you want to change the transaction custom categories, change the CustomCategoryEnum in the config.py file.
3. Update the public.accounts.is_operation_account field to true for your everyday transaction accounts.
4. Create a .flaskenv file in the main directory, reference the .flaskenv.example file

## Mint API Setup
1. Create a .env file in the main directoy, reference the .env.example file for the environment variables.
2. The MFA_TOKEN variable is obtained by:  
    i. Setting your Mint account to be two-factor authentication and while doing that

    ii. Before scanning the QR code, take the ID you have to enter manually. That is your MFA_TOKEN value.  

    *Warning: keep this in a safe place. Someone who gains access to this can gain access to your account.*