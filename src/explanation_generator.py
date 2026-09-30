# --------------------------------------------------
# Generate business-friendly explanations
# --------------------------------------------------

def generate_explanation(metric, value, change):

    direction = "increased" if change > 0 else "decreased"

    percentage = abs(change)

    # Revenue explanation
    if metric == "Revenue":

        if change > 0:
            explanation = (
                f"Revenue increased by {percentage:.1f}% "
                f"above the average. This may indicate "
                f"unusually strong sales activity."
            )
        else:
            explanation = (
                f"Revenue decreased by {percentage:.1f}% "
                f"below the average. This may indicate "
                f"lower-than-usual sales activity."
            )

    # Conversion Rate explanation
    elif metric == "Conversion_Rate":

        if change < 0:
            explanation = (
                f"Conversion rate decreased by {percentage:.1f}% "
                f"below the average. Traffic may not be converting "
                f"into orders effectively."
            )
        else:
            explanation = (
                f"Conversion rate increased by {percentage:.1f}% "
                f"above the average. Customer conversion "
                f"performance is unusually high."
            )

    # Traffic explanation
    elif metric == "Traffic":

        if change > 0:
            explanation = (
                f"Traffic increased by {percentage:.1f}% "
                f"above the average. There may be an unusual "
                f"increase in website visitors."
            )
        else:
            explanation = (
                f"Traffic decreased by {percentage:.1f}% "
                f"below the average. Website visits are "
                f"lower than usual."
            )

    # Cost explanation
    elif metric == "Cost":

        if change > 0:
            explanation = (
                f"Cost increased by {percentage:.1f}% "
                f"above the average. Operational or marketing "
                f"expenses may require investigation."
            )
        else:
            explanation = (
                f"Cost decreased by {percentage:.1f}% "
                f"below the average."
            )

    # Refund explanation
    elif metric == "Refunds":

        if change > 0:
            explanation = (
                f"Refunds increased by {percentage:.1f}% "
                f"above the average. This may indicate "
                f"an unusual increase in returned orders."
            )
        else:
            explanation = (
                f"Refunds decreased by {percentage:.1f}% "
                f"below the average."
            )

    # Orders explanation
    elif metric == "Orders":

        explanation = (
            f"Orders {direction} by {percentage:.1f}% "
            f"compared with the average."
        )

    # Default explanation
    else:

        explanation = (
            f"{metric} {direction} by "
            f"{percentage:.1f}% compared with the average."
        )

    return explanation