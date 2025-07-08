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
            id="retrieve_lead_information",
            name="Retrieve Real-Estate Lead Data",
            description=(
                "Queries the real-estate leads  to fetch and analyze lead-related data. "
                "Supports tables like: leads, agents, interactions, followups. "
                "Useful for monitoring lead status, filtering by budget, city,status, property preferences, and identifying follow-up gaps."
            
            ),
            tags=["Leads", "CRM", "Sales", "Budget", "Follow-Up",
                "Real-Estate-Clients", "Contact-Status", "City-Wise-Search",
                "Agent-Assignment", "Cold-Warm-Hot", "Conversion", "Client-Pipeline"
                  ],

            examples=["List all leads interested in Surat with budget over ₹80 lakhs",
                "Show me leads who haven't been contacted in the last 7 days",
                "Who are the new leads added this week?",
                "List leads assigned to agent Ramesh",
                "Get follow-up status for lead Anjali Mehta",
                "Show all leads marked as 'Interested' for 3BHK properties",
                "Which leads came from Facebook and have a budget over ₹1 crore?",
                "How many converted leads do we have this month?",
                "List cold leads in the system",
                "Get contact info for leads interested in Project X"
                      ],
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



