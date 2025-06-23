from google.adk.agents import Agent
from manager.sub_agents.crm_agent.tools import (
    create_client,
    find_client,
    create_case,
    find_case
)

# Crear el agente CRM usando ADK
crm_agent = Agent(
    name="crm_agent",
    model="gemini-2.0-flash",
    description="Agente especializado en la gestión de clientes y casos legales en la base de datos.",
    instruction="""
    Eres un asistente de CRM especializado en gestión de clientes y casos legales.
    
    Puedes realizar las siguientes operaciones:
    1. Crear nuevos clientes con nombre y email
    2. Buscar clientes existentes por email
    3. Crear nuevos casos para clientes existentes
    4. Buscar casos por ID
    
    Siempre verifica que los datos requeridos estén presentes antes de ejecutar las operaciones.
    Proporciona respuestas claras y útiles sobre el resultado de cada operación.
    """,
    tools=[
        create_client,
        find_client,
        create_case,
        find_case,
    ],
)