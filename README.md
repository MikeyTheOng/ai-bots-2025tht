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
- Knowledge base personalization:
  - Text extraction from common file types (.pdf, .docx, .doc, .xlsx, .xls, .ppt, .pptx)
  - Text extraction from specified websites
  - Tokenization of extracted text
  - Prioritization of knowledge base usage over tool usage
  - Token limit validation (120k token maximum context)

## Sample Output

```markdown
Example Query: Should I invest into Space Ong, Nvidia or Wikipedia?
```


**Summary**: When considering investments in Space Ong, Nvidia, or Wikipedia, each option presents unique opportunities and risks. Space Ong is part of a rapidly growing space economy projected to reach $1.8 trillion by 2035. Nvidia has shown remarkable growth, particularly in AI, with stock prices soaring significantly in 2023. Wikipedia, however, is not a traditional investment vehicle as it operates as a non-profit organization.

**Detailed Analysis**:

### Space Ong
Space Ong is projected to be part of a burgeoning space economy, which is expected to grow to $1.8 trillion by 2035, driven by advancements in space-enabled technologies and applications [1][2]. The investment landscape in the space sector is becoming increasingly attractive, with significant private equity investments and a variety of space-focused ETFs available for investors [3][4]. However, specific details about Space Ong's financial health or market position are not widely available, making it essential to conduct further research on the company's fundamentals before investing.

### Nvidia
Nvidia has emerged as a leading player in the tech industry, particularly in the fields of artificial intelligence and graphics processing units (GPUs). The company's stock has seen a remarkable increase, with a reported 239% rise in 2023 alone [5][6]. Analysts are optimistic about Nvidia's future, with some suggesting that the stock could potentially increase tenfold due to new growth vectors in AI and other technologies [7]. This strong performance and growth potential make Nvidia a compelling investment option, especially for those interested in technology and AI sectors.

### Wikipedia
Wikipedia operates as a non-profit organization and does not offer traditional investment opportunities. It relies on donations and grants to fund its operations and maintain its platform. While it is a valuable resource and has a significant impact on information dissemination, it does not generate profits or provide returns on investment in the conventional sense [8]. Therefore, investing in Wikipedia is not feasible in the same way as investing in a for-profit company like Space Ong or Nvidia.

**Key Insights**:
- **Space Ong**: Potentially high growth in a booming sector, but requires more specific financial data for informed investment.
- **Nvidia**: Strong growth and market position in AI and technology, making it a promising investment.
- **Wikipedia**: Not a viable investment option as it operates as a non-profit.

**References**:
1. [How to invest in the space industry: A beginner's guide](https://www.bankrate.com/investing/how-to-invest-in-space/)
2. [Space is booming. Here's how to embrace the $1.8 trillion opportunity](https://www.weforum.org/stories/2024/04/space-economy-technology-invest-rocket-opportunity/)
3. [5 Space Stocks to Watch in 2025 and Beyond - The Motley Fool](https://www.fool.com/investing/stock-market/market-sectors/industrials/space-stocks/)
4. [Space Capital | Insights | Investing in the Space Economy](https://www.spacecapital.com/publications/investing-in-the-space-economy)
5. [Where Will Nvidia Stock Be In 5 Years? - Forbes](https://www.forbes.com/sites/investor-hub/article/where-will-nvidia-nvda-stock-be-5-years/)
6. [Nvidia Stock Soared 239% in 2023, and 1 Wall Street Analyst Says It ...](https://www.fool.com/investing/2024/03/20/nvidia-stock-soared-239-in-2023-and-1-wall-street/)
7. [Nvidia Stock Could Rise 10-Fold On New $10 Billion Growth Vector - Forbes](https://www.forbes.com/sites/petercohan/2024/06/09/nvidia-stock-could-rise-10-fold-on-new-10-billion-growth-vector/)
8. [Investment - Wikipedia](https://en.wikipedia.org/wiki/Investment)



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

4. Docker Setup (Recommended)
```bash
# Build and start with Docker Compose
docker-compose up -d
```

5. Manual MongoDB Setup (Alternative to Docker)
```bash
docker pull mongo
docker run -d --name i-love-mongo \
    -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=password \
    mongo
```

6. Run FastAPI server (if not using Docker)
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