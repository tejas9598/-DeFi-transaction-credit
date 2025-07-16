# 📊 Aave Wallet Credit Score Analysis

This report analyzes the score distribution and wallet behaviors based on historical Aave V2 transactions.

---

## 🧠 Method Overview

Each wallet was evaluated using a rule-based scoring engine that considered:

- Total USD value transacted
- Types of actions performed (borrow, repay, deposit, etc.)
- Transaction frequency (txns/day)
- Duration of activity (first to last transaction)
- Behavioral patterns (e.g., only deposits, short lifespan)

Credit scores range from **0 to 1000**, where:

- Higher scores = healthy, consistent borrowing and repayment behavior
- Lower scores = risky, single-use, or passive activity

---

## 📊 Score Distribution

| Score Range | Behavior Summary | Approx. Proportion |
|-------------|------------------|---------------------|
| 0–100       | Single deposit, flash user, 1-day activity | ~20% |
| 100–200     | Low activity, passive users               | ~15% |
| 200–500     | Moderate usage, some diversity            | ~40% |
| 500–800     | Active wallets, longer engagement         | ~20% |
| 800–1000    | Very active, multi-action, responsible    | ~5% (in full data) |

<img width="990" height="490" alt="image" src="https://github.com/user-attachments/assets/2d7288cb-ab40-4f47-9bc6-bd6af64a6539" />

*Figure: Score distribution for a sample of 100 wallets. Most fall in the low to mid-range. High scores are rare but meaningful.*

---

## 🔴 Low Score Wallet Behavior (< 200)

These wallets typically:

- Performed only **1 transaction**
- Were active for **only 1 day**
- Did not borrow or repay
- Had minimal financial impact on the protocol

```text
Stat Summary:
 - total_txns: 1
 - borrow, repay: 0
 - txns_per_day: 1.0
 - active_days: 1
