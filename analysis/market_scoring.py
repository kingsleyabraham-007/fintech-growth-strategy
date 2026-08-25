import pandas as pd

# Load market scoring data
data = pd.read_csv("../data/market_scoring.csv")

# Weights for each evaluation factor
weights = {
    "market_opportunity": 0.25,
    "digital_payment_adoption": 0.20,
    "customer_need": 0.20,
    "competitive_opportunity": 0.15,
    "regulatory_feasibility": 0.10,
    "partnership_potential": 0.10
}

# Calculate weighted score
data["weighted_score"] = (
    data["market_opportunity"] * weights["market_opportunity"]
    + data["digital_payment_adoption"] * weights["digital_payment_adoption"]
    + data["customer_need"] * weights["customer_need"]
    + data["competitive_opportunity"] * weights["competitive_opportunity"]
    + data["regulatory_feasibility"] * weights["regulatory_feasibility"]
    + data["partnership_potential"] * weights["partnership_potential"]
)

# Convert score to a percentage
data["score_percentage"] = (data["weighted_score"] / 5) * 100

# Rank markets
data = data.sort_values(
    by="weighted_score",
    ascending=False
).reset_index(drop=True)

data["rank"] = data.index + 1


# Assign strategic priority
def classify_market(score):
    if score >= 4.0:
        return "Priority 1 - Enter"
    elif score >= 3.5:
        return "Priority 2 - Validate"
    elif score >= 3.0:
        return "Priority 3 - Monitor"
    else:
        return "Do Not Enter"


data["priority"] = data["weighted_score"].apply(classify_market)


# Display results
print("\nAFRICAN FINTECH MARKET PRIORITIZATION")
print("=" * 50)

print(
    data[
        [
            "rank",
            "market",
            "weighted_score",
            "score_percentage",
            "priority"
        ]
    ].to_string(index=False)
)

print("\nTop Priority Markets")
print("=" * 50)

top_markets = data[data["priority"] == "Priority 1 - Enter"]

for _, market in top_markets.iterrows():
    print(
        f"{market['rank']}. {market['market']} "
        f"- Score: {market['score_percentage']:.1f}%"
    )
