# 🎯 HealthKart Influencer Campaign Tracker

**A dynamic, no-code Streamlit dashboard enabling marketers to ingest custom influencer data, track campaign performance, and extract high‑impact ROAS insights.**

---

## 📌 Table of Contents

1. [🚀 About](#-about)
2. [🎨 Visual Showcase](#-visual-showcase)
3. [📋 Context & Objective](#-context--objective)
4. [🔄 Project Workflow](#-project-workflow)
5. [🗂️ Data Model & Synthetic Generator](#-data-model--synthetic-generator)
6. [🚦 Usage Guide](#-usage-guide)
7. [📊 Key Insights](#-key-insights)
8. [📁 Project Structure](#-project-structure)
9. [🔧 Local Installation & Setup](#-local-installation--setup)
10. [🤝 Contributing](#-contributing)
11. [📄 License](#-license)

---

## 🚀 About

HealthKart Influencer Campaign Tracker is an open‑source **Streamlit** dashboard that empowers marketing teams to:

* Ingest their own influencer & campaign datasets.
* Monitor real‑time KPIs (reach, engagements, orders, revenue).
* Calculate incremental ROAS and export reports.
* Track and analyze influencer payouts.

🔗 [**Try the Live Demo**](https://influencertracker-bysuman.streamlit.app)

---

## 🎨 Visual Showcase

A sneak peek at the core user flow:

1. **App Home (Before Upload)**

   !\[App Home Before]\(images/app before.png)

2. **Data Upload (Before)**

   !\[Data Upload Before]\(images/data upload before.png)

3. **Data Upload (After)**

   !\[Data Upload After]\(images/data upload after.png)

4. **App Home (After Upload)**

   !\[App Home After]\(images/app after.png)

> 🔗 **Explore more pages & generate insights:** [Live Dashboard](https://influencertracker-bysuman.streamlit.app)

---

## 📋 Context & Objective

HealthKart collaborates with influencers across Instagram, YouTube, Twitter, and link‑based channels (SwipeUp, BioLink, PromoCode). Payouts occur per post or per tracked order. This project aims to:

1. 📊 **Track** influencer & campaign performance in a unified dashboard.
2. 💰 **Calculate** real incremental ROAS by attribution model.
3. 🔍 **Surface** high‑value insights at both campaign and influencer levels.
4. 🧾 **Monitor** and **export** influencer payout breakdowns.

---

## 🔄 Project Workflow

1. **Synthetic Data Generation**

   * Run `assets/Synthetic_data_generator.ipynb` to generate:

     * `influencers.csv`
     * `posts.csv`
     * `tracking_data.csv`
     * `payouts.csv`

2. **Dashboard Development**

   * Build with **Streamlit** and **Plotly**, following “vibe coding” UI principles (consistent palette, whitespace, rounded cards).

3. **Cloud Deployment**

   ```bash
   streamlit deploy streamlit_app/app.py
   ```

   * **Live:** [influencertracker-bysuman.streamlit.app](https://influencertracker-bysuman.streamlit.app)

4. **Data Upload & Insights**

   * Upload your CSVs in **Data Upload** tab.
   * View campaign KPIs, influencer ROAS, payout tables, incremental ROAS analysis.

> ⚠️ **Dynamic Data Only:** Upload your own datasets (matching schemas) to power the insights.

---

## 🗂️ Data Model & Synthetic Generator

### Table Schemas (CSV)

| Table              | Columns                                                                                  |
| ------------------ | ---------------------------------------------------------------------------------------- |
| **influencers**    | `id`, `name`, `category`, `gender`, `follower_count`, `platform`                         |
| **posts**          | `influencer_id`, `platform`, `date`, `url`, `caption`, `reach`, `likes`, `comments`      |
| **tracking\_data** | `source`, `campaign`, `influencer_id`, `user_id`, `product`, `date`, `orders`, `revenue` |
| **payouts**        | `influencer_id`, `basis`, `rate`, `orders`, `total_payout`                               |

### ER Diagram & Relationships

!\[Data Modeling]\(images/data modeling.png)

* influencers → posts     (1\:many)
* influencers → tracking\_data (1\:many)
* influencers → payouts     (1\:many)
* posts ↔ tracking\_data  (join via influencer\_id)

### Synthetic Data Generator

1. Open `assets/Synthetic_data_generator.ipynb`.
2. Execute all cells or:

   ```bash
   jupyter nbconvert --to notebook --execute assets/Synthetic_data_generator.ipynb
   ```
3. Find generated CSVs in **assets/**.

---

## 🚦 Usage Guide

1. **Data Upload**

   * Go to **Data Upload** tab.
   * Upload `influencers.csv`, `posts.csv`, `tracking_data.csv`, `payouts.csv`.

2. **Campaign Performance**

   * Filter by campaign, date range.
   * Review reach, engagement, orders, revenue.

3. **Influencer Insights**

   * Drill into category, platform.
   * Rank top/bottom influencers by ROAS.

4. **Payout Tracking**

   * Select payout basis.
   * View influencer‑level cost tables.

5. **ROI & ROAS Analysis**

   * Compare total vs. incremental ROAS.
   * Track daily ROI trends & high/low segments.

6. **Export**

   * Download tables as CSV or PDF.

---

## 📊 Key Insights

1. **Link Channels Drive Revenue** 🔗
   100% of orders (19,009) and ₹3.78 M revenue via SwipeUp, BioLink & PromoCode — despite \~6 M reach on organic platforms.

2. **Strong Unit Economics** 💹

   * **AOV:** ₹199 | **CPO:** ₹66 | **ROAS:** 3.0× — highly effective link‑based campaigns.

3. **SwipeUp’s Premium Edge** 📈
   Generates highest revenue (₹1.28 M) per order count — suggests premium conversions.

4. **Untapped YouTube Potential** 🎥
   Top reach & engagement but 0 tracked sales — integrate trackable codes/links.

5. **Leaky Funnel Alert** 🚨
   4.57% engagement → 0.33% conversion — optimize CTAs & tracking in organic posts.

6. **Portfolio Health** 🏆
   90% of influencers profitable; top 90 drive ₹3.43 M on ₹0.69 M spend (avg ROI \~397%).

---

## 📁 Project Structure

```
├── assets/                   # Synthetic generator & CSVs
│   └── Synthetic_data_generator.ipynb
│   └── *.csv
├── images/                   # Screenshots & diagram
│   └── app before.png
│   └── data upload before.png
│   └── data upload after.png
│   └── app after.png
│   └── data modeling.png
├── streamlit_app/            # Streamlit code & config
│   ├── .streamlit/
│   ├── pages/
│   ├── utils/
│   ├── app.py
│   └── requirements.txt
├── README.md
└── LICENSE
```

---

## 🔧 Local Installation & Setup

```bash
# Clone repo
git clone https://github.com/techysuman27/HealthKart-Influencer-Campaign-Tracker.git
cd HealthKart-Influencer-Campaign-Tracker

# Virtual env
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate    # Windows

# Install
pip install -r streamlit_app/requirements.txt

# Run local server
streamlit run streamlit_app/app.py --server.port 8501
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feat/YourFeature`)
3. Commit (`git commit -m 'Add feature'`)
4. Push & open a PR

---

## 📄 License

This project is licensed under MIT License. See [LICENSE](LICENSE) for details.

---

> Built with ❤️ by **Suman Sadhukhan** | Hosted on Streamlit Cloud
