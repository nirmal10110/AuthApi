import traceback
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models.virtualCard import VirtualCardModel
from visa.visaAPI import MVisa
from walletAPI.wallet import Wallet
from datetime import datetime
import time
from pan import PAN
import uuid

CARD_GENERATED = "CARD IS ALREADY GENERATED"
CARD_NOT_GENERATED = "CARD NOT GENERATED"
INTERNAL_SERVER_ERROR = 'INTERNAL SERVER ERROR'
FAILED_TO_CREATE = 'FAILED TO CREATE'
KYC_STATUS = 'WALLET UNAUTHORIZED CHECK KYC STATUS'
PAN_CREATED = 'PAN CREATED SUCCESSFULLY,HURRAY!!'
AMOUNT_ADDED = 'MONEY ADDED'
INSUFFICIENT_FUNDS = 'INSUFFICIENT FUNDS'

wallet = Wallet()
visa = MVisa()


class VirtualCard(Resource):

    @classmethod
    @jwt_required
    def get(cls, mobile_number: str):
        """
        Accessing already generated card.
        :param mobile_number:
        :return:
        """
        
        try:
            virtual_card = VirtualCardModel.find_by_mobile_number(mobile_number)
        except:
            return {"message": INTERNAL_SERVER_ERROR}, 500

        if not virtual_card:
            return {"message": CARD_NOT_GENERATED}, 404

        return {"message": CARD_GENERATED, "pan": virtual_card.pan}, 200

    @classmethod
    @jwt_required
    def post(cls, mobile_number: str):
        """
        It creates PAN details if not yet created while checking your wallet was authorized.
        :param mobile_number:
        :return:
        """

        virtual_card = VirtualCardModel.find_by_mobile_number(mobile_number)

        if virtual_card:
            return {"message": CARD_NOT_GENERATED}, 400

        wallet_response = wallet.authorize(mobile_number)
        print(wallet_response)

        if not wallet_response:
            return {"message": INTERNAL_SERVER_ERROR}, 500

        if wallet_response.status_code == 400:
            return {"message": KYC_STATUS}, 400

        pan_pref = '40'
        pan = pan_pref + str(uuid.uuid4().int >> 32)[0:14]

        while pan in PAN:
            pan = pan_pref + str(uuid.uuid4().int >> 32)[0:14]

        card_generated_time = datetime.fromtimestamp(time.time()).isoformat()
        virtual_card = VirtualCardModel(pan, card_generated_time, mobile_number)
        print(pan)
        try:
            virtual_card.save_to_db()
            PAN.add(pan)
        except:
            traceback.print_exc()
            return {"message": FAILED_TO_CREATE}, 500

        return {"message": PAN_CREATED}, 201


class AddAmount(Resource):

    @classmethod
    @jwt_required
    def put(cls, mobile_number: str):
        """
        Adds amount to your virtual card temporarily.
        :param mobile_number:
        :return:
        """

        payload = request.get_json()
        virtual_card = VirtualCardModel.find_by_mobile_number(mobile_number)
        if not virtual_card:
            return {"message": CARD_NOT_GENERATED}, 400

        wallet_response = wallet.get_amount(mobile_number, payload['amount'])

        if not wallet_response:
            return {'message': INTERNAL_SERVER_ERROR}, 500

        if wallet_response.status_code != 200:
            return {'message': wallet_response.json()}, 400

        virtual_card.amount += payload['amount']

        try:
            virtual_card.save_to_db()
        except:
            return {"message": INTERNAL_SERVER_ERROR}, 500

        return {"message": AMOUNT_ADDED}, 200


class Payment(Resource):

    @classmethod
    @jwt_required
    def put(cls, mobile_number: str):
        """
        Completes the payment via VISA NET using mVisa API.
        :param mobile_number:
        :return:
        """

        payload = request.get_json()

        virtual_card = VirtualCardModel.find_by_mobile_number(mobile_number)

        if not virtual_card:
            return {'message': CARD_NOT_GENERATED}, 400

        if virtual_card.amount < float(payload['amount']):
            return {'message': INSUFFICIENT_FUNDS}, 400

        payload['senderAccountNumber'] = virtual_card.pan
        payload['localTransactionDateTime'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        visa_response = visa.cash_in_push_payments_post_payload(payload)
        print(visa_response, type(visa_response))
        if not visa_response or visa_response.status_code != 200:
            return {"message": INTERNAL_SERVER_ERROR}, 500

        virtual_card.amount -= float(payload['amount'])
        virtual_card.last_transaction_time = datetime.fromtimestamp(time.time()).isoformat()
        virtual_card.count += 1

        try:
            virtual_card.save_to_db()
        except:
            return {"message": INTERNAL_SERVER_ERROR}, 500

        return {'message': visa_response.json()}, 200
