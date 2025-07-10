import sys
import os
import requests
import json
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from typing import Dict
from prompt import instruction

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from constants import (
    MODEL, 
    REMOTE_2_AGENT_NAME,
    REMOTE_2_AGENT_DATABASE_API_URL,
    REMOTE_2_AGENT_DATABASE_DBNAME,
    )

#use this when get the database connection
def get_mongodb(collection: str, filter: str, projection: str, limit: int = 3) -> Dict:
    """
    Fetch data from MongoDB via the Node.js API using the provided query parameters.

    Args:
        collection (str): The name of the MongoDB collection (e.g., 'categories').
        filter (str): The filter criteria as a JSON string (e.g., '{"is_available": true}').
        limit (int): The maximum number of documents to return.

    Returns:
        dict: The data fetched from the MongoDB database via the API, or an error message.
    """
    # Parse JSON string for filter
    try:
        filter_dict = json.loads(filter)
        projection_dict = json.loads(projection)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON in filter: {str(e)}"}
    
    # Construct the query dictionary for the Node.js API
    query = {
        "isprod":1,
        "dbname": REMOTE_2_AGENT_DATABASE_DBNAME,
        "collection": collection,
        "paginationinfo": {
            "pagelimit": limit,
            "filter": filter_dict,
            "projection": projection_dict
        }
    }
    
    # Send the query to the Node.js API
    api_url = REMOTE_2_AGENT_DATABASE_API_URL
    try:
        response = requests.post(api_url, json=query)
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses
        data = response.json()
        # Ensure the return value is always a dictionary
        if isinstance(data, list):
            return {"data": data}
        return data
    except requests.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

# Create a FunctionTool without the 'declaration' parameter
get_mongodb_tool = FunctionTool(func=get_mongodb)


  
    # except requests.RequestException as e:
    #     return {"error": f"error: {str(e)}"}

def create_agent() -> LlmAgent:
    """Constructs the ADK agent for RemoteAgent."""
    return LlmAgent(
        model=MODEL,
        name=REMOTE_2_AGENT_NAME,
        description="Specialized agent for querying MongoDB collections via FastAPI mock. This agent is registered as 'preoss_Agent' and should be referenced by this name in the host agent prompt.",
        instruction=instruction,
        tools=[get_mongodb_tool],
    )

#______________________________________________________________________________



# import json
# import requests
# from typing import Dict, Any, Optional

# def get_mongodb(
#     collection: str,
#     filter_str: str,
#     projection_str: str,
#     limit: int,
#     sort_str: Optional[str] = None,
#     api_url: str = "http://localhost:5005/api/query"
# ) -> Dict[str, Any]:
#     """
#     Fetch data from the FastAPI dummy‑Mongo endpoint using the provided query parameters.

#     Args:
#         collection (str): Name of the collection (e.g., 'projects', 'users', 'tasks').
#         filter_str (str): Filter criteria as a JSON string (e.g., '{"status": "active"}').
#         projection_str (str): Projection spec as a JSON string (e.g., '{"name": 1, "budget": 1}').
#         limit (int): Maximum number of documents to return.
#         sort_str (Optional[str]): Sort spec as a JSON string (e.g., '{"budget": -1}'). Defaults to None.
#         api_url (str): Full URL to the FastAPI `/api/query` endpoint. Defaults to localhost.

#     Returns:
#         dict: The JSON response from the API, either `{"data": [...]}` or `{"error": "..."}`
#     """
#     # Use default if api_url is empty
#     if not api_url:
#         api_url = "http://localhost:5005/api/query"

#     # Parse JSON inputs
#     try:
#         filter_dict = json.loads(filter_str)
#     except json.JSONDecodeError as e:
#         return {"error": f"Invalid JSON in filter: {e}"}
#     try:
#         projection_dict = json.loads(projection_str)
#     except json.JSONDecodeError as e:
#         return {"error": f"Invalid JSON in projection: {e}"}
#     sort_dict = None
#     if sort_str:
#         try:
#             sort_dict = json.loads(sort_str)
#         except json.JSONDecodeError as e:
#             return {"error": f"Invalid JSON in sort: {e}"}

#     # Build the payload
#     payload: Dict[str, Any] = {
#         "collection": collection,
#         "filter": filter_dict,
#         "projection": projection_dict,
#         "limit": limit,
#     }
#     if sort_dict is not None:
#         payload["sort"] = sort_dict

#     # Send the request
#     try:
#         resp = requests.post(api_url, json=payload)
#         resp.raise_for_status()
#         return resp.json()
#     except requests.RequestException as e:
#         return {"error": f"API request failed: {e}"}


# get_mongodb_tool = FunctionTool(func=get_mongodb)
  



# def create_agent() -> LlmAgent:
#     """Constructs the ADK agent for RemoteAgent."""
#     return LlmAgent(
#         model=MODEL,
#         name=REMOTE_2_AGENT_NAME,
#         description="Specialized agent for querying MongoDB collections via Node.js API. This agent is registered as 'preoss_Agent' and should be referenced by this name in the host agent prompt and system configuration.",
#         instruction = instruction,
#         tools=[get_mongodb_tool],
#     )

# root_agent = create_agent()

#_______________________________________________________________________

# import sys
# import os
# import requests
# import json
# from typing import Dict, Any, Optional
# from google.adk.agents import LlmAgent
# from google.adk.tools import FunctionTool
# from prompt import instruction

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from constants import (
#     MODEL, 
#     REMOTE_2_AGENT_NAME,
# )

# def get_mongodb(
#     collection: str,
#     filter_str: str,
#     projection_str: str,
#     limit: int,
#     sort_str: Optional[str] = None,
#     api_url: str = "http://localhost:5005/api/query"
# ) -> Dict[str, Any]:
#     """
#     Fetch data from the FastAPI dummy‑Mongo endpoint using the provided query parameters.

#     Args:
#         collection (str): Name of the collection (e.g., 'projects', 'users', 'tasks').
#         filter_str (str): Filter criteria as a JSON string (e.g., '{"status": "active"}').
#         projection_str (str): Projection spec as a JSON string (e.g., '{"name": 1, "budget": 1}').
#         limit (int): Maximum number of documents to return.
#         sort_str (Optional[str]): Sort spec as a JSON string (e.g., '{"budget": -1}'). Defaults to None.
#         api_url (str): Full URL to the FastAPI `/api/query` endpoint. Defaults to localhost.

#     Returns:
#         dict: The formatted text response to be used by the agent.
#     """
#     if not api_url:
#         api_url = "http://localhost:5005/api/query"

#     # Parse JSON input strings
#     try:
#         filter_dict = json.loads(filter_str)
#     except json.JSONDecodeError as e:
#         return {"result": [{"kind": "text", "text": f"❌ Invalid JSON in filter: {e}"}]}

#     try:
#         projection_dict = json.loads(projection_str)
#     except json.JSONDecodeError as e:
#         return {"result": [{"kind": "text", "text": f"❌ Invalid JSON in projection: {e}"}]}

#     sort_dict = None
#     if sort_str:
#         try:
#             sort_dict = json.loads(sort_str)
#         except json.JSONDecodeError as e:
#             return {"result": [{"kind": "text", "text": f"❌ Invalid JSON in sort: {e}"}]}

#     payload: Dict[str, Any] = {
#         "collection": collection,
#         "filter": filter_dict,
#         "projection": projection_dict,
#         "limit": limit,
#     }
#     if sort_dict is not None:
#         payload["sort"] = sort_dict

#     try:
#         resp = requests.post(api_url, json=payload)
#         resp.raise_for_status()
#         response_data = resp.json()

#         if "data" in response_data and isinstance(response_data["data"], list):
#             data = response_data["data"]
#             if not data:
#                 return {"result": [{"kind": "text", "text": "⚠️ No matching documents found."}]}

#             # Format each document clearly
#             formatted_docs = []
#             for i, doc in enumerate(data, 1):
#                 doc_lines = [f"{i}."]
#                 for key, val in doc.items():
#                     doc_lines.append(f"  {key}: {val}")
#                 formatted_docs.append("\n".join(doc_lines))

#             return {
#                 "result": [{"kind": "text", "text": "\n\n".join(formatted_docs)}]
#             }

#         return {"result": [{"kind": "text", "text": "⚠️ Unexpected response format or no data returned."}]}

#     except requests.RequestException as e:
#         return {"result": [{"kind": "text", "text": f"❌ API request failed: {e}"}]}


# # Register the tool with the agent
# get_mongodb_tool = FunctionTool(func=get_mongodb)



