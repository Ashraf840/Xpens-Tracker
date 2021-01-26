// console.log('register.js is working');

// fetch all the elements' id regarding username input & it's feedback
const usernameInput = document.getElementById("id_username");
const feedbackField = document.getElementById('invalid-feedback');
const usrnameLoadingSpinner = document.getElementById('loader');
const usrnameCheckMark = document.getElementById('sign');
const usrnameLoadingIndicator = document.getElementById('usrnameLoadingIndic');

// fetch all the elements' id regarding email input & it's feedback
const emailInput = document.getElementById('id_email');
const feedbackField2 = document.getElementById('invalid-feedback2');
const emailLoadingSpinner = document.getElementById('loader2');
const emailCheckMark = document.getElementById('sign2');
const emailLoadingIndicator = document.getElementById('emailLoadingIndic');

// fetch the register btn by the ID
const registerBtn = document.getElementById('send_btn');




// Username validation
usernameInput.addEventListener('keyup', (e) => {
    // console.log('User input is working!');

    // Fetch the value what the user is typing
    const userInput = e.target.value;
    // console.log(userInput);

    usernameInput.classList.remove("is-invalid");
    feedbackField.innerHTML = '';

    // display the loader & indicator
    usrnameLoadingSpinner.style.display = 'inline-block';
    usrnameCheckMark.style.display = 'none';
    usrnameLoadingIndicator.style.display = 'inline-block';
    usrnameLoadingIndicator.style.visibility = 'hidden';

    // usrnameLoadingIndicator.textContent = `Checking ${userInput}`;

    // Check of the username is not empty
    if (userInput.length > 0) {
        // Make an API-call to our server using 'fetch()'
        fetch('../../authentication/validate-username/', {
            method:"POST",
            body: JSON.stringify({ 'username':userInput, }),
        })
        .then(res => res.json())
        .then(data => {
            // console.log(data);

            if (data.username_error) {
                registerBtn.disabled = true
                registerBtn.style.background = '#58646d'
                registerBtn.style.color = '#8a8a8a'

                // if found error then hide the loader & indicator
                usrnameLoadingSpinner.style.display = 'none';
                usrnameCheckMark.style.display = 'none';
                usrnameLoadingIndicator.style.display = 'none';
                
                usernameInput.classList.add("is-invalid");      // Highlights the input field as red-squared box (Bootstrap class)
                feedbackField.innerHTML = `<p><b> ${data.username_error} </b></p>`;
            }else{
                registerBtn.disabled = false
                registerBtn.style.background = '#313c44'
                registerBtn.style.color = '#f3f3f3'

                usernameInput.classList.remove("is-invalid");
                feedbackField.innerHTML = '';

                // if found valid then display the indicator
                usrnameLoadingSpinner.style.display = 'none';
                usrnameCheckMark.style.display = 'inline-block';
                usrnameLoadingIndicator.style.display = 'inline-block';
                usrnameLoadingIndicator.style.visibility = 'visible';
            }
        });
    }else{
        // if the input is empty then hide the loader & indicator
        usrnameLoadingSpinner.style.display = 'none';
        usrnameCheckMark.style.display = 'none';
        usrnameLoadingIndicator.style.display = 'none';
    }
});





// Email validation
emailInput.addEventListener('keyup', (e) => {
    // Fetch the value what the user is typing
    const userInput = e.target.value;
    // console.log(userInput);

    // if the email error exists, it removes them everytime
    emailInput.classList.remove("is-invalid");
    feedbackField2.innerHTML = '';

    
    // display the loader & indicator
    emailLoadingSpinner.style.display = 'inline-block';
    emailCheckMark.style.display = 'none';
    emailLoadingIndicator.style.display = 'inline-block';
    emailLoadingIndicator.style.visibility = 'hidden';


    if (userInput.length > 0) {
        // Make an API-call to our server using 'fetch()'
        fetch('../../authentication/validate-email/', {
            method:"POST",
            body: JSON.stringify({ 'email':userInput, }),
        })
        .then(res => res.json())
        .then(data => {
            // console.log(data);

            if (data.email_error) {
                registerBtn.disabled = true
                registerBtn.style.background = '#58646d'
                registerBtn.style.color = '#8a8a8a'

                // if found error then hide the loader & indicator
                emailLoadingSpinner.style.display = 'none';
                emailCheckMark.style.display = 'none';
                emailLoadingIndicator.style.display = 'none';

                emailInput.classList.add("is-invalid");      // Highlights the input field as red-squared box (Bootstrap class)
                feedbackField2.innerHTML = `<p><b> ${data.email_error} </b></p>`;
            }else{
                registerBtn.disabled = false
                registerBtn.style.background = '#313c44'
                registerBtn.style.color = '#f3f3f3'
                
                // if found valid then display the indicator
                emailLoadingSpinner.style.display = 'none';
                emailCheckMark.style.display = 'inline-block';
                emailLoadingIndicator.style.display = 'inline-block';
                emailLoadingIndicator.style.visibility = 'visible';
            }
        });
    }else{
        // if the input is empty then hide the loader & indicator
        emailLoadingSpinner.style.display = 'none';
        emailCheckMark.style.display = 'none';
        emailLoadingIndicator.style.display = 'none';
    }
});