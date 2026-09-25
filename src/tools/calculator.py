from langchain_core.tools import tool

@tool
def calculate_imc(weight: float, height: float) -> str:
    """Calculate Body Mass Index (BMI) based on weight (kg) and height (m)."""
    try:
        imc = weight / (height ** 2)
        if imc < 18.5:
            classification = "Underweight"
        elif 18.5 <= imc < 25:
            classification = "Normal weight"
        elif 25 <= imc < 30:
            classification = "Overweight"
        else:
            classification = "Obesity"
        return f"Your BMI is {imc:.2f}, classified as: {classification}."
    except Exception as e:
        return f"Error calculating BMI: {str(e)}"