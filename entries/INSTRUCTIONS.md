<br>

#### What is FacePass
FacePass is a service that allows people to own their personal information and to have full control over what information they want to share with other online services - as opposed to the other way around. Through FacePass, people can authenticate to any affiliated online service through face recognition and can decide what piece of information they want to share and make available to the service.

[Watch the demo](https://youtu.be/B52id0zRDA8)

<br>
<hr>

#### How to use the service
Given the scope of the project, we implemented the key features of FacePass to be able to present a typical flow for an end-user trying to connect to an affiliated company. We identified 2 user flows to help you explore the power of FacePass

<br>

##### User Flow 1: Creating a FacePass account
In this use case, you  are looking to create an acccount and to train FacePass to recognize you.

1. **[Create an account](register)**

    Upon creation, you will be redirected to see all the active passes. Those represent authorizations that you have given affiliated companies. Initially, you won't have any.

2. **[Set up FaceId](onboard)**
    
    Before using FacePass with affiliated companies, you need to train FacePass to recognize your face.

3. **[Complete your personal information](personalinformation)**

    A big advantage of using FacePass is to centralize all your personal information in one place and to provide punctual access to them to affiliated companies. 

**You are all set and you can now start using FacePass**

<br />

##### User Flow 2: Using FacePass to connect with  affiliated companies
We populated the database with some companies to illustrate how FacePass is used to identify end-users and to empower them to control what information to share with the company they are connecting to.

1. **[Pick a random company](testcompany)**

    Every time you visit the Test Company page, a random company is offered to you as an example. You will notice a FacePass button. That is how the whole experience starts.

    **The identification flow consists of 2 steps:**

    + **Face Identification**

        In this phase, you will be asked to show your face in the camera for recognition. If you are a registered FacePass user (if you completed use case 1), then the system will be able to recognize you. Otherwise, it will inform you.

    + **Permission Control**

        Once the system recognizes you, it will tell you what information the company needs from you. At this point, you can choose to allow or deny access to the information.

        If you allow access, only the information that the company asked for will be available for its use. We created a page to illustrate that.

        If you don't allow access, no information will be shared at all.

    **For Fun**

    The system doesn't make a difference between a real face and a picture of a face. We populated the database with some famous celebrities face signatures. Here are some that you can try by pointing their picture in your phone to your computer camera:

    + Steve Jobs
    + Michael Jordan
    + Lisa Minelli
    + Lucy Lu
    + Aziz Ansari
    + Caitlyn Jenner
    
    
    <br>

2. **[View all passes](passes)**

    Connect to your FacePass account to view the pass (as well as all passes) of the companies that you authorized. The companies that you did not authorize will not be displayed.



<br>

