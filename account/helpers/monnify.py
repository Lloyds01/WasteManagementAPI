import json
import uuid
from base64 import b64encode

import requests
from django.conf import settings


# Monnify disbursement API integration.
class Monnify:
    """
    Authorize API calls with generated Bearer token.
    Get token using: API_KEY & SECRET_KEY.
    """

    def __init__(self) -> None:
        self.base_url = settings.MONNIFY_BASE_URL
        self.api_key = settings.MONNIFY_API_KEY
        self.secret_key = settings.MONNIFY_SECRET_KEY
        self.monnify_source_account = settings.MONNIFY_SOURCE_ACCOUNT

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

    def generate_reference_code(self, length: int = 16):
        """
        Generate reference code with desired length.
        Defaults to a sixteen(16) length string.
        """
        unique_code = uuid.uuid4()
        return str(unique_code).replace("-", "")[:length]

    def encrypt(self, text: str):
        """
        Returns a base64 value to access the API(s).
        """
        text_bytes = text.encode("ascii")
        encrypted_text = b64encode(text_bytes).decode("ascii")
        return encrypted_text

    def login(self):
        endpoint = "/api/v1/auth/login"

        url = f"{self.base_url}{endpoint}"
        auth = self.encrypt(text=f"{self.api_key}:{self.secret_key}")
        payload = {}
        headers = {"Content-Type": "application/json", "Authorization": f"Basic {auth}"}
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get("requestSuccessful") == True and data.get("responseMessage") == "success":
                token = data.get("responseBody").get("accessToken")
                return dict(status=True, token=token)
            return dict(status=False, token=None)
        return dict(status=False, token=None)

    def initiate_single_transfer(self, amount, reference, narration, bank_code, account_no, account_name):
        # from accounts.models import MonnifyLog

        endpoint = "/api/v2/disbursements/single"
        print(self.monnify_source_account)
        url = f"{self.base_url}{endpoint}"
        auth = self.login()
        amount = round(amount, 2)
        payload = json.dumps(
            {
                "amount": amount,
                "reference": reference,
                "narration": narration,
                "destinationBankCode": bank_code,
                "destinationAccountNumber": account_no,
                "currency":"NGN",
                "sourceAccountNumber": self.monnify_source_account,
                "destinationAccountName": account_name,
            }
        )

        # first_monnify_log = MonnifyLog.objects.create(
        #     reference=data.get("reference"),
        #     status="PAYOUT_REQUEST",
        #     payload=payload,
        # )

        if auth.get("status") == True:
            token = auth.get("token")

            # ("payload", payload)
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            }

            try:

                response = requests.request("POST", url, headers=headers, data=payload)
                # first_monnify_log.response = response.text
                # first_monnify_log.save()

                if response.status_code == 200:
                    data = response.json()
                    if data.get("requestSuccessful") == True and data.get("responseMessage") == "success":
                        return dict(status=True, response=data.get("responseBody"))
                    return dict(status=False, response=None)
                return dict(status=False, response=response.text)

            except Exception as e:
                response = str(e)

        else:
            response = "Token is invalid or expired."

        # first_monnify_log.response = response
        # first_monnify_log.save()

        return dict(status=False, response=response)

    def get_single_transfer_status(self, reference: str):
        # from accounts.models import MonnifyLog

        endpoint = f"/api/v2/disbursements/single/summary?reference={reference}"
        url = f"{self.base_url}{endpoint}"
        auth = self.login()
        if auth.get("status") == True:
            token = auth.get("token")
            payload = {}
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            }
            response = requests.request("GET", url, headers=headers, data=payload)

            """
            SAMPLE RESPONSE

            {
                "requestSuccessful": true,
                "responseMessage": "success",
                "responseCode": "0",
                "responseBody": {
                    "amount": 230.00,
                    "reference": "Final-Reference-3a",
                    "narration": "911 Transaction",
                    "currency": "NGN",
                    "fee": 20.00,
                    "twoFaEnabled": false,
                    "status": "SUCCESS",
                    "transactionDescription": "Approved or completed successfully",
                    "transactionReference": "MFDS2020080523"
                    "destinationBankCode": "058",
                    "destinationAccountNumber": "0111946768",
                    "destinationAccountName": "MEKILIUWA, SMART CHINONSO",
                    "destinationBankName": "GTBank",
                    "createdOn": "13/11/2019 09:42:07 PM"
                }
            }

            SAMPLE STATUS
            1. SUCCESS
            2. FAILED
            3. PENDING
            4. OTP_EMAIL_DISPATCH_FAILED
            5. PENDING_AUTHORIZATION


            """

            # MonnifyLog.objects.create(
            #     reference=reference,
            #     status="PAYOUT_VERIFICATION_REQUEST",
            #     response=response.text,
            # )

            try:
                return response.json()
            except:
                return response.text

        return dict(status=False, response="Token is invalid or expired.")

    def verify_monnify_disbursement(self, reference, return_res_body=False):
        verification_response = self.get_single_transfer_status(reference=reference)

        reversal_status = ["FAILED", "OTP_EMAIL_DISPATCH_FAILED", "D02"]

        # print("monnify verification_response", verification_response)

        if isinstance(verification_response, dict):
            trans_status = verification_response.get("responseBody", {}).get("status")
            transaction_not_found_status_code = verification_response.get("responseCode")
            trans_bank_id = verification_response.get("responseBody", {}).get("transactionReference")

            if transaction_not_found_status_code in reversal_status:
                data = {
                    "status": True,
                    "reversed": True,
                    "transferred": False,
                    "data": {"escrow_id": trans_bank_id, "message": "failed"},
                }

            elif trans_status in reversal_status:
                data = {
                    "status": True,
                    "reversed": True,
                    "transferred": False,
                    "data": {"escrow_id": trans_bank_id, "message": "failed"},
                }

            elif trans_status == "SUCCESS":
                data = {
                    "status": True,
                    "transferred": True,
                    "data": {"escrow_id": trans_bank_id, "message": "success"},
                }

            else:
                data = {
                    "status": True,
                    "transferred": False,
                    "data": {"escrow_id": trans_bank_id, "message": "pending"},
                }

            if return_res_body:
                data["data"] = verification_response

            return data

        else:
            data = {"status": False, "transferred": False, "data": {"escrow_id": "", "message": "pending"}}

            if return_res_body:
                data["data"] = verification_response

            return data

    def check_monnify_balance(self):
      account_no = settings.MONNIFY_SOURCE_ACCOUNT
      endpoint = f"/api/v2/disbursements/wallet-balance?accountNumber={account_no}"

      url = f"{self.base_url}{endpoint}"
      auth = self.login()
      if auth.get("status") == True:
        token = auth.get("token")
        payload = {}
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                }
        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()

    
          