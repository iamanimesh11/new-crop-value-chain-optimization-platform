$(document).ready(function () {
    // Check if the user is logged in
    var isLoggedIn = sessionStorage.getItem('isLoggedIn') === 'true';

    if (isLoggedIn) {
        // User is logged in
        var userName = sessionStorage.getItem('userName');
        console.log('ho')

        // Update the UI to show the user's name and the dropdown
        $('#userName').text(userName);
        $('#userProfileDropdown').show();
        $('#loginButton').hide();

        // Add an event listener for the logout button
        $('#logout').on('click', function () {
            // Perform logout actions if needed
            // Clear the session storage
            sessionStorage.clear();
             // Hide the dropdown and show the login button
            $('#userProfileDropdown').hide();
            $('#loginButton').show();
            // Redirect to the login page
            window.location.href = 'index.html';
        });
    } else {
        // User is not logged in
        $('#loginButton').show();
        $('#userProfileDropdown').hide();

        // Add an event listener for the logout button
        $('#logout').on('click', function () {
            // Clear the session storage
            sessionStorage.clear();
            // Redirect to the index page
            window.location.href = 'index.html'; // Change the URL as needed
        });
    }
    // Your other page initialization code here
});
