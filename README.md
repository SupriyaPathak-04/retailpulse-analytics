# RetailPulse Analytics 

**Turning retail transactions into actionable business insights.**

## About the Project

RetailPulse Analytics is a data analytics and machine learning project that explores online retail transactions to understand sales performance, customer purchasing behavior, and customer value.

Using Python, this project combines exploratory data analysis, RFM analysis, K-Means clustering, and predictive modelling to demonstrate how transaction data can support data-driven business decisions.

## Project Objectives

- Clean and preprocess retail transaction data.
- Analyze revenue trends and best-selling products.
- Understand customer purchase frequency.
- Identify valuable customers using RFM analysis.
- Segment customers using K-Means clustering.
- Build and evaluate a machine learning model to predict future customer purchases.
- Develop an interactive dashboard using Streamlit.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and modelling |
| Pandas | Data manipulation and cleaning |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Scikit-learn | Clustering and machine learning |
| Google Colab | Development environment |
| Streamlit | Interactive dashboard — planned |

## Dataset

This project uses the **Online Retail** dataset from the UCI Machine Learning Repository.

**Source:** https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains transactional records from a UK-based online retailer, including invoice numbers, product descriptions, quantities, invoice dates, unit prices, customer IDs, and countries.

## Project Workflow

### 1. Data Collection and Cleaning
- Inspect dataset structure and data types.
- Identify and remove duplicate records.
- Examine missing values.
- Exclude cancelled transactions and invalid quantities or prices from the sales analysis.
- Calculate revenue from quantity and unit price.

### 2. Exploratory Data Analysis (EDA)
- Analyze monthly revenue trends.
- Identify the top-selling products.
- Examine customer purchase frequency.
- Visualize the distributions of customer metrics.
- Compare revenue across countries.

### 3. RFM Analysis
Calculate three customer metrics:

- **Recency:** How recently a customer purchased.
- **Frequency:** How many distinct orders a customer placed.
- **Monetary:** The customer's total recorded spending.

Use these metrics to understand customer purchasing behavior and value.

### 4. Customer Segmentation
Apply K-Means clustering to standardized RFM features to group customers with similar purchasing patterns. Use cluster summaries and visualizations to interpret the resulting segments.

### 5. Predictive Modelling
Develop a Logistic Regression model to predict whether a customer makes a purchase during a later observation period. Evaluate its performance using classification metrics and a confusion matrix.

### 6. Interactive Dashboard
An interactive Streamlit dashboard is planned to present key sales metrics, visualizations, and customer insights in one place.

## Key Learning Outcomes

- Data cleaning and preprocessing with Pandas.
- Exploratory data analysis and visualization.
- Customer analytics using RFM metrics.
- Unsupervised learning with K-Means.
- Supervised learning with Logistic Regression.
- Model evaluation and interpretation.
- Translating data findings into business insights.

## How to Run the Project

1. Open the notebook in Google Colab.
2. Download the dataset from the UCI Machine Learning Repository.
3. Upload the dataset to your Colab session or connect it through Google Drive.
4. Update the file path in the notebook if necessary.
5. Run the notebook cells in order.

Required Python libraries include:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

## Limitations

- The dataset represents a historical observation period and may not reflect current purchasing behavior.
- Customers without a recorded future purchase may have purchased outside the available observation window.
- Customer segments depend on the selected features and clustering parameters.
- Predictive model performance should be interpreted using multiple evaluation metrics rather than accuracy alone.

## Project Status

**In progress**

Data cleaning, exploratory analysis, RFM analysis, K-Means clustering, and predictive modelling are part of the current project. The Streamlit dashboard is planned as the next development step.

---

*Built as a hands-on Big Data and Data Analytics learning project.*
