import base64
import os
from requests import exceptions, request
from string import Template, punctuation
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as text



# Create your reusable function(s) and class(es) here.
def validate_password(password: str):
    """
    Validates the given password based on specific criteria.
    Args:
        password (str): The password string to be validated.
    Raises:
        ValidationError: If the password fails to meet any of the following criteria:
            - The length of the password is less than 8 characters.
            - The password does not contain at least one numeric digit.
            - The password does not contain at least one uppercase character.
            - The password does not contain at least one lowercase character.
            - The password does not contain at least one special character.
    Returns:
        bool: True if the password passes all validation criteria.
    Note:
        - The password must be at least 8 characters long.
        - The password must contain at least one numeric digit (0-9).
        - The password must contain at least one uppercase letter (A-Z).
        - The password must contain at least one lowercase letter (a-z).
        - The password must contain at least one special character (e.g., !@#$%^&*()_-+=).
    """
    special_characters = list(punctuation)

    if len(password) < 8:
        raise ValidationError(
            text("Error: the length of password cannot be less than 8 characters.")
        )
    if not any(char.isdigit() for char in password):
        raise ValidationError(
            text("Error: password should have at least one numeric digit."))
    if not any(char.isupper() for char in password):
        raise ValidationError(
            text("Error: password should have at least one uppercase character."))
    if not any(char.islower() for char in password):
        raise ValidationError(x,
            text("Error: password should have at least one lowercase character."))
    if not any(char in special_characters for char in password):
        raise ValidationError(
            text("Error: password should have at least one special character.")
        )
    return True


def make_request(request_type: str, params: dict) -> dict:
    """
    Make an HTTP request using the specified request_type and parameters.
    Args:
        request_type (str): The type of HTTP request to make (e.g., 'GET', 'POST', 'PUT', 'DELETE', etc.).
        params (dict): A dictionary containing the parameters to be passed in the HTTP request.
    Returns:
        dict: A dictionary containing the response status, data, and error details.

        The returned dictionary has the following keys:
        - 'status': A boolean indicating if the request was successful (True) or not (False).
        - 'data': A dictionary containing the JSON response data if the request was successful, otherwise None.
        - 'error': A dictionary containing error details if the request failed, otherwise None.

        If the request is successful, 'data' will contain the JSON response obtained from the HTTP request.
        If the request fails, 'error' will contain the following keys:
        - 'message': A string containing the error message.
        - 'provider_response': A string containing the raw response received from the provider (if available).
    Raises:
        None. This function handles exceptions internally.
    Note:
        This function depends on the `request` function from the `requests` module and the `exceptions` module from the same package.
        Make sure to have those modules installed and imported before using this function.
    """
    try:
        response = request(request_type, **params)
        # print(response, "HERE IS THE REQUEST MIDDLEWARE BODY !!!!")
        return {
            "status": True,
            "data": response.json(),
            "error": None
        }
    except exceptions.RequestException as error:
        # print(error, "HERE IS THE ERROR MESSAGE AND EXCEPTION !!!!!")
        return {
            "status": False,
            "data": None,
            "error": str(error),
        }


def convert_string_to_base32(text: str):
    """
    Convert a given string to a base32-encoded string.
    Args:
        text (str): The input string that needs to be encoded.
    Returns:
        str: The base32-encoded string representing the input text.
    """
    encoded_bytes = base64.b32encode(text.encode())
    encoded_string = encoded_bytes.decode()
    return encoded_string


def email_sender(
    recipient: list,
    subject: str,
    template_directory: str = None,
    file=None,
    file_name=None,
    use_template: bool = False,
    has_attachment: bool = False,
    text: str = None,
    **substitutes
):
    """
    Send an email to one or more recipients using Mailgun API.
    Args:
    recipient (list): A list of email addresses of the recipients.
    subject (str): The subject of the email.
    template_directory (str, optional): The directory containing the email HTML template file. Defaults to None.
    file (object, optional): The file to be attached to the email. Defaults to None.
    file_name (str, optional): The name of the attached file. Defaults to None.
    use_template (bool, optional): Flag indicating whether to use an HTML template for the email body. Defaults to True.
    has_attachment (bool, optional): Flag indicating whether the email has an attachment. Defaults to False.
    text (str, optional): The plain-text body of the email. Used when `use_template` is False. Defaults to None.
    **substitutes: Keyword arguments used for substituting variables in the email template if `use_template` is True.
    Returns:
    dict: A dictionary containing the Mailgun API response. The response can be retrieved using the 'email_sender_response' key.
    """

    url = settings.MAILGUN_URL
    api_key = settings.MAILGUN_API_KEY

    if use_template and has_attachment:
        TEMPLATE_DIR = os.path.join("templates", template_directory)
        html_temp = os.path.abspath(TEMPLATE_DIR)

        with open(html_temp) as temp_file:
            template = temp_file.read()

        template = Template(template).safe_substitute(substitutes)

        response = make_request(
            "POST",
            dict(
                url=url,
                auth=("api", api_key),
                data={
                    "from": "Waste Management LTD",
                    "to": recipient,
                    "subject": subject,
                    "html": template,
                },
                files=[("attachment", (file_name, open(str(file), "rb").read()))]
            )
        )
    elif use_template:
        TEMPLATE_DIR = os.path.join("templates", template_directory)
        html_temp = os.path.abspath(TEMPLATE_DIR)
        
        with open(html_temp) as temp_file:
            template = temp_file.read()

        template = Template(template).safe_substitute(substitutes)

        response = make_request(
            "POST",
            dict(
                url=url,
                auth=("api", api_key),
                data={
                    "from": "Liberty Technologies Ltd. <segzyoly@gmail.com>",
                    "to": recipient,
                    "subject": subject,
                    "html": template,
                }
            )
        )
    else:
        # print("I GOT TO THE ELSE CONDITION !!!!!!!!!!!")
        response = make_request(
            "POST",
            dict(
                url=url,
                auth=("api", api_key),
                data={
                    "from": "Liberty Technologies Ltd. <postmaster@whispersms.com>",
                    "to": recipient,
                    "subject": subject,
                    "text": text
                }
            )
        )
        # print(response, "HERE IS THE RESPONSE !!!!")

    if response.get("status") == True:
        return dict(email_sender_response=response)
    else:
        return dict(email_sender_response=response)


def get_estate_agent(user_address: str):
    from waste_auth.models import ConstantTable
    const = ConstantTable.get_constant_instance()
    estates = const.estate_address

    for estate in estates:
        for keyword in estate.get("keywords", []):
            if keyword.lower() in user_address.lower():
                agent_id = estate.get("agent_id")
                # fetch and return the agent
                try:
                    return Agent.objects.get(id=agent_id)
                except Agent.DoesNotExist:
                    return None
    return None

def assign_agent_to_product(waste_product):
    from waste_auth.models import User, WasteProduct, RecycleAgents 
    from waste_auth.models import ConstantTable

    """
    This function assigns an agent to a newly scheduled product pickup.
    It checks through the agents and assigns the most available agent:
    - one with the fewest pending pickups
    - and who serves the estate matched in user's address
    """

    product = WasteProduct.objects.filter(id=waste_product.id).first()
    product_address = product.user.address if product and product.user else None
    if not product_address:
        return None 
    constant = ConstantTable.get_constant_instance()
    estate_config = constant.estate_address  
    matched_estate = None

    for estate in estate_config:
        for keyword in estate.get("keywords", []):
            if keyword.lower() in product_address.lower():
                matched_keyword = keyword.lower()
                print(matched_keyword, "this is the matched keyword")
                agent = RecycleAgents.objects.filter(estate=matched_keyword).last()
                 # Assign agent to product
                product.agent = agent
                product.save()
            else:
                #Check for the list of agents in the estate and make sure the work load is evenly distributed
                pass

    return agent   
               