import json
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.files.storage import default_storage
from markdown2 import Markdown
import base64

DEFAULT_CONTEXT = {
    "message": "",
    "success_message": ""
}

# Context functions


def initialize_context(request):
    """
    Initialize the session variable
    that holds the context

    """

    if "context" in request.session:
        return get_context(request)
    else:
        return save_context(request, DEFAULT_CONTEXT)


def save_context(request, context):
    """
     Save the context into the session
     in JSON format

    """
    request.session["context"] = json.dumps(context)
    return context


def get_context(request):
    """
    Read the context from the session

    """

    if "context" in request.session and request.session["context"]:
        return json.loads(request.session["context"])
    else:
        return None


def update_context(request, updated_dict):
    """
    Update the context with the new
    context

    """

    context = get_context(request)
    context.update(updated_dict)
    return save_context(request, context)


def reset_context(request):
    """
    Reset the context to the default

    """
    return save_context(request, DEFAULT_CONTEXT)

# Form functions


def render_form(request, data, options={}):
    """
    Prepares the data for rendering
    in the view

    """

    # Initialize context
    context = initialize_context(request)

    # Combine the data with context
    data = {
        "form": data
    }
    data.update(options)
    data.update(context)

    # reset the context
    reset_context(request)

    return data


def get_method(request):
    """
    Gets the api method submitted in request

    """

    if request.method == "POST":
        method = request.POST.get("_method", '')
    elif request.method == "GET":
        method = request.GET.get("_method", '')

    return method.upper() if method else request.method


# Validators

def validate_greater_than(value, threshold, err="Your input"):
    """
    Validates that the input is greater
    than the passed threshold

    """

    if value <= threshold:
        raise ValidationError(
            f"{err} should be more than {threshold} characters"
        )


def validate_less_than(value, threshold, err="Your input"):
    """
    Validates that the input is less than
    the passed threshold

    """

    if value > threshold:
        raise ValidationError(
            f"{err} should be less than {threshold} characters"
        )


def validate_token(token, duration=1800):
    """
    Validatess the token

    """
    timestamp = token["timestamp"] or None
    if datetime.datetime.now().timestamp() - timestamp > duration:
        raise ValidationError("Unauthorized. The token is no longer valid")


# RegEx Validators
validate_phone = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: \
        '+999999999'. Up to 15 digits allowed.")


# md to html
def get_entry(filename):
    """
    Retrieves an md file
    to output to the view
    Inspired from Wiki Assignment
    """
    try:
        f = default_storage.open(f"entries/{filename}.md")
        return f.read().decode("utf-8")

    except FileNotFoundError:
        return None


def md_to_html(md):
    """
    Convert markdown to html
    """
    if md:
        markdown = Markdown()
        return markdown.convert(md)

    else:
        return ''


# Encryption
def encode(data):
    message_bytes = data.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')


def decode(data):
    base64_bytes = data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('ascii')
