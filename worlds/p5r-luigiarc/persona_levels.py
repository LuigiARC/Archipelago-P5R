"""Native Persona base levels and their logical Palace-access balance tiers."""

# Source PERSONA.TBL SHA-256: 94c0305e2562c6a15c09ed15fec2bbc8fc4f16b4fd000db63b94e2706c26fa9f
PERSONA_BASE_LEVELS = {
    1: 89,  # Metatron
    2: 87,  # Beelzebub
    3: 76,  # Cu Chulainn
    4: 2,  # Jack-o'-Lantern
    5: 11,  # Jack Frost
    6: 2,  # Pixie
    7: 55,  # Cerberus
    8: 32,  # Lilim
    9: 16,  # Eligor
    10: 84,  # Odin
    11: 9,  # Hua Po
    12: 32,  # Decarabia
    13: 73,  # Mara
    14: 42,  # Ose
    15: 64,  # Thor
    16: 39,  # Unicorn
    17: 81,  # Uriel
    18: 50,  # Sarasvati
    19: 44,  # Valkyrie
    20: 20,  # Yaksini
    21: 53,  # Ganesha
    22: 34,  # Anubis
    23: 72,  # Mot
    24: 78,  # Raphael
    25: 77,  # Scathach
    26: 16,  # High Pixie
    27: 52,  # Barong
    28: 43,  # Girimehkala
    29: 61,  # King Frost
    30: 48,  # Narcissus
    31: 26,  # Isis
    32: 26,  # Lamia
    33: 38,  # Legion
    34: 24,  # Rakshasa
    35: 9,  # Mokoi
    36: 63,  # Forneus
    37: 25,  # Setanta
    38: 56,  # Titania
    39: 5,  # Incubus
    40: 20,  # Oni
    41: 60,  # Lilith
    42: 48,  # Rangda
    43: 15,  # Makami
    44: 56,  # Parvati
    45: 77,  # Gabriel
    46: 80,  # Zaou-Gongen
    47: 83,  # Alice
    48: 63,  # Kali
    49: 31,  # Kurama Tengu
    50: 66,  # Oberon
    51: 18,  # Shiki-Ouji
    52: 64,  # Yamata-no-Orochi
    53: 17,  # Orobas
    54: 64,  # Hanuman
    55: 14,  # Archangel
    56: 8,  # Obariyon
    57: 43,  # Queen Mab
    58: 75,  # Sandalphon
    59: 75,  # Abaddon
    60: 15,  # Shiisaa
    61: 23,  # Sandman
    62: 82,  # Belial
    63: 19,  # Leanan Sidhe
    64: 83,  # Cybele
    65: 62,  # Chernobog
    66: 19,  # Flauros
    67: 13,  # Ippon-Datara
    68: 21,  # Orthrus
    69: 7,  # Succubus
    70: 33,  # Mothman
    72: 68,  # Dominion
    73: 17,  # Nekomata
    74: 67,  # Black Frost
    75: 35,  # Arahabaki
    76: 9,  # Angel
    77: 53,  # Skadi
    78: 40,  # Kikuri-Hime
    79: 88,  # Chi You
    80: 41,  # Power
    81: 14,  # Inugami
    82: 74,  # Nebiros
    84: 10,  # Slime
    85: 25,  # Anzu
    86: 57,  # Yatagarasu
    87: 87,  # Yoshitsune
    88: 26,  # Take-Minakata
    89: 13,  # Ame-no-Uzume
    90: 42,  # Kushinada
    91: 42,  # Kumbhanda
    92: 89,  # Ongyo-Ki
    93: 25,  # Kin-Ki
    94: 24,  # Sui-Ki
    95: 23,  # Fuu-Ki
    96: 51,  # Jatayu
    97: 36,  # Kaiwan
    98: 6,  # Kelpie
    99: 36,  # Thoth
    100: 71,  # Dionysus
    101: 11,  # Apsaras
    102: 27,  # Andras
    104: 9,  # Koropokguru
    105: 11,  # Koppa Tengu
    106: 10,  # Regent
    107: 15,  # Queen's Necklace
    108: 20,  # Stone of Scone
    109: 25,  # Koh-i-Noor
    110: 30,  # Orlov
    111: 35,  # Emperor's Amulet
    112: 40,  # Hope Diamond
    113: 50,  # Crystal Skull
    114: 60,  # Orichalcum
    121: 3,  # Mandrake
    122: 82,  # Baal
    123: 50,  # Dakini
    124: 6,  # Silky
    125: 49,  # Bugs
    126: 18,  # Black Ooze
    127: 4,  # Bicorn
    128: 39,  # Mithras
    129: 17,  # Sudama
    130: 11,  # Kodama
    131: 3,  # Agathion
    132: 12,  # Onmoraki
    133: 20,  # Nue
    134: 28,  # Pisaca
    135: 58,  # Melchizedek
    136: 58,  # Baphomet
    137: 55,  # Raja Naga
    138: 24,  # Naga
    139: 52,  # Garuda
    140: 60,  # Moloch
    141: 52,  # Norn
    142: 37,  # Belphegor
    143: 9,  # Berith
    144: 28,  # Choronzon
    151: 22,  # Nigi Mitama
    152: 12,  # Kushi Mitama
    153: 30,  # Ara Mitama
    154: 6,  # Saki Mitama
    156: 82,  # Shiva
    157: 87,  # Michael
    158: 76,  # Asura
    159: 90,  # Mada
    160: 85,  # Mother Harlot
    161: 27,  # Clotho
    162: 35,  # Lachesis
    163: 39,  # Atropos
    164: 84,  # Ardha
    166: 83,  # Vishnu
    167: 40,  # Hariti
    168: 43,  # Yurlungur
    169: 42,  # Hecatoncheires
    170: 95,  # Satanael
    181: 26,  # Orpheus
    182: 65,  # Thanatos
    183: 20,  # Izanagi
    184: 44,  # Magatsu-Izanagi
    185: 16,  # Kaguya
    186: 30,  # Ariadne
    187: 56,  # Asterius
    188: 50,  # Tsukiyomi
    189: 81,  # Messiah
    190: 90,  # Messiah Picaro
    191: 29,  # Orpheus Picaro
    192: 69,  # Thanatos Picaro
    193: 23,  # Izanagi Picaro
    194: 48,  # M. Izanagi Picaro
    195: 25,  # Kaguya Picaro
    196: 42,  # Ariadne Picaro
    197: 62,  # Asterius Picaro
    198: 55,  # Tsukiyomi Picaro
    201: 1,  # Arsene
    252: 92,  # Satan
    253: 93,  # Lucifer
    254: 76,  # Kohryu
    255: 54,  # Okuninushi
    259: 86,  # Futsunushi
    261: 51,  # Seth
    262: 85,  # Ishtar
    266: 69,  # Lakshmi
    272: 46,  # Fortuna
    273: 16,  # Suzaku
    274: 62,  # Seiryu
    275: 7,  # Genbu
    276: 45,  # Byakko
    277: 67,  # Bishamonten
    278: 49,  # Koumokuten
    279: 22,  # Jikokuten
    280: 31,  # Zouchouten
    281: 37,  # Hell Biker
    282: 40,  # Daisoujou
    283: 59,  # Trumpeter
    284: 38,  # White Rider
    285: 17,  # Matador
    286: 54,  # Pale Rider
    287: 47,  # Horus
    289: 82,  # Attis
    292: 80,  # Sraosha
    295: 33,  # Mitra
    296: 21,  # Phoenix
    297: 29,  # Principality
    298: 30,  # Neko Shogun
    299: 68,  # Vasuki
    300: 44,  # Ananta
    303: 66,  # Quetzalcoatl
    304: 41,  # Red Rider
    305: 59,  # Black Rider
    308: 45,  # Pazuzu
    330: 93,  # Maria
    331: 80,  # Vohu Manah
    333: 52,  # Mishaguji
    360: 80,  # Izanagi no Okami
    362: 46,  # Athena
    363: 76,  # Raoul
    365: 11,  # Orpheus (F)
    366: 89,  # Izanagi no Okami Picaro
    368: 50,  # Athena Picaro
    371: 13,  # Orpheus (F) Picaro
    424: 73,  # Macabre
    425: 81,  # Alilat
    426: 34,  # Thunderbird
    427: 86,  # Fafnir
    428: 70,  # Byakhee
    429: 84,  # Hastur
    430: 27,  # Tam Lin
    431: 72,  # Throne
    432: 83,  # Surt
    433: 70,  # Loa
    434: 74,  # Chimera
    435: 65,  # Atavaka
    436: 5,  # Caith Sith
    437: 84,  # Siegfried
}

# Inclusive maximum base level for each of the eight Palace-access tiers.
# These are balance bands, not fixed AP sphere numbers or runtime level caps.
COMPENDIUM_LEVEL_TIERS = (15, 25, 35, 45, 55, 65, 75, 99)


def persona_level_tier(persona_id: int) -> int:
    level = PERSONA_BASE_LEVELS[persona_id]
    return next(tier for tier, maximum in enumerate(COMPENDIUM_LEVEL_TIERS, 1)
                if level <= maximum)
