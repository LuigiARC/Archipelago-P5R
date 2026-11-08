"""Place non-progression inventory rewards by strength in the final logical spheres."""

from collections import deque


def legal_assignment(items, locations, state):
    """Match ranked items to ranked slots, retaining hard item/locality/exclusion rules."""
    if all(location.can_fill(state, item, check_access=False) for item, location in zip(items, locations)):
        return items

    # The original fill is a valid matching. Alternating paths find another valid
    # matching while preferring slots nearest each item's intended strength rank.
    allowed = {}
    preferences = []
    for rank, item in enumerate(items):
        if item.name not in allowed:
            allowed[item.name] = [slot for slot, location in enumerate(locations)
                                  if location.can_fill(state, item, check_access=False)]
        preferences.append(sorted(allowed[item.name], key=lambda slot: (abs(slot - rank), slot)))
    occupants = {}
    item_slots = {}
    for root in range(len(items)):
        queue = deque([root])
        visited_items = {root}
        previous = {}
        free = None
        while queue and free is None:
            item_index = queue.popleft()
            for slot in preferences[item_index]:
                if slot in previous:
                    continue
                previous[slot] = item_index
                if slot not in occupants:
                    free = slot
                    break
                other = occupants[slot]
                if other not in visited_items:
                    visited_items.add(other)
                    queue.append(other)
        if free is None:
            # No partial writes: keep the valid original placements in this case.
            return None
        while free is not None:
            item_index = previous[free]
            old_slot = item_slots.get(item_index)
            occupants[free] = item_index
            item_slots[item_index] = free
            free = old_slot
    return [items[occupants[slot]] for slot in range(len(locations))]


def order_inventory_rewards(world, rewards):
    # This runs in finalize_multiworld, after progression balancing. None of these
    # items is used by access rules, so moving them does not change logical spheres.
    spheres = {}
    for number, sphere in enumerate(world.multiworld.get_spheres(), 1):
        if not sphere:  # Leave unreachable locations untouched.
            break
        spheres.update((location, number) for location in sphere)
    locations = sorted(
        (location for location in spheres if location.item and not location.locked
         and location.item.player == world.player and not location.item.advancement
         and location.item.name in rewards),
        key=lambda location: (location.player, location.address or 0, location.name),
    )
    world.random.shuffle(locations)
    locations.sort(key=spheres.__getitem__)
    items = [location.item for location in locations]
    # Utility/filler rewards keep random positions; equipment is anchored to its
    # strength relative to the full catalog, not to its ID or just this seed's sample.
    def rank(item):
        power = rewards[item.name].get("equipment_power")
        return power if power is not None else world.random.randrange(10001)
    items.sort(key=rank)
    state = world.multiworld.get_all_state()
    assignment = legal_assignment(items, locations, state)
    if assignment is not None:
        for location, item in zip(locations, assignment):
            location.item = item
            item.location = location
    return {
        (location.player, location.address): {"item": location.item.name, "sphere": sphere,
                                             "power": rewards[location.item.name]["equipment_power"]}
        for location, sphere in spheres.items()
        if location.item and location.item.player == world.player
        and location.item.name in rewards and "equipment_power" in rewards[location.item.name]
    }
