import requests
from requests.auth import HTTPBasicAuth
from typing import Optional, Dict, List, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import User

class NetworkHelper:
    
    def __init__(self, base_url: str, username: Optional[str] = None, password: Optional[str] = None, 
                 token: Optional[str] = None, session_key: Optional[str] = None, user: Optional['User'] = None):
        self.base_url = base_url.rstrip('/')
        self.auth = None
        self.headers = {}
        self.session = requests.Session()
        
        # HTTP Basic Auth
        if username and password:
            self.auth = HTTPBasicAuth(username, password)
        
        # Token-based auth
        elif token:
            self.headers['Authorization'] = f'Token {token}'
        
        # Django session auth
        elif session_key:
            self.session.cookies['sessionid'] = session_key
        
        # User-based auth (get from Django session)
        elif user and user.is_authenticated:
            # Можна додати логіку для отримання токену користувача
            pass
    
    def get_list(self) -> List[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/", 
                auth=self.auth, 
                headers=self.headers, 
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            print(f"Помилка підключення до {self.base_url}")
            return []
        except requests.exceptions.Timeout:
            print(f"Час очікування відповіді від {self.base_url} вичерпано")
            return []
        except requests.exceptions.HTTPError as e:
            print(f"HTTP помилка: {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Помилка запиту: {e}")
            return []
        except ValueError:
            print("Помилка декодування JSON")
            return []
    
    def get_by_id(self, obj_id: int) -> Optional[Dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/{obj_id}/", 
                auth=self.auth, 
                headers=self.headers, 
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            print(f"Помилка підключення до {self.base_url}/{obj_id}/")
            return None
        except requests.exceptions.Timeout:
            print(f"Час очікування відповіді вичерпано")
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Об'єкт з ID {obj_id} не знайдено")
            else:
                print(f"HTTP помилка: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Помилка запиту: {e}")
            return None
        except ValueError:
            print("Помилка декодування JSON")
            return None
    
    def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            response = self.session.post(
                f"{self.base_url}/",
                json=data,
                auth=self.auth,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            print(f"Помилка підключення до {self.base_url}")
            return None
        except requests.exceptions.Timeout:
            print(f"Час очікування відповіді вичерпано")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP помилка: {e}")
            if hasattr(e.response, 'text'):
                print(f"Деталі помилки: {e.response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Помилка запиту: {e}")
            return None
        except ValueError:
            print("Помилка декодування JSON")
            return None
    
    def update(self, obj_id: int, data: Dict[str, Any], partial: bool = False) -> Optional[Dict[str, Any]]:
        try:
            method = self.session.patch if partial else self.session.put
            response = method(
                f"{self.base_url}/{obj_id}/",
                json=data,
                auth=self.auth,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            print(f"Помилка підключення до {self.base_url}/{obj_id}/")
            return None
        except requests.exceptions.Timeout:
            print(f"Час очікування відповіді вичерпано")
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Об'єкт з ID {obj_id} не знайдено")
            else:
                print(f"HTTP помилка: {e}")
            if hasattr(e.response, 'text'):
                print(f"Деталі помилки: {e.response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Помилка запиту: {e}")
            return None
        except ValueError:
            print("Помилка декодування JSON")
            return None
    
    def delete(self, obj_id: int) -> bool:
        try:
            response = self.session.delete(
                f"{self.base_url}/{obj_id}/",
                auth=self.auth,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.exceptions.ConnectionError:
            print(f"Помилка підключення до {self.base_url}/{obj_id}/")
            return False
        except requests.exceptions.Timeout:
            print(f"Час очікування відповіді вичерпано")
            return False
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Об'єкт з ID {obj_id} не знайдено")
            else:
                print(f"HTTP помилка: {e}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"Помилка запиту: {e}")
            return False
