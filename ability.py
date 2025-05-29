import streamlit as st
import itertools

DEFAULT_BASE_ABILITY_POWER = 100
DEFAULT_MAX_COST = 20000

# Item format as dicts
ITEMS = [
    {
        "Name": "Icy Coolant",
        "Ability Power": 0,
        "CDR": 5,
        "Cost": 5000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Hardlight Accelerator",
        "Ability Power": 0,
        "CDR": 10,
        "Cost": 11000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Power Playbook",
        "Ability Power": 10,
        "CDR": 0,
        "Cost": 1000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Custom Stock",
        "Ability Power": 10,
        "CDR": 0,
        "Cost": 3750,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Biolight Overflow",
        "Ability Power": 5,
        "CDR": 0,
        "Cost": 3750,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Energized Bracers",
        "Ability Power": 10,
        "CDR": 0,
        "Cost": 4000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Wristwraps",
        "Ability Power": 5,
        "CDR": 0,
        "Cost": 4000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Multitool",
        "Ability Power": 10,
        "CDR": 5,
        "Cost": 4500,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Nano cola",
        "Ability Power": 20,
        "CDR": 0,
        "Cost": 6000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Threetap Tommygun",
        "Ability Power": 10,
        "CDR": 0,
        "Cost": 9500,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Biotech Maximizer",
        "Ability Power": 10,
        "CDR": 10,
        "Cost": 10000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Catalytic Crystal",
        "Ability Power": 15,
        "CDR": 0,
        "Cost": 10000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Lumerico Fusion Drive",
        "Ability Power": 15,
        "CDR": 0,
        "Cost": 10000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "SuperFlexor",
        "Ability Power": 25,
        "CDR": 0,
        "Cost": 10000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Cybervenom",
        "Ability Power": 10,
        "CDR": 5,
        "Cost": 10000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Iridescent Iris",
        "Ability Power": 20,
        "CDR": 10,
        "Cost": 11000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Liquid Nitrogen",
        "Ability Power": 10,
        "CDR": 0,
        "Cost": 13000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Mark of the Kitsune",
        "Ability Power": 10,
        "CDR": 0,
        "Cost": 11000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Champion's Kit",
        "Ability Power": 35,
        "CDR": 0,
        "Cost": 14000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Ironclad Exhaust Ports",
        "Ability Power": 0,
        "CDR": 5,
        "Cost": 4000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Martian Mender",
        "Ability Power": 0,
        "CDR": 10,
        "Cost": 10000,
        "Required": 0,
        "Character": "all"
    },
    {
        "Name": "Eye of the Yokai",
        "Ability Power": 10.01,
        "CDR": 0,
        "Cost": 4000,
        "Required": 0,
        "Character": "kiriko"
    },
    {
        "Name": "Donut Delivery",
        "Ability Power": 10.01,
        "CDR": 0,
        "Cost": 10000,
        "Required": 0,
        "Character": "kiriko"
    },
    {
        "Name": "Our Bikes",
        "Ability Power": 15.01,
        "CDR": 0,
        "Cost": 10000,
        "Required": 0,
        "Character": "kiriko"
    },
    {
        "Name": "Talisman of Velocity",
        "Ability Power": 15.01,
        "CDR": 0,
        "Cost": 10000,
        "Required": 0,
        "Character": "kiriko"
    },
    {
        "Name": "Talisman of Life",
        "Ability Power": 20.01,
        "CDR": 0,
        "Cost": 11000,
        "Required": 0,
        "Character": "kiriko"
    },
    {
        "Name": "Lock on shield",
        "Ability Power": 10.01,
        "CDR": 0,
        "Cost": 4000,
        "Required": 0,
        "Character": "juno"
    },
    {
        "Name": "Lux Loop",
        "Ability Power": 10.01,
        "CDR": 0,
        "Cost": 4000,
        "Required": 0,
        "Character": "juno"
    },
    {
        "Name": "Pulsar Destroyers",
        "Ability Power": 0,
        "CDR": 0,
        "Cost": 10000,
        "Required": 0,
        "Character": "juno"
    },
    {
        "Name": "Solar Shielding",
        "Ability Power": 15.01,
        "CDR": 0,
        "Cost": 10000,
        "Required": 0,
        "Character": "juno"
    },
    {
        "Name": "Red Promise Regulator",
        "Ability Power": 15.02,
        "CDR": 0,
        "Cost": 10000,
        "Required": 0,
        "Character": "juno"
    },
    {
        "Name": "Pulse Spike",
        "Ability Power": 0,
        "CDR": 0,
        "Cost": 11000,
        "Required": 0,
        "Character": "juno"
    },
    {
        "Name": "Boosted Rockets",
        "Ability Power": 0,
        "CDR": 0,
        "Cost": 4000,
        "Required": 0,
        "Character": "juno"
    },
    {
        "Name": "Sturdy Snowfort",
        "Ability Power": 15.01,
        "CDR": 0,
        "Cost": 10000,
        "Required": 0,
        "Character": "mei"
    },
    {
        "Name": "Icy Veins",
        "Ability Power": 10.01,
        "CDR": 0,
        "Cost": 10000,
        "Required": 0,
        "Character": "mei"
    },
]


def filter_items(character, exclude_names):
    return [
        item for item in ITEMS
        if item["Name"] not in exclude_names and
        (character == "Generic" and item["Character"] == "all" or
         character != "Generic" and (item["Character"] == "all" or item["Character"] == character))
    ]

def calculate(combo, ignore_cdr, base_ability_power, base_cooldown):
    ap_bonus = sum(item["Ability Power"] for item in combo) / 100
    cdr_bonus = min(sum(item["CDR"] for item in combo) / 100, 0.99)
    cost = sum(item["Cost"] for item in combo)
    final_ap = base_ability_power * (1 + ap_bonus)

    pulsar_bonus = 0
    if any(item["Name"] == "Pulsar Destroyers" for item in combo):
        pulsar_bonus = 20 * (1 + ap_bonus)
        final_ap += pulsar_bonus

    cooldown_eff = 1.0 if ignore_cdr else 1 / (1 - cdr_bonus)
    output = final_ap if ignore_cdr else final_ap * cooldown_eff

    return output, ap_bonus, cdr_bonus, final_ap, cooldown_eff, cost, pulsar_bonus

def find_best_combo(items, max_items, max_cost, ignore_cdr, cdr_only, base_ability_power, base_cooldown):
    required = [i for i in items if i["Required"] == 1]
    optional = [i for i in items if i["Required"] == 0]
    best = (None, 0, ())

    for r in range(0, max_items - len(required) + 1):
        for combo in itertools.combinations(optional, r):
            full_combo = required + list(combo)
            if len(full_combo) > max_items:
                continue
            output, ap, cdr, ap_final, ceff, cost, pulsar = calculate(full_combo, ignore_cdr, base_ability_power, base_cooldown)
            if cost > max_cost:
                continue
            value = cdr if cdr_only else output
            if value > best[1] or (value == best[1] and cost < best[2][-2] if best[2] else True):
                best = (full_combo, value, (ap, cdr, ap_final, ceff, cost, pulsar))

    return best

# --- Streamlit UI ---

st.title("Ability Optimizer")

base_ability_power = st.number_input("Base Ability Power", min_value=1, value=DEFAULT_BASE_ABILITY_POWER, step=1)
base_cooldown = st.number_input("Base Cooldown (seconds)", min_value=0.1, value=10.0, step=0.1, format="%.2f")

# Get all characters present (except 'all'), add 'Generic' option
characters = sorted(set(item["Character"] for item in ITEMS if item["Character"] != "all"))
characters.insert(0, "Generic")

character = st.selectbox("Select Character", characters)

blacklist_names = st.multiselect("Blacklist Items", options=[item["Name"] for item in ITEMS])

filtered = filter_items(character, blacklist_names)
item_names = [item["Name"] for item in filtered]

required_names = st.multiselect("Select Required Items", options=item_names)

# Update 'Required' flag in filtered items based on required_names
filtered = [
    {
        "Name": item["Name"],
        "Ability Power": item["Ability Power"],
        "CDR": item["CDR"],
        "Cost": item["Cost"],
        "Required": 1 if item["Name"] in required_names else 0,
        "Character": item["Character"]
    }
    for item in filtered
]

ignore_cdr = st.checkbox("Ignore Cooldown Reduction", value=True)
cdr_only = st.checkbox("Optimize Only Cooldowns")
max_items = st.slider("Max Number of Items", 1, 6, 6)
max_cost = st.number_input("Max Total Cost", min_value=0, max_value=150000, value=DEFAULT_MAX_COST, step=1000)

best_combo, value, stats = find_best_combo(filtered, max_items, max_cost, ignore_cdr, cdr_only, base_ability_power, base_cooldown)

if best_combo:
    st.subheader("Best Combo:")
    for item in best_combo:
        st.write(f"- {item['Name']} (AP: {item['Ability Power']}%, CDR: {item['CDR']}%, Cost: {item['Cost']})")

    ap_bonus, cdr_bonus, final_ap, cooldown_eff, total_cost, pulsar_bonus = stats
    st.markdown("---")
    st.write(f"**Total Cost:** {total_cost} / {max_cost}")
    st.write(f"**Remaining Money:** {max_cost - total_cost}")
    st.write(f"**Total AP Bonus:** {ap_bonus * 100:.2f}%")
    st.write(f"**Total Cooldown Reduction:** {cdr_bonus * 100:.2f}%")

    if not cdr_only:
        st.write(f"**Final Ability Power:** {final_ap:.2f}")
        if pulsar_bonus > 0:
            st.write(f"**Pulsar Destroyers Bonus:** +{pulsar_bonus:.2f}")
        if ignore_cdr:
            st.write(f"**Cooldown Reduction Ignored**")
        else:
            effective_cooldown = base_cooldown * (1 - cdr_bonus)
            st.write(f"**Cooldown Efficiency:** x{cooldown_eff:.2f}")
            st.write(f"**Effective Cooldown:** {effective_cooldown:.2f}s")
        st.success(f"Max Effective Ability Output: {value:.2f}")
    else:
        effective_cooldown = base_cooldown * (1 - cdr_bonus)
        st.success(f"Max Cooldown Reduction: {cdr_bonus * 100:.2f}% (Cooldown: {effective_cooldown:.2f}s)")
else:
    st.error("No valid combination found within cost and item limits.")
