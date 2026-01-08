def calculate_option_premium(
    spot_price: float,
    strike_price: float,
    option_type: str
):
    intrinsic = 0

    if option_type == "CE":
        intrinsic = max(spot_price - strike_price, 0)
    elif option_type == "PE":
        intrinsic = max(strike_price - spot_price, 0)

    time_value = 50  # constant approximation
    return round(intrinsic + time_value, 2)
