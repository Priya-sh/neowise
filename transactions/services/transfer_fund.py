from bson.objectid import ObjectId
from utils import get_database
from bson.json_util import dumps

class FundTransfer:

    
    def __init__(self, sender_id, receiver_id, amount):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount

    
    def check_sufficient_balance(self, transfer_data):
        sender_id = transfer_data['sender_id']
        transfer_amount = transfer_data['amount']
        user_data = self.get_user_data({'user_id': sender_id})
        # Converting to the JSON
        if float(user_data['balance']) > float(transfer_amount):
            return True
        else:
            return False

        
    def transfer_fund_to_receiver(self, transfer_data):
        sender_id = transfer_data['sender_id']
        receiver_id = transfer_data['receiver_id']
        transfer_amount = transfer_data['amount']
        sender_has_suff_bal = self.check_sufficient_balance(transfer_data)
        if sender_has_suff_bal:
            debit_success = self.debit(transfer_data)
            if debit_success:
                credit_success = self.credit(transfer_data)
                if credit_success:
                    return {'code': 200, 'message': 'Fund transfer successful'}
                else:
                    self.reverse_transfer({'sender_id': sender_id, 'receiver_id': receiver_id, 'amount' : transfer_amount})
            else:
                self.reverse_transfer({'sender_id': sender_id, 'receiver_id': receiver_id, 'amount' : transfer_amount})
        else:
            return {'code': 500, 'message': 'Insuffucient balance'}


    def get_user_data(self, transfer_data):
        db = get_database()
        user_id = transfer_data['user_id']
        users_collection = db['users']
        user_data = users_collection.find({'id': user_id})
        list_cur = list(user_data)
        return list_cur[0]
    
    
    def reverse_transfer(self, transfer_data):
        sender_id = transfer_data['sender_id']
        receiver_id = transfer_data['receiver_id']
        transfer_data['receiver_id'] = sender_id
        transfer_data['sender_id'] = receiver_id
        # add money back to sender
        credit_success = self.credit(transfer_data)
        if credit_success:
            # deduct money from receiver
            debit_success = self.debit(transfer_data)
            if debit_success:
                return {'code': 200, 'message': 'Fund transfer reversed successfully'}
            else:
                return {'code': 200, 'message': 'Error occured while transferring funds'}
        else:
            return {'code': 200, 'message': 'Error occured while transferring funds'}
        

    # deduct amount from sender
    def debit(self, transfer_data):
        sender_id = transfer_data['sender_id']
        user_data = self.get_user_data({'user_id': sender_id})
        if user_data:
            new_balance = float(user_data['balance']) - float(transfer_data['amount'])
            self.update_balance_in_user_account({'user_id': sender_id, 'new_balance': new_balance})
            return {'code': 200, 'message': 'Debited successfully'}
        return {'code': 200, 'message': 'Debited successfully'}


    # credit amount to receiver
    def credit(self, transfer_data):
        receiver_id = transfer_data['receiver_id']
        user_data = self.get_user_data({'user_id': receiver_id})
        if user_data:
            new_balance = float(user_data['balance']) + float(transfer_data['amount'])
            self.update_balance_in_user_account({'user_id': receiver_id, 'new_balance': new_balance})
            return {'code': 200, 'message': 'Credited successfully'}
        return {'code': 200, 'message': 'Credited successfully'}


    def update_balance_in_user_account(self, transfer_data):
        user_id = transfer_data['user_id']
        new_balance = transfer_data['new_balance']
        db = get_database()
        users_collection = db['users']
        user_filter = {'id': user_id}
        new_values = {"$set": {'balance': new_balance}}
        users_collection.update_one(user_filter, new_values)