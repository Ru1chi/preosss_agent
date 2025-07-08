# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Dict, Optional, List
# from bson import ObjectId
# from datetime import datetime, timezone, timedelta

# app = FastAPI()

# # Define expected query structure
# class MongoQuery(BaseModel):
#     collection: str
#     filter: Dict={}
#     projection: Dict
#     limit: int
#     sort: Optional[Dict] = None

# # Combine your dummy data
# DUMMY_DATA = {
#     "projects": [
#         {
#             "_id": str(ObjectId()),
#             "name": "Website Redesign",
#             "status": "active",
#             "budget": 50000,
#             "owner_id": str(ObjectId()),
#             "created_at": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(),
#             "city": "Mumbai"
#         },
#         {
#             "_id": str(ObjectId()),
#             "name": "Mobile App Dev",
#             "status": "inactive",
#             "budget": 75000,
#             "owner_id": str(ObjectId()),
#             "created_at": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(),
#             "city": "Delhi"
#         },
#         {
#             "_id": str(ObjectId()),
#             "name": "Database Migration",
#             "status": "active",
#             "budget": 120000,
#             "owner_id": str(ObjectId()),
#             "created_at": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(),
#             "city": "Bangalore"
#         },
#         {
#             "_id": str(ObjectId()),
#             "name": "E-commerce Platform",
#             "status": "active",
#             "budget": 200000,
#             "owner_id": str(ObjectId()),
#             "created_at": datetime.now(timezone(timedelta(hours=5, minutes=30))) - timedelta(days=5),
#             "city": "Chennai"
#         },
#         {
#             "_id": str(ObjectId()),
#             "name": "Cloud Infrastructure Setup",
#             "status": "inactive",
#             "budget": 95000,
#             "owner_id": str(ObjectId()),
#             "created_at": datetime.now(timezone(timedelta(hours=5, minutes=30))) - timedelta(days=10),
#             "city": "Pune"
#         },
#         {
#             "_id": str(ObjectId()),
#             "name": "AI Chatbot Integration",
#             "status": "active",
#             "budget": 150000,
#             "owner_id": str(ObjectId()),
#             "created_at": datetime.now(timezone(timedelta(hours=5, minutes=30))) - timedelta(days=2),
#             "city": "Kolkata"
#         }
#     ],

#     "users": [
#         {"_id": str(ObjectId()), "first_name": "Ruchi", "last_name": "Sharma", "active": True},
#         {"_id": str(ObjectId()), "first_name": "Amit", "last_name": "Verma", "active": False},
#         {"_id": str(ObjectId()), "first_name": "Priya", "last_name": "Patel", "active": True},
#         {"_id": str(ObjectId()), "first_name": "Karan", "last_name": "Mehta", "active": True},
#         {"_id": str(ObjectId()), "first_name": "Neha", "last_name": "Gupta", "active": False},
#         {"_id": str(ObjectId()), "first_name": "Vikas", "last_name": "Rao", "active": True}
#     ],

#     "tasks": [
#         {
#             "_id": str(ObjectId()),
#             "title": "Design Homepage",
#             "user_id": str(ObjectId()),
#             "project_id": str(ObjectId()),
#             "due_date": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(),
#             "completed": False,
#             "priority": "high"
#         },
#         {
#             "_id": str(ObjectId()),
#             "title": "Implement API",
#             "user_id": str(ObjectId()),
#             "project_id": str(ObjectId()),
#             "due_date": (datetime.now(timezone(timedelta(hours=5, minutes=30))) + timedelta(days=7)).isoformat(),
#             "completed": True,
#             "priority": "medium"
#         },
#         {
#             "_id": str(ObjectId()),
#             "title": "Test Database",
#             "user_id": str(ObjectId()),
#             "project_id": str(ObjectId()),
#             "due_date": (datetime.now(timezone(timedelta(hours=5, minutes=30))) + timedelta(days=3)).isoformat(),
#             "completed": False,
#             "priority": "low"
#         },
#         {
#             "_id": str(ObjectId()),
#             "title": "Deploy to Production",
#             "user_id": str(ObjectId()),
#             "project_id": str(ObjectId()),
#             "due_date": (datetime.now(timezone(timedelta(hours=5, minutes=30))) + timedelta(days=1)).isoformat(),
#             "completed": False,
#             "priority": "high"
#         },
#         {
#             "_id": str(ObjectId()),
#             "title": "Write Documentation",
#             "user_id": str(ObjectId()),
#             "project_id": str(ObjectId()),
#             "due_date": (datetime.now(timezone(timedelta(hours=5, minutes=30))) + timedelta(days=4)).isoformat(),
#             "completed": True,
#             "priority": "medium"
#         },
#         {
#             "_id": str(ObjectId()),
#             "title": "Client Demo Presentation",
#             "user_id": str(ObjectId()),
#             "project_id": str(ObjectId()),
#             "due_date": (datetime.now(timezone(timedelta(hours=5, minutes=30))) + timedelta(days=2)).isoformat(),
#             "completed": False,
#             "priority": "high"
#         }
#     ]
# }
# # Helper functions
# def apply_filter(data: List[Dict], filter_dict: Dict) -> List[Dict]:
#      filtered_data = []
#      for item in data:
#          matches = all(item.get(k) == v for k, v in filter_dict.items())
#          if matches:
#              filtered_data.append(item)
#      return filtered_data




# def apply_projection(data: List[Dict], projection: Dict) -> List[Dict]:
#     projected_data = []
#     for item in data:
#         projected_item = {"_id": item["_id"]}
#         for key, value in projection.items():
#             if value == 1 and key in item:
#                 projected_item[key] = item[key]
#         projected_data.append(projected_item)
#     return projected_data

# def apply_sort(data: List[Dict], sort: Dict) -> List[Dict]:
#     if not sort:
#         return data
#     for key, order in sort.items():
#         return sorted(data, key=lambda x: x.get(key, 0), reverse=(order == -1))
#     return data





# # Main API endpoint
# @app.post("/api/query")
# async def handle_query(query: MongoQuery):
#     collection = query.collection
#     if collection not in DUMMY_DATA:
#         return {"error": f"Collection '{collection}' not found"}

#     data = DUMMY_DATA[collection]
#     filtered = apply_filter(data, query.filter)
#     projected = apply_projection(filtered, query.projection)
#     sorted_data = apply_sort(projected, query.sort or {})
#     limited = sorted_data[:query.limit]

#     return {"data": limited}

# # Start server
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5005)




from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Optional, List, Any
from bson import ObjectId
from datetime import datetime, timezone, timedelta
from dateutil.parser import parse as parse_date

app = FastAPI()

# Define expected query structure
class MongoQuery(BaseModel):
    collection: str
    filter: Dict[str, Any] = {}
    projection: Optional[Dict[str, int]] = None
    limit: Optional[int] = None
    sort: Optional[Dict[str, int]] = None

# Dummy data
DUMMY_DATA = {
    "projects": [
        {
            "_id": str(ObjectId()),
            "name": "Website Redesign",
            "status": "active",
            "budget": 50000,
            "owner_id": str(ObjectId()),
            "created_at": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(),
            "city": "Mumbai"
        },
        {
            "_id": str(ObjectId()),
            "name": "Mobile App Dev",
            "status": "inactive",
            "budget": 75000,
            "owner_id": str(ObjectId()),
            "created_at": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(),
            "city": "Delhi"
        },
        {
            "_id": str(ObjectId()),
            "name": "Database Migration",
            "status": "active",
            "budget": 120000,
            "owner_id": str(ObjectId()),
            "created_at": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(),
            "city": "Bangalore"
        },
        {
            "_id": str(ObjectId()),
            "name": "E-commerce Platform",
            "status": "active",
            "budget": 200000,
            "owner_id": str(ObjectId()),
            "created_at": (datetime.now(timezone(timedelta(hours=5, minutes=30))) - timedelta(days=5)).isoformat(),
            "city": "Chennai"
        },
        {
            "_id": str(ObjectId()),
            "name": "Cloud Infrastructure Setup",
            "status": "inactive",
            "budget": 95000,
            "owner_id": str(ObjectId()),
            "created_at": (datetime.now(timezone(timedelta(hours=5, minutes=30))) - timedelta(days=10)).isoformat(),
            "city": "Pune"
        },
        {
            "_id": str(ObjectId()),
            "name": "AI Chatbot Integration",
            "status": "active",
            "budget": 150000,
            "owner_id": str(ObjectId()),
            "created_at": (datetime.now(timezone(timedelta(hours=5, minutes=30))) - timedelta(days=2)).isoformat(),
            "city": "Kolkata"
        }
    ],
    "users": [
        {"_id": str(ObjectId()), "first_name": "Ruchi", "last_name": "Sharma", "active": True},
        {"_id": str(ObjectId()), "first_name": "Amit", "last_name": "Verma", "active": False},
        {"_id": str(ObjectId()), "first_name": "Priya", "last_name": "Patel", "active": True},
        {"_id": str(ObjectId()), "first_name": "Karan", "last_name": "Mehta", "active": True},
        {"_id": str(ObjectId()), "first_name": "Neha", "last_name": "Gupta", "active": False},
        {"_id": str(ObjectId()), "first_name": "Vikas", "last_name": "Rao", "active": True}
    ],
    "tasks": [
        {
            "_id": str(ObjectId()),
            "title": "Design Homepage",
            "user_id": str(ObjectId()),
            "project_id": str(ObjectId()),
            "due_date": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(),
            "completed": False,
            "priority": "high"
        },
        {
            "_id": str(ObjectId()),
            "title": "Implement API",
            "user_id": str(ObjectId()),
            "project_id": str(ObjectId()),
            "due_date": (datetime.now(timezone(timedelta(hours=5, minutes=30))) + timedelta(days=7)).isoformat(),
            "completed": True,
            "priority": "medium"
        },
        {
            "_id": str(ObjectId()),
            "title": "Test Database",
            "user_id": str(ObjectId()),
            "project_id": str(ObjectId()),
            "due_date": (datetime.now(timezone(timedelta(hours=5, minutes=30))) + timedelta(days=3)).isoformat(),
            "completed": False,
            "priority": "low"
        },
        {
            "_id": str(ObjectId()),
            "title": "Deploy to Production",
            "user_id": str(ObjectId()),
            "project_id": str(ObjectId()),
            "due_date": (datetime.now(timezone(timedelta(hours=5, minutes=30))) + timedelta(days=1)).isoformat(),
            "completed": False,
            "priority": "high"
        },
        {
            "_id": str(ObjectId()),
            "title": "Write Documentation",
            "user_id": str(ObjectId()),
            "project_id": str(ObjectId()),
            "due_date": (datetime.now(timezone(timedelta(hours=5, minutes=30))) + timedelta(days=4)).isoformat(),
            "completed": True,
            "priority": "medium"
        },
        {
            "_id": str(ObjectId()),
            "title": "Client Demo Presentation",
            "user_id": str(ObjectId()),
            "project_id": str(ObjectId()),
            "due_date": (datetime.now(timezone(timedelta(hours=5, minutes=30))) + timedelta(days=2)).isoformat(),
            "completed": False,
            "priority": "high"
        }
    ]
}

# --- Helper functions ---

def apply_filter(data: List[Dict[str, Any]], filter_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    def match(item: Dict[str, Any], key: str, condition: Any) -> bool:
        value = item.get(key)
        if isinstance(condition, dict):
            for op, target in condition.items():
                if op == "$gt" and not (value > target): return False
                if op == "$gte" and not (value >= target): return False
                if op == "$lt" and not (value < target): return False
                if op == "$lte" and not (value <= target): return False
                if op == "$eq" and not (value == target): return False
                if op == "$ne" and not (value != target): return False
            return True
        else:
            return value == condition
    return [item for item in data if all(match(item, key, cond) for key, cond in filter_dict.items())]

def apply_sort(data: List[Dict], sort: Optional[Dict[str, int]]) -> List[Dict]:
    if not sort:
        return data
    for key, order in sort.items():
        reverse = (order == -1)
        def sort_key(x):
            value = x.get(key)
            if value is None:
                return 0
            if key == "created_at":
                try:
                    return parse_date(value) if isinstance(value, str) else value
                except:
                    return datetime.min
            return value
        return sorted(data, key=sort_key, reverse=reverse)
    return data

def apply_projection(data: List[Dict], projection: Optional[Dict[str, int]]) -> List[Dict]:
    if not projection:
        return data
    result = []
    for item in data:
        projected = {"_id": item["_id"]}
        for key, include in projection.items():
            if include == 1 and key in item:
                projected[key] = item[key]
        result.append(projected)
    return result

# --- API Endpoint ---
@app.post("/api/query")
async def handle_query(query: MongoQuery):
    collection = query.collection
    if collection not in DUMMY_DATA:
        return {"error": f"Collection '{collection}' not found"}

    data = DUMMY_DATA[collection]
    filtered = apply_filter(data, query.filter)
    sorted_data = apply_sort(filtered, query.sort)
    limited = sorted_data[:query.limit] if query.limit else sorted_data
    projected = apply_projection(limited, query.projection)
    return {"data": projected}

# --- Start server ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5005)
