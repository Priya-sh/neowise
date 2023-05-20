from django.urls import path
from transactions.views import TransactionList, Transaction

urlpatterns = [
	path('transactions/', TransactionList.as_view(), name='transactions-all'),
    path('transaction/<str:transaction_id>', Transaction.as_view(), name='transaction')
]