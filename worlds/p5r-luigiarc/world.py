from collections.abc import Mapping
import hashlib
from typing import Any

from BaseClasses import CollectionState, Item, ItemClassification, Location, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import set_rule
from Options import OptionError

from .options import ITEM_CATEGORY_OPTIONS, Persona5RoyalOptions
from .catalog_data import catalog_bytes
from .locations import CATALOG as CHEST_DOCUMENT
from .palaces import CATALOG as PALACE_DOCUMENT
from .confidant_abilities import CATALOG as CONFIDANT_DOCUMENT
from .personas import CATALOG as PERSONA_DOCUMENT
from .persona_levels import persona_level_tier
from .items import CATALOG as TV_BUNDLE_DOCUMENT
from .reward_placement import order_inventory_rewards


GAME_NAME = "Persona 5 Royal (luigiarc)"
CHEST_DATA_BYTES = catalog_bytes(CHEST_DOCUMENT)
CHESTS = CHEST_DOCUMENT["locations"]
CHEST_CATALOG_VERSION = CHEST_DOCUMENT["catalog_version"]
CHEST_CATALOG_HASH = hashlib.sha256(CHEST_DATA_BYTES).hexdigest()
PALACE_DATA_BYTES = catalog_bytes(PALACE_DOCUMENT)
PALACES = PALACE_DOCUMENT["locations"]
PALACE_CATALOG_VERSION = PALACE_DOCUMENT["catalog_version"]
PALACE_CATALOG_HASH = hashlib.sha256(PALACE_DATA_BYTES).hexdigest()
CONFIDANT_DATA_BYTES = catalog_bytes(CONFIDANT_DOCUMENT)
CONFIDANT_ABILITIES = CONFIDANT_DOCUMENT["locations"]
CONFIDANT_CATALOG_VERSION = CONFIDANT_DOCUMENT["catalog_version"]
CONFIDANT_CATALOG_HASH = hashlib.sha256(CONFIDANT_DATA_BYTES).hexdigest()
PERSONA_DATA_BYTES = catalog_bytes(PERSONA_DOCUMENT)
PERSONAS = PERSONA_DOCUMENT["locations"]
PERSONA_CATALOG_VERSION = PERSONA_DOCUMENT["catalog_version"]
PERSONA_CATALOG_HASH = hashlib.sha256(PERSONA_DATA_BYTES).hexdigest()
TV_BUNDLE_DATA_BYTES = catalog_bytes(TV_BUNDLE_DOCUMENT)
TV_BUNDLES = TV_BUNDLE_DOCUMENT["bundles"]
TV_BUNDLE_CATALOG_HASH = hashlib.sha256(TV_BUNDLE_DATA_BYTES).hexdigest()
TV_BUNDLE_ITEMS = {bundle["name"]: bundle["item_id"] for bundle in TV_BUNDLES}
RANDOMIZED_BUNDLE_ITEMS = {
    bundle["name"]: bundle["item_id"] for bundle in TV_BUNDLES if "category" not in bundle
}
NATIVE_ITEMS = {
    item["name"]: item["item_id"] for item in TV_BUNDLE_DOCUMENT["native_items"]
}
RANDOMIZED_NATIVE_ITEMS = {
    item["name"]: item["item_id"] for item in TV_BUNDLE_DOCUMENT["native_items"] if item["randomized"]
}
RANDOM_REWARD_ITEMS = {**RANDOMIZED_BUNDLE_ITEMS, **RANDOMIZED_NATIVE_ITEMS}
INVENTORY_REWARDS = {
    item["name"]: item for item in (*TV_BUNDLES, *TV_BUNDLE_DOCUMENT["native_items"])
}
NATIVE_ITEM_CATEGORIES = {
    item["contents"][0]["item_id"]: item["category"]
    for item in TV_BUNDLE_DOCUMENT["native_items"]
}
# 0x5052_1001 is reserved for the now unused connectivity token
TEST_FILLER_NAME = "Test Filler"
TEST_FILLER_ID = 0x5052_1002
VICTORY_NAME = "Victory"
VICTORY_ID = 0x5052_1003
PALACE_CLEAR_TOKEN_NAME = "Palace Clear Token"
PALACE_CLEAR_TOKEN_ID = 0x5052_1004
COMPENDIUM_ENTRY_TOKEN_NAME = "Compendium Entry Token"
COMPENDIUM_ENTRY_TOKEN_ID = 0x5052_1008
CASINO_CLEAR_NAME = "Casino of Jealousy - Palace Clear"
SHIDO_CLEAR_NAME = "Cruiser of Pride - Palace Clear"
LABORATORY_CLEAR_NAME = "Laboratory of Melancholy - Palace Clear"
PALACE_BY_KEY = {palace["key"]: palace for palace in PALACES}
DEFAULT_GOAL_KEYS = frozenset({"shido"})
SHOP_LOCATION_BASE_ID = 0x5052_0C00
SHOP_ITEM_COUNT_MAX = 500
SHOP_LOCATION_NAMES = {n: f"Shop Item #{n}" for n in range(1, SHOP_ITEM_COUNT_MAX + 1)}

# Two shared progressive items replace 16 distinct per-Palace items
PROGRESSIVE_ACCESS_NAME = "Progressive Palace Access"
PROGRESSIVE_ACCESS_ID = PALACE_DOCUMENT["progressive_access_item_id"]
PROGRESSIVE_CALLING_CARD_NAME = "Progressive Calling Card"
PROGRESSIVE_CALLING_CARD_ID = PALACE_DOCUMENT["progressive_calling_card_item_id"]


def _palace_base_name(palace: dict) -> str:
    return palace["name"].rsplit(" - ", 1)[0]


def _palace_merged_item_name(palace: dict) -> str:
    return f"{_palace_base_name(palace)} Palace"


PALACE_BASE_NAMES = {palace["key"]: _palace_base_name(palace) for palace in PALACES}
# The alternative to the two progressive items: one item per Palace, granting both access and
# calling-card together, independent of order.
PALACE_MERGED_ITEM_NAMES = {palace["key"]: _palace_merged_item_name(palace) for palace in PALACES}
# Finale-area chest groups have their own post-Shido access rules below.
CHESTS_BY_PALACE_BASE_NAME: dict[str, list[dict]] = {}
for _chest in CHESTS:
    CHESTS_BY_PALACE_BASE_NAME.setdefault(_chest["palace"], []).append(_chest)

# Generic, per-Path Mementos chest locations (Qimranut, Aiyatsbus, Chemdah, Kaitul, Akzeriyyuth, Adyeshach, Sheriruth, Da'at) 
MEMENTOS_PATHS = (
    "Qimranut", "Aiyatsbus", "Chemdah", "Kaitul", "Akzeriyyuth",
    "Adyeshach", "Sheriruth", "Iweleth", "Da'at",
)
# Keep Iweleth's old block reserved in the datapackage. Has no chests.
MEMENTOS_CHEST_PATH_INDICES = tuple(i for i in range(len(MEMENTOS_PATHS)) if i != 7)
MEMENTOS_CHESTS_PER_PATH_MAX = 20
MEMENTOS_GENERIC_CHEST_MAX = len(MEMENTOS_PATHS) * MEMENTOS_CHESTS_PER_PATH_MAX
MEMENTOS_GENERIC_CHEST_BASE_ID = 0x5052_0400


def _mementos_generic_chest_name(path_index: int, n: int) -> str:
    return f"Mementos - {MEMENTOS_PATHS[path_index]} Chest #{n}"


MEMENTOS_GENERIC_CHEST_NAMES = {
    (path_index, n): _mementos_generic_chest_name(path_index, n)
    for path_index in range(len(MEMENTOS_PATHS))
    for n in range(1, MEMENTOS_CHESTS_PER_PATH_MAX + 1)
}

# Eight copies unlock the eight Paths below Qimranut in order
MEMENTOS_PROGRESS_NAME = "Progressive Mementos Access"
MEMENTOS_PROGRESS_ID = 0x5052_1007
MEMENTOS_PROGRESS_TIERS = 8

# Characters recruitment items
PARTY_RECRUIT_ITEMS = {
    "Recruit Yusuke": 0x5052_1010,
    "Recruit Makoto": 0x5052_1011,
    "Recruit Haru": 0x5052_1012,
    "Recruit Futaba": 0x5052_1013,
    "Recruit Akechi": 0x5052_1014,
    "Recruit Sumire": 0x5052_1015,
}

# Shared level rewards apply to every unlocked party member
PARTY_LEVEL_ITEMS = {
    "Party Level Up +1": 0x5052_1018,
    "Party Level Up +3": 0x5052_1019,
    "Party Level Up +5": 0x5052_101A,
}
PARTY_LEVEL_VALUES = {
    "Party Level Up +1": 1,
    "Party Level Up +3": 3,
    "Party Level Up +5": 5,
}
PARTY_LEVEL_ITEM_COUNTS = {
    "Party Level Up +1": 20,
    "Party Level Up +3": 12,
    "Party Level Up +5": 5,
}

class Persona5RoyalItem(Item):
    game = GAME_NAME


class Persona5RoyalLocation(Location):
    game = GAME_NAME


class Persona5RoyalWebWorld(WebWorld):
    game = GAME_NAME
    theme = "dirt"
    tutorials = [
        Tutorial(
            "Persona 5 AP Setup Guide",
            "A guide to testing Persona 5 Royal Palace checks and goals with Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["luigiarc"],
        )
    ]


class Persona5RoyalWorld(World):
    """An integration test for P5R chests, Palace clears, and confidant abilities."""

    game = GAME_NAME
    web = Persona5RoyalWebWorld()
    options_dataclass = Persona5RoyalOptions
    options: Persona5RoyalOptions

    def generate_early(self) -> None:
        if not hasattr(World, "finalize_multiworld"):
            raise OptionError("Strength-based equipment placement requires Archipelago with finalize_multiworld support. Use the matching Archipelago fork to generate this world.")
        minimum = self.options.shop_minimum_price.value
        maximum = self.options.shop_maximum_price.value
        if minimum > maximum:
            raise OptionError("shop_minimum_price must not exceed shop_maximum_price")
        self.shop_prices = {
            str(SHOP_LOCATION_BASE_ID + n - 1): self.random.randint(minimum, maximum)
            for n in range(1, self.options.shop_item_count.value + 1)
        }

    item_name_to_id = {
        TEST_FILLER_NAME: TEST_FILLER_ID,
        VICTORY_NAME: VICTORY_ID,
        PALACE_CLEAR_TOKEN_NAME: PALACE_CLEAR_TOKEN_ID,
        COMPENDIUM_ENTRY_TOKEN_NAME: COMPENDIUM_ENTRY_TOKEN_ID,
        PROGRESSIVE_ACCESS_NAME: PROGRESSIVE_ACCESS_ID,
        PROGRESSIVE_CALLING_CARD_NAME: PROGRESSIVE_CALLING_CARD_ID,
        MEMENTOS_PROGRESS_NAME: MEMENTOS_PROGRESS_ID,
        **PARTY_RECRUIT_ITEMS,
        **PARTY_LEVEL_ITEMS,
        **TV_BUNDLE_ITEMS,
        **NATIVE_ITEMS,
        **{
            PALACE_MERGED_ITEM_NAMES[palace["key"]]: palace["merged_access_item_id"]
            for palace in PALACES
        },
    }
    location_name_to_id = {
        **{name: SHOP_LOCATION_BASE_ID + n - 1 for n, name in SHOP_LOCATION_NAMES.items()},
        **{chest["name"]: chest["location_id"] for chest in CHESTS},
        **{palace["name"]: palace["location_id"] for palace in PALACES},
        **{palace["calling_card_name"]: palace["calling_card_location_id"] for palace in PALACES},
        **{ability["name"]: ability["location_id"] for ability in CONFIDANT_ABILITIES},
        **{persona["name"]: persona["location_id"] for persona in PERSONAS},
        **{
            name: MEMENTOS_GENERIC_CHEST_BASE_ID
            + path_index * MEMENTOS_CHESTS_PER_PATH_MAX + n - 1
            for (path_index, n), name in MEMENTOS_GENERIC_CHEST_NAMES.items()
        },
    }

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        menu.locations.extend(
            Persona5RoyalLocation(self.player, chest["name"], chest["location_id"], menu)
            for chest in CHESTS
        )
        menu.locations.extend(
            Persona5RoyalLocation(self.player, SHOP_LOCATION_NAMES[n], SHOP_LOCATION_BASE_ID + n - 1, menu)
            for n in range(1, self.options.shop_item_count.value + 1)
        )
        if self.compendium_sanity_enabled():
            menu.locations.extend(
                Persona5RoyalLocation(self.player, persona["name"], persona["location_id"], menu)
                for persona in PERSONAS
            )
        menu.locations.extend(
            Persona5RoyalLocation(self.player, palace["name"], palace["location_id"], menu)
            for palace in PALACES
        )
        menu.locations.extend(
            Persona5RoyalLocation(
                self.player,
                palace["calling_card_name"],
                palace["calling_card_location_id"],
                menu,
            )
            for palace in PALACES
        )
        for path_index in MEMENTOS_CHEST_PATH_INDICES:
            menu.locations.extend(
                Persona5RoyalLocation(
                    self.player,
                    MEMENTOS_GENERIC_CHEST_NAMES[path_index, n],
                    self.location_name_to_id[MEMENTOS_GENERIC_CHEST_NAMES[path_index, n]],
                    menu,
                )
                for n in range(1, self.options.mementos_chests_per_path.value + 1)
            )
        self.multiworld.regions.append(menu)

    def goal_palace_keys(self) -> list[str]:
        selected = set(self.options.goal_palaces.value)
        if not selected and not self.options.goal_compendium.value:
            selected = set(DEFAULT_GOAL_KEYS)
        return sorted(selected)

    def compendium_sanity_enabled(self) -> bool:
        return bool(self.options.compendium_sanity.value or self.options.goal_compendium.value)

    def create_items(self) -> None:
        locked_locations = 0
        goal_keys = self.goal_palace_keys()
        if len(goal_keys) == 1:
            target = PALACE_BY_KEY[goal_keys[0]]
            self.get_location(target["name"]).place_locked_item(self.create_item(VICTORY_NAME))
            locked_locations += 1
        else:
            for key in goal_keys:
                self.get_location(PALACE_BY_KEY[key]["name"]).place_locked_item(
                    self.create_item(PALACE_CLEAR_TOKEN_NAME)
                )
                locked_locations += 1

        if self.options.goal_compendium.value:
            for persona in PERSONAS:
                self.get_location(persona["name"]).place_locked_item(
                    self.create_item(COMPENDIUM_ENTRY_TOKEN_NAME)
                )
                locked_locations += 1

        if self.options.progressive_palace_access.value:
            self.multiworld.itempool.extend(
                self.create_item(PROGRESSIVE_ACCESS_NAME) for _ in PALACES
            )
            self.multiworld.itempool.extend(
                self.create_item(PROGRESSIVE_CALLING_CARD_NAME) for _ in PALACES
            )
        else:
            self.multiworld.itempool.extend(
                self.create_item(PALACE_MERGED_ITEM_NAMES[palace["key"]]) for palace in PALACES
            )

        self.multiworld.itempool.extend(
            self.create_item(MEMENTOS_PROGRESS_NAME) for _ in range(MEMENTOS_PROGRESS_TIERS)
        )
        self.multiworld.itempool.extend(
            self.create_item(name) for name in PARTY_RECRUIT_ITEMS
        )
        self.multiworld.itempool.extend(
            self.create_item(name)
            for name, count in PARTY_LEVEL_ITEM_COUNTS.items()
            for _ in range(count)
        )

        total_locations = self.total_location_count()
        reward_count = (
            total_locations - locked_locations - self.palace_item_count()
            - MEMENTOS_PROGRESS_TIERS - len(PARTY_RECRUIT_ITEMS)
            - sum(PARTY_LEVEL_ITEM_COUNTS.values())
        )
        rewards = self.random.choices(self.reward_item_names(), k=reward_count)
        # Useful items cannot fill excluded checks. Supply real filler for at
        # least this world's active exclusions, even with equipment-only settings.
        excluded_count = sum(location.name in self.options.exclude_locations.value
                             for location in self.multiworld.get_locations(self.player))
        missing_filler = max(0, excluded_count - sum(
            self.create_item(name).classification == ItemClassification.filler for name in rewards))
        for index in range(len(rewards)):
            if missing_filler and self.create_item(rewards[index]).classification != ItemClassification.filler:
                rewards[index] = self.get_filler_item_name()
                missing_filler -= 1
        self.multiworld.itempool.extend(self.create_item(name) for name in rewards)

    def palace_item_count(self) -> int:
        return len(PALACES) * 2 if self.options.progressive_palace_access.value else len(PALACES)

    def total_location_count(self) -> int:
        return (
            len(CHESTS) + len(PALACES) * 2 + self.options.shop_item_count.value
            + (len(PERSONAS) if self.compendium_sanity_enabled() else 0)
            + len(MEMENTOS_CHEST_PATH_INDICES) * self.options.mementos_chests_per_path.value
        )

    def create_item(self, name: str) -> Persona5RoyalItem:
        classification = ItemClassification.filler
        if name in {
            VICTORY_NAME, PALACE_CLEAR_TOKEN_NAME,
            COMPENDIUM_ENTRY_TOKEN_NAME,
            PROGRESSIVE_ACCESS_NAME, PROGRESSIVE_CALLING_CARD_NAME,
            MEMENTOS_PROGRESS_NAME,
        } or name in PALACE_MERGED_ITEM_NAMES.values() or name in PARTY_RECRUIT_ITEMS:
            classification = ItemClassification.progression
        elif name in PARTY_LEVEL_ITEMS:
            classification = ItemClassification.useful
        elif name in INVENTORY_REWARDS:
            classification = ItemClassification[INVENTORY_REWARDS[name]["classification"]]
        return Persona5RoyalItem(name, classification, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.filler_item_names())

    def filler_item_names(self) -> tuple[str, ...]:
        candidates = tuple(name for name in self.reward_item_names()
                           if self.create_item(name).classification == ItemClassification.filler)
        return candidates or (TEST_FILLER_NAME,)

    def reward_item_names(self) -> tuple[str, ...]:
        disabled = {category for category, option in ITEM_CATEGORY_OPTIONS.items()
                    if not getattr(self.options, option).value}
        candidates = tuple(
            item["name"]
            for item in (*TV_BUNDLES, *TV_BUNDLE_DOCUMENT["native_items"])
            if item["name"] in RANDOM_REWARD_ITEMS and not any(
                NATIVE_ITEM_CATEGORIES[content["item_id"]] in disabled
                for content in item["contents"]
            )
        )
        return candidates or (TEST_FILLER_NAME,)

    def finalize_multiworld(self) -> None:
        self.equipment_spheres = order_inventory_rewards(self, INVENTORY_REWARDS)

    def _palace_access_met(self, state: "CollectionState", palace: Mapping[str, Any]) -> bool:
        if self.options.progressive_palace_access.value:
            return state.has(PROGRESSIVE_ACCESS_NAME, self.player, palace["progressive_index"])
        return state.has(PALACE_MERGED_ITEM_NAMES[palace["key"]], self.player)

    def _palace_calling_card_met(self, state: "CollectionState", palace: Mapping[str, Any]) -> bool:
        if self.options.progressive_palace_access.value:
            return state.has(
                PROGRESSIVE_ACCESS_NAME, self.player, palace["progressive_index"]
            ) and state.has(PROGRESSIVE_CALLING_CARD_NAME, self.player, palace["progressive_index"])
        return state.has(PALACE_MERGED_ITEM_NAMES[palace["key"]], self.player)

    def _palace_progress_met(self, state: "CollectionState", tier: int) -> bool:
        if self.options.progressive_palace_access.value:
            return state.has(PROGRESSIVE_ACCESS_NAME, self.player, tier)
        held = sum(
            1 for palace in PALACES
            if state.has(PALACE_MERGED_ITEM_NAMES[palace["key"]], self.player)
        )
        return held >= tier

    def set_rules(self) -> None:
        if self.compendium_sanity_enabled():
            for persona in PERSONAS:
                tier = persona_level_tier(persona["persona_id"])
                set_rule(
                    self.get_location(persona["name"]),
                    lambda state, tier=tier: self._palace_progress_met(state, tier),
                )

        for palace in PALACES:
            # Exploring the Palace's chests only needs Palace access.
            for chest in CHESTS_BY_PALACE_BASE_NAME.get(PALACE_BASE_NAMES[palace["key"]], []):
                set_rule(
                    self.get_location(chest["name"]),
                    lambda state, palace=palace: self._palace_access_met(state, palace),
                )
            set_rule(
                self.get_location(palace["calling_card_name"]),
                lambda state, palace=palace: self._palace_calling_card_met(state, palace),
            )

            # Clearing the Palace (defeating the boss) requires raid-day state
            set_rule(
                self.get_location(palace["name"]),
                lambda state, palace=palace: self._palace_calling_card_met(state, palace),
            )

        depths_of_mementos_tier = PALACE_BY_KEY["shido"]["progressive_index"]
        qliphoth_world_tier = depths_of_mementos_tier
        
        for path_index in MEMENTOS_CHEST_PATH_INDICES:
            if path_index == 0:
                continue
            for n in range(1, self.options.mementos_chests_per_path.value + 1):
                set_rule(
                    self.get_location(MEMENTOS_GENERIC_CHEST_NAMES[path_index, n]),
                    lambda state, tier=path_index: state.has(
                        MEMENTOS_PROGRESS_NAME, self.player, tier
                    ),
                )

        for chest in CHESTS_BY_PALACE_BASE_NAME.get("Depths of Mementos", []):
            set_rule(
                self.get_location(chest["name"]),
                lambda state: self._palace_access_met(state, PALACE_BY_KEY["shido"]),
            )

        for chest in CHESTS_BY_PALACE_BASE_NAME.get("Qliphoth World", []):
            set_rule(
                self.get_location(chest["name"]),
                lambda state: self._palace_access_met(state, PALACE_BY_KEY["shido"]),
            )
            
        for n in range(1, self.options.shop_item_count.value + 1):
            # Spread numbered purchases over the same eight Palace tiers as the old shop.
            tier = 1 + ((n - 1) * (len(PALACES) - 1) // max(1, self.options.shop_item_count.value - 1))
            set_rule(
                self.get_location(SHOP_LOCATION_NAMES[n]),
                lambda state, tier=tier: self._palace_progress_met(state, tier),
            )

        goal_keys = self.goal_palace_keys()
        palace_required = len(goal_keys)
        compendium_required = bool(self.options.goal_compendium.value)

        def goal_complete(state: CollectionState) -> bool:
            palace_complete = (
                palace_required == 0
                or (palace_required == 1 and state.has(VICTORY_NAME, self.player))
                or (palace_required > 1 and state.has(
                    PALACE_CLEAR_TOKEN_NAME, self.player, palace_required
                ))
            )
            compendium_complete = (
                not compendium_required
                or state.has(COMPENDIUM_ENTRY_TOKEN_NAME, self.player, len(PERSONAS))
            )
            return palace_complete and compendium_complete

        self.multiworld.completion_condition[self.player] = goal_complete

    def fill_slot_data(self) -> Mapping[str, Any]:
        goal_keys = self.goal_palace_keys()
        total_locations = self.total_location_count()
        return {
            "client_version": 13,
            "randomized_item_categories": [category for category, option in ITEM_CATEGORY_OPTIONS.items()
                                           if getattr(self.options, option).value],
            "shop_item_count": self.options.shop_item_count.value,
            "shop_location_base_id": SHOP_LOCATION_BASE_ID,
            "shop_prices": dict(self.shop_prices),
            "shop_minimum_price": self.options.shop_minimum_price.value,
            "shop_maximum_price": self.options.shop_maximum_price.value,
            "grant_confidant_abilities": True,
            "chest_catalog_version": CHEST_CATALOG_VERSION,
            "chest_catalog_hash": CHEST_CATALOG_HASH,
            "chest_count": len(CHESTS),
            "palace_catalog_version": PALACE_CATALOG_VERSION,
            "palace_catalog_hash": PALACE_CATALOG_HASH,
            "palace_clear_count": len(PALACES),
            "calling_card_count": len(PALACES),
            "confidant_catalog_version": CONFIDANT_CATALOG_VERSION,
            "confidant_catalog_hash": CONFIDANT_CATALOG_HASH,
            "confidant_ability_count": len(CONFIDANT_ABILITIES),
            "persona_catalog_version": PERSONA_CATALOG_VERSION,
            "persona_catalog_hash": PERSONA_CATALOG_HASH,
            "persona_check_count": len(PERSONAS) if self.compendium_sanity_enabled() else 0,
            "compendium_sanity": self.compendium_sanity_enabled(),
            "goal_compendium": bool(self.options.goal_compendium.value),
            "compendium_entry_token_item_id": COMPENDIUM_ENTRY_TOKEN_ID,
            "required_compendium_entry_tokens": len(PERSONAS) if self.options.goal_compendium.value else 0,
            "goal_palace_keys": goal_keys,
            "goal_name": ",".join(goal_keys),
            "victory_item_id": VICTORY_ID,
            "palace_clear_token_item_id": PALACE_CLEAR_TOKEN_ID,
            "required_palace_clear_tokens": 0 if len(goal_keys) == 1 else len(goal_keys),
            "required_palace_goal_count": len(goal_keys),
            "total_location_count": total_locations,
            "mementos_chests_per_path": self.options.mementos_chests_per_path.value,
            "mementos_path_count": len(MEMENTOS_PATHS),
            "mementos_chest_path_ids": [index + 1 for index in MEMENTOS_CHEST_PATH_INDICES],
            "depths_access_tier": PALACE_BY_KEY["shido"]["progressive_index"],
            "mementos_chests_per_path_max": MEMENTOS_CHESTS_PER_PATH_MAX,
            "mementos_generic_chest_base_id": MEMENTOS_GENERIC_CHEST_BASE_ID,
            "progressive_palace_access": bool(self.options.progressive_palace_access.value),
            "xp_multiplier": self.options.xp_multiplier.value,
            "money_multiplier": self.options.money_multiplier.value,
            "item_multiplier": self.options.item_multiplier.value,
            "death_link": bool(self.options.death_link.value),
            "death_link_damage_percent": self.options.death_link_damage_percent.value,
            "party_recruit_item_ids": list(PARTY_RECRUIT_ITEMS.values()),
            "party_level_up_1_item_id": PARTY_LEVEL_ITEMS["Party Level Up +1"],
            "party_level_up_3_item_id": PARTY_LEVEL_ITEMS["Party Level Up +3"],
            "party_level_up_5_item_id": PARTY_LEVEL_ITEMS["Party Level Up +5"],
            "party_level_item_values": {
                str(PARTY_LEVEL_ITEMS[name]): value
                for name, value in PARTY_LEVEL_VALUES.items()
            },
            "party_level_item_counts": dict(PARTY_LEVEL_ITEM_COUNTS),
            "tv_bundle_catalog_version": TV_BUNDLE_DOCUMENT["catalog_version"],
            "tv_bundle_catalog_hash": TV_BUNDLE_CATALOG_HASH,
            "tv_bundle_count": len(TV_BUNDLES),
            "tv_bundle_item_ids": list(TV_BUNDLE_ITEMS.values()),
        }
