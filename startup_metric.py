# Calculate Overall Market Size
def calculate_market_size(consumer_payment, market_size, market_share_in_3_years):
    """
    Calculate the overall market size based on user inputs.

    Parameters:
    consumer_payment (float): The amount consumers are currently paying annually.
    market_size (float): The total market size.
    market_share_in_3_years (float): The projected market share in 3 years.

    Returns:
    float: The calculated market size.
    """
    market_size_value = consumer_payment * market_size * (market_share_in_3_years / 100)
    return market_size_value

# Calculate Total Available Market
def calculate_tam(market_size):
    """
    Calculate the Total Available Market (TAM).

    Parameters:
    market_size (float): The total market size in units.

    Returns:
    float: The TAM value.
    """
    tam = market_size
    return tam

# Calculate Segmented Available Market
def calculate_sam(tam, target_segment_percentage):
    """
    Calculate the Segmented Available Market (SAM).

    Parameters:
    tam (float): The Total Available Market.
    target_segment_percentage (float): The percentage of the TAM that is the target market.

    Returns:
    float: The SAM value.
    """
    sam = tam * (target_segment_percentage / 100)
    return sam

# Calculate Segmented Obtainable Market
def calculate_som(sam, projected_market_share):
    """
    Calculate the Segmented Obtainable Market (SOM).

    Parameters:
    sam (float): The Segmented Available Market.
    projected_market_share (float): The percentage of the SAM that you can realistically capture.

    Returns:
    float: The SOM value.
    """
    som = sam * (projected_market_share / 100)
    return som


# Calculate the Customer Lifetime Value (CLTV)
def calculate_cltv(average_revenue_per_user, customer_lifetime, profit_margin, customer_acquisition_cost):
    """
    Calculate the Customer Lifetime Value (CLTV).

    Parameters:
    average_revenue_per_user (float): Average revenue generated per user.
    customer_lifetime (float): The average lifetime of a customer in years.
    profit_margin (float): Profit margin as a percentage.
    customer_acquisition_cost (float): Cost to acquire a customer.

    Returns:
    float: The CLTV value.
    """
    cltv = (average_revenue_per_user * customer_lifetime * (profit_margin / 100)) - customer_acquisition_cost
    return cltv

# Calculate Revenue Projection
def calculate_revenue_projection(som, average_revenue_per_user):
    """
    Calculate projected revenue.

    Parameters:
    som (float): The Segmented Obtainable Market.
    average_revenue_per_user (float): The average revenue generated per user.

    Returns:
    float: The projected revenue.
    """
    projected_revenue = som * average_revenue_per_user
    return projected_revenue

# Calculate Customer Acquisition Cost
def calculate_cac(total_sales_and_marketing_costs, number_of_customers_acquired):
    """
    Calculate the Customer Acquisition Cost (CAC).

    Parameters:
    total_sales_and_marketing_costs (float): Total spent on sales and marketing.
    number_of_customers_acquired (int): Number of customers acquired.

    Returns:
    float: The CAC value.
    """
    cac = total_sales_and_marketing_costs / number_of_customers_acquired
    return cac


# Calculate Month-over-Month Growth
def calculate_mom_growth(current_month_value, previous_month_value):
    """
    Calculate Month-over-Month (MoM) growth.

    Parameters:
    current_month_value (float): The value of the metric for the current month.
    previous_month_value (float): The value of the metric for the previous month.

    Returns:
    float: The MoM growth rate as a percentage.
    """
    if previous_month_value == 0:
        return None  # Avoid division by zero
    mom_growth = ((current_month_value - previous_month_value) / previous_month_value) * 100
    return mom_growth

# Calculate Year-over-Year Growth
def calculate_yoy_growth(current_year_value, previous_year_value):
    """
    Calculate Year-over-Year (YoY) growth.

    Parameters:
    current_year_value (float): The value of the metric for the current year.
    previous_year_value (float): The value of the metric for the previous year.

    Returns:
    float: The YoY growth rate as a percentage.
    """
    if previous_year_value == 0:
        return None  # Avoid division by zero
    yoy_growth = ((current_year_value - previous_year_value) / previous_year_value) * 100
    return yoy_growth

# Calculate Total Revenue
def calculate_total_revenue(sales_data):
    """
    Calculate the total revenue.

    Parameters:
    sales_data (list of float): A list of revenue figures over a specific period.

    Returns:
    float: The total revenue.
    """
    return sum(sales_data)

# Calculate Average Revenue Per User (ARPU)
def calculate_arpu(total_revenue, num_customers):
    """
    Calculate the Average Revenue Per User (ARPU).

    Parameters:
    total_revenue (float): The total revenue generated.
    num_customers (int): The number of customers.

    Returns:
    float: The ARPU value.
    """
    return total_revenue / num_customers

# Calculate Revenue Growth Rate
def calculate_revenue_growth_rate(current_period_revenue, previous_period_revenue):
    """
    Calculate the Revenue Growth Rate.

    Parameters:
    current_period_revenue (float): The revenue in the current period.
    previous_period_revenue (float): The revenue in the previous period.

    Returns:
    float: The revenue growth rate as a percentage.
    """
    return ((current_period_revenue - previous_period_revenue) / previous_period_revenue) * 100

# Calculate Gross Profit
def calculate_gross_profit(total_revenue, cogs):
    """
    Calculate Gross Profit.

    Parameters:
    total_revenue (float): The total revenue generated.
    cogs (float): Cost of Goods Sold (COGS).

    Returns:
    float: The gross profit.
    """
    return total_revenue - cogs

# Calculate Gross Margin
def calculate_gross_margin(gross_profit, total_revenue):
    """
    Calculate Gross Margin.

    Parameters:
    gross_profit (float): The gross profit.
    total_revenue (float): The total revenue generated.

    Returns:
    float: The gross margin as a percentage.
    """
    return (gross_profit / total_revenue) * 100

# Calculate Net Profit
def calculate_net_profit(gross_profit, total_expenses):
    """
    Calculate Net Profit.

    Parameters:
    gross_profit (float): The gross profit.
    total_expenses (float): Total operating expenses.

    Returns:
    float: The net profit.
    """
    return gross_profit - total_expenses

# Calculate Net Profit Margin
def calculate_net_profit_margin(net_profit, total_revenue):
    """
    Calculate Net Profit Margin.

    Parameters:
    net_profit (float): The net profit.
    total_revenue (float): The total revenue generated.

    Returns:
    float: The net profit margin as a percentage.
    """
    return (net_profit / total_revenue) * 100

# Calculate Sales Conversion Rate
def calculate_sales_conversion_rate(num_sales, num_leads):
    """
    Calculate the Sales Conversion Rate.

    Parameters:
    num_sales (int): The number of successful sales.
    num_leads (int): The number of leads generated.

    Returns:
    float: The sales conversion rate as a percentage.
    """
    return (num_sales / num_leads) * 100

# Calculate Customer Lifetime Value (CLTV)
def calculate_cltv(avg_purchase_value, purchase_frequency, customer_lifespan):
    """
    Calculate Customer Lifetime Value (CLTV).

    Parameters:
    avg_purchase_value (float): The average purchase value.
    purchase_frequency (float): The frequency of purchases.
    customer_lifespan (float): The lifespan of a customer in years.

    Returns:
    float: The CLTV value.
    """
    return avg_purchase_value * purchase_frequency * customer_lifespan

# Calculate Customer Acquisition Cost (CAC)
def calculate_cac(total_sales_marketing_cost, num_new_customers):
    """
    Calculate Customer Acquisition Cost (CAC).

    Parameters:
    total_sales_marketing_cost (float): The total cost of sales and marketing.
    num_new_customers (int): The number of new customers acquired.

    Returns:
    float: The CAC value.
    """
    return total_sales_marketing_cost / num_new_customers

# Calculate CAC to LTV Ratio
def calculate_cac_to_ltv_ratio(cltv, cac):
    """
    Calculate CAC to LTV Ratio.

    Parameters:
    cltv (float): The Customer Lifetime Value.
    cac (float): The Customer Acquisition Cost.

    Returns:
    float: The CAC to LTV ratio.
    """
    return cltv / cac

# Calculate Customer Churn Rate
def calculate_churn_rate(num_customers_lost, total_num_customers):
    """
    Calculate Customer Churn Rate.

    Parameters:
    num_customers_lost (int): The number of customers lost in a period.
    total_num_customers (int): The total number of customers at the start of the period.

    Returns:
    float: The customer churn rate as a percentage.
    """
    return (num_customers_lost / total_num_customers) * 100

# Calculate Customer Retention Rate
def calculate_retention_rate(churn_rate):
    """
    Calculate Customer Retention Rate.

    Parameters:
    churn_rate (float): The customer churn rate.

    Returns:
    float: The customer retention rate as a percentage.
    """
    return 100 - churn_rate

# Calculate Gross Profit
def calculate_gross_profit(revenue, cogs):
    """
    Calculate the Gross Profit.

    Parameters:
    revenue (float): Total revenue generated by the company.
    cogs (float): Cost of Goods Sold.

    Returns:
    float: The Gross Profit value.
    """
    gross_profit = revenue - cogs
    return gross_profit

# Calculate Operating Income (EBIT)
def calculate_ebit(gross_profit, operating_expenses):
    """
    Calculate the Operating Income (EBIT).

    Parameters:
    gross_profit (float): Gross Profit value.
    operating_expenses (float): Total operating expenses.

    Returns:
    float: The EBIT value.
    """
    ebit = gross_profit - operating_expenses
    return ebit

# Calculate EBITDA
def calculate_ebitda(ebit, depreciation, amortization):
    """
    Calculate Earnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA).

    Parameters:
    ebit (float): Earnings Before Interest and Taxes.
    depreciation (float): Depreciation expense.
    amortization (float): Amortization expense.

    Returns:
    float: The EBITDA value.
    """
    ebitda = ebit + depreciation + amortization
    return ebitda

# Calculate Net Income
def calculate_net_income(revenue, cogs, operating_expenses, interest, taxes):
    """
    Calculate the Net Income.

    Parameters:
    revenue (float): Total revenue generated by the company.
    cogs (float): Cost of Goods Sold.
    operating_expenses (float): Total operating expenses.
    interest (float): Interest expense.
    taxes (float): Taxes expense.

    Returns:
    float: The Net Income value.
    """
    net_income = revenue - cogs - operating_expenses - interest - taxes
    return net_income

# Calculate Operating Cash Flow (OCF)
def calculate_ocf(net_income, depreciation, amortization, change_in_working_capital):
    """
    Calculate the Operating Cash Flow (OCF).

    Parameters:
    net_income (float): Net income value.
    depreciation (float): Depreciation expense.
    amortization (float): Amortization expense.
    change_in_working_capital (float): Change in working capital.

    Returns:
    float: The OCF value.
    """
    ocf = net_income + depreciation + amortization + change_in_working_capital
    return ocf

# Calculate Free Cash Flow (FCF)
def calculate_fcf(ocf, capital_expenditures):
    """
    Calculate the Free Cash Flow (FCF).

    Parameters:
    ocf (float): Operating Cash Flow.
    capital_expenditures (float): Capital Expenditures.

    Returns:
    float: The FCF value.
    """
    fcf = ocf - capital_expenditures
    return fcf

# Calculate Total Assets
def calculate_total_assets(current_assets, non_current_assets):
    """
    Calculate Total Assets.

    Parameters:
    current_assets (float): Total current assets.
    non_current_assets (float): Total non-current assets.

    Returns:
    float: The Total Assets value.
    """
    total_assets = current_assets + non_current_assets
    return total_assets

# Calculate Total Liabilities
def calculate_total_liabilities(current_liabilities, non_current_liabilities):
    """
    Calculate Total Liabilities.

    Parameters:
    current_liabilities (float): Total current liabilities.
    non_current_liabilities (float): Total non-current liabilities.

    Returns:
    float: The Total Liabilities value.
    """
    total_liabilities = current_liabilities + non_current_liabilities
    return total_liabilities

# Calculate Shareholder's Equity
def calculate_shareholders_equity(total_assets, total_liabilities):
    """
    Calculate Shareholder's Equity.

    Parameters:
    total_assets (float): Total assets.
    total_liabilities (float): Total liabilities.

    Returns:
    float: The Shareholder's Equity value.
    """
    equity = total_assets - total_liabilities
    return equity

# Calculate Net Working Capital
def calculate_net_working_capital(current_assets, current_liabilities):
    """
    Calculate Net Working Capital.

    Parameters:
    current_assets (float): Total current assets.
    current_liabilities (float): Total current liabilities.

    Returns:
    float: The Net Working Capital value.
    """
    net_working_capital = current_assets - current_liabilities
    return net_working_capital

# Calculate Current Ratio
def calculate_current_ratio(current_assets, current_liabilities):
    """
    Calculate the Current Ratio.

    Parameters:
    current_assets (float): Total current assets.
    current_liabilities (float): Total current liabilities.

    Returns:
    float: The Current Ratio value.
    """
    if current_liabilities == 0:
        return None  # Avoid division by zero
    current_ratio = current_assets / current_liabilities
    return current_ratio

# Calculate Quick Ratio
def calculate_quick_ratio(current_assets, inventory, current_liabilities):
    """
    Calculate the Quick Ratio.

    Parameters:
    current_assets (float): Total current assets.
    inventory (float): Total inventory.
    current_liabilities (float): Total current liabilities.

    Returns:
    float: The Quick Ratio value.
    """
    if current_liabilities == 0:
        return None  # Avoid division by zero
    quick_ratio = (current_assets - inventory) / current_liabilities
    return quick_ratio

# Calculate Gross Margin
def calculate_gross_margin(gross_profit, revenue):
    """
    Calculate the Gross Margin.

    Parameters:
    gross_profit (float): Gross Profit value.
    revenue (float): Total revenue generated by the company.

    Returns:
    float: The Gross Margin percentage.
    """
    if revenue == 0:
        return None  # Avoid division by zero
    gross_margin = (gross_profit / revenue) * 100
    return gross_margin

# Calculate Operating Margin
def calculate_operating_margin(ebit, revenue):
    """
    Calculate the Operating Margin.

    Parameters:
    ebit (float): Earnings Before Interest and Taxes (EBIT).
    revenue (float): Total revenue generated by the company.

    Returns:
    float: The Operating Margin percentage.
    """
    if revenue == 0:
        return None  # Avoid division by zero
    operating_margin = (ebit / revenue) * 100
    return operating_margin

# Calculate Net Profit Margin
def calculate_net_profit_margin(net_income, revenue):
    """
    Calculate the Net Profit Margin.

    Parameters:
    net_income (float): Net Income value.
    revenue (float): Total revenue generated by the company.

    Returns:
    float: The Net Profit Margin percentage.
    """
    if revenue == 0:
        return None  # Avoid division by zero
    net_profit_margin = (net_income / revenue) * 100
    return net_profit_margin

# Calculate Debt-to-Equity Ratio
def calculate_debt_to_equity_ratio(total_liabilities, shareholders_equity):
    """
    Calculate the Debt-to-Equity Ratio.

    Parameters:
    total_liabilities (float): Total liabilities.
    shareholders_equity (float): Shareholder's equity.

    Returns:
    float: The Debt-to-Equity Ratio value.
    """
    if shareholders_equity == 0:
        return None  # Avoid division by zero
    debt_to_equity_ratio = total_liabilities / shareholders_equity
    return debt_to_equity_ratio

# Calculate Interest Coverage Ratio
def calculate_interest_coverage_ratio(ebit, interest_expense):
    """
    Calculate the Interest Coverage Ratio.

    Parameters:
    ebit (float): Earnings Before Interest and Taxes (EBIT).
    interest_expense (float): Interest expense.

    Returns:
    float: The Interest Coverage Ratio value.
    """
    if interest_expense == 0:
        return None  # Avoid division by zero
    interest_coverage_ratio = ebit / interest_expense
    return interest_coverage_ratio

# Calculate Asset Turnover Ratio
def calculate_asset_turnover_ratio(revenue, total_assets):
    """
    Calculate the Asset Turnover Ratio.

    Parameters:
    revenue (float): Total revenue generated by the company.
    total_assets (float): Total assets.

    Returns:
    float: The Asset Turnover Ratio value.
    """
    if total_assets == 0:
        return None  # Avoid division by zero
    asset_turnover_ratio = revenue / total_assets
    return asset_turnover_ratio

# Calculate Inventory Turnover
def calculate_inventory_turnover(cogs, average_inventory):
    """
    Calculate the Inventory Turnover.

    Parameters:
    cogs (float): Cost of Goods Sold.
    average_inventory (float): Average inventory value.

    Returns:
    float: The Inventory Turnover value.
    """
    if average_inventory == 0:
        return None  # Avoid division by zero
    inventory_turnover = cogs / average_inventory
    return inventory_turnover

# Calculate Earnings Per Share (EPS)
def calculate_eps(net_income, dividends_preferred_stock, outstanding_shares):
    """
    Calculate Earnings Per Share (EPS).

    Parameters:
    net_income (float): Net Income value.
    dividends_preferred_stock (float): Dividends paid on preferred stock.
    outstanding_shares (int): Number of outstanding shares.

    Returns:
    float: The EPS value.
    """
    if outstanding_shares == 0:
        return None  # Avoid division by zero
    eps = (net_income - dividends_preferred_stock) / outstanding_shares
    return eps

# Calculate Return on Equity (ROE)
def calculate_roe(net_income, shareholders_equity):
    """
    Calculate Return on Equity (ROE).

    Parameters:
    net_income (float): Net Income value.
    shareholders_equity (float): Shareholder's equity.

    Returns:
    float: The ROE percentage.
    """
    if shareholders_equity == 0:
        return None  # Avoid division by zero
    roe = (net_income / shareholders_equity) * 100
    return roe

# Calculate Return on Assets (ROA)
def calculate_roa(net_income, total_assets):
    """
    Calculate Return on Assets (ROA).

    Parameters:
    net_income (float): Net Income value.
    total_assets (float): Total assets.

    Returns:
    float: The ROA percentage.
    """
    if total_assets == 0:
        return None  # Avoid division by zero
    roa = (net_income / total_assets) * 100
    return roa
