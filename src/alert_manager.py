# Manage anomaly alert
def create_alert(metric, value, change):

    alert = {
        "metric": metric,
        "value": value,
        "change_percent": round(change, 2),
        "severity": determine_severity(change)
    }

    return alert
def determine_severity(change):
    
    if abs(change) >= 100:
        return "Critical"

    elif abs(change) >= 50:
        return "High"

    elif abs(change) >= 20:
        return "Medium"

    else:
        return "Low"