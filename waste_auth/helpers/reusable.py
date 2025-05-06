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


def assign_agent_to_product(waste_pruduct):
    from waste_auth.models import User, UserType, WasteProduct
    """ This function assign agent to a newly scheduled product pickup and its checks throuhgh 
    the agents and assign the most available and the most has the less pickup to do and closest
    to the user """
    pruduct = WasteProduct.objects.filter(id=waste_pruduct.id).first()
    priduct_address = pruduct.user.address
    if priduct_address:
        #check if user address string existe in the list of estates in the constant table attribute estate_address
        pass
    available_agent = User.objects.filter(user_type=UserType.AGENT, is_active=True)
    for agent in available_agent:
        pass


        # # Check if the agent has any scheduled pickups
        # if agent.pickup_set.filter(status="scheduled").exists():
        #     # If the agent has scheduled pickups, assign them to the product
        #     print(f"Agent {agent.username} has scheduled pickups.")
        # else:
        #     # If the agent doesn't have any scheduled pickups, assign them to the product
        #     print(f"Agent {agent.username} is available for assignment.")
        print(agent, "AGENT USER NAME")


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
    from waste_auth.models import User, WasteProduct, Agent  # adjust import as needed
    from waste_core.models import ConstantTable

    """
    This function assigns an agent to a newly scheduled product pickup.
    It checks through the agents and assigns the most available agent:
    - one with the fewest pending pickups
    - and who serves the estate matched in user's address
    """

    product = WasteProduct.objects.filter(id=waste_product.id).first()
    product_address = product.user.address if product and product.user else None

    if not product_address:
        return None  # No address to work with

    # Fetch the constant config
    constant = ConstantTable.get_constant_instance()
    estate_config = constant.estate_address  # List of estates and keywords

    matched_estate = None

    # Try to match user's address with estate keywords
    for estate in estate_config:
        for keyword in estate.get("keywords", []):
            if keyword.lower() in product_address.lower():
                matched_estate = estate.get("estate_name")
                break
        if matched_estate:
            break

    if not matched_estate:
        return None  # No matching estate found

    # Filter agents who serve the matched estate
    available_agents = Agent.objects.filter(estate__iexact=matched_estate)

    if not available_agents.exists():
        return None  # No agents found in that estate

    # Get agent with the least number of pending pickups
    agents_with_counts = [
        {
            "agent": agent,
            "pending_pickups": WasteProduct.objects.filter(
                assigned_agent=agent, status="pending"  # or whatever your pending status is
            ).count()
        }
        for agent in available_agents
    ]

    # Sort to get agent with the least pickups
    best_agent = sorted(agents_with_counts, key=lambda x: x["pending_pickups"])[0]["agent"]

    # Assign agent to product
    product.assigned_agent = best_agent
    product.save()

    return best_agent
