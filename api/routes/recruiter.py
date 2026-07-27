from fastapi import APIRouter

router = APIRouter()


@router.get("/recruiter-report")

def recruiter_report():

    return {

        "hiring_confidence": "Medium",

        "role_fit":

        "Junior Backend Developer",

        "salary_band": "4-8 LPA",

        "final_verdict":

        "Recommended with Improvements"
    }