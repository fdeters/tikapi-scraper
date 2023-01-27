import tikapi
import pandas as pd


class Scraper:
    def __init__(self, api_obj: tikapi.TikAPI) -> None:
        self._api = api_obj

        self._num_calls = 0

    
    def get_hashtag_feed(self, hashtag: str) -> pd.DataFrame:
        try:
            df_list = []

            hashtag_id = self.get_hashtag_id(hashtag)
            response = self._api.public.hashtag(
                id=hashtag_id
            )
            self._num_calls += 1

            while(response):
                cursor = response.json().get('cursor')
                print(f"Retrieved {cursor} items so far for #{hashtag}")
                response = response.next_items()
                self._num_calls += 1
                try:
                    result = response.json()
                    df = pd.json_normalize((result['itemList']))
                    df['hashtag_feed'] = hashtag
                    df_list.append(df)
                except KeyError:
                    pass
                except AttributeError:
                    pass
            
            return self.concatenate_dataframes(df_list)
                
        except tikapi.ValidationException as e:
            print(e, e.field)

        except tikapi.ResponseException as e:
            print(e, e.response.status_code)
        
        return pd.DataFrame()


    def get_hashtag_id(self, hashtag: str) -> str:
        response = self._api.public.hashtag(
            name=hashtag
        )
        self._num_calls += 1
        return response.json()['challengeInfo']['challenge']['id']

    
    @property
    def num_calls(self):
        return self._num_calls

    @staticmethod
    def concatenate_dataframes(items_to_concatenate) -> pd.DataFrame:
        """Wrap pd.concat() to handle empty lists"""
        try: 
            return pd.concat(items_to_concatenate)
        except ValueError:
            return pd.DataFrame()