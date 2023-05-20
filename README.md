Pull the code from the repo.

Install the requirements using:
  pip install -r requirements.txt

To connect to a mongodb database, run the script create_collection.py
Make sure to change the connection string, for this eg, I have used mongodb atlas.

Run the project using:
  python manage.py runserver
 
Following are the APIs:
  1. For all transactions - api/transactions (METHOD- GET)
  2. To add a new transaction - api/transactions (METHOD - POST)
  3. To retrieve a transaction - api/transaction/<transaction_id> (METHOD - GET)
  4. To reverse a transaction - api/transactions/<transaction_id> (METHOD - DELETE)
