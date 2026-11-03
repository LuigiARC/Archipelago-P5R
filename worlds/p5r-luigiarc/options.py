from dataclasses import dataclass
from Options import (
    DeathLink as BaseDeathLink, OptionSet, PerGameCommonOptions, Range,
    StartInventoryPool, Toggle,
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


class StartingInventoryFromPool(StartInventoryPool):
    """Start with these items removed from the randomized pool and replaced with filler."""

    default = {"Progressive Palace Access": 1, "Progressive Mementos Access": 1}


@dataclass
class Persona5RoyalOptions(PerGameCommonOptions):
    shop_item_count: ShopItemCount
    shop_minimum_price: ShopMinimumPrice
    shop_maximum_price: ShopMaximumPrice
    goal_palaces: GoalPalaces
    goal_compendium: GoalCompendium
    compendium_sanity: CompendiumSanity
    mementos_chests_per_path: MementosChestsPerPath
    progressive_palace_access: ProgressivePalaceAccess
    death_link: DeathLink
    death_link_damage_percent: DeathLinkDamagePercent
    start_inventory_from_pool: StartingInventoryFromPool
