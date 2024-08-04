from pydantic import BaseModel, Field
from typing import Optional, Dict, Tuple, Any

class DocumentAttributes(BaseModel):
    entry_name: Optional[str] = Field("entry_name")
    type: Optional[str] = Field("type")
    status: Optional[str] = Field("status")
    active: Optional[str] = Field("active")
    origin_db_path: Optional[str] = Field("origin_db_path")
    assignment: Optional[str] = Field("assignment")
    assigned_to: Optional[str] = Field("assigned_to")
    definition: Optional[str] = Field("definition")
    tasks: Optional[str] = Field("tasks")
    components: Optional[str] = Field("components")
    config: Optional[str] = Field("config")
    data: Optional[str] = Field("data")
    children: Optional[str] = Field("children")
    visual_children: Optional[str] = Field("visual_children")
    parent: Optional[str] = Field("parent")
    visual_parent: Optional[str] = Field("visual_parent")
    date: Optional[str] = Field("date")
    time: Optional[str] = Field("time")
    owner: Optional[str] = Field("owner")
    description: Optional[str] = Field("description")
    parent_task: Optional[str] = Field("parent_task")
    representation: Optional[str] = Field("representation")

if __name__ == "__main__":
    dd = DocumentAttributes()
    print(dd.entry_name)