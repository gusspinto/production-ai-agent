from langchain_core.tools import tool


@tool
def calculate_imc(peso: float, altura: float) -> str:
  """Calculates the Body Mass Index (BMI) based on weight in kg and height in meters.
  Use this tool whenever the user wants to calculate their BMI.
  """
  imc = peso / (altura**2)
  return f"The calculated BMI is {imc:.2f}."