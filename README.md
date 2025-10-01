# 📈 Supply Chain & Logistics Strategy Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.2-purple.svg)
![ORTools](https://img.shields.io/badge/Google%20OR--Tools-9.9-green.svg)

A multi-page, interactive web application designed for Operations and Strategy Analysts to optimize logistics, manage inventory, and perform data-driven scenario planning. This tool transforms raw operational data into actionable business insights.

###  dashboards (Live Demo Link - *Coming Soon*)

---

## 📸 Dashboard Screenshots

**Home Page & File Uploader:**
*A user-friendly landing page allowing users to either use sample data or upload their own custom datasets.*
![Home Page]
<img width="1365" height="625" alt="image" src="https://github.com/user-attachments/assets/c082a8ba-84e4-43d4-a0e1-c5a4baa542e6" />

**Transportation Optimizer:**
*Interactive map visualization of optimized routes, scenario controls, and sustainability tracking.*
![Transportation Page]
<img width="1364" height="637" alt="image" src="https://github.com/user-attachments/assets/af611441-f427-43f4-8a38-215704f845b4" />


**Inventory Optimization:**
*A strategic calculator to determine optimal safety stock and reorder points based on demand variability and desired service levels.*
![Inventory Page]
<img width="1356" height="630" alt="image" src="https://github.com/user-attachments/assets/5fba301d-485d-4292-9fa1-fdecf880faf4" />

---

## 🔑 Key Features & Skills Demonstrated

This project showcases a blend of technical implementation and strategic business thinking, directly targeting the responsibilities of an Operations and Strategy role.

#### **🔹 Strategic Planning & Scenario Analysis**
-   **Interactive Sidebar Controls:** Instantly model the impact of operational disruptions like a **truck breakdown** (by de-selecting active trucks) or market volatility like a **fuel price spike**.
-   **"What-If" Analysis:** Quantify the exact financial and operational impact of changing variables, demonstrating an ability to provide data-driven answers to executive questions.

#### **🔹 Logistics & Transportation Optimization**
-   **Vehicle Routing Problem (VRP) Solver:** Implemented Google's OR-Tools to solve for the most efficient routes, minimizing total distance and operational cost.
-   **Capacity Utilization Tracking:** The "Per-Truck Performance" table analyzes the efficiency of each vehicle, highlighting opportunities for consolidation or fleet right-sizing.
-   **Sustainability & ESG Tracking:** The dashboard calculates the **estimated carbon footprint (CO₂) in kg** for the planned routes, aligning operational efficiency with modern sustainability goals.

#### **🔹 Inventory Management & Optimization**
-   **Statistical Safety Stock Calculation:** A dedicated module uses demand variability, lead times, and a desired service level (Z-score) to calculate the optimal safety stock.
-   **Dynamic Reorder Point Suggestion:** Provides clear, actionable recommendations on when to reorder inventory to prevent stockouts while minimizing holding costs.

#### **🔹 User-Centric Design & Automation**
-   **Custom Data Upload:** The application is not a static demo; it's a flexible tool that allows users to upload their own `Farms`, `Markets`, `Trucks`, and `Road Network` files for a fully custom analysis.
-   **Multi-Page Dashboard:** The application is structured logically into distinct modules, demonstrating an ability to build scalable and maintainable analytical tools.

---

## 🛠️ Technology Stack

-   **Backend:** Python
-   **Dashboard/Frontend:** Streamlit
-   **Data Manipulation:** Pandas, NumPy
-   **Optimization Solver:** Google OR-Tools
-   **Statistical Analysis:** SciPy
-   **Mapping:** Folium, Streamlit-Folium
-   **Data Validation:** Pydantic

---

## 🚀 Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YourUsername/YourRepositoryName.git
    cd YourRepositoryName
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ▶️ Running the Application

1.  **Generate Sample Data (First Time Only):**
    This script creates the `data` folder and populates it with sample CSV and JSON files.
    ```bash
    python scripts/generate_dummy_data.py
    ```

2.  **Launch the Streamlit App:**
    This command starts the web server and opens the application in your browser.
    ```bash
    python -m streamlit run src/1_Home.py
    ```
The application will be accessible at `http://localhost:8501`.
