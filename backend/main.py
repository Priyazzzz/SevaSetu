
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.matcher import match_schemes

app = FastAPI(
    title="SevaSetu API",
    description="Government Scheme Discovery & Assistance Platform",
    version="1.0.0"
)


# -------------------------------------------------
# CORS
# Allows our frontend to communicate with backend
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# Citizen Profile Model
# -------------------------------------------------

class CitizenProfile(BaseModel):

    name: str
    dob: str
    gender: str

    marital_status: str | None = None
    category: str | None = None

    income: int | None = None

    education: str | None = None
    occupation: str | None = None

    state: str
    district: str | None = None

    area_type: str | None = None

    family_size: int | None = None
    dependents: int | None = None

    disability: str | None = None
    land_owner: str | None = None

    existing_schemes: str | None = None


# -------------------------------------------------
# HOME
# -------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "SevaSetu backend is running!",
        "status": "success"
    }


# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# -------------------------------------------------
# RECEIVE CITIZEN PROFILE
# -------------------------------------------------

@app.post("/api/profile")
def create_profile(profile: CitizenProfile):

    profile_data = profile.model_dump()

    print("\n==============================")
    print("NEW CITIZEN PROFILE RECEIVED")
    print("==============================")
    print(profile_data)

    matched_schemes = match_schemes(profile_data)

    print("\n==============================")
    print("SCHEME MATCHING RESULTS")
    print("==============================")

    for scheme in matched_schemes:
        print(
            scheme["scheme_name"],
            "→",
            scheme["status"]
        )

    return {
        "status": "success",
        "message": "Profile processed successfully.",
        "profile": profile_data,
        "matched_schemes": matched_schemes
    }