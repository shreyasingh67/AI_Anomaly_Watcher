# Generate business-friendly explanation

def generate_explanation(metric, value, change):

    direction = "above" if change > 0 else "below"

    explanation = (
        f"{metric} was {value}, "
        f"which is {abs(change):.1f}% "
        f"{direction} the average."
    )

    return explanation