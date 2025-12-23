"""Registry and loader for the Muse's World DNA (Locations and Objects)."""

from typing import Dict, List, Optional
from app.matrix.models import WorldLocation, WorldObject

class WorldRegistry:
    """Manages the persistent environmental assets of the Muse."""

    def __init__(self):
        self.locations: Dict[str, WorldLocation] = {}
        self.objects: Dict[str, WorldObject] = {}

    def register_location(self, location: WorldLocation):
        """Adds a location to the registry."""
        self.locations[location.location_id] = location

    def register_object(self, obj: WorldObject):
        """Adds a persistent object to the registry."""
        self.objects[obj.object_id] = obj

    def get_location(self, location_id: str) -> Optional[WorldLocation]:
        """Retrieves a location by its ID."""
        return self.locations.get(location_id)

    def get_object(self, object_id: str) -> Optional[WorldObject]:
        """Retrieves an object by its ID."""
        return self.objects.get(object_id)

    def list_locations(self) -> List[WorldLocation]:
        """Returns all registered locations."""
        return list(self.locations.values())

    def get_location_context(self, location_id: str) -> str:
        """Generates a descriptive context for a location, including its recurring objects."""
        loc = self.get_location(location_id)
        if not loc:
            return ""
        
        objects_desc = []
        for obj_id in loc.recurring_objects:
            obj = self.get_object(obj_id)
            if obj:
                objects_desc.append(f"- {obj.name}: {obj.description}")
        
        objs_str = "\n".join(objects_desc) if objects_desc else "None"
        
        return (
            f"Location: {loc.name}\n"
            f"Description: {loc.description}\n"
            f"Lighting: {loc.lighting_setup}\n"
            f"Persistent Objects:\n{objs_str}"
        )
