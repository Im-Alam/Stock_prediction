from src.db_models.base import Base
from src.db_models.company import Company
from src.db_models.relationships import NewsCompanyAssociation
from typing import List, Optional
from sqlalchemy import Integer, String, ForeignKey, DateTime, func, select, insert, or_, Text, Numeric, join
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.db.pgdb_connect import engine
from src.utils.reqRes import apiError, apiResponse




class News(Base):
    __tablename__ = 'news_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    headline: Mapped[str] = mapped_column(String(100), nullable = False )
    content: Mapped[str] = mapped_column(Text, nullable = True )
    topic: Mapped[Optional[str]]
    news_url: Mapped[str] = mapped_column(String, nullable=False)
    sentiment:Mapped[int] = mapped_column(Integer, nullable=False)
    sentiment_statement: Mapped[str] = mapped_column(String, nullable = True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    companies = relationship(Company, secondary='news_company_association', back_populates='news', passive_deletes=True)

    
    def __repr__(self):
        return (f'{self.id}: {self.headline}' if self.id and self.headline else "<News (no headline)>")


    def insert_news(news_data: dict):
        """
        Inserts a news entry into the news table and associates it with specified companies.

        Args:
            news_data (dict): Dictionary containing news data.
        """
        # Create a new News object
        session = Session(engine)
        
        try:
            new_news = News(
                headline=news_data["headline"], 
                content=news_data["content"],
                topic = news_data["topic"],
                news_url = news_data["news_url"],
                sentiment = news_data["sentiment"],
                sentiment_statement = news_data["Sentiment_statement"],

                )
            
            company_names = news_data.get("company_names", [])

            for company_name_ in company_names:
                # Check if the company already exists
                company = session.query(Company).filter_by(name=company_name_).first()
                if not company:
                    # If the company does not exist, create a new Company object
                    company = Company(company_name=company_name_)
                    session.add(company)
                
                # Associate the news with the company
                new_news.companies.append(company)

            # Add the new news to the session
            session.add(new_news)
            
            # Commit the transaction
            session.commit()
        except Exception as e:
            session.rollback()
            return apiError(400, "Error occured in inserting news")
        finally:
            session.close()



    def insert_news_in_bulk(news_data_list: list):
        """
        Inserts multiple news entries into the news table and associates them with specified companies.

        Args:
            session (Session): SQLAlchemy session object.
            news_data_list (list): List of dictionaries containing news data and associated company names.
        """
        try:
            session = Session(engine)
            # Prepare news data for bulk insert
            news_mappings = [
                {
                    "heading": news_data["heading"],
                    "content": news_data["content"],
                    "topic": news_data["topic"],
                    "news_url": news_data["news_url"],
                    "sentiment": news_data["sentiment"],
                    "sentiment_description": news_data["sentiment_description"]
                }
                for news_data in news_data_list
            ]
            
            # Insert news entries in bulk and return the inserted primary keys
            session.bulk_insert_mappings(News, news_mappings)
            session.commit()

            # Fetch the inserted news entries to get their IDs
            inserted_news = session.query(News).order_by(News.id.desc()).limit(len(news_mappings)).all()

            # Prepare company and association data for bulk insert
            association_mappings = []
            for news_entry, news_data in zip(inserted_news, news_data_list):
                company_names = news_data.get("company_names", [])
                for company_name in company_names:
                    # Check if the company already exists
                    company = session.query(Company).filter_by(name=company_name).first()
                    if not company:
                        # If the company does not exist, create a new Company object
                        company = Company(company_name=company_name)
                        session.add(company)
                        session.commit()
                    association_mappings.append({"news_id": news_entry.id, "company_id": company.id})

            # Insert associations in bulk
            session.execute(insert(NewsCompanyAssociation).values(association_mappings))
            session.commit()
        except Exception as e:
            session.rollback()
            return apiError(400, "Error occured in bulk insertion")
        finally:
            session.close()

    #####
    def fetch_recent_news(limit_: int = 30):
        session = Session(engine)
        try:
            stmt = (select(News, Company)
                .join(NewsCompanyAssociation, News.id == NewsCompanyAssociation.news_id)
                .join(Company, NewsCompanyAssociation.company_id == Company.id)
                .order_by(News.id.desc())
                .limit(limit_))
            
            news_list = session.execute(stmt).all()
            return news_list
        except Exception as e:
            session.rollback()
            return apiError(500, 'Server error')
        finally:
            session.close()


    #####    
    def fetch_recent_news_by_company_name(company_name: str, limit: int = 10):
        """
        Fetches the most recent news entries associated with a specific company name.

        Args:
            session (Session): SQLAlchemy session object.
            company_name (str): Name of the company.
            limit (int): Number of news entries to fetch. Default is 10.

        Returns:
            List of recent news entries associated with the specified company.
        """
        session = Session(engine)
        try:
            stmt = (select(News, Company)
                .join(NewsCompanyAssociation, News.id == NewsCompanyAssociation.news_id)
                .join(Company, NewsCompanyAssociation.company_id == Company.id)
                .where(Company.company_name == company_name)
                .order_by(News.id)
                .limit(limit))
            
            recent_news = session.execute(stmt).all()
            
            return recent_news
        
        except Exception as e:
            session.rollback()
            print(e)
            return e
        finally:
            session.close()


    def fetch_n_recent_news_for_each_company(company_names: list, n: int=5):
        with Session(engine) as session:
            try:
                # Get the company IDs for the specified company names
                company_ids = session.query(Company.id).filter(Company.name.in_(company_names)).all()
                company_ids = [cid[0] for cid in company_ids]

                # Fetch recent news entries for the specified company IDs
                news_entries = (session.query(News, Company.name)
                                .join(NewsCompanyAssociation)
                                .join(Company)
                                .filter(Company.id.in_(company_ids))
                                .order_by(News.id.desc())
                                .all())

                # Organize news entries by company name
                result = {}
                for news, company_name in news_entries:
                    if company_name not in result:
                        result[company_name] = []
                    if len(result[company_name]) < n:
                        result[company_name].append(news)
                
                return result
            except:
                session.rollback()
                return apiError(400, "Error occcured in fetching n_details for different company")
            

