# -DeFi-transaction-credit
# 💳 Aave V2 Wallet Credit Scoring

This project implements a robust rule-based system to generate **credit scores (0–1000)** for wallets interacting with the Aave V2 protocol on the Polygon network. The scores reflect reliability, financial activity, and risk behavior based on historical transactions.

---

## 📌 Problem Statement

Given 100K+ wallet-level transaction records from Aave V2 (`deposit`, `borrow`, `repay`, `redeemUnderlying`, `liquidationCall`), assign a **credit score between 0 and 1000** to each wallet.

- **High score (800–1000)**: Healthy borrowing + repayment, diverse and stable usage.
- **Low score (0–200)**: Risky, bot-like, single-action, or flash users.

---

## ⚙️ Input Data

- Format: JSON file (`user-wallet-transactions.json`)
- Fields of interest:
  - `userWallet`, `action`, `amount`, `assetPriceUSD`
  - `timestamp`, `protocol`, `network`

---

## 🧠 Feature Engineering

Transactions were grouped by wallet to extract the following features:

| Feature | Description |
|--------|-------------|
| `total_usd_transacted` | USD value of all interactions (amount × price) |
| `avg_usd_per_txn` | Average transaction value |
| `txns_per_day` | Frequency of wallet usage |
| `active_days` | Time difference between first and last activity |
| `borrow`, `repay`, `deposit`, `redeemunderlying`, `liquidationcall` | Count of each action |

---

## 📊 Credit Scoring Logic

We implemented a transparent, rule-based scoring function:

| Rule | Condition | Score Impact |
|------|-----------|--------------|
| High volume | Total USD > \$100K | +200 |
| Medium volume | USD \$10K–\$100K | +100 |
| Borrowing and Repayment present | Both actions | +150 |
| High frequency | >1 transaction/day | +150 |
| Long-term activity | Active > 7 days | +100 |
| Only deposits | No borrow/repay/redeem | –100 |
| One-day lifespan | Active for only 1 day | –50 |

**Final scores are clipped between 0 and 1000.**

---

## 🚀 Output Files

| File | Description |
|------|-------------|
| `wallet_credit_scores_full.csv` | Credit scores with wallet addresses (CSV) |
| `wallet_credit_scores_full.json` | Credit scores in JSON format |
| `analysis.md` | Score distribution, insights on user behavior |

---

## 📈 Score Example

| userWallet | credit_score |
|------------|--------------|
| 0x000...b6d4b6 | 50 |
| 0x000...7e2dc | 200 |
| 0x000...f3e5a7 | 600 |
| ... | ... |

---

## 🏗️ How to Run

```bash
pip install pandas numpy matplotlib seaborn
python credit_score_generator.py
