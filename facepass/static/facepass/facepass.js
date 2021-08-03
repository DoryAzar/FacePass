/* globals FaceDetector, faceapi */

document.addEventListener('DOMContentLoaded', function () {

    // /* 
    // * Runtime application that exhibits the different features of the framework
    // * author: Dory Azar
    // */

    const detectorApp  = document.querySelector("#detection").dataset.app || null;
    run('detection', detectorApp);

});


/* 
* Asynchronous runtime that loads all the example adds
* @mediaId: the video or image ID that face recognition and detection will be anaylzing
* @detectorApp: app dataset element that will tell the view to trigger a the recognize app
*/
async function run(mediaId, detectorApp = null) {

    // Initialize the Face Detection framework with a video input to illustrate the webcam features
    let detector =  new FaceDetector(mediaId);

    if (detector) {
        
        if (detectorApp === "recognize") {
            
            await detector.loadApp({
                id: "2",
                name: "Identify",
                custom: true,
                method: recognize,
                options: {
                    detection: true
                }
            });

        } else {
            // Create a custom app that will capture a model to recognize on the fly
            await detector.loadApp({
                id: "1",
                name: "Get Started",
                custom: true,
                method: findMe,
                options: {
                }

            });
        }
    }
}

/* 
* FacePass recognition app
* @facedetector: defines the face detection object itself
*
*/
async function recognize(facedetector) {
    
    let identifyButton = document.querySelector("#app2") || null;
    identifyButton.innerHTML = "Identify";

    // initialize the session memory that will hold the labels and images detected
    let memory = {
        labels: [],
        images: [],
        sampleSize: 3
    };

    // clear the display and build the last action to start detection
    facedetector.clearDisplay();

    facedetector.display("FacePass loading...", 'status');

    // Get the token
    const token  = document.querySelector("#detection").dataset.token || null;

    // create a new app configuration object that will run the recognition app with the loaded model
    let app = {
        name: 'Recognize',
        method: facedetector.recognize,
        options: {
            welcome: "FacePass detecting...",
            recognition: true
        },
        algorithm: faceapi.SsdMobilenetv1Options
    };

    //update the database
    facePassApi("api/identify", 'POST', {
        "token": token
    })
    .then(async (result) => {
        
        memory = {
            labels: result.labels,
            images: result.images,
            sampleSize: 3
        };
        
        //loop through the images to parse their content
        memory.images.forEach((v,k)=> {
                memory.images[k] = JSON.parse(v);
        });
        
        if (!Array.isArray(memory.images) || !memory.images.length)  {
            throw "There are no users with pictures in the system";
        }

        app.options.recognitionModel = await facedetector.loadRecognition(memory); 

        (facedetector.detectFaces(app, facedetector))();
        let runningEvent = facedetector.detect((recognitions, facedetector) => { 

            if (recognitions.length > 0 && recognitions[0].label) {

                clearInterval(runningEvent);
                clearInterval(facedetector.runningEvent);

                // Remove canva
                const canva = document.querySelector("#detectfaces") || null;
                if (canva) {
                    canva.parentNode.removeChild(canva);
                }

                // Get the detected person info
                let recognized = {};
                recognized.label = recognitions[0].label ||  null;
                recognized.key = memory.labels.findIndex(label => label === recognized.label);

                // Display the detection
                facedetector.clearDisplay();

                // If recognized
                if (recognized.label && recognized.label !== 'unknown') {
                    // Proceed with Pass checking
                    checkPass(recognized, result, facedetector);
                    
                } else {
                    facedetector.display("We were not able to recognize you", 'status');
                    identifyButton.innerHTML = "Retry";
                }
            }
        }, true);

    })
    .catch(error => {
        facedetector.display(error, 'status');
        console.log(`Access ${error}`);
        return false;
    });

}


/* 
* Creates a FacePass
* @recognized: the recognized object {key, id}
* @result: the result from the fetch from the server
* @facedetector: defines the face detection object itself
*
*/
function checkPass(recognized, result, facedetector) {

    // Remove Identify button
    const identifyButton = document.querySelector("#app2") || null;
    if (identifyButton) {
        identifyButton.parentNode.removeChild(identifyButton);
    }
    
    // Fetch the needed info
    const userId = recognized.label;
    const userKey = recognized.key;
    const companyId = result.company_id;
    const companyName = result.company_name;
    const userPasses = result.passes[userKey] || null;

    // Detected message
    facedetector.display(`Hi ${result.usernames[userKey]}!`, 'status');

    // Stop the video and repurpose the app button
    facedetector.stopStream();
    facedetector.media.style.display = "none";

    // Change the message if previous pass made with same company
    if (!userPasses || !userPasses.length) {
        facedetector.display(`${companyName} requires the following information from you`, 'companyinfo');
    } else  {
        facedetector.display(`You have connected with ${companyName} before. It now requires the following information`, 'companyinfo');
    }

    // Add all the requested information
    const referenceElement = document.querySelector(".controls");
    result.requested_information.forEach((information, k) => {
        let pElement = document.createElement("p");
        pElement.id = `information${k}`;
        pElement.innerHTML = `${information.field}`;
        referenceElement.parentNode.insertBefore(pElement, referenceElement);
    });

    // Add question statement
    const statementElement = document.createElement("p");
    statementElement.id = `question`;
    statementElement.innerHTML = "Would you like to allow access to the above information?";
    referenceElement.parentNode.insertBefore(statementElement, referenceElement);

    // Add yes, no buttons
    const appElement = document.querySelector("#apps");
    const answers = ["Yes", "No"];
    answers.forEach(answer => {
        let answerButton = document.createElement("button");
        answerButton.id = answer.toLowerCase();
        answerButton.innerHTML = answer;
        answerButton.addEventListener('click', () => {
                    resolvePass(companyId, userId, userPasses, answer);
        });
        appElement.appendChild(answerButton);
    });
    
}

/* 
* Function that adds or removes a pass to control permissions
* @companyId: the id of the company
* @userId: the id of the detected user
* @answer: allow or disallow
*
*/
function resolvePass(companyId, userId, userPasses, answer) {

    // Evaluate parameters
    const resolveAnswer = answer.toLowerCase() === 'yes';
    
    // take the most recent pass connecting user and company
    const passId = userPasses[0]? userPasses[0].id || "" : "";

    facePassApi("api/pass",'PUT', {
        "allow": resolveAnswer,
        "user_id": userId,
        "company_id": companyId,
        "pass_id": passId
    })
    .then(result => {
        console.log(result);
        if (result.allow) {
            window.location.href = result.redirect_url ? result.redirect_url
             : `pass/${userId}?token=${result.token}`;
        } else {
            window.location.href = result.redirect_url ? result.redirect_url
            : `pass/${userId}?token=${result.token}`;
        }
    })
    .catch(error => console.log(error));

}

/* 
* Custom app that onboards a new face and detects it on the fly
* @facedetector: defines the face detection object itself
*
*/
async function findMe(facedetector) {

    let args = facedetector.app || null;

    // initialize the session memory that will hold the labels and images detected
    let memory = {
        labels: [],
        images: [],
        sampleSize: 3
    };
    let images = [];


    // A sequential form is built as a promise
    try {

        // Change the name of the app button
        const appButton = document.querySelector(`#app${args.id}`);
        if (appButton)  {
            appButton.innerHTML = "Restart";
        }
        

        // build the form to capture the firstname. It will return a promise 
        await buildForm({
            buttonName: 'captureName',
            callback: capture,
            htmltext: "Pick a name for testing purposes<input type='text' id='firstname' name='firstname'><button type='submit' id='captureName'>Submit</button>",
            memory: memory
        }, facedetector);

        // build the form that will take 6 face captures of the person to onboard
        for (let i = 0; i < memory.sampleSize; i++) {

            // Clear the canva after a delay to give feedback to the user about the image captured
            setTimeout(() => args.canvas.getContext('2d').clearRect(0, 0, args.canvas.width, args.canvas.height), 1000);

            images[i] = await buildForm({
                buttonName: 'captureImage',
                callback: capture,
                htmltext: `We need to capture ${memory.sampleSize} pics of you. Let's do capture ${i+1}.<button type='submit' id='captureImage'>Capture</button>`,
                memory: memory,
                canvas: args.canvas
            }, facedetector);

        }

    } catch (error) {
        console.log(error);
    }

    // clear the display and build the last action to start detection
    facedetector.clearDisplay();

    facedetector.display("Hold tight...As soon as it's ready, you will be able to test it", 'status');

    // Clear the canva
    args.canvas.getContext('2d').clearRect(0, 0, args.canvas.width, args.canvas.height);


    // create a new app configuration object that will run the recognition app with the loaded model
    let app = {
        name: 'Recognize',
        method: facedetector.recognize,
        options: {
            welcome: "All set! We can now recognize you",
            recognition: true
        },
        algorithm: faceapi.SsdMobilenetv1Options
    };

    try {
        app.options.recognitionModel = await facedetector.loadRecognition(memory); 
    } catch(error) {
        console.log(error);
    }

    //update the database
    facePassApi("onboard", 'PUT', {
        "images": images 
    })
    .then(result => {
        facedetector.display("Are you ready to test?<button type='submit' id='findMe'>Recognize me</button>", 'status');

        const buttonName = document.querySelector('#findMe');
    
        // run the detection that will run the defined app
        buttonName.addEventListener('click', () => {
            (facedetector.detectFaces(app, facedetector))();
            facedetector.display("If you see a red rectangle around your face, you are good to go", 'information');
            facedetector.display("To see FacePass in action, <a href='testcompany'>check out the test company</a>");

        });

    })
    .catch(error => console.log(`Update ${error}`));

}

/* 
* Utility method that builds a form and returns a promise when a value is returned from the event handler
* @formArgs: object definition of the form to be built
* @facedetector: defines the face detection object itself
*
*/
function buildForm(formArgs, facedetector) {
    // return a promise that will resolve upon the completion of the event handler
    return new Promise((resolve, reject) => {

        // prepare the innerHTML of the form elements
        facedetector.clearDisplay();
        facedetector.display(formArgs.htmltext, 'status');

        // fetch the button element from the document
        const buttonName = document.querySelector(`#${formArgs.buttonName}`);
        if (buttonName) {
            // add the handler that is defined in the args
            buttonName.addEventListener('click', e => {
                resolve(formArgs.callback(e, formArgs, facedetector));
            });
        } else {
            reject(console.log('error'));
        }
    });

}


/* 
* Utility method that handles the events defined in the buildForm
* @e: the event
* @formArgs: defines the form configuration that is also used in buildForm
* @facedetector: defines the face detection object itself
*
*/
async function capture(e, formArgs, facedetector) {
    switch (formArgs.buttonName) {

        // When it is the capture name form
        case 'captureName':
            let firstname = document.querySelector('#firstname').value || null;

            // The name is optional, set to Anonymous in case not specified
            firstname = firstname ? firstname : 'Anonymous';

            // When there is a firstname entered save it in our object
            if (formArgs.memory && firstname) {
                formArgs.memory.labels.push(firstname);
                return firstname;
            }
            break;

            // When it is the capture images forms
        case 'captureImage':

            // capture the image in the canva
            let image = facedetector.fetchImage(formArgs.canvas, facedetector.media);

            if (formArgs.memory && image) {

                // save the image blob to the object
                formArgs.memory.images.push(image);

                return image;
            }
            break;
        default:

    }
}


/*
* Generic facePass api function
*/

function facePassApi(url, method = 'GET', data = null, authorization = null) {
    return new Promise((resolve, reject) => {

        // fetch the csrf token from the view
        let csrftoken = document.querySelector("[name=csrfmiddlewaretoken");
        csrftoken = csrftoken? csrftoken.value : null;
        method = method.toUpperCase() ||  'GET';
    
        // Prepare headers
        let headers = {};
        headers["X-CSRFToken"] = csrftoken;


        // prepare request
        let request = {};
        request.method = method;
        request.headers = headers;
        if (method ===  'POST' || method === 'PUT' ) {
            request.body = JSON.stringify(data);
        }
        
        // if authorization
        if (authorization) {
            headers.Authorization = `Bearer: ${authorization}`;
            request.WithCredentials = true;
            request.credentials = 'include';
        }
    
        fetch(url, request)                
        .then((response) => response.json())
        .then((result) => {

            // result return error throw exception to catch
            if (result.error)  {
                throw new Error(result.error);
            }
    
            else {
                // If no errors, render post
                resolve(result);
            }
        })
        .catch(error => {
            reject(error);
        });
    });
}