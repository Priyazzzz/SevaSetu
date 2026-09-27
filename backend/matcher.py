import json


def load_schemes():
    with open(
        "data/processed/schemes.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def check_pmay_u(profile, scheme):

    eligibility = scheme["eligibility"]

    reasons = []
    failed_reasons = []

    complete_fields = []
    missing_fields = []

    # -------------------------
    # Income
    # -------------------------

    income = profile.get("income")

    if income is None or income == "":
        missing_fields.append("Income")
    else:
        complete_fields.append("Income")

        if income <= eligibility["income_max"]:
            reasons.append(
                "Income falls within the scheme's income limit"
            )
        else:
            failed_reasons.append(
                "Income exceeds the scheme's income limit"
            )

    # -------------------------
    # Area
    # -------------------------

    area_type = profile.get("area_type")

    if not area_type:
        missing_fields.append("Area type")
    else:
        complete_fields.append("Area type")

        if area_type == "Urban":
            reasons.append(
                "Applicant lives in an urban area"
            )
        else:
            failed_reasons.append(
                "Applicant does not belong to an urban area"
            )

    # -------------------------
    # House ownership
    # -------------------------

    land_owner = profile.get("land_owner")

    if not land_owner:
        missing_fields.append(
            "House/property ownership"
        )
    else:
        complete_fields.append(
            "House/property ownership"
        )

        if land_owner == "No":
            reasons.append(
                "Applicant does not own a house/property"
            )
        else:
            failed_reasons.append(
                "House/property ownership condition needs verification"
            )

    # -------------------------
    # Calculate completeness
    # -------------------------

    total_fields = (
        len(complete_fields) +
        len(missing_fields)
    )

    if total_fields > 0:
        completeness = round(
            (len(complete_fields) / total_fields) * 100
        )
    else:
        completeness = 0

    # -------------------------
    # Final status
    # -------------------------

    if failed_reasons:
        status = "NOT_ELIGIBLE"
        final_reasons = failed_reasons

    elif missing_fields:
        status = "NEEDS_VERIFICATION"
        final_reasons = reasons

    else:
        status = "ELIGIBLE"
        final_reasons = reasons

    return {
        "status": status,
        "reasons": final_reasons,
        "complete_fields": complete_fields,
        "missing_fields": missing_fields,
        "completeness": completeness
    }


def check_pm_jay(profile, scheme):

    complete_fields = []
    missing_fields = []

    # Basic information available
    basic_fields = [
        "gender",
        "state",
        "district",
        "family_size"
    ]

    for field in basic_fields:

        if profile.get(field):
            complete_fields.append(field)
        else:
            missing_fields.append(field)

    # PM-JAY requires verification against
    # government beneficiary databases.
    missing_fields.append(
        "Official beneficiary database verification"
    )

    total_fields = (
        len(complete_fields) +
        len(missing_fields)
    )

    completeness = round(
        (len(complete_fields) / total_fields) * 100
    )

    return {
        "status": "NEEDS_VERIFICATION",
        "reasons": [
            "Eligibility needs verification against the official beneficiary database"
        ],
        "complete_fields": complete_fields,
        "missing_fields": missing_fields,
        "completeness": completeness
    }


def match_schemes(profile):

    schemes = load_schemes()

    results = []

    for scheme in schemes:

        if scheme["id"] == "pmay_u":

            result = check_pmay_u(
                profile,
                scheme
            )

        elif scheme["id"] == "pm_jay":

            result = check_pm_jay(
                profile,
                scheme
            )

        else:

            result = {
                "status": "NEEDS_VERIFICATION",
                "reasons": [
                    "Eligibility rules are not configured yet"
                ],
                "complete_fields": [],
                "missing_fields": [],
                "completeness": 0
            }

        results.append({
            "scheme_id": scheme["id"],
            "scheme_name": scheme["name"],
            "category": scheme["category"],
            "status": result["status"],
            "reasons": result["reasons"],
            "complete_fields": result["complete_fields"],
            "missing_fields": result["missing_fields"],
            "completeness": result["completeness"],
            "documents": scheme["documents"],
            "application_url": scheme["application_url"],
            "source_url": scheme["source_url"]
        })

    # --------------------------------
    # PRIORITY ORDER
    # Highest data completeness first
    # --------------------------------
    status_priority = {
    "ELIGIBLE": 1,
    "NEEDS_VERIFICATION": 2,
    "NOT_ELIGIBLE": 3
}
    results.sort(
    key=lambda x: (
        status_priority.get(
            x["status"],
            4
        ),
        -x["completeness"]
    )
)   
    return results