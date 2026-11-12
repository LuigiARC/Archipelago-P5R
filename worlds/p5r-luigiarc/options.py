from dataclasses import dataclass
from collections import Counter
from Options import (
    DeathLink as BaseDeathLink, OptionError, OptionSet, PerGameCommonOptions, Range,
    StartInventory, StartInventoryPool, Toggle,
)


PALACE_KEYS = frozenset({
    "kamoshida",
    "madarame",
    "kaneshiro",
    "futaba",
    "okumura",
    "niijima",
    "shido",
    "maruki",
})


class GoalPalaces(OptionSet):
    """ Which Palace clears are required to goal. 
    Multiple are allowed and if multiple are specified, all must be cleared to goal
    Clear is sent after the respective boss is defeated.

    Valid names: kamoshida, madarame, kaneshiro, futaba, okumura, niijima, shido, maruki (has issues)
    """

    display_name = "Goal Palaces"
    valid_keys = PALACE_KEYS
    default = frozenset({"shido"})


class MementosChestsPerPath(Range):
    """How many regenerating chest checks each of Mementos's eight chest-bearing Paths contributes."""

    display_name = "Mementos Chests Per Path"
    range_start = 1
    range_end = 20
    default = 5


class CompendiumSanity(Toggle):
    """Adds one AP location for each of the 232 tracked Persona registrations."""

    display_name = "Compendium Sanity"
    default = False


class ShopItemCount(Range):
    """Number of numbered AP shop checks purchased with yen."""

    display_name = "Shop Item Count"
    range_start = 0
    range_end = 500
    default = 20


class ShopMinimumPrice(Range):
    """Lowest possible shop price in yen. Prices are rolled once during generation."""
    display_name = "Shop Minimum Price"
    range_start = 1
    range_end = 9999999
    default = 1000


class ShopMaximumPrice(ShopMinimumPrice):
    """Highest possible shop price in yen. Must be at least shop_minimum_price."""
    display_name = "Shop Maximum Price"
    default = 10000


class GoalCompendium(Toggle):
    """Requires registering every tracked Persona. This implicitly enables Compendium Sanity
    and may be combined with any Palace goals."""

    display_name = "Goal: Complete Compendium"
    default = False


class ProgressivePalaceAccess(Toggle):
    """Whether Palace access/calling-card permissions come from two shared progressive items
    (on, default) or from 8 distinct per-Palace items instead (off).
    """

    display_name = "Progressive Palace Access"
    default = True


class XpMultiplier(Range):
    """Multiply battle EXP throughout the game."""
    display_name = "XP Multiplier"
    range_start = 1
    range_end = 10
    default = 1


class MoneyMultiplier(Range):
    """Multiply battle money throughout the game."""
    display_name = "Money Multiplier"
    range_start = 1
    range_end = 10
    default = 1


class ItemMultiplier(Range):
    """Multiply quantities of items in battle results."""
    display_name = "Item Multiplier"
    range_start = 1
    range_end = 10
    default = 1


class DeathLinkDamagePercent(Range):
    """Percentage of each active party member's maximum HP removed when receiving a
    DeathLink. Damage is nonlethal (survivors stop at 1 HP), and 0 makes DeathLink
    send-only while still consuming received links.
    """

    display_name = "DeathLink Received Damage Percent"
    range_start = 0
    range_end = 100
    default = 30


class DeathLink(BaseDeathLink):
    """Send a DeathLink on a party wipe. Received links apply the configured nonlethal damage."""

    default = True


class _InventoryListInput:
    @classmethod
    def from_any(cls, data):
        if isinstance(data, list):
            if any(not isinstance(name, str) or not name.strip() for name in data):
                raise OptionError("Starting inventory lists must contain item names.")
            data = dict(Counter("Perma-Pick" if name == "Eternal Lockpick" else name for name in data))
        elif isinstance(data, dict) and "Eternal Lockpick" in data:
            data = data.copy()
            data["Perma-Pick"] = data.get("Perma-Pick", 0) + data.pop("Eternal Lockpick")
        # AP's generation/protocol code expects a name-to-count dictionary internally.
        return super().from_any(data)


class StartingInventory(_InventoryListInput, StartInventory):
    """Item names received at the start of the run. Use [] to opt out.
    Repeat a name to request more copies. Name-to-count dictionaries also work.
    Native inventory items are delivered once through the connected AP hub.
    """

    default = ["Perma-Pick"]


class StartingInventoryFromPool(_InventoryListInput, StartInventoryPool):
    """Item names to remove from the randomized pool and replace with filler.
    Repeat a name for more copies; name-to-count dictionaries also work.
    """

    default = ["Progressive Palace Access", "Progressive Mementos Access"]


class CategoryItemCount(Range):
    """Category reward count. Set to 0 to disable.
    Exact counts sample with replacement and exclude bundles containing this category.
    """
    range_start = 0
    range_end = 500
    default = 0

    def __init__(self, value):
        # Keep old automatic/true configurations readable without exposing them in templates.
        if value == -1:
            self.value = value
        else:
            super().__init__(value)

    @classmethod
    def from_any(cls, data):
        if isinstance(data, bool):
            return cls(-1 if data else 0)
        return super().from_any(data)

    @classmethod
    def from_text(cls, text):
        if text.lower() in {"automatic", "true", "on", "yes"}:
            return cls(-1)
        if text.lower() in {"false", "off", "no"}:
            return cls(0)
        return super().from_text(text)


class RandomizeMeleeWeapons(CategoryItemCount):
    """Individual melee weapon rewards: set to 0 to disable (range 0–500).
    195 individual items. Example: Rebel Knife.
    Duplicates allowed; counts must fit available slots. Explicit counts exclude bundles.
    """
    display_name = "Melee Weapon Pool Count"
    default = 20


class RandomizeGuns(CategoryItemCount):
    """Individual gun rewards: set to 0 to disable (range 0–500).
    106 individual items. Example: Tkachev.
    Duplicates allowed; counts must fit available slots. Explicit counts exclude bundles.
    """
    display_name = "Gun Pool Count"
    default = 15


class RandomizeArmor(CategoryItemCount):
    """Individual armor rewards: set to 0 to disable (range 0–500).
    200 individual items. Example: Dark Undershirt.
    Duplicates allowed; counts must fit available slots. Explicit counts exclude bundles.
    """
    display_name = "Armor Pool Count"
    default = 25


class RandomizeAccessories(CategoryItemCount):
    """Individual accessory rewards: set to 0 to disable (range 0–500).
    439 individual items. Example: Hip Glasses.
    Duplicates allowed; counts must fit available slots. Explicit counts exclude bundles.
    """
    display_name = "Accessory Pool Count"
    default = 25


class RandomizeConsumables(CategoryItemCount):
    """Individual consumable rewards: set to 0 to disable (range 0–500).
    551 individual items. Example: Soma.
    Duplicates allowed; counts must fit available slots. Explicit counts exclude bundles.
    """
    display_name = "Consumable Pool Count"
    default = 48


class RandomizeMaterials(CategoryItemCount):
    """Individual material rewards: set to 0 to disable (range 0–500).
    168 individual items. Example: Gold Coin.
    Duplicates allowed; counts must fit available slots. Explicit counts exclude bundles.
    """
    display_name = "Material Pool Count"
    default = 0


class RandomizeSkillCards(CategoryItemCount):
    """Individual skill card rewards: set to 0 to disable (range 0–500).
    459 individual items. Example: Agi.
    Duplicates allowed; counts must fit available slots. Explicit counts exclude bundles.
    """
    display_name = "Skill Card Pool Count"
    default = 30


class RandomizeOutfits(CategoryItemCount):
    """Individual outfit rewards: set to 0 to disable (range 0–500).
    273 individual items. Example: Shujin Uniform.
    Duplicates allowed; counts must fit available slots. Explicit counts exclude bundles.
    """
    display_name = "Outfit Pool Count"
    default = 0


ITEM_CATEGORY_OPTIONS = {
    "melee_weapon": "randomize_melee_weapons",
    "ranged_weapon": "randomize_guns",
    "armor": "randomize_armor",
    "accessory": "randomize_accessories",
    "consumable": "randomize_consumables",
    "skill_card": "randomize_skill_cards",
    "material": "randomize_materials",
    "outfit": "randomize_outfits",
}


@dataclass
class Persona5RoyalOptions(PerGameCommonOptions):
    start_inventory: StartingInventory
    randomize_melee_weapons: RandomizeMeleeWeapons
    randomize_guns: RandomizeGuns
    randomize_armor: RandomizeArmor
    randomize_accessories: RandomizeAccessories
    randomize_consumables: RandomizeConsumables
    randomize_skill_cards: RandomizeSkillCards
    randomize_materials: RandomizeMaterials
    randomize_outfits: RandomizeOutfits
    shop_item_count: ShopItemCount
    shop_minimum_price: ShopMinimumPrice
    shop_maximum_price: ShopMaximumPrice
    goal_palaces: GoalPalaces
    goal_compendium: GoalCompendium
    compendium_sanity: CompendiumSanity
    mementos_chests_per_path: MementosChestsPerPath
    progressive_palace_access: ProgressivePalaceAccess
    xp_multiplier: XpMultiplier
    money_multiplier: MoneyMultiplier
    item_multiplier: ItemMultiplier
    death_link: DeathLink
    death_link_damage_percent: DeathLinkDamagePercent
    start_inventory_from_pool: StartingInventoryFromPool
