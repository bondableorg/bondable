import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

# from address we pass to our Mail object, edit with your name
FROM_EMAIL = "rahul.paurakhi@atopetrelo.com"

# update to your dynamic template id from the UI
TEMPLATE_ID = "d-fabcf1b04e3c49ada143775825811d67"

# list of emails and preheader names, update with yours
TO_EMAILS = [
    # ("keisuke.inagaki@atopetrelo.com", "Keisuke inagaki"),
    ("rahul.paurakhi@atopetrelo.com", "Rahul Paurakhi"),
    # update email and name
    ("pandey.dipesh50@gmail.com", "Dipesh Pandey"),
]


def SendDynamic(data):
    """Send a dynamic email to a list of email addresses

    :returns API response code
    :raises Exception e: raises an exception"""
    # create Mail object and populate
    message = Mail(from_email=FROM_EMAIL, to_emails=data["toemail"])
    # pass custom values for our HTML placeholders
    message.dynamic_template_data = {
        "firstname": data["firstname"],
        "lastname": data["lastname"],
        "email": data["email"],
        "phone": data["phone"],
        "message": data["message"],
        "country": data["country"],
        "address": data["address"],
        "pettype": data["pettype"],
        "npets": data["npets"],
        "petname": data.get("petname"),
        "petbreed": data["petbreed"],
        "reloctype": data["reloctype"],
    }
    message.template_id = TEMPLATE_ID
    # create our sendgrid client object, pass it our key, then send and return our response objects
    try:
        sg = SendGridAPIClient(api_key="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")
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("Messages Sent!")
    except Exception as e:
        print("Error: {0}".format(e))
        return e
    return str(response.status_code)


if __name__ == "__main__":
    SendDynamic()
