// =====================================================
// SEVASETU REGISTRATION
// =====================================================

const profileForm =
    document.getElementById("profileForm");


profileForm.addEventListener(
    "submit",
    async function (event) {

        // Stop normal browser form submission
        event.preventDefault();


        // Collect form data
        const formData =
            new FormData(profileForm);


        // Convert FormData into a normal JavaScript object
        const citizenProfile =
            Object.fromEntries(formData.entries());


        // Convert numeric fields from text to numbers
        if (citizenProfile.income) {
            citizenProfile.income =
                Number(citizenProfile.income);
        }

        if (citizenProfile.family_size) {
            citizenProfile.family_size =
                Number(citizenProfile.family_size);
        }

        if (citizenProfile.dependents) {
            citizenProfile.dependents =
                Number(citizenProfile.dependents);
        }


        try {

            // Send profile to Python backend
            const response =
                await fetch(
                    "http://127.0.0.1:8000/api/profile",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                citizenProfile
                            )
                    }
                );


            // Read backend response
            const result =
                await response.json();


            console.log(
                "Backend response:",
                result
            );


            if (response.ok) {

                // Store matched schemes temporarily
                sessionStorage.setItem(
                    "schemeResults",
                    JSON.stringify(
                        result.matched_schemes
                    )
                );


                // Also store profile temporarily
                sessionStorage.setItem(
                    "sevaSetuProfile",
                    JSON.stringify(
                        result.profile
                    )
                );


                // Go to recommendations page
                window.location.href =
                    "schemes.html";

            } else {

                alert(
                    "Something went wrong. Please try again."
                );
            }


        } catch (error) {

            console.error(
                "Backend connection error:",
                error
            );

            alert(
                "Could not connect to SevaSetu backend."
            );
        }
    }
);