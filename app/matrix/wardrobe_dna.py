"""Registry for the Muse's Wardrobe and Props."""

from typing import Dict, List, Optional
from app.matrix.models import WardrobeItem, SceneProp

class WardrobeRegistry:
    """Manages the Muse's persistent look and tools."""

    def __init__(self):
        self.items: Dict[str, WardrobeItem] = {}
        self.props: Dict[str, SceneProp] = {}

    def register_item(self, item: WardrobeItem):
        self.items[item.item_id] = item

    def register_prop(self, prop: SceneProp):
        self.props[prop.prop_id] = prop

    def get_item(self, item_id: str) -> Optional[WardrobeItem]:
        return self.items.get(item_id)

    def get_prop(self, prop_id: str) -> Optional[SceneProp]:
        return self.props.get(prop_id)

    def list_by_tag(self, tag: str) -> List[WardrobeItem]:
        """Returns items matching a specific style tag."""
        return [item for item in self.items.values() if tag in item.tags]

    def get_look_context(self, item_ids: List[str], prop_ids: List[str]) -> str:
        """Generates a descriptive context for the selected look."""
        items_desc = []
        for i_id in item_ids:
            item = self.get_item(i_id)
            if item:
                items_desc.append(f"- {item.name}: {item.description}")
        
        props_desc = []
        for p_id in prop_ids:
            prop = self.get_prop(p_id)
            if prop:
                props_desc.append(f"- {prop.name}: {prop.description}")
                
        return (
            f"Outfit: {', '.join(items_desc) if items_desc else 'Default'}\n"
            f"Props: {', '.join(props_desc) if props_desc else 'None'}"
        )
