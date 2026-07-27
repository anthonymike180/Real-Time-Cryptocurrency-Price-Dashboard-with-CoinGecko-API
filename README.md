# Real-Time Cryptocurrency Price Dashboard

<div align="center">

![Dashboard Preview](https://github.com/anthonymike180/Real-Time-Cryptocurrency-Price-Dashboard-with-CoinGecko-API/blob/main/Image%20py.png)

**A live, interactive dashboard for monitoring real-time cryptocurrency prices using the CoinGecko API**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Screenshots & Resources](#screenshots--resources)
- [Use Cases](#use-cases)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## 🧩 Overview

This project provides a **real-time cryptocurrency price dashboard** that fetches live market data from the [CoinGecko API](https://www.coingecko.com/en/api). The dashboard displays current pricing, market capitalization, trading volume, and 24-hour price changes for the top cryptocurrencies, enabling users to monitor market trends and make informed decisions at a glance.

Built with **Streamlit** for an intuitive web interface and **Plotly** for interactive visualizations, this application offers a clean, responsive design that updates at configurable intervals.

---

## ✨ Features

- **Live Data Fetching**: Retrieves real-time cryptocurrency prices directly from CoinGecko API
- **Interactive Dashboard**: Clean, responsive UI with auto-refresh capabilities
- **Key Market Metrics**: Displays total market cap, trading volume, and average price changes
- **Visual Analytics**: 
  - Bar charts showing current prices with color-coded performance indicators
  - Pie charts illustrating market cap distribution
- **Configurable Refresh**: Customizable auto-refresh intervals (10–120 seconds)
- **Data Export**: Option to save historical data to CSV for further analysis
- **Responsive Design**: Optimized layout for various screen sizes

---

## 🛠️ Technologies

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Primary programming language |
| **Streamlit** | Web application framework |
| **Requests** | HTTP library for API calls |
| **Pandas** | Data manipulation and analysis |
| **Plotly** | Interactive data visualization |
| **CoinGecko API** | Cryptocurrency market data source |
| **Jupyter Notebook** | Exploratory data analysis |

---

## 📦 Prerequisites

Before running this application, ensure you have:

- Python 3.8 or higher installed
- pip (Python package manager)
- A stable internet connection (for API access)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/anthonymike180/Real-Time-Cryptocurrency-Price-Dashboard-with-CoinGecko-API.git
cd Real-Time-Cryptocurrency-Price-Dashboard-with-CoinGecko-API
```

### 2. Install Dependencies

```bash
pip install streamlit requests pandas plotly
```

### 3. Verify Installation

Ensure all packages are installed correctly:

```bash
python -c "import streamlit, requests, pandas, plotly; print('All dependencies installed successfully!')"
```

---

## 💻 Usage

### Running the Web Application

Launch the dashboard using Streamlit:

```bash
streamlit run crypto_app.py
```

The application will open automatically in your default web browser at `http://localhost:8501`.

### Using the Jupyter Notebook

For exploratory data analysis and visualization:

```bash
jupyter notebook "Real-Time Cryptocurrency Price Dashboard with CoinGecko API.ipynb"
```

### Dashboard Controls

- **Auto-refresh Toggle**: Enable/disable automatic data refresh
- **Refresh Interval Slider**: Set update frequency (10–120 seconds)
- **Last Updated Timestamp**: View the time of the most recent data fetch

---

## ⚙️ Configuration

Customize the dashboard by modifying the following parameters in `crypto_app.py`:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `vs_currency` | Fiat currency for price display | `'usd'` |
| `per_page` | Number of cryptocurrencies to display | `10` |
| `refresh_interval` | Auto-refresh duration (seconds) | `30` |
| Cryptocurrency List | Modify API parameters to track different coins | Top 10 by market cap |

### Exporting Historical Data

To save historical price data for analysis:

```python
# Add to crypto_app.py or use the notebook
df.to_csv('crypto_data.csv', index=False)
```

---

## 📁 Project Structure

```
Real-Time-Cryptocurrency-Price-Dashboard-with-CoinGecko-API/
├── crypto_app.py              # Main Streamlit web application
├── crypto_data.csv            # Sample/exported cryptocurrency data
├── Real-Time Cryptocurrency Price Dashboard with CoinGecko API.ipynb  # Jupyter notebook
├── Image py.png               # Dashboard screenshot
├── Crypto dashboard.pdf       # Documentation/screenshot PDF
├── README.md                  # Project documentation
└── .gitignore                 # Git ignore rules
```

---

## 📸 Screenshots & Resources

| Resource | Description | Link |
|----------|-------------|------|
| **Dashboard Screenshot** | Visual preview of the interface | [View Image](https://github.com/anthonymike180/Real-Time-Cryptocurrency-Price-Dashboard-with-CoinGecko-API/blob/main/Image%20py.png) |
| **PDF Documentation** | Detailed dashboard overview | [Download PDF](https://github.com/anthonymike180/Real-Time-Cryptocurrency-Price-Dashboard-with-CoinGecko-API/blob/main/Crypto%20dashboard.pdf) |
| **Dataset** | Sample cryptocurrency data | [View CSV](https://github.com/anthonymike180/Real-Time-Cryptocurrency-Price-Dashboard-with-CoinGecko-API/blob/main/crypto_data.csv) |
| **Web Application** | Main Streamlit app source code | [View Script](https://github.com/anthonymike180/Real-Time-Cryptocurrency-Price-Dashboard-with-CoinGecko-API/blob/main/crypto_app.py) |
| **Jupyter Notebook** | Exploratory analysis notebook | [View Notebook](https://github.com/anthonymike180/Real-Time-Cryptocurrency-Price-Dashboard-with-CoinGecko-API/blob/main/Real-Time%20Cryptocurrency%20Price%20Dashboard%20with%20CoinGecko%20API.ipynb) |

---

## 🎯 Use Cases

- **Traders & Investors**: Monitor real-time price movements and market trends
- **Educational Projects**: Learn API integration, data visualization, and web app development
- **Market Analysis**: Track cryptocurrency performance and compare market caps
- **Portfolio Tracking**: Foundation for building personalized crypto portfolio dashboards
- **Alert Systems**: Extend functionality to add price alerts and notifications

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read the [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Anthony Michael**  
📧 Email: [anthonymike180@gmail.com](mailto:anthonymike180@gmail.com)  
🐙 GitHub: [@anthonymike180](https://github.com/anthonymike180)

---

<div align="center">

**If you find this project helpful, please consider giving it a ⭐ on GitHub!**

</div>
