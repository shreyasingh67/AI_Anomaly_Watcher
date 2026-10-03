# --------------------------------------------------
# Generate business-friendly explanations
# --------------------------------------------------

def generate_explanation(metric, value, change):

    percentage = abs(change)

    # Total Sales explanation
    if metric == "total_sales_inr":

        if change > 0:
            explanation = (
                f"Total sales increased by {percentage:.1f}% "
                f"above the average. This may indicate "
                f"unusually strong sales activity for this order."
            )
        else:
            explanation = (
                f"Total sales decreased by {percentage:.1f}% "
                f"below the average. This may indicate "
                f"lower-than-usual sales value for this order."
            )

    # Profit explanation
    elif metric == "profit_inr":

        if change > 0:
            explanation = (
                f"Profit increased by {percentage:.1f}% "
                f"above the average. This order generated "
                f"an unusually high profit."
            )
        else:
            explanation = (
                f"Profit decreased by {percentage:.1f}% "
                f"below the average. This order generated "
                f"lower-than-usual profit."
            )

    # Quantity Sold explanation
    elif metric == "quantity_sold":

        if change > 0:
            explanation = (
                f"Quantity sold increased by {percentage:.1f}% "
                f"above the average. This may indicate "
                f"an unusually large order quantity."
            )
        else:
            explanation = (
                f"Quantity sold decreased by {percentage:.1f}% "
                f"below the average. This order contains "
                f"lower-than-usual quantity."
            )

    # Price explanation
    elif metric == "price_inr":

        if change > 0:
            explanation = (
                f"Product price increased by {percentage:.1f}% "
                f"above the average. This may indicate "
                f"an unusually high-priced product."
            )
        else:
            explanation = (
                f"Product price decreased by {percentage:.1f}% "
                f"below the average. This may indicate "
                f"an unusually low-priced product."
            )

    # Default explanation
    else:

        direction = (
            "increased"
            if change > 0
            else "decreased"
        )

        explanation = (
            f"{metric} {direction} by "
            f"{percentage:.1f}% compared with the average."
        )

    return explanation