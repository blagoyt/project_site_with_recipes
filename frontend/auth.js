function getUser() {
    return localStorage.getItem('siteUser');
}

function isAuthenticated() {
    return !!getUser();
}

function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
    }
}

function setUser(name) {
    localStorage.setItem('siteUser', name);
}

function logout() {
    localStorage.removeItem('siteUser');
    window.location.href = 'login.html';
}

function showUserBadge() {
    const userBadge = document.getElementById('userBadge');
    if (!userBadge) return;
    const user = getUser() || 'Guest';
    userBadge.textContent = `Welcome, ${user}`;
}

document.addEventListener('DOMContentLoaded', () => {
    showUserBadge();
    const logoutLink = document.getElementById('logoutLink');
    if (logoutLink) {
        logoutLink.addEventListener('click', (event) => {
            event.preventDefault();
            logout();
        });
    }
});
