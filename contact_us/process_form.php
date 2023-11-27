<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST["name"];
    $email = $_POST["email"];
    $message = $_POST["message"];

    // Your email address where you want to receive emails
    $to = "animeshm27singh@gmail.com";

    // Subject of the email
    $subject = "New Form Submission";

    // Email body
    $body = "Name: $name\n";
    $body .= "Email: $email\n";
    $body .= "Message:\n$message";

    // Additional headers
    $headers = "From: $email\r\n";
    $headers .= "Reply-To: $email\r\n";

    // Send email
    if (mail($to, $subject, $body, $headers)) {
        // Email sent successfully

        // Send a confirmation email to the user
        $user_subject = "Thank you for your submission";
        $user_body = "Dear $name,\n\nThank you for submitting the form. We have received your message and will get back to you as soon as possible.\n\nBest regards,\nYour Company Name";
        mail($email, $user_subject, $user_body);

        // Redirect or display a success message
        header("Location: success.html"); // Redirect to a success page
        exit();
    } else {
        // Failed to send email
        echo "Error sending email. Please try again.";
    }
} else {
    // Invalid request
    echo "Invalid request.";
}
?>
