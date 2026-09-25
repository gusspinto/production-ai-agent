from langchain_core.tools import tool

@tool
def calculate_imc(weight: float, height: float) -> str:
    """Calcula o Índice de Massa Corporal (IMC) com base no peso (kg) e altura (m)."""
    try:
        imc = weight / (height ** 2)
        if imc < 18.5:
            classification = "Abaixo do peso"
        elif 18.5 <= imc < 25:
            classification = "Peso normal"
        elif 25 <= imc < 30:
            classification = "Sobrepeso"
        else:
            classification = "Obesidade"
        return f"O seu IMC é {imc:.2f}, classificado como: {classification}."
    except Exception as e:
        return f"Erro ao calcular o IMC: {str(e)}"