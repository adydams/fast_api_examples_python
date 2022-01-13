web: uvicorn app.main:app --host=0.0.0.0 --port=${POT:-5000} 
