<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $conn = new mysqli("localhost", "root", "", "user_registration_db");

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $name = $_POST["name"];
    $email = $_POST["email"];
    $phone = $_POST["phone"];
    $password = password_hash($_POST["password"], PASSWORD_DEFAULT);

    $sql = "INSERT INTO users (name, email, phone, password) VALUES ('$name', '$email', '$phone', '$password')";

    if ($conn->query($sql) === TRUE) {
        echo "Registration successful!";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }

    $conn->close();
}
?>
