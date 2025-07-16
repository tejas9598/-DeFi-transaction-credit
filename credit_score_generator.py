import json
import pandas as pd
import numpy as np
import os

def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def flatten_dataframe(raw_data):
    df = pd.DataFrame(raw_data)
    action_data_df = pd.json_normalize(df['actionData'])
    df = pd.concat([df.drop(columns=['actionData']), action_data_df], axis=1)

    # Convert time fields
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')
    df["createdAt"] = pd.to_datetime(df["createdAt"].apply(lambda x: x["$date"]))
    df["updatedAt"] = pd.to_datetime(df["updatedAt"].apply(lambda x: x["$date"]))

    # Numeric conversions
    df["amount"] = df["amount"].astype(float)
    df["assetPriceUSD"] = df["assetPriceUSD"].astype(float)
    df["usd_value"] = df["amount"] * df["assetPriceUSD"]

    return df

def engineer_features(df):
    action_counts = df.pivot_table(index="userWallet", 
                                    columns="action", 
                                    values="txHash", 
                                    aggfunc="count", 
                                    fill_value=0)

    wallet_features = df.groupby("userWallet").agg(
        total_txns=("txHash", "count"),
        total_usd_transacted=("usd_value", "sum"),
        avg_usd_per_txn=("usd_value", "mean"),
        first_txn=("timestamp", "min"),
        last_txn=("timestamp", "max")
    )

    wallet_features = wallet_features.merge(action_counts, left_index=True, right_index=True)
    wallet_features["active_days"] = (wallet_features["last_txn"] - wallet_features["first_txn"]).dt.days + 1
    wallet_features["txns_per_day"] = wallet_features["total_txns"] / wallet_features["active_days"]

    return wallet_features.reset_index()

def score_wallet(row):
    score = 0

    if row["total_usd_transacted"] > 100_000:
        score += 200
    elif row["total_usd_transacted"] > 10_000:
        score += 100

    if row.get("borrow", 0) > 0 and row.get("repay", 0) > 0:
        score += 150

    if row["txns_per_day"] > 1:
        score += 150
    if row["active_days"] > 7:
        score += 100

    if row.get("deposit", 0) > 0 and row.get("borrow", 0) == 0 and row.get("repay", 0) == 0 and row.get("redeemunderlying", 0) == 0:
        score -= 100

    if row["active_days"] <= 1:
        score -= 50

    return max(0, min(1000, score))

def apply_scoring(wallet_df):
    wallet_df["credit_score"] = wallet_df.apply(score_wallet, axis=1)
    return wallet_df[["userWallet", "credit_score"]]

def save_output(wallet_scores, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "wallet_credit_scores_full.csv")
    json_path = os.path.join(output_dir, "wallet_credit_scores_full.json")

    wallet_scores.to_csv(csv_path, index=False)
    wallet_scores.to_json(json_path, orient="records", indent=2)

    print(f"✅ Credit scores saved to:\n - {csv_path}\n - {json_path}")

def main():
    input_file = "user-wallet-transactions.json"
    raw_data = load_json(input_file)

    print(f"📦 Loaded {len(raw_data)} records")

    df = flatten_dataframe(raw_data)
    print("🔄 Flattened and preprocessed transactions")

    features = engineer_features(df)
    print("🧠 Engineered wallet-level features")

    scores = apply_scoring(features)
    print("💳 Assigned credit scores to all wallets")

    save_output(scores)

if __name__ == "__main__":
    main()
