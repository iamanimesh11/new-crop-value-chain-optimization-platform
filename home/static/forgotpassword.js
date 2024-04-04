// Function to show the Forgot Password modal
function showForgotPasswordModal() {
    $('#resetPasswordFields').hide(); // Set fields as readonly
        $('#confirmPasswordFields').hide(); // Set fields as readonly initially

    document.getElementById('resetpassbttn').disabled = true;



    $('#forgotPasswordModal').modal('show');

}


function sendforgotEmailVerification() {
     var fotp = document.getElementById("fverifyEmailOTP").value;
    var femail = document.getElementById("floginEmail").value;

    document.getElementById('resetpassbttn').disabled = true;
     if (femail === "" ) {
        // Display error message in red
        document.getElementById("fmessage").innerHTML = "<span style='color: red;'>plz enter registered Email.</span>";
        return;
    }

     // Display spinner and hide button content
    document.getElementById('fverifyButtonContent').style.display = 'none';
    document.getElementById('fverifyButtonSpinner').style.display = 'inline-block';

        // Add a message element to show the status
        var messageElement = document.getElementById('fmessage');
        messageElement.innerHTML = ''; // Clear previous messages

        // Use AJAX to send the email verification request to Flask endpoint
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5002/send-forgotpass-email-verification',
            data: { email: femail},
            success: function (response) {
                console.log(response);
                 if (response.status==='error') {
                // If the response is successful, display the success message
                 messageElement.innerHTML = '<div class="alert alert-danger" role="alert">' + response.message + '</div>';
              } else {
                // If the response indicates an error, display the error message
                messageElement.innerHTML = '<div class="alert alert-success" role="alert">OTP sent successfully!</div>';

               }
                // Hide spinner and show button content
                document.getElementById('fverifyButtonContent').style.display = 'inline-block';
                document.getElementById('fverifyButtonSpinner').style.display = 'none';

                document.getElementById('resetpassbttn').disabled = true;

                // Update the button text and click event handler
                var verifyButton = document.getElementById('fverifyButton');
                verifyButton.innerHTML = 'Verify OTP';
                verifyButton.onclick = function() {
                    fverifyfEmailOTP();
                };
            },
            error: function (error) {
                console.error(error.responseText);
                messageElement.innerHTML = '<div class="alert alert-danger" role="alert">Failed to send OTP. Please try again.</div>';
               document.getElementById('resetpassbttn').disabled = true;

            }
        });
    }

    function fverifyfEmailOTP() {
    var femail = document.getElementById("floginEmail").value;
     var fotp = document.getElementById("fverifyEmailOTP").value;

        // Add a message element to show the status
        var messageElement = document.getElementById('fmessage');
        messageElement.innerHTML = ''; // Clear previous messages

        // Use AJAX to send the OTP verification request to Flask endpoint
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5002/fverify-email-otp',
            data: { femail: femail, fcode: fotp },
            success: function (response) {
                console.log(response);
                messageElement.innerHTML = '<div class="alert alert-success" role="alert">OTP verification successful!</div>';
                isOTPVerified = true;
                document.getElementById('fverifyButton').disabled = true;
                document.getElementById('resetpassbttn').disabled = false;


                $('#resetPasswordFields').show(); // Set fields as readonly
               $('#confirmPasswordFields').show(); // Set fields as readonly initially
        },
        error: function (error) {
            console.error(error.responseText);
            messageElement.innerHTML = '<div class="alert alert-danger" role="alert">' + error.responseText + '</div>';

            document.getElementById('resetpassbttn').disabled = true;

            // Hide the password fields
            document.getElementById('resetPasswordFields').style.display = 'none';
            document.getElementById('confirmPasswordFields').style.display = 'none';
        }
    });
}

    function resetPassword() {
    // Get values from the input fields
    var newPassword = document.getElementById("newPassword").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    var messageElement = document.getElementById('fmessage');
        messageElement.innerHTML = ''; // Clear previous messages


    // Validate that both passwords match
    if (newPassword !== confirmPassword) {
        // Display an error message
        document.getElementById("fmessage").innerHTML = '<div class="alert alert-danger" role="alert">Passwords do not match. Please try again.</div>';
        return;
    }

    // Validate the strength of the password (add your own password strength validation logic if needed)
    if (newPassword.length < 8) {
        // Display an error message
        document.getElementById("fmessage").innerHTML = '<div class="alert alert-danger" role="alert">Password must be at least 8 characters long.</div>';
        return;
    }

    // If both passwords match and meet the criteria, you can proceed to update the password in your 'users' data
    // Example: Update the password in the 'users' object
    var userEmail = document.getElementById("floginEmail").value;

     $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5002/freset-password',
            data: { femail: userEmail, fpassword: confirmPassword },
            success: function (response) {
                console.log(response);
                $('#congratulationsModal').modal('show');
                messageElement.innerHTML = '<div class="alert alert-success" role="alert">Password reset success ,Now log in with new password</div>';
                // Hide the password fields
            document.getElementById('resetPasswordFields').style.display = 'none';
            document.getElementById('confirmPasswordFields').style.display = 'none';
            document.getElementById("fverifyEmailOTP").disabled = true;
            document.getElementById("floginEmail").disabled = true;
            document.getElementById('resetpassbttn').disabled = true;
            document.getElementById("fotpHelp").hide() ;
        },
        error: function (error) {
            console.error(error.responseText);
            messageElement.innerHTML = '<div class="alert alert-danger" role="alert">' + error.responseText + '</div>';

        }
    });

        // Display a success message
    }
