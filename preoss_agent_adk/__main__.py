import logging
import os
import sys

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent import create_agent
from agent_executor import RealEstateLeadAgentExecutor
from dotenv import load_dotenv
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, DatabaseSessionService

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from constants import (
    REMOTE_2_AGENT_NAME,
    REMOTE_2_AGENT_VERSION,
    REMOTE_2_AGENT_HOST,
    REMOTE_2_AGENT_PORT,
    REMOTE_2_AGENT_DEFAULT_USER_ID,
)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""
    pass


class DatabaseConnectionError(Exception):
    """Exception for database connection issues."""
    pass


def main():
    """Starts the agent server."""

    try:
        # Check for API key only if Vertex AI is not configured
        if not os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "TRUE":
            if not os.getenv("GOOGLE_API_KEY"):
                raise MissingAPIKeyError(
                    "GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE."
                )
    
    
        capabilities = AgentCapabilities(streaming=True)

        skill = AgentSkill(
            id="retrieve_real_estate_insights",
            name="Retrieve Real-Estate Data Insights",
            description=(
                "Retrieves and analyzes real-estate-related data from multiple collections including leads, "
                "site visits, and unit block bookings. Supports queries on lead ownership, project cities, booking value, "
                "visit activity, sales opportunity status, and unit availability. Helps monitor sales pipeline, "
                "filter by customer preferences, booking metadata, and identify engagement gaps."
            ),
            tags=[
                "Leads", "Projects", "Bookings", "Unit Blocks", "CRM", "SalesOps", "Site Visits",
                "Budget", "City-Based Search", "Opportunity", "Visit Tracking", "Lead Status",
                "Pipeline Monitoring", "Sales Follow-up"
            ],
            examples=[
                "List all leads from Bangalore with active status",
                "Show leads whose OwnerPartyName is 'Ramesh Kumar'",
                "Which unit blocks have TotalSaleValue above 1 crore?",
                "List unitblocks with status 'unblock' and project name 'Prestige Park Grove-Apartments'",
                "Show me site visits that happened in the last 7 days",
                "Which visits were conducted by owner 'Amit Singh'?",
                "List leads whose QualificationLevelCodeText is 'High'",
                "Give me all bookings where NeedHomeLoan is 'Yes'",
                "Find units booked with more than one car park",
                "Show me all units with Opportunity status 'In Process'",
                "Which site visits have not been updated yet?",
                "Give me details of bookings where Is_Nri is true",
                "List all unit blocks where PaymentPlan is 'Time linked Plan PPG Apartment'",
                "Show unit blocks with high FloorRiseChargesAsCPI",
                "Which leads have Mobile_No starting with '+91-98'?"
            ]
        )

        agent_card = AgentCard(
            name=REMOTE_2_AGENT_NAME,
            description=(
            "An agent that retrieves comprehensive real-estate lead information from the CRM database, including lead details,status, contact information, property preferences, budget range, assigned agents, inquiry source, status updates, and follow-up history."
            ),
            url=f"http://{REMOTE_2_AGENT_HOST}:{REMOTE_2_AGENT_PORT}/",
            version=REMOTE_2_AGENT_VERSION,
            defaultInputModes=["text/plain"],
            defaultOutputModes=["text/plain"],
            capabilities=capabilities,
            skills=[skill],
        )

        adk_agent = create_agent()
        runner = Runner(
            app_name=agent_card.name,
            agent=adk_agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            # session_service=DatabaseSessionService(db_url=db_url),
            memory_service=InMemoryMemoryService(),
        )
        agent_executor = RealEstateLeadAgentExecutor(runner)

        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor,
            task_store=InMemoryTaskStore(),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        uvicorn.run(server.build(), host=REMOTE_2_AGENT_HOST, port=REMOTE_2_AGENT_PORT)
    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)


if __name__ == "__main__":
    main()



