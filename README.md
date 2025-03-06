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

```markdown
Example Query: Should I invest into nvidia or apple?
```


**Summary**: Both Nvidia and Apple present compelling investment opportunities, but they cater to different market dynamics. Nvidia is heavily focused on the AI sector, showing strong growth and profitability, while Apple is investing significantly in U.S. infrastructure and maintaining a robust product ecosystem despite recent challenges in iPhone sales.

**Detailed Analysis**:

### Nvidia Investment Outlook
1. **Strong Financial Performance**: Nvidia has recently reported impressive earnings, doubling its profits in 2024, largely driven by the demand for AI technology. This growth has positioned Nvidia as a leader in the AI chip market, which is expected to continue expanding [CNN](https://www.msn.com/en-us/money/other/nvidia-doubled-profits-in-2024-and-its-outlook-is-rosy-despite-ai-jitters/ar-AA1zRkP2).

2. **Market Position and Growth Potential**: The company has seen its stock price triple since October 2023, reflecting optimism in the AI sector. However, there are concerns about competition, particularly from new entrants like the Chinese startup DeepSeek, which could impact Nvidia's market dominance [InvestmentNews](https://www.investmentnews.com/industry-news/why-options-traders-are-cautious-about-nvidia-earnings-this-week/259426).

3. **Investment Sentiment**: Analysts suggest that despite some volatility, Nvidia remains a strong buy due to its pivotal role in the AI revolution and the growing demand for its products [The Motley Fool](https://www.fool.com/investing/2025/02/19/2-reasons-buy-nvidia-stock-wake-deepseek/).

### Apple Investment Outlook
1. **Significant U.S. Investment**: Apple has announced plans to invest over $500 billion in the U.S. over the next four years, which includes building new facilities and creating jobs. This move is seen as a strategic effort to bolster its domestic operations and mitigate risks associated with international supply chains [Forbes](https://www.forbes.com/sites/siladityaray/2025/02/24/apple-promises-500-billion-us-investment-and-20000-jobs/).

2. **Challenges in Sales**: Despite its strong brand and ecosystem, Apple faced a decline in iPhone sales in 2023. Analysts are cautiously optimistic about a potential rebound, but the company must navigate market saturation and competition in the smartphone sector [TheStreet.com](https://www.thestreet.com/apple/stock/apple-stock-outlook-2024-challenges-and-trends).

3. **Long-term Growth Strategy**: Apple's investment strategy is aimed at sustaining its growth trajectory and enhancing its competitive edge, particularly in the face of economic uncertainties and evolving consumer preferences [USA Today](https://www.usatoday.com/story/money/investing/2025/02/06/apple-725-billion-investment/78015792007/).

**Key Insights**:
- **Nvidia** is positioned for growth in the AI sector, with strong financial results and a leading market position, but faces competitive threats.
- **Apple** is making substantial investments in the U.S. to strengthen its operations, although it is currently dealing with challenges in iPhone sales.

**References**:
1. [CNN - Nvidia doubled profits in 2024](https://www.msn.com/en-us/money/other/nvidia-doubled-profits-in-2024-and-its-outlook-is-rosy-despite-ai-jitters/ar-AA1zRkP2)
2. [The Motley Fool - 2 Reasons to Buy Nvidia Stock](https://www.fool.com/investing/2025/02/19/2-reasons-buy-nvidia-stock-wake-deepseek/)
3. [InvestmentNews - Why options traders are cautious about Nvidia](https://www.investmentnews.com/industry-news/why-options-traders-are-cautious-about-nvidia-earnings-this-week/259426)
4. [Forbes - Apple Promises $500 Billion U.S. Investment](https://www.forbes.com/sites/siladityaray/2025/02/24/apple-promises-500-billion-us-investment-and-20000-jobs/)
5. [TheStreet.com - Apple Stock Outlook 2024](https://www.thestreet.com/apple/stock/apple-stock-outlook-2024-challenges-and-trends)
6. [USA Today - Apple's $725 billion investment](https://www.usatoday.com/story/money/investing/2025/02/06/apple-725-billion-investment/78015792007/)



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