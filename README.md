## Description

A backend application that manages a Research Agent designed to assist users in performing complex research tasks. The Research Agent pulls data from multiple sources and synthesizes user-directed content through tool calling with OpenAI's GPT-4o-mini.

## Features

- Create, retrieve, and delete research agents
- Store agent details in MongoDB
- Process user queries through the research agent
- Integration with research tools:
  - Wikipedia for general knowledge
  - Web search via DuckDuckGo
- Tool selection based on query requirements
- Research synthesis into coherent responses

## Sample Output

When querying the Research Agent about investment comparison between Nvidia and Apple:

```
1. **Summary**: Both Nvidia and Apple are strong contenders for investment in 2023, but they cater to different market segments and have distinct growth trajectories. Nvidia has shown remarkable growth, particularly in the AI and gaming sectors, while Apple continues to maintain a solid market presence with steady growth forecasts.

2. **Detailed Information**:

   - **Nvidia (NVDA)**:
     - Nvidia's stock has experienced significant growth, soaring 239% in 2023, driven by its dominance in the graphics processing unit (GPU) market and increasing demand for AI technologies [1](https://www.fool.com/investing/2024/01/10/why-nvidia-stock-skyrocketed-239-in-2023/).
     - Analysts have a \"Strong Buy\" rating on Nvidia, indicating confidence in its future performance [2](https://stockanalysis.com/stocks/nvda/forecast/).
     - Despite a recent dip in the market, Nvidia's earnings reports have consistently set records, suggesting a robust business model and potential for continued growth [3](https://www.fool.com/investing/2024/03/20/nvidia-stock-soared-239-in-2023-and-1-wall-street/).
     - The stock is currently valued at approximately $101 per share, which some analysts believe is undervalued given its growth potential [4](https://www.forbes.com/sites/greatspeculations/2025/03/05/nvidia-stock-are-tariff-fears-overblown/).

   - **Apple (AAPL)**:
     - Apple has an average analyst rating of \"Buy,\" with a 12-month price forecast of $242.36, indicating a slight expected increase from its current price [5](https://stockanalysis.com/stocks/aapl/forecast/).
     - Analysts predict a range of price targets for Apple, with estimates as low as $180 and as high as $325, reflecting varying opinions on its future performance [6](https://stockanalysis.com/stocks/aapl/).
     - The company is expected to benefit from new product launches, including an AR/VR headset, which could enhance its market value [7](https://www.forbes.com/sites/qai/2022/12/28/apple-stock-predictions-2023-to-2025/).
     - Apple's consistent performance and strong brand loyalty make it a stable investment option, although its growth may not be as explosive as Nvidia's.

3. **References**:
   1. [Why Nvidia Stock Skyrocketed 239% in 2023](https://www.fool.com/investing/2024/01/10/why-nvidia-stock-skyrocketed-239-in-2023/)
   2. [NVIDIA Corporation (NVDA) Stock Forecast & Price Targets](https://stockanalysis.com/stocks/nvda/forecast/)
   3. [Nvidia Stock Soared 239% in 2023, and 1 Wall Street Analyst Says It ...](https://www.fool.com/investing/2024/03/20/nvidia-stock-soared-239-in-2023-and-1-wall-street/)
   4. [Nvidia Stock: Are Tariff Fears Overblown?](https://www.forbes.com/sites/greatspeculations/2025/03/05/nvidia-stock-are-tariff-fears-overblown/)
   5. [Apple Inc. (AAPL) Stock Forecast & Price Targets](https://stockanalysis.com/stocks/aapl/forecast/)
   6. [Apple Inc. (AAPL) Analyst Ratings, Estimates & Forecasts](https://finance.yahoo.com/quote/AAPL/analysis/)
   7. [Apple Stock Predictions: 2023 To 2025](https://www.forbes.com/sites/qai/2022/12/28/apple-stock-predictions-2023-to-2025/)"
```


## Setup and Installation

1. Clone the repository
```bash
git clone https://github.com/mikeytheong/ai-bots-2025tht.git
cd ai-bots-2025tht
```

2. Initialize and activate virtual environment
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. Set up environment variables
   - Create a `.env` file in the project root directory
   - Use the template in `.env.example` as a reference
   - Be sure to add your `OPENAI_API_KEY` 

4. Set up MongoDB
```bash
docker pull mongo
docker run -d --name i-love-mongo \
    -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=password \
    mongo
```

5. Run FastAPI server
```bash
fastapi dev main.py
```

## API Documentation

The API endpoints can be accessed and tested through the Swagger UI:
```
http://localhost:8000/docs
```

This provides an interactive interface where you can:
- View all available endpoints
- Send test requests
- See request/response schemas
- Authenticate if needed

## Testing

Run the test suite:
```bash
pytest
```

For specific test files:
```bash
pytest tests/test_agents.py -v
```