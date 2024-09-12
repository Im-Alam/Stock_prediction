from src.db_models.news import News
from src.db_models.relationships import NewsCompanyAssociation
from src.db_models.company import Company
from src.utils.reqRes import *
from collections import defaultdict
import json

"""
Get news by different sector, different companies, must include some news about nifty index: in last 5 days.
get news by company name.

#Further work: We can get most relevant news based on some ML based algorithm
"""

####
def news_from_all_sectors():
    """
    -Get all news in last week
    -Then group them by sector
    -return each group in json format
    """
    try:
        recent_news = News.fetch_recent_news(50)
        result = {}

        # Directly populate the result dictionary
        for news, company in recent_news:
            news_detail = {
                "headline": news.headline,
                "content": news.content,
                "url": news.news_url,
                "sentiment": news.sentiment,
                "date": str(news.created_at)  # Convert date to string for JSON serialization
            }
            
            # Check if the sector already exists in the result dictionary
            if company.sector not in result:
                result[company.sector] = []
            
            # Check if this news item is already added to the sector
            existing_news = next((item for item in result[company.sector] if item["headline"] == news.headline), None)
            """
            next(...):
            next() is a built-in Python function that retrieves the next item from an iterator (in this case, the generator created by the expression).
            If the generator finds a match, next() will return the first matching item.
            """

            if existing_news:
                existing_news["companies"].append(company.company_name)
            else:
                # If it's a new news item, add it along with the company
                result[company.sector].append({
                    "headline": news.headline,
                    "content": news.content,
                    "news_url": news.news_url,
                    "sentiment": news.sentiment,
                    "news_date": str(news.created_at),
                    "companies": [company.company_name]  # Initialize the company list
                })
            
            return json.dumps(result)
    except Exception as e:
        return apiError(500, "server error in sector wise news collection")

###
def get_news_by_company_name(name: str):
    try:
        news_list = News.fetch_recent_news_by_company_name(name, 10)
        
        news_data = [
        {
            "id": news.id,
            "headline": news.headline,
            "content": news.content,
            "topic": news.topic,
            "news_url": news.news_url,
            "sentiment": news.sentiment,
            "sentiment_statement": news.sentiment_statement,
            "created_at": news.created_at,
            
            "company": {
                "company_id": company.id,
                "company_name": company.company_name,
                "company_sector": company.sector
            }
        }
        for news, company in news_list
        ]
        return json.dump(news_data)
    
    except:
        return apiError(500, "Internal server error")
    


