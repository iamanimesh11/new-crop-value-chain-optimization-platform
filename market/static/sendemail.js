
var isOTPVerified = false;

function sendEmailVerification() {
     var name = document.getElementById("registerName").value;
    var email = document.getElementById("registerEmail").value;

    document.getElementById('submitBtn').disabled = true;
     if (name === "" || email === "" ) {
        // Display error message in red
        document.getElementById("message").innerHTML = "<span style='color: red;'>Please ENTER Name ,Email.</span>";
        return;
    }

     // Display spinner and hide button content
    document.getElementById('verifyButtonContent').style.display = 'none';
    document.getElementById('verifyButtonSpinner').style.display = 'inline-block';

        // Add a message element to show the status
        var messageElement = document.getElementById('message');
        messageElement.innerHTML = ''; // Clear previous messages

        // Use AJAX to send the email verification request to Flask endpoint
        $.ajax({
            type: 'POST',
            url: '/send-email-verification',
            data: { email: email ,name: name},
            success: function (response) {
                console.log(response);
                messageElement.innerHTML = '<div class="alert alert-success" role="alert">OTP sent successfully!</div>';
                // Hide spinner and show button content
                document.getElementById('verifyButtonContent').style.display = 'inline-block';
                document.getElementById('verifyButtonSpinner').style.display = 'none';

                document.getElementById('submitBtn').disabled = true;

                // Update the button text and click event handler
                var verifyButton = document.getElementById('verifyButton');
                verifyButton.innerHTML = 'Verify OTP';
                verifyButton.onclick = function() {
                    verifyEmailOTP();
                };
            },
            error: function (error) {
                console.error(error.responseText);
                messageElement.innerHTML = '<div class="alert alert-danger" role="alert">Failed to send OTP. Please try again.</div>';
               document.getElementById('submitBtn').disabled = true;

            }
        });
    }

    function verifyEmailOTP() {
        var email = document.getElementById('registerEmail').value;
        var enteredOTP = document.getElementById('verifyEmailOTP').value;

        // Add a message element to show the status
        var messageElement = document.getElementById('message');
        messageElement.innerHTML = ''; // Clear previous messages

        // Use AJAX to send the OTP verification request to Flask endpoint
        $.ajax({
            type: 'POST',
            url: '/verify-email-otp',
            data: { email: email, code: enteredOTP },
            success: function (response) {
                console.log(response);
                messageElement.innerHTML = '<div class="alert alert-success" role="alert">OTP verification successful!</div>';
                isOTPVerified = true;
                document.getElementById('verifyButton').disabled = true;

                document.getElementById('submitBtn').disabled = false;

            },
            error: function (error) {
                console.error(error.responseText);
                messageElement.innerHTML = '<div class="alert alert-danger" role="alert">' + error.responseText + '</div>';

                   document.getElementById('submitBtn').disabled = true;

            }
        });
    }

    function submitRegisterForm() {
    // Check if all fields are filled
    var name = document.getElementById("registerName").value;
    var email = document.getElementById("registerEmail").value;
    var password = document.getElementById("registerPassword").value;

    if (name === "" || email === "" || password === "") {
        // Display error message in red
        document.getElementById("message").innerHTML = "<span style='color: red;'>Please fill all fields.</span>";
        return;
    }

    // Rest of the registration form submission logic
    // ...
    if (!isOTPVerified) {
        // Display error message for unverified OTP
        document.getElementById("message").innerHTML = "<span style='color: red;'>Please verify your email by OTP.</span>";
        return;
    }

    document.getElementById("registerForm").style.display = "none";
    // Show the "Thank you" message with a specific text color
    var successMessage = document.getElementById("registrationSuccessMessage");
    successMessage.innerHTML = "Thank you for registering! Now you can log in.";
    successMessage.style.color = "green";  // Change the color to your desired value

    document.getElementById("registrationSuccess").style.display = "block";





}

