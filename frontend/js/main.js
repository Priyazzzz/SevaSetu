// =====================================================
// SEVASETU - LANDING PAGE
// =====================================================


// Find My Schemes button

const findSchemeBtn =
    document.getElementById("findSchemeBtn");


if (findSchemeBtn) {

    findSchemeBtn.addEventListener("click", () => {

        // Registration page will be created next.
        window.location.href = "./register.html";

    });

}



// Login / Register button

const loginButton =
    document.getElementById("loginButton");


if (loginButton) {

    loginButton.addEventListener("click", () => {

        // Registration page will be created next.
        window.location.href = "register.html";

    });

}
