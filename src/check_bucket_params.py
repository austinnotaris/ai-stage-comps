import sys
sys.path.append("../src")
from bucket_orders import *
def check_bucket_params(GB, CB, MB, RB):  
    df = {"Growth Bucket":"Valid", "Capex Bucket":"Valid", "Margin Bucket":"Valid", "Revenue Bucket":"Valid"}
    if GB not in growth_buckets:
        df["Growth Bucket"] = "Nonexistent Value"
    if CB not in capex_buckets:
        df["Capex Bucket"] = "Nonexistent Value"
    if MB not in margin_buckets:
        df["Margin Bucket"] = "Nonexistent Value"
    if RB not in revenue_buckets:
        df["Revenue Bucket"] = "Nonexistent Value"
    return df