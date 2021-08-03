+ By: Dory Azar

![](static/facepass/images/facepass.png)

<br />

#### What is FacePass
FacePass is a service that allows people to own their personal information and to have full control over what information they want to share with other online services - as opposed to the other way around. Through FacePass, people can authenticate to any affiliated online service through face recognition and can decide what piece of information they want to share and make available to the service.

[Watch the demo](https://youtu.be/B52id0zRDA8)

<br>

#### Scope
We were able to implement the major features in order to best illustrate the concept:

+ Authentication
+ Registration
+ Creation of a FacePass account
+ Setting up face identification that trains FacePass to recognize a user
+ Editing Personal Information
+ Viewing authorized Passes
+ Connecting to an affiliated company through Face Recognition
+ Authorize/Unauthorize access to personal information
+ Built-in admin interface

The following features will need to be performed on the Admin interface:

+ Managing (CRUD) affiliated companies
+ Manual management (CRUD) of Passes
+ Managing type of information that FacePass handles

<br>

#### Credits & Resources

* [face-api library](https://github.com/justadudewhohacks/face-api.js/): this project uses the face api javascript library developed by Vincent Muhler

* detect.js: Proprietary open source class that I created to make the use of the face-api library easier to use and to integrate in third party applications and frameworks. `detect.js` is included in the package

* [TensorFlow](https://www.tensorflow.org/): Tensor flow is an end-to-end open source platform with comprehensive tools and libraries that lets developers easily build machine learning powered applications

* [ml5.js](https://ml5js.org/): ML5 is an open source library, with exhaustive documentation and tutorials for understanding machine learning algorithms and how to use TensorFlow Models

<br />

#### Code Structure

FacePass uses the capabilities of both server and client sides to provide a smooth user experience.

+ **Models**

    There 4 main entities that drive the whole experience: `User`, `PersonalInformation`, `CompanyProfile`, `Pass` - represent the user, the company, the pass and all the connections between them.

    Additionally, we have a 5th entity - `AllowedInformation` - that is more of a general setup model that controls what pieces of information (Firstname, lastname, credit card number etc.) FacePass makes available to affiliated companies to request from users.

<hr>

+ **Dynamic Template & Components**
    
    + **html templates**
    
        The entire application is driven by one dynamic page template `index.html` that is served by Python routes and views. 

        The dynamic page template includes a variety of templatized html components such as banner messages, forms, navbars etc. Those components can be found in `templates/facepass/components`

        The face detection user interface is also an html component that is powered by a the above-mentioned javascript libraries

    + **Form models**

        Python form models have been used primarily to generate long and dynamic forms such as the Personal Information one. The form model can be found in `forms.py`

    + **MarkDown Content**

        The application uses MarkDown content - specifically for the instructions (the homepage) and the README pages - that we included into the experience. The main reason for including markdown pages is for the need to include instructions and documentation as part of this project.

        The Markdown content is injected into the application. All markdown entries can be found in the `/entries` folder


<hr>


+ **View Controllers**

    `views.py` is our main view controller that interfaces with the models to render the information as either html templates or JSON responses to be consumed on the client side.

<hr>

+ **API endpoints**

    3 endpoints are provided for API interfacing:

    + `PUT - api/pass`: authorize/unauthorize access to companies
    + `POST - api/identify`: endpoint to initiate protected face detection from the face detection user interface
    + `PUT - /onboard`: endpoint to save user face signatures

<hr>
    
+ **Face detection user interface**

    The face detection user interface is driven by the `facepass.js` code. `facepass.js` uses the open source libraries `face-api.min.js` (by  Vincent  Muhler) and `detect.js` (written by me) and uses the API endpoints to interface with the database and the FacePass dynamic views.
    Both libraries have been included in the code structure `static/facepass`.

    The face detection and recognition libraries require the use of heavily trained tensor flow models. Those models have been integrated into the code structure and can be found in `static/facepass/models` folder.

<hr>

+ **Utilities**

    Several utility functions for session management, generic renderers, validators, converters (md to html), encryption etc. were build to be used across the entire application. All those functions can be found in `utils.py`

<hr>

+ **Admin Interface**

    The built-in admin interface has been activated to help maintain the application. The models have been registered in `admin.py`



<br />

#### Getting Started

1. Install the distribution code and unzip it locally
2. Open the unzipped folder`finalproject` in the command line
3. Run the command `python manage.py makemigrations` to make sure all the models are created properly
4. Run the command `python manage.py migrate` to seed the database
5. Run the command `python manage.py runserver`  to run the application
6. Visit the local server at the specified port
7. You should be redirected to the home page that will have the necessary instructions on what to do
