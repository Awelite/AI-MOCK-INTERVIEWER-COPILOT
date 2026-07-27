from fastapi import APIRouter

router = APIRouter()


@router.get("/analytics")

def get_analytics():

    return {

        "average_score": 83,

        "highest_score": 91,

        "lowest_score": 74,

        "growth_trend":

        "Stable Performance",

        "consistency":

        "Highly Consistent"
    }