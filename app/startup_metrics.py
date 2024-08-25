def calculate_metrics(startup_data):
    metrics = {}
    
    # Calculate Burn Rate
    if "expenses" in startup_data and "revenue" in startup_data:
        burn_rate = startup_data["expenses"] - startup_data["revenue"]
        metrics["burn_rate"] = burn_rate
    
    # Calculate Customer Acquisition Cost (CAC)
    if "marketing_spend" in startup_data and "new_customers" in startup_data:
        cac = startup_data["marketing_spend"] / startup_data["new_customers"]
        metrics["customer_acquisition_cost"] = cac
    
    # Calculate Customer Lifetime Value (CLV)
    if "average_revenue_per_customer" in startup_data and "customer_lifespan" in startup_data:
        clv = startup_data["average_revenue_per_customer"] * startup_data["customer_lifespan"]
        metrics["customer_lifetime_value"] = clv
    
    # Calculate Startup Valuation (simple multiple of revenue)
    if "revenue" in startup_data:
        valuation = startup_data["revenue"] * 5  # Using a simple 5x multiple
        metrics["startup_valuation"] = valuation
    
    # Add more metric calculations as needed
    
    return metrics
