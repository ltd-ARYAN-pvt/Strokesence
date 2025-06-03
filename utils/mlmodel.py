import random

# utils/balance_model.py
def analyze_balance(accel, gyro):
    num=random.randint(0,1)
    res="normal" if num==0 else "stroke_detected"
    bal="Good Balance" if num==0 else "Bad Balance"
    return {
        "result": res,
        "confidence_score": random.uniform(0.90,0.99),
        "model_version": "v1.0",
        "notes": bal 
    }