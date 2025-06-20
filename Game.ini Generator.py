import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

# --- Daten der ARK Game.ini Optionen ---
# Dies muss manuell aus der Wiki-Seite befüllt werden, hier sind alle gewünschten Optionen integriert.
OPTIONS_DATA = {
    # Server Settings (aus Original-Anfrage)
    "bPvEDisableFriendlyFire": {
        "description": "If true, players on the same tribe cannot damage each other.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = friendly fire disabled, False = friendly fire enabled.",
        "section": "ServerSettings"
    },
    "MaxDifficulty": {
        "description": "Sets the maximum wild dino level based on difficulty offset. MaxDifficulty = 1 provides wild dinosaurs up to level 30 (DifficultyOffset 1). MaxDifficulty = 5 provides wild dinosaurs up to level 150 (DifficultyOffset 1).",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = higher max wild dino level.",
        "section": "ServerSettings"
    },
    "DinoDamageMultiplier": {
        "description": "Multiplies the damage dealt by player tamed, ridden, and wild dinosaurs. This affects all wild dinosaurs on the map.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = more damage, Lower value = less damage. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "HarvestAmountMultiplier": {
        "description": "Multiplies the amount of resources harvested from nodes.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = more resources, Lower value = fewer resources. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "XPMultiplier": {
        "description": "Multiplies the amount of experience gained by players.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = more experience, Lower value = less experience. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "bAllowUnlimitedRespecs": {
        "description": "Set to true to allow more than one usage of Mindwipe Tonic without 24 hours cooldown.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = unlimited respecs, False = limited respecs.",
        "section": "ServerSettings"
    },
    "BabyMatureSpeedMultiplier": {
        "description": "Higher number decreases (by percentage) time needed for baby dino to mature.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = faster maturation, Lower value = slower maturation. 1.0 is normal.",
        "section": "ServerSettings"
    },
    # Neue Optionen aus deiner Liste
    "ConfigOverrideItemMaxQuantity": {
        "description": "Allows manually overriding item stack size on a per-item basis. Example: ConfigOverrideItemMaxQuantity=(ItemClassString=\"PrimalItemAmmo_ArrowTranq_C\",Quantity=(MaxItemQuantity=543, bIgnoreMultiplier=true))",
        "type": "complex_string",
        "default": "",
        "value_impact": "Syntax: (ItemClassString=\"<Class Name>\",Quantity=(MaxItemQuantity=<n>, bIgnoreMultiplier=<value>)). Each entry must be on a new line in the INI. Enter one full line at a time.",
        "section": "ServerSettings"
    },
    "bOnlyAllowSpecifiedEngrams": {
        "description": "If true, any Engram not explicitly specified in the OverrideEngramEntries or OverrideNamedEngramEntries list will be hidden. All Items and Blueprints based on hidden Engrams will be removed.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Only explicitly specified Engrams are visible. False = All Engrams visible unless hidden.",
        "section": "ServerSettings"
    },
    "LevelExperienceRampOverrides": {
        "description": "Configure total player and dinosaur levels and XP needed for each. Must list ALL levels sequentially starting from zero. First entry for players, second for dinosaurs. Last 75 levels are for ascension.",
        "type": "multi_line_string",
        "default": "",
        "value_impact": "Syntax: ExperiencePointsForLevel[<n>]=<points>. Enter ONE complete line for Players, then ONE complete line for Dinos. E.g., for players: (ExperiencePointsForLevel[0]=1,ExperiencePointsForLevel[1]=5,...)",
        "section": "ServerSettings"
    },
    "OverridePlayerLevelEngramPoints": {
        "description": "Configure the number of engram points granted to players for each level gained. This option must be repeated for each player level (e.g., 65 times for 65 levels).",
        "type": "multi_line_string",
        "default": "",
        "value_impact": "Syntax: OverridePlayerLevelEngramPoints=<points>. Add one line for each player level you want to define. Each line is separate.",
        "section": "ServerSettings"
    },
    "GlobalSpoilingTimeMultiplier": {
        "description": "Scales the spoiling time of perishables globally. Higher values prolong the time.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = items spoil slower (longer shelf life). Lower value = items spoil faster. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "GlobalItemDecompositionTimeMultiplier": {
        "description": "Scales the decomposition time of dropped items, loot bags etc. globally. Higher values prolong the time.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = dropped items decompose slower. Lower value = faster. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "GlobalCorpseDecompositionTimeMultiplier": {
        "description": "Scales the decomposition time of corpses (player and dinosaur) globally. Higher values prolong the time.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = corpses decompose slower. Lower value = faster. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "HarvestResourceItemAmountClassMultipliers": {
        "description": "Scales on a per-resource type basis, the amount of resources harvested. Higher values increase the amount per swing/attack.",
        "type": "complex_string",
        "default": "",
        "value_impact": "Syntax: (ClassName=\"<classname>\",Multiplier=<value>). Add one line for each resource type. E.g., for 2x thatch: (ClassName=\"PrimalItemResource_Thatch_C\",Multiplier=2.0)",
        "section": "ServerSettings"
    },
    "OverrideMaxExperiencePointsPlayer": {
        "description": "Overrides the Max XP cap of player characters by exact specified amount.",
        "type": "integer",
        "default": "0", # Wiki: N/A, using 0 to indicate no override by default
        "value_impact": "Sets the maximum experience points a player can accumulate. 0 means no override.",
        "section": "ServerSettings"
    },
    "OverrideMaxExperiencePointsDino": {
        "description": "Overrides the Max XP cap of dinosaur characters by exact specified amount.",
        "type": "integer",
        "default": "0", # Wiki: N/A, using 0 to indicate no override by default
        "value_impact": "Sets the maximum experience points a dinosaur can accumulate. 0 means no override.",
        "section": "ServerSettings"
    },
    "PreventDinoTameClassNames": {
        "description": "Prevents taming of specific dinosaurs via classname. E.g. PreventDinoTameClassNames=\"Argent_Character_BP_C\"",
        "type": "multi_line_string",
        "default": "",
        "value_impact": "Enter one ClassName per line to prevent its taming. Each line is separate.",
        "section": "ServerSettings"
    },
    "PreventTransferForClassName": {
        "description": "Prevents transfer of specific dinosaurs via classname. E.g. PreventTransferForClassName=\"Argent_Character_BP_C\"",
        "type": "multi_line_string",
        "default": "",
        "value_impact": "Enter one ClassName per line to prevent its transfer. Each line is separate.",
        "section": "ServerSettings"
    },
    "DinoClassDamageMultipliers": {
        "description": "Multiplies damage dealt by specific wild dinosaurs via classname. Higher values increase the damage dealt.",
        "type": "complex_string",
        "default": "",
        "value_impact": "Syntax: (ClassName=\"<classname>\",Multiplier=<multiplier>). Add one line for each dino type. Each line is separate.",
        "section": "ServerSettings"
    },
    "TamedDinoClassDamageMultipliers": {
        "description": "Multiplies damage dealt by specific tamed dinosaurs via classname. Higher values increase the damage dealt.",
        "type": "complex_string",
        "default": "",
        "value_impact": "Syntax: (ClassName=\"<classname>\",Multiplier=<multiplier>). Add one line for each tamed dino type. Each line is separate.",
        "section": "ServerSettings"
    },
    "DinoClassResistanceMultipliers": {
        "description": "Multiplies resistance of specific wild dinosaurs via classname. Higher values decrease the damage received.",
        "type": "complex_string",
        "default": "",
        "value_impact": "Syntax: (ClassName=\"<classname>\",Multiplier=<multiplier>). Add one line for each dino type. Each line is separate.",
        "section": "ServerSettings"
    },
    "TamedDinoClassResistanceMultipliers": {
        "description": "Multiplies resistance of specific tamed dinosaurs via classname. Higher values decrease the damage received.",
        "type": "complex_string",
        "default": "",
        "value_impact": "Syntax: (ClassName=\"<classname>\",Multiplier=<multiplier>). Add one line for each tamed dino type. Each line is separate.",
        "section": "ServerSettings"
    },
    "ResourceNoReplenishRadiusPlayers": {
        "description": "Allows resources to regrow closer or farther away from players. Values higher than 1 increase the distance.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = resources regrow further from players. Lower value = resources regrow closer. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "ResourceNoReplenishRadiusStructures": {
        "description": "Allows resources to regrow closer or farther away from structures. Values higher than 1 increase the distance.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = resources regrow further from structures. Lower value = resources regrow closer. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "bIncreasePvPRespawnInterval": {
        "description": "If true, enables an optional +1 minute additional respawn that doubles each time if killed by a team within 5 minutes of previous death (timer indicated on Spawn UI). Helps prevent PvO ammo-wasting.",
        "type": "boolean",
        "default": "False", # Wiki: N/A, setting to False as per common sense
        "value_impact": "True = Respawn interval increases with repeated PvP deaths. False = Standard respawn interval.",
        "section": "ServerSettings"
    },
    "IncreasePvPRespawnIntervalCheckPeriod": {
        "description": "Time (in seconds) to check for repeated PvP deaths within for respawn interval increase. (value1)",
        "type": "float",
        "default": "300.0",
        "value_impact": "Higher value = longer period to check for repeated deaths. Requires bIncreasePvPRespawnInterval=True.",
        "section": "ServerSettings"
    },
    "IncreasePvPRespawnIntervalMultiplier": {
        "description": "Multiplier for the additional respawn time (value2) when bIncreasePvPRespawnInterval is active.",
        "type": "float",
        "default": "2.0",
        "value_impact": "Higher value = respawn interval increases more. Requires bIncreasePvPRespawnInterval=True.",
        "section": "ServerSettings"
    },
    "IncreasePvPRespawnIntervalBaseAmount": {
        "description": "Base amount in seconds (value3) for the additional respawn time when bIncreasePvPRespawnInterval is active.",
        "type": "float",
        "default": "60.0",
        "value_impact": "Higher value = higher base additional respawn time. Requires bIncreasePvPRespawnInterval=True.",
        "section": "ServerSettings"
    },
    "bAutoPvETimer": {
        "description": "If true, allows switching from PvE to PvP mode at pre-specified in-game times OR a pre-specified real-world (server-side) times.",
        "type": "boolean",
        "default": "False", # Wiki: N/A, setting to False as per common sense
        "value_impact": "True = Automatic PvE/PvP switching enabled. False = No automatic switching.",
        "section": "ServerSettings"
    },
    "bAutoPvEUseSystemTime": {
        "description": "If true, AutoPvE will use real-world (server-side) time instead of in-game time.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Use system time for AutoPvE. False = Use in-game time. Requires bAutoPvETimer=True.",
        "section": "ServerSettings"
    },
    "AutoPvEStartTimeSeconds": {
        "description": "Start time in seconds (0 to 86400) for AutoPvE mode.",
        "type": "integer",
        "default": "0", # Wiki: N/A, using 0 as placeholder
        "value_impact": "Sets the start time for automatic PvE/PvP switching. Requires bAutoPvETimer=True.",
        "section": "ServerSettings"
    },
    "AutoPvEStopTimeSeconds": {
        "description": "Stop time in seconds (0 to 86400) for AutoPvE mode.",
        "type": "integer",
        "default": "0", # Wiki: N/A, using 0 as placeholder
        "value_impact": "Sets the stop time for automatic PvE/PvP switching. Requires bAutoPvETimer=True.",
        "section": "ServerSettings"
    },
    "bDisableFriendlyFire": {
        "description": "Prevent-Friendly-Fire (among tribesmates/tribesdinos/tribesstructures) option for PvP servers.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Friendly fire disabled on PvP. False = Friendly fire enabled on PvP.",
        "section": "ServerSettings"
    },
    "bFlyerPlatformAllowUnalignedDinoBasing": {
        "description": "If true, Quetz platforms will not allow any non-allied dino to base on them when they are flying.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Non-allied dinos can stand on platforms. False = Only allied dinos.",
        "section": "ServerSettings"
    },
    "bUseCorpseLocator": {
        "description": "If true, you will see a green light beam at the location of your death.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Corpse locator beam enabled. False = No corpse locator.",
        "section": "ServerSettings"
    },
    "MatingIntervalMultiplier": {
        "description": "Higher number increases (on a percentage scale) interval between which dinosaurs can mate.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = longer wait between matings. Lower value = shorter wait. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "MatingSpeedMultiplier": {
        "description": "Higher number increases (by percentage) speed at which dinosaurs mate with each other.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = faster mating. Lower value = slower mating. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "EggHatchSpeedMultiplier": {
        "description": "Higher number decreases (by percentage) time needed for fertilized egg to hatch.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = faster hatching. Lower value = slower hatching. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "BabyFoodConsumptionSpeedMultiplier": {
        "description": "Lower number decreases (by percentage) the speed that baby dinos eat their food.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = babies eat faster. Lower value = babies eat slower. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "CropGrowthSpeedMultiplier": {
        "description": "Higher number increases (by percentage) speed of crop growth.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = faster crop growth. Lower value = slower crop growth. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "LayEggIntervalMultiplier": {
        "description": "Higher number increases (by percentage) time between eggs spawning / being laid.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = longer wait for eggs. Lower value = shorter wait. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "PoopIntervalMultiplier": {
        "description": "Higher number decreases (by percentage) how frequently you can poop.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = less frequent pooping. Lower value = more frequent pooping. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "CropDecaySpeedMultiplier": {
        "description": "Higher number decreases (by percentage) speed of crop decay in plots.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = slower crop decay. Lower value = faster crop decay. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "HairGrowthSpeedMultiplier": {
        "description": "Higher number increases speed of hair growth.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = faster hair growth. Lower value = slower hair growth. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "StructureDamageRepairCooldown": {
        "description": "Option for cooldown period on structure repair from the last time damaged. Set to 0 to disable it.",
        "type": "integer",
        "default": "180",
        "value_impact": "Value in seconds. Higher value = longer cooldown before structures can be repaired again. 0 to disable.",
        "section": "ServerSettings"
    },
    "bPvEAllowTribeWar": {
        "description": "If False, disables capability for Tribes to officially declare war on each other for mutually-agreed-upon period of time.",
        "type": "boolean",
        "default": "True",
        "value_impact": "True = Tribe wars allowed in PvE. False = Tribe wars disabled in PvE.",
        "section": "ServerSettings"
    },
    "bPvEAllowTribeWarCancel": {
        "description": "If True, allows cancellation of an agreed-upon war before it has actually started.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = War cancellation allowed. False = No war cancellation.",
        "section": "ServerSettings"
    },
    "bPassiveDefensesDamageRiderlessDinos": {
        "description": "If True, allow spike walls to damage wild/riderless Dinos.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Passive defenses damage riderless dinos. False = No damage.",
        "section": "ServerSettings"
    },
    "CustomRecipeEffectivenessMultiplier": {
        "description": "Higher number increases (by percentage) the effectiveness of a custom recipe.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = more effective custom recipes. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "CustomRecipeSkillMultiplier": {
        "description": "Higher number increases (by percentage) the effect of the players crafting speed level that is used as a base for the formula in creating a custom recipe.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = greater impact of crafting speed on custom recipes. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "DinoHarvestingDamageMultiplier": {
        "description": "Higher number increases (by percentage) the damage done to a harvestable item/entity by a Dino. The higher number, the faster you collect.",
        "type": "float",
        "default": "3.2",
        "value_impact": "Higher value = dinos collect resources faster. Lower value = slower. 3.2 is normal.",
        "section": "ServerSettings"
    },
    "PlayerHarvestingDamageMultiplier": {
        "description": "Higher number increases (by percentage) the damage done to a harvestable item/entity by a Player. The higher number, the faster you collect.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = players collect resources faster. Lower value = slower. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "DinoTurretDamageMultiplier": {
        "description": "Higher number increases (by percentage) the damage done by Turrets towards a Dino.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = turrets deal more damage to dinos. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "bDisableLootCrates": {
        "description": "If True, prevent spawning of Loot crates (artifact crates will still spawn).",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Loot crates disabled. False = Loot crates enabled.",
        "section": "ServerSettings"
    },
    "SupplyCrateLootQualityMultiplier": {
        "description": "Increases the quality of items that have a quality in the supply crates. Range = 1 to 5.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = higher quality items from supply crates. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "FishingLootQualityMultiplier": {
        "description": "Increases the quality of items that have a quality when fishing. Range = 1 to 5.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = higher quality items from fishing. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "KickIdlePlayersPeriod": {
        "description": "Time after which characters that have not moved or interacted will be kicked (if -EnableIdlePlayerKick as command line parameter is set). Value is in seconds.",
        "type": "integer",
        "default": "3600",
        "value_impact": "Higher value = longer idle time before players are kicked. 0 to disable.",
        "section": "ServerSettings"
    },
    "TribeSlotReuseCooldown": {
        "description": "Locks a tribe slot for the value in seconds, so a value of 3600 would mean that if someone leaves the tribe, their place cannot be taken by another player (or rejoin) for 1 hour. Used on Official Small Tribes Servers.",
        "type": "float",
        "default": "0.0",
        "value_impact": "Value in seconds. Higher value = longer cooldown for tribe slot reuse. 0 to disable.",
        "section": "ServerSettings"
    },
    "MaxNumberOfPlayersInTribe": {
        "description": "Set this to a number > 0 to act as a limit. 1 Player Tribes effectively disables Tribes.",
        "type": "integer",
        "default": "0", # Wiki: N/A, assuming 0 for no limit
        "value_impact": "Sets the maximum number of players allowed in a tribe. 0 means no limit.",
        "section": "ServerSettings"
    },
    "BabyImprintingStatScaleMultiplier": {
        "description": "How much of an effect on stats the Imprinting Quality has. Set it to 0 to effectively disable the system.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = greater stat bonus from imprinting. 0 to disable imprinting stats.",
        "section": "ServerSettings"
    },
    "BabyImprintAmountMultiplier": {
        "description": "Multiplier applied to the percentage each imprints provide. For example, if an imprint usually give 10%, setting this multiplier to 0.5 means they would now give 5% each. This multiplier is global.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = each imprint gives more progress. Lower value = less progress. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "BabyCuddleIntervalMultiplier": {
        "description": "How often Babies wanna cuddle. More often means you'll need to cuddle with them more frequently to gain Imprinting Quality.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = less frequent cuddles needed. Lower value = more frequent cuddles needed. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "BabyCuddleGracePeriodMultiplier": {
        "description": "A multiplier on how long after delaying cuddling with the Baby before Imprinting Quality starts to decrease.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = longer grace period before imprint quality decreases. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "BabyCuddleLoseImprintQualitySpeedMultiplier": {
        "description": "A multiplier on how fast Imprinting Qualitiy decreases after the grace period if you haven't yet cuddled with the Baby.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = faster quality decrease after grace period. Lower value = slower quality decrease. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "ConfigOverrideItemCraftingCosts": {
        "description": "Allows overriding item crafting costs. Currently doesn't change repair cost and demolish refund of edited structures. Note: if using stack mods, refer to mod new resources instead of vanilla ones.",
        "type": "complex_string",
        "default": "",
        "value_impact": "Syntax example: (ItemClassString=\"PrimalItem_WeaponShotgun_C\",BaseCraftingResourceRequirements=((ResourceItemClassString=\"PrimalItemResource_Wood_C\",BaseResourceRequirement=100,bCraftingStationUsage=False,bDisplayOnly=False)))",
        "section": "ServerSettings" # This is often under [ServerSettings] but can be in a dedicated section depending on game version
    },
    "ConfigOverrideSupplyCrateItems": {
        "description": "Allows overriding items found in supply crates.",
        "type": "complex_string",
        "default": "",
        "value_impact": "Complex syntax: See wiki for detailed structure (MinItemSets, MaxItemSets, ItemSets with multiple ItemEntries etc.).",
        "section": "ServerSettings" # This is often under [ServerSettings]
    },
    "ExcludeItemIndices": {
        "description": "Exclude an item from supply crates. You can have multiple lines of this option.",
        "type": "multi_line_string",
        "default": "",
        "value_impact": "Enter one Item ID per line to exclude it from supply crates. Each line is separate.",
        "section": "ServerSettings"
    },
    "MaxTribeLogs": {
        "description": "How many Tribe logs are displayed for each tribe.",
        "type": "integer",
        "default": "100",
        "value_impact": "Sets the maximum number of tribe logs displayed. Higher value = more logs.",
        "section": "ServerSettings"
    },
    "PvPZoneStructureDamageMultiplier": {
        "description": "Specifies the scaling factor for damage structures take within caves. The lower the value, the less damage the structure takes.",
        "type": "float",
        "default": "6.0",
        "value_impact": "Higher value = more damage to structures in caves. Lower value = less damage. 6.0 is normal.",
        "section": "ServerSettings"
    },
    "bDisableDinoRiding": {
        "description": "If True, disables dino riding.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Dino riding disabled. False = Dino riding enabled.",
        "section": "ServerSettings"
    },
    "bDisableDinoTaming": {
        "description": "If True, disables dino taming.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Dino taming disabled. False = Dino taming enabled.",
        "section": "ServerSettings"
    },
    "bDisableStructurePlacementCollision": {
        "description": "If 'True' allows for structures to clip into the terrain.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Structures can clip into terrain. False = Normal collision.",
        "section": "ServerSettings"
    },
    "bAllowCustomRecipes": {
        "description": "If True, enables custom recipes.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Custom recipes enabled. False = Custom recipes disabled.",
        "section": "ServerSettings"
    },
    "bAutoUnlockAllEngrams": {
        "description": "Unlocks all Engrams available. Ignores OverrideEngramEntries and OverrideNamedEngramEntries entries.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = All engrams unlocked automatically. False = Engrams must be learned.",
        "section": "ServerSettings"
    },
    "EngramEntryAutoUnlocks": {
        "description": "Automatically unlocks the specified Engram when reaching the level specified.",
        "type": "complex_string",
        "default": "",
        "value_impact": "Syntax: (EngramClassName=\"<index>\",LevelToAutoUnlock=<value>). Add one line for each engram to auto-unlock. Each line is separate.",
        "section": "ServerSettings"
    },
    "bHardLimitTurretsInRange": {
        "description": "Enables a hard limit for turrets in range.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Turrets have a hard range limit. False = No hard limit.",
        "section": "ServerSettings"
    },
    "bShowCreativeMode": {
        "description": "Enables creative mode.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Creative mode enabled. False = Creative mode disabled.",
        "section": "ServerSettings"
    },
    "PreventOfflinePvPConnectionInvincibleInterval": {
        "description": "Time in seconds (float) players are invincible after connecting in PvP. Default = 5.0.",
        "type": "float",
        "default": "5.0",
        "value_impact": "Value in seconds. Higher value = longer invincibility after connection. 5.0 is normal.",
        "section": "ServerSettings"
    },
    "TamedDinoCharacterFoodDrainMultiplier": {
        "description": "A multiplier on how fast tame dinos consume food.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = tamed dinos consume food faster. Lower value = slower consumption. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "WildDinoCharacterFoodDrainMultiplier": {
        "description": "A multiplier on how fast wild dinos consume food.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = wild dinos consume food faster. Lower value = slower consumption. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "WildDinoTorporDrainMultiplier": {
        "description": "A multiplier on how fast wild dinos lose torpor.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = wild dinos lose torpor faster. Lower value = slower torpor drain. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "PassiveTameIntervalMultiplier": {
        "description": "A multiplier on how often you get tame requests for passive tame dinos.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = less frequent passive tame requests. Lower value = more frequent. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "TamedDinoTorporDrainMultiplier": {
        "description": "A multiplier on how fast tamed dinos lose torpor.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = tamed dinos lose torpor faster. Lower value = slower torpor drain. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "KillXPMultiplier": {
        "description": "A multiplier to scale the amount of XP earned for a kill.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = more XP from kills. Lower value = less XP. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "HarvestXPMultiplier": {
        "description": "A multiplier to scale the amount of XP earned for harvesting.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = more XP from harvesting. Lower value = less XP. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "CraftXPMultiplier": {
        "description": "A multiplier to scale the amount of XP earned for crafting.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = more XP from crafting. Lower value = less XP. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "GenericXPMultiplier": {
        "description": "A multiplier to scale the amount of XP earned for generic XP (automatic over time).",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = more passive XP. Lower value = less passive XP. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "SpecialXPMultiplier": {
        "description": "A multiplier to scale the amount of XP earned for SpecialEvents.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = more XP from special events. Lower value = less XP. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "ModIDS": {
        "description": "Specify a manual list of extra Steam Workshop Mods/Maps/TC ID's to download/install/update in your Game.ini via (with the commandline(-automanagedmods) as normal to actually use them in-game).",
        "type": "multi_line_string", # Typically multiple ModIDs, one per line
        "default": "",
        "value_impact": "Enter one ModID per line. Each line is separate. This section is usually [ModInstaller].",
        "section": "ModInstaller"
    },
    "FastDecayInterval": {
        "description": "Enable this option for a fixed constant decay period for \"Fast Decay\" structures (such as pillars or lone foundations). Value is in seconds.",
        "type": "integer",
        "default": "43200",
        "value_impact": "Value in seconds. Higher value = longer decay period for fast decay structures. 43200 is default.",
        "section": "ServerSettings"
    },
    "MaxAlliancesPerTribe": {
        "description": "Define the maximum alliances a tribe can form or be part of.",
        "type": "integer",
        "default": "0", # Wiki: N/A, assuming 0 for no limit
        "value_impact": "Sets the maximum number of alliances a tribe can form. 0 means no limit.",
        "section": "ServerSettings"
    },
    "MaxTribesPerAlliance": {
        "description": "Define the maximum of tribes in an alliance.",
        "type": "integer",
        "default": "0", # Wiki: N/A, assuming 0 for no limit
        "value_impact": "Sets the maximum number of tribes allowed in an alliance. 0 means no limit.",
        "section": "ServerSettings"
    },
    "bUseTameLimitForStructuresOnly": {
        "description": "If true, Tame Units will only be applied and used for Platforms with Structures and Rafts, effectively disabling Tame Units for Dinos without Platform Structures.",
        "type": "boolean",
        "default": "False", # Wiki: N/A, assuming false
        "value_impact": "True = Tame limit applies only to structures on platforms/rafts. False = Tame limit applies to all tamed dinos.",
        "section": "ServerSettings"
    },
    "UseCorpseLifeSpanMultiplier": {
        "description": "Modifies corpse AND dropped box lifespan.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = longer lifespan for corpses and dropped items. Lower value = shorter lifespan. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "FuelConsumptionIntervalMultiplier": {
        "description": "Define the interval of fuel consumption.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = fuel lasts longer. Lower value = fuel consumed faster. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "GlobalPoweredBatteryDurabilityDecreasePerSecond": {
        "description": "Global decrease rate of durability for powered batteries per second.",
        "type": "float",
        "default": "3.0",
        "value_impact": "Higher value = faster battery durability decrease. Lower value = slower decrease. 3.0 is normal.",
        "section": "ServerSettings"
    },
    "DestroyTamesOverLevelClamp": {
        "description": "Tames that exceed that level will be deleted on server start. Official servers have it set to 449.",
        "type": "integer",
        "default": "0",
        "value_impact": "Sets the maximum level for tamed creatures. Tames above this level will be deleted. 0 to disable.",
        "section": "ServerSettings"
    },
    "LimitNonPlayerDroppedItemsRange": {
        "description": "Limit the number of dropped items in an area (together with LimitNonPlayerDroppedItemsCount). Official servers have it set to 1600.",
        "type": "integer",
        "default": "0",
        "value_impact": "Value in units (e.g., 1600). Higher value = larger range for item limit. 0 to disable.",
        "section": "ServerSettings"
    },
    "LimitNonPlayerDroppedItemsCount": {
        "description": "Limit the number of dropped items in an area (together with LimitNonPlayerDroppedItemsRange). Official servers have it set to 600.",
        "type": "integer",
        "default": "0",
        "value_impact": "Sets the maximum number of dropped items allowed in the specified range (e.g., 600). 0 to disable.",
        "section": "ServerSettings"
    },
    "MaxFallSpeedMultiplier": {
        "description": "Defines the falling speed multiplier at which players start taking fall damage. Higher value = players can fall longer without damage.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = players can fall further without damage. Lower value = fall damage sooner. 1.0 is normal.",
        "section": "ServerSettings"
    },
    "bIgnoreStructuresPreventionVolumes": {
        "description": "If true, enables building in Mission Volumes on Genesis Part 1.",
        "type": "boolean",
        "default": "True",
        "value_impact": "True = Building allowed in Genesis Mission Volumes. False = Building restricted.",
        "section": "ServerSettings"
    },
    "bGenesisUseStructuresPreventionVolumes": {
        "description": "If true, disables building in mission areas on Genesis Part 1.",
        "type": "boolean",
        "default": "True",
        "value_impact": "True = Building restricted in Genesis Mission Areas. False = Building allowed.",
        "section": "ServerSettings"
    },
    "bAllowFlyerSpeedLeveling": {
        "description": "Specifies whether flyer creatures can have their Movement Speed leveled up.",
        "type": "boolean",
        "default": "False",
        "value_impact": "True = Flyer speed can be leveled. False = Flyer speed cannot be leveled.",
        "section": "ServerSettings"
    },
    "CraftingSkillBonusMultiplier": {
        "description": "A multiplier to modify the bonus received from upgrading the Crafting Skill.",
        "type": "float",
        "default": "1.0",
        "value_impact": "Higher value = greater bonus from Crafting Skill. Lower value = smaller bonus. 1.0 is normal.",
        "section": "ServerSettings"
    }
}

class ArkIniGenerator:
    def __init__(self, master):
        self.master = master
        master.title("ARK: Survival Ascended Game.ini Generator")
        master.geometry("1000x700")

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=3)
        self.master.grid_rowconfigure(0, weight=1)

        # Initialisiere current_settings mit Standardwerten
        self.current_settings = {option: OPTIONS_DATA[option]["default"] for option in OPTIONS_DATA}

        # --- Linke Seite: Optionen-Liste ---
        self.frame_options = tk.Frame(master, bd=2, relief="groove")
        self.frame_options.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_options.grid_rowconfigure(0, weight=1)
        self.frame_options.grid_columnconfigure(0, weight=1)

        self.listbox_options = tk.Listbox(self.frame_options)
        self.listbox_options.pack(fill="both", expand=True)
        self.listbox_options.bind("<<ListboxSelect>>", self.on_option_select)

        # Fülle die Liste mit sortierten Optionsnamen
        for option_name in sorted(OPTIONS_DATA.keys()):
            self.listbox_options.insert(tk.END, option_name)

        # --- Rechte Seite: Detailansicht ---
        self.frame_details = tk.Frame(master, bd=2, relief="groove")
        self.frame_details.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        # NEUE ANPASSUNG: Reduziere das Gewicht der Zeile für die Beschreibung
        # Anstatt weight=1, das es maximal ausdehnt, lassen wir es ohne weight,
        # damit es nur den benötigten Platz einnimmt.
        # self.frame_details.grid_rowconfigure(2, weight=1) # AUSKOMMENTIERT oder auf weight=0 gesetzt
        self.frame_details.grid_rowconfigure(2, weight=0) # Setze weight auf 0, um unnötige Ausdehnung zu verhindern
        self.frame_details.grid_columnconfigure(0, weight=1)


        # Labels und Eingabefelder für Details
        tk.Label(self.frame_details, text="Option Name:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.option_name_label = tk.Label(self.frame_details, text="", font=("TkDefaultFont", 10, "bold"))
        self.option_name_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        tk.Label(self.frame_details, text="Current Value:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.value_entry_frame = tk.Frame(self.frame_details)
        self.value_entry_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.value_entry = tk.Entry(self.value_entry_frame)
        self.value_entry.pack(side="left", fill="x", expand=True)
        self.value_entry.bind("<KeyRelease>", self.on_value_change)

        self.boolean_var = tk.BooleanVar()
        self.boolean_checkbox = tk.Checkbutton(self.value_entry_frame, variable=self.boolean_var,
                                               command=self.on_boolean_change)
        self.boolean_checkbox.pack_forget() # Checkbox anfangs versteckt

        tk.Label(self.frame_details, text="Description:").grid(row=2, column=0, sticky="nw", padx=5, pady=2)
        # NEUE ANPASSUNG: Reduziere die Höhe des ScrolledText-Widgets
        self.description_text = scrolledtext.ScrolledText(self.frame_details, wrap=tk.WORD, width=60, height=4) # Höhe reduziert
        self.description_text.grid(row=2, column=1, sticky="nsew", padx=5, pady=2)
        self.description_text.config(state=tk.DISABLED) # Nur lesbar

        tk.Label(self.frame_details, text="Value Impact:").grid(row=3, column=0, sticky="nw", padx=5, pady=2)
        self.value_impact_text = scrolledtext.ScrolledText(self.frame_details, wrap=tk.WORD, width=60, height=5)
        self.value_impact_text.grid(row=3, column=1, sticky="nsew", padx=5, pady=2)
        self.value_impact_text.config(state=tk.DISABLED) # Nur lesbar

        # --- Unterer Bereich: Generieren Button ---
        self.frame_bottom = tk.Frame(master)
        self.frame_bottom.grid(row=1, column=0, columnspan=2, pady=10)

        self.generate_button = tk.Button(self.frame_bottom, text="Generate Game.ini", command=self.generate_ini_file)
        self.generate_button.pack(padx=10, pady=5)

        self.selected_option = None # Speichert die aktuell ausgewählte Option

    def on_option_select(self, event):
        """Wird aufgerufen, wenn eine Option in der Liste ausgewählt wird."""
        if not self.listbox_options.curselection():
            return

        selected_index = self.listbox_options.curselection()[0]
        self.selected_option = self.listbox_options.get(selected_index)
        data = OPTIONS_DATA[self.selected_option]

        self.option_name_label.config(text=self.selected_option)

        # Beschreibung aktualisieren
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert(tk.END, data["description"])
        self.description_text.config(state=tk.DISABLED)

        # Wert-Auswirkung aktualisieren
        self.value_impact_text.config(state=tk.NORMAL)
        self.value_impact_text.delete("1.0", tk.END)
        self.value_impact_text.insert(tk.END, data["value_impact"])
        self.value_impact_text.config(state=tk.DISABLED)

        # Eingabefeldtyp anpassen (Checkbox oder Texteingabe)
        self.value_entry.pack_forget()
        self.boolean_checkbox.pack_forget()

        if data["type"] == "boolean":
            self.boolean_var.set(self.current_settings[self.selected_option] == "True")
            self.boolean_checkbox.pack(side="left")
        else:
            self.value_entry.delete(0, tk.END)
            self.value_entry.insert(0, str(self.current_settings[self.selected_option]))
            self.value_entry.pack(side="left", fill="x", expand=True)

    def on_value_change(self, event=None):
        """Wird bei Änderungen im Texteingabefeld aufgerufen."""
        if self.selected_option and OPTIONS_DATA[self.selected_option]["type"] != "boolean":
            self.current_settings[self.selected_option] = self.value_entry.get()

    def on_boolean_change(self):
        """Wird bei Änderungen der Checkbox aufgerufen."""
        if self.selected_option and OPTIONS_DATA[self.selected_option]["type"] == "boolean":
            self.current_settings[self.selected_option] = str(self.boolean_var.get())

    def generate_ini_file(self):
        """Generiert die Game.ini-Datei basierend auf den aktuellen Einstellungen."""
        ini_content = {}
        for option, value in self.current_settings.items():
            # Überspringe leere Werte für komplexe/mehrzeilige Optionen, es sei denn, sie sind explizit der Standard
            if (OPTIONS_DATA[option]["type"] in ["complex_string", "multi_line_string"] and not value):
                continue

            section = OPTIONS_DATA[option]["section"]
            if section not in ini_content:
                ini_content[section] = []
            ini_content[section].append(f"{option}={value}")

        output_string = ""
        # Sortiere Sektionen alphabetisch für eine bessere Lesbarkeit der Ausgabe
        for section in sorted(ini_content.keys()):
            output_string += f"[{section}]\n"
            # Sortiere Optionen innerhalb jeder Sektion alphabetisch
            for option_line in sorted(ini_content[section]):
                output_string += f"{option_line}\n"
            output_string += "\n" # Füge eine Leerzeile zwischen Sektionen für bessere Lesbarkeit hinzu

        file_path = filedialog.asksaveasfilename(
            defaultextension=".ini",
            filetypes=[("INI files", "*.ini")],
            initialfile="Game.ini"
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(output_string)
                messagebox.showinfo("Success", f"Game.ini successfully saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save Game.ini:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ArkIniGenerator(root)
    root.mainloop()