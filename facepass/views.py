import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.models.fields import NullBooleanField
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import *
from . import utils, forms
from random import choice

# Create your views here.


def index(request):
    """
    The MD content will be
    displayed here

    """
    if request.method == "GET":
        fetched_content = request.GET.get("content",  "INSTRUCTIONS")
    else:
        fetched_content = "INSTRUCTIONS"

    # Get the content of the md file
    content = utils.get_entry(fetched_content)
    content = utils.md_to_html(content)

    # Render it
    return render(request, "facepass/index.html", {
        "title": "FacePass",
        "content": content
    })


def testcompany_view(request):
    """
    Test company view that illustrates
    the FacePass button

    """
    if request.method == "GET":

        token = request.GET.get('token') or None

        # If a token is provided
        # decrypt and validate
        if token:
            try:

                encrypted_token = token

                # decrypt the token
                token = json.loads(utils.decode(token))
                company_id = token["company_id"] or None
                success_url = token["success_url"] or None
                error_url = token["error_url"] or None

                # Validate the 30 min token
                utils.validate_token(token)

                # Fetch company information
                company = CompanyProfile.objects.get(id=company_id)

                return render(request, "facepass/index.html", {
                    "title": company.name,
                    "detector": True,
                    "app": "recognize",
                    "token": encrypted_token,
                    "success_url": success_url,
                    "error_url": error_url
                })

            except ValidationError as err:
                return render(request, "facepass/index.html", {
                    "message": err.message
                })

            except Exception:
                return render(request, "facepass/index.html", {
                    "message": "This FacePass is no longer available"
                })

        # If no token provided in the url
        # render page that will generate it
        # and send it back
        else:
            user = request.user
            message = ""

            # logout the user if authenticated for better test experience
            if user.is_authenticated:
                logout(request)
                message = "You have been logged out in order to test FacePass"

            # Fetch all the affiliated companies that have an api key
            companies = CompanyProfile.objects.exclude(
                api_key__isnull=True).order_by("name").all()

            if (companies):
                # if affiliated companies exist
                random_company = choice(companies)

                # generate token to send
                token = utils.encode(json.dumps({
                    "company_id": random_company.id,
                    "success_url": random_company.success_url,
                    "error_url": random_company.error_url,
                    "timestamp": datetime.datetime.now().timestamp()
                }))

                return render(request, "facepass/index.html", {
                    "warning_message": message,
                    "title": random_company.name,
                    "facepass": True,
                    "company": random_company,
                    "token": token
                })

            else:
                # If no companies are configured
                return render(request, "facepass/index.html", {
                    "warning_message":
                    "There are no affiliated companies.\
                        Add them from the admin interface."
                })


def login_view(request):
    """
    Login route

    """

    next = request.GET.get("next", None)

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("passes")
        else:
            return render(request, "facepass/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "facepass/login.html")


def logout_view(request):
    """
    Logout route

    """
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    """
    Register route

    """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # List comprehension that captures the empty post fields
        missing_fields = [key for (key, value) in
                          [
            ('username', username),
            ('email', email),
            ('password', password),
            ('confirmation', confirmation)
        ] if not value
        ]

        # Check that username and email are filled
        if not username or not email or not password or not confirmation:
            message = f"Missing fields: {', '.join(missing_fields)}"

            return render(request, "facepass/register.html", {
                "message": message
            })

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "facepass/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            personal_information = PersonalInformation(
                owner=user, email=user.email)
            personal_information.save()

        except IntegrityError:
            return render(request, "facepass/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "facepass/register.html")


@login_required(login_url="login")
def personal_information_view(request):
    """
    Personal Information route

    """
    user = request.user

    # Fetch the user personal information if it exists
    if hasattr(user, 'personal_information'):
        personal_information = user.personal_information.serialize()
    else:
        # create it if it doesn't
        personal_information = PersonalInformation(
            owner=user, email=user.email)
        personal_information.save()
        return redirect('personal_information')

    form = forms.PersonalInformationForm(personal_information)

    if request.method in ["POST", "PUT"]:

        # Get the form entries
        if request.method == "PUT":
            form = forms.PersonalInformationForm(request.PUT)
        else:
            form = forms.PersonalInformationForm(
                request.POST, instance=user.personal_information)

        if form.is_valid():

            # If the form is valid update the info
            personal_information = form.save(commit=False)
            personal_information.user = user
            personal_information.save()

            # update messaging
            utils.update_context(request, {
                "message": "",
                "success_message":
                "Your personal information have been updated"
            })

            # redirect to form
            return redirect('personal_information')

        else:
            utils.update_context(request, {
                "message": "Sorry your input is not valid",
                "success_message": ""
            })

    # render the form
    data = utils.render_form(request, form, {
        "title": "Personal Information",
        "form_method": forms.set_method("PUT"),
        "hide_legend": True,
        "custom_button_label":  "Save"
    })
    return render(request, "facepass/index.html", data)


@login_required(login_url="login")
def passes_view(request):
    """
    Passes view route

    """
    passes = request.user.passes.all()

    return render(request, "facepass/index.html", {
        "title": "Passes",
        "display_list": True,
        "list": passes
    })


@login_required(login_url="login")
def onboard_view(request):
    """
    Onboard view route

    """

    if request.method == "PUT":

        # Fetch the data
        data = json.loads(request.body)
        if data.get("images") is not None:
            images = data["images"]

        try:
            user = request.user
            user.face_signature = json.dumps(images)
            user.save()
            return JsonResponse({
                "images": images,
                "message": "Images saved"
            }, status=201)

        except Exception:
            return JsonResponse({
                "error": "Sorry something went wrong"
            }, status=400)

    else:
        return render(request, "facepass/index.html", {
            "title": "FaceId Setup",
            "detector": True
        })


def identify(request):
    """
    Api Route to start identification

    """
    if request.method == 'POST':

        # Fetch the data
        data = json.loads(request.body)
        token = data.get("token") or None
        token = json.loads(utils.decode(token)) or None

        try:
            # Validate token
            utils.validate_token(token)

            # decrypt the token
            company_id = token["company_id"] or None
            success_url = token["success_url"] or None
            error_url = token["error_url"] or None

            # Get the user information
            users = User.objects.exclude(face_signature="").all()
            passes = [
                [passe.serialize() for passe in user.passes
                 .filter(company__id=company_id)
                 .exclude(is_active=False)
                 .order_by("-updated_on")
                 .all()]

                for user in users
            ]
            users = [user.signature() for user in users]
            usernames = [user["username"] for user in users]
            labels = [user["label"] for user in users]
            images = [user["images"] for user in users]

            # Get the company information
            company = CompanyProfile.objects.get(id=company_id)
            company_name = company.name
            requested_information = [
                information.serialize() for information
                in company.requested_information.all()
            ]

            # Send the response upon success
            return JsonResponse({
                "usernames": usernames,
                "labels": labels,
                "images": images,
                "passes": passes,
                "company_id": company_id,
                "company_name": company_name,
                "requested_information": requested_information,
                "success_url": success_url,
                "error_url": error_url
            }, status=201)

        except ValidationError as err:
            return JsonResponse({
                "error": err.message
            }, status=400)

        except Exception:
            return JsonResponse({
                "error": "Unauthorized. The token is no longer valid"
            }, status=400)


def resolve_pass(request):
    """
    Api Route to add/remove
    user's permissions for a company

    """
    if request.method == 'PUT':

        # Fetch the data
        data = json.loads(request.body)
        user_id = data.get("user_id") or None
        company_id = data.get("company_id") or None
        pass_id = data.get("pass_id") or None
        allow = data.get("allow") or False

        try:
            user_id = int(user_id) or None
            company_id = int(company_id) or None
            pass_id = int(pass_id) if pass_id else None
            user = User.objects.get(id=user_id) or None
            company = CompanyProfile.objects.get(id=company_id) or None

            # Protected result signature preparation
            personal_information = {}
            personal_information["timestamp"] = datetime.datetime.now(
            ).timestamp()
            personal_information["company_name"] = company.name

            # default url to defined company error
            url = company.error_url

            # If a pass exists already
            if pass_id:
                passe = Pass.objects.get(id=pass_id)
                if allow:
                    # add allowed info
                    for information in company.requested_information.all():
                        passe.allowed_information.add(information)
                        field = information.field
                        personal_information[field] = getattr(
                            user.personal_information, field)
                    url = company.success_url
                else:
                    # delete the pass
                    passe.delete()
            elif allow:
                # if no pass and allowed then create
                passe = Pass(owner=user, company=company)
                passe.save()
                for information in company.requested_information.all():
                    passe.allowed_information.add(information)
                    field = information.field
                    personal_information[field] = getattr(
                        user.personal_information, field)
                passe.save()
                url = company.success_url

            return JsonResponse({
                "allow": allow,
                "redirect_url": url,
                "token": utils.encode(json.dumps(personal_information))
            }, status=201)

        except Exception as err:
            return JsonResponse({
                "error": "Something went wrong"
            }, status=400)


def protected_view(request, token):
    """
    Route to view the protected data

    """
    token = request.GET.get('token') or None

    # If a token is provided
    # decrypt and validate
    if token:
        try:

            # decrypt the token
            token = json.loads(utils.decode(token))

            # Validate the 30 min token
            utils.validate_token(token)

            company_name = token.get("company_name", "")
            del(token["company_name"])
            del(token["timestamp"])

            return render(request, "facepass/index.html", {
                "title": company_name,
                "protected": True,
                "personal_information": token
            })

        except ValidationError as err:
            return render(request, "facepass/index.html", {
                "message": err.message
            })

        except Exception:
            return render(request, "facepass/index.html", {
                "message": "This FacePass is no longer available"
            })
    else:
        return render(request, "facepass/index.html", {
            "message": "There are no active FacePasses"
        })


def message(request):
    """"
    Generic message route

    """

    if request.method == 'GET':

        data = {}
        message = request.GET.get("message", "")
        type = request.GET.get("type", "")
        data[f"{type}_message" if type else "message"] = message

        # Render error
        return render(request, "facepass/index.html", data)
