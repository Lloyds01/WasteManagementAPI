import hashlib
from dataclasses import dataclass
from json import JSONDecodeError
import requests
from django.conf import settings
from helpers.reusable_functions import generate_random_acct_digit


@dataclass
class VfdBank:
    environment = settings.ENVIRONMENT
    # wallet2_live = "https://api-apps.vfdbank.systems/vtech-wallet/api/v1/wallet2/"
    wallet2_test = "https://api-devapps.vfdbank.systems/vtech-wallet/api/v1.1/wallet2/"
    # base_url = "https://api-apps.vfdbank.systems/vtech-wallet/api/v1/"
    access_token = f"{settings.VFD_ACCESS_TOKEN_LIVE}"
    wallet_credentials = f"{settings.VFD_WALLET_CREDENTIALS_LIVE}"

    headers = {"Authorization": f"Bearer {access_token}", "accept": "application/json"}
    params = {"wallet-credentials": f"{wallet_credentials}"}

    @classmethod
    def create_wallet(cls, firstname, middlename, dob, address, gender, bvn, lastname, phone):

        payload = {
            "firstname": f"{firstname}",
            "middlename": f"{middlename}",
            "lastname": f"{lastname}",
            "dob": f"{dob}",
            "address": f"{address}",
            "phone": f"{phone}",
            "gender": f"{gender}",
            "bvn": f"{bvn}",
        }

        if cls.environment == "dev":

            payload["accountNo"] = generate_random_acct_digit()
            fake_response = {"status": "00", "message": "Successful Creation", "data": payload}
            return fake_response
        elif cls.environment == "prod":

            try:
                # print("in try")
                filter_url = "wallet2/clientdetails/create"
                url = cls.base_url + filter_url
                request_response = requests.request(
                    "POST", url=url, headers=cls.headers, params=cls.params, json=payload
                )
                # print(request_response.text)
                response = request_response.json()
                # print(response)
                # print("completed try")
                return response

            except requests.exceptions.RequestException as e:

                return {"error": "VFD Request Broken", "message": f"{e}"}

    @classmethod
    def vfd_account_enquiry(cls, account_number=None):
        filter_url = "wallet2/account/enquiry"
        url = cls.base_url + filter_url
        cls.params["accountNumber"] = account_number
        response = requests.request("GET", url=url, headers=cls.headers, params=cls.params)

        # sample_response = {'status': '00', 'message': 'Account Details',
        #                    'data': {'accountNo': '',
        #                    'accountBalance': '100.000000',
        #                    'accountId': '2759924',
        #                    'client': 'Libertycredi-EDMUND DAVID GIWA', 'clientId': '',
        #                    'savingsProductName': 'Libertycredi Wallet Deposits', 'bvn': ''}
        #                    }

        return response.json()

    @classmethod
    def vfd_get_transfer_recipient(cls, transfer_type, account_number, bank_code):

        filter_url = "wallet2/transfer/recipient"
        url = cls.base_url + filter_url

        cls.params["accountNo"] = account_number
        cls.params["transfer_type"] = transfer_type
        cls.params["bank"] = bank_code

        response = requests.request("GET", url=url, headers=cls.headers, params=cls.params)

        return response.json()

    @classmethod
    def initiate_payout(
        cls,
        beneficiary_nuban,
        beneficiary_bank_code,
        narration,
        amount,
        transfer_type,
        user_bvn,
        reference,
        source_account=None,
    ):
        if cls.environment == "dev":
            return {
                "status": "00",
                "message": "785xr55555%990",
                "data": {"txnId": reference, "sessionId": "9099xdd899999900773636333333333", "reference": reference},
            }

        elif cls.environment == "prod":
            filter_url = "wallet2/transfer"
            url = cls.base_url + filter_url

            if source_account is None:
                enquire_for_user_account = cls.vfd_account_enquiry()
            else:
                enquire_for_user_account = cls.vfd_account_enquiry(account_number=source_account)

            if enquire_for_user_account.get("vfd_error"):
                return {"error": "VFD Request Broken", "message": f"{enquire_for_user_account}"}

            fromSavingsId = enquire_for_user_account.get("data")["accountId"]
            fromClient = enquire_for_user_account.get("data")["client"]
            fromClientId = enquire_for_user_account.get("data")["clientId"]
            fromAccount = enquire_for_user_account.get("data")["accountNo"]

            get_recipient = cls.vfd_get_transfer_recipient(
                transfer_type=transfer_type,
                account_number=beneficiary_nuban,
                bank_code=beneficiary_bank_code,
            )

            if get_recipient["status"] == "00":
                toClient = get_recipient.get("data")["name"]
                toClientBvn = get_recipient.get("data")["bvn"]
                toClientId = get_recipient.get("data")["clientId"]
                toSavings_or_sessions_id = get_recipient.get("data")["account"]["id"]

                get_signature = f"{fromAccount}{beneficiary_nuban}"
                signature_code = hashlib.sha512(str(get_signature).encode("utf-8")).hexdigest()

                payload = {
                    "fromSavingsId": fromSavingsId,
                    "amount": float(amount),
                    "toAccount": beneficiary_nuban,
                    "fromBvn": user_bvn,
                    "signature": signature_code,
                    "fromAccount": fromAccount,
                    "toBvn": toClientBvn,
                    "remark": narration,
                    "fromClientId": fromClientId,
                    "fromClient": fromClient,
                    "toKyc": "99",
                    "reference": reference,
                    "toClientId": toClientId,
                    "toClient": toClient,
                    "toSession": toSavings_or_sessions_id,
                    "transferType": transfer_type,
                    "toBank": beneficiary_bank_code,
                    "toSavingsId": toSavings_or_sessions_id,
                }

                try:
                    response = requests.request("POST", url=url, headers=cls.headers, params=cls.params, json=payload)
                    return response.json()

                except requests.exceptions.RequestException as e:
                    return {"error": "VFD Request Broken", "message": f"{e}"}

            return {"error": "No Recipient", "message": f"{get_recipient}"}

    @classmethod
    def vfd_transaction_verification_handler(cls, reference):

        filter_url = "wallet2/transactions"
        url = cls.base_url + filter_url

        cls.params["reference"] = reference

        response = requests.request("GET", url=url, headers=cls.headers, params=cls.params)

        # {
        #     "status": "00",
        #     "message": "Successful Transaction Retrieval",
        #     "data": {
        #         "TxnId": "LGLP-VDF-33eac366-21ee-48ea-9850-f1fd2dc3bddf",
        #         "amount": "30.0",
        #         "accountNo": "1011974622",
        #         "transactionStatus": "00",
        #         "transactionDate": "2022-07-15 13:37:39.0",
        #         "toBank": "999999",
        #         "fromBank": "999999",
        #         "sessionId": "",
        #         "bankTransactionId": "109810011",
        #     },
        # }

        resp = response.json()
        # print(resp)
        return resp

    @classmethod
    def get_vfd_float_balance(cls, account_number=None):

        filter_url = "wallet2/account/enquiry"
        url = cls.base_url + filter_url

        cls.params["accountNumber"] = account_number

        response = requests.request("GET", url=url, headers=cls.headers, params=cls.params)

        resp = response.json()

        if resp.get("status") == "00":
            vfd_balance = float(resp.get("data").get("accountBalance"))
        else:
            vfd_balance = None

        return vfd_balance

    @classmethod
    def create_corporate_account(cls, rc_number, company_name, incorp_date, bvn):
        print("at create_corporate_account")
        if cls.environment == "dev":
            accountNo = generate_random_acct_digit()
            payload = {
                "rcNumber": f"{rc_number}",
                "companyName": f"{company_name}",
                "incorporationDate": f"{incorp_date}",
                "bvn": f"{bvn}",
            }
            response = {
                "main_data": {
                    "status": "00",
                    "message": "Corporate account created successfully",
                    "data": {"accountNo": accountNo, "accountName": company_name},
                },
                "initial_payload": payload,
            }

            return response
        elif cls.environment == "prod":
            print("at production")

            filter_url = "wallet2/corporateclient/create"
            url = cls.base_url + filter_url

            # if user.vfd_bvn_acct_num_count < 1:
            #     final_bvn = bvn
            #
            # else:
            #     number_to_add = (user.vfd_bvn_acct_num_count - 1) + 1
            #     final_bvn = f"{bvn}-{number_to_add}"

            payload = {
                "rcNumber": f"{rc_number}",
                "companyName": f"{company_name}",
                "incorporationDate": f"{incorp_date}",
                "bvn": f"{bvn}",
            }
            print(payload)
            try:
                print("at try")
                response = requests.request("POST", url=url, json=payload, headers=cls.headers, params=cls.params)
                print(response.text)
                res = response.json()
                return {"main_data": res, "initial_payload": payload}

            except requests.exceptions.RequestException as err:
                print({"main_data": {"status": "99", "message": str(err)}, "initial_payload": payload})
                return {"main_data": {"status": "99", "message": str(err)}, "initial_payload": payload}


    @classmethod
    def update_bvn_nin(cls, account_number, bvn, nin: str = None, dob=None):
        # filter_url = "wallet2/client/update"
        filter_url = "wallet2/client/upgrade"
        url = cls.base_url + filter_url

        if not dob:
            payload = {"accountNo": account_number, "action": "Update-BVN"}
        else:
            payload = {
                "accountNo": account_number,
                "dob": dob,
                "action": "Recomply-With-BVN",
            }

        if nin:
            payload["nin"] = nin
        else:
            payload["bvn"] = bvn
        try:
            response = requests.request("POST", url=url, headers=cls.headers, params=cls.params, json=payload)
            res = response.json()
            return {
                "main_data": res,
            }
        except requests.exceptions.RequestException as err:
            return {
                "main_data": {"status": "99", "message": str(err)},
            }
