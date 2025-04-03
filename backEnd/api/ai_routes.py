from fastapi import APIRouter, Request, Query
from services.aiManager.ml import generate_credentials
from services.aiManager.nlp import nlp_clean_csv

router = APIRouter()


@router.post("/nlp/clean")
def clean_data():
    nlp_clean_csv('data/crawled_data.csv', 'data/cleaned_data.csv')
    return {"message": "Data cleaned successfully"}

@router.post("/ml/generate")
def generate_creds():
    creds = generate_credentials('data/cleaned_data.csv')
    return {"credentials": creds}