import streamlit as st
import itertools

DEFAULT_BASE_ABILITY_POWER = 100
DEFAULT_MAX_COST = 20000

# Item format: (name, ap%, cdr%, cost, required, character)
ITEMS = [
    ("Icy Coolant", 0, 5, 5000, 0, "all"),
    ("Hardlight Accelerator", 0, 10, 11000, 0, "all"),
    ("Power Playbook", 10, 0, 1000, 0, "all"),
    ("Custom Stock", 10, 0, 3750, 0, "all"),
    ("Biolight Overflow", 5, 0, 3750, 0, "all"),
    ("Energized Bracers", 10, 0, 4000, 0, "all"),
    ("Wristwraps", 5, 0, 4000, 0, "all"),
    ("Multitool", 10, 5, 4500, 0, "all"),
    ("Nano cola", 20, 0, 6000, 0, "all"),
    ("Threetap Tommygun", 10, 0, 9500, 0, "all"),
    ("Biotech Maximizer", 10, 10, 10000, 0, "all"),
    ("Catalytic Crystal", 15, 0, 10000, 0, "all"),
    ("Lumerico Fusion Drive", 15, 0, 10000, 0, "all"),
    ("SuperFlexor", 25, 0, 10000, 0, "all"),
    ("Cybervenom", 10, 5, 10000, 0, "all"),
    ("Iridescent Iris", 20, 10, 11000, 0, "all"),
    ("Liquid Nitrogen", 10, 0, 13000, 0, "all"),
    ("Mark of the Kitsune", 10, 0, 11000, 0, "all"),
    ("Champion's Kit", 35, 0, 14000, 0, "all"),
    ("Ironclad Exhaust Ports", 0, 5, 4000, 0, "all"),
    ("Martian Mender", 0, 10, 10000, 0, "all"),
    ("Eye of the Yokai", 10.01, 0, 4000, 0, "kiriko"),
    ("Donut Delivery", 10.01, 0, 10000, 0, "kiriko"),
    ("Our Bikes", 15.01, 0, 10000, 0, "kiriko"),
    ("Talisman of Velocity", 15.01, 0, 10000, 0, "kiriko"),
    ("Talisman of Life", 20.01, 0, 11000, 0, "kiriko"),
    ("Lock on shield", 10.01, 0, 4000, 0, "juno"),
    ("Lux Loop", 10.01, 0, 4000, 0, "juno"),
    ("Pulsar Destroyers", 0, 0, 10000, 0, "juno"),
    ("Solar Shielding", 15.01, 0, 10000, 0, "juno"),
    ("Red Promise Regulator", 15.02, 0, 10000, 0, "juno"),
    ("Pulse Spike", 0 , 0, 11000, 0, "juno"),
    ("Boosted Rockets", 0 , 0, 4000, 0, "juno"),
    ("Sturdy Snowfort", 15.01, 0, 10000, 0, "mei"),
    ("Icy Veins", 10.01, 0, 10000, 0, "mei"),
]

def filter_items(character, exclude_names):
    return [item for item in ITEMS if item[0] not in exclude_names and (character == "Generic" and item[5] == "all" or character != "Generic" and (item[5] == "all" or item[5] == character))]

def calculate(combo, ignore_cdr, base_ability_power, base_cooldown):
    ap_bonus = sum(item[1] for item in combo) / 100
    cdr_bonus = min(sum(item[2] for item in combo) / 100, 0.99)
    cost = sum(item[3] for item in combo)
    final_ap = base_ability_power * (1 + ap_bonus)

    pulsar_bonus = 0
    if any(item[0] == "Pulsar Destroyers" for item in combo):
        pulsar_bonus = 20 * (1 + ap_bonus)
        final_ap += pulsar_bonus

    cooldown_eff = 1.0 if ignore_cdr else 1 / (1 - cdr_bonus)
    output = final_ap if ignore_cdr else final_ap * cooldown_eff

    return output, ap_bonus, cdr_bonus, final_ap, cooldown_eff, cost, pulsar_bonus

def find_best_combo(items, max_items, max_cost, ignore_cdr, cdr_only, base_ability_power, base_cooldown):
    required = [i for i in items if i[4] == 1]
    optional = [i for i in items if i[4] == 0]
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

characters = sorted(set(i[5] for i in ITEMS if i[5] != "all"))
characters.insert(0, "Generic")
character = st.selectbox("Select Character", characters)

blacklist_names = st.multiselect("Blacklist Items", options=[item[0] for item in ITEMS])

filtered = filter_items(character, blacklist_names)
item_names = [item[0] for item in filtered]
required_names = st.multiselect("Select Required Items", options=item_names)

filtered = [
    (item[0], item[1], item[2], item[3], 1 if item[0] in required_names else 0, item[5])
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
        st.write(f"- {item[0]} (AP: {item[1]}%, CDR: {item[2]}%, Cost: {item[3]})")

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
