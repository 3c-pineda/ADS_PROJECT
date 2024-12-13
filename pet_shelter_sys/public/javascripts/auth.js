function checkLoginStatusAndRedirect() {
    // Retrieve the value of 'login_status' from sessionStorage
    const loginStatus = sessionStorage.getItem('login_status');
    
    // Check if the login status is 'success'
    if (loginStatus === 'success') {
        // Redirect to the admin dashboard if logged in
    } else {
        // Redirect to the login page if not logged in
        window.location.href = '/admin/login';
    }
}
