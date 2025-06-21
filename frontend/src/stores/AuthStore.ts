import { makeAutoObservable } from 'mobx';
import { makePersistable } from 'mobx-persist-store';
import { ReadUser } from '../api/types';

interface Tokens {
  refresh: string;
  access: string;
}

class AuthStore {
  isAuth = false;
  user: ReadUser | null = null;
  tokens: Tokens | null = null;
  isLoading = false;
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
    
    // Для сохранения состояния в localStorage
    makePersistable(this, {
      name: 'AuthStore',
      properties: ['isAuth', 'user', 'tokens'],
      storage: window.localStorage,
    });
  }

  setAuth(bool: boolean) {
    this.isAuth = bool;
  }

  setUser(user: ReadUser | null) {
    this.user = user;
  }

  setTokens(tokens: Tokens | null) {
    this.tokens = tokens;
  }

  setLoading(bool: boolean) {
    this.isLoading = bool;
  }

  setError(error: string | null) {
    this.error = error;
  }

  async login(username: string, password: string) {
    this.setLoading(true);
    this.setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json', // ← Добавляем
        },
        body: JSON.stringify({ username, password }),
      });

  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      // Проверяем, есть ли тело ответа
      const contentLength = response.headers.get('Content-Length');
      if (contentLength === '0' || !response.body) {
        throw new Error('Empty response');
      }
  
      // Альтернативный способ проверки
      const text = await response.text();
      if (!text) {
        throw new Error('Empty response body');
      }
  
      const data = JSON.parse(text);

      console.log(data);
      
      this.setUser(data.user || data);
      this.setTokens(data.tokens);
      this.setAuth(true);
      
      return true;
    } catch (error) {
      console.error('Login error:', error);
      this.setError(error instanceof Error ? error.message : 'Server error');
      return false;
    } finally {
      this.setLoading(false);
    }
  }

  async register(userData: {
    username: string;
    email: string;
    password: string;
    first_name: string;
    last_name: string;
    middle_name?: string;
    phone?: string;
  }) {
    this.setLoading(true);
    this.setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка регистрации');
      }


      const data = await response.json();

      this.setUser(data);
      this.setTokens(data.tokens);
      this.setAuth(true);
      
      return true;
    } catch (error) {
      this.setError(error instanceof Error ? error.message : 'Произошла ошибка');
      return false;
    } finally {
      this.setLoading(false);
    }
  }

  async logout() {
    try {
      if (!this.tokens?.refresh) {
        throw new Error("No refresh token available");
      }
  
      const response = await fetch('http://localhost:8000/api/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.tokens.access}`,
        },
        body: JSON.stringify({
          refresh: this.tokens.refresh  // Отправляем refresh token
        }),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Logout failed');
      }
  
      // Очищаем состояние независимо от ответа сервера
      this.setAuth(false);
      this.setUser(null);
      this.setTokens(null);
      
    } catch (error) {
      console.error('Logout error:', error);
      // Все равно очищаем состояние на фронте
      this.setAuth(false);
      this.setUser(null);
      this.setTokens(null);
    }
  }

  async refreshToken() {
    if (!this.tokens?.refresh) {
      return false;
    }

    try {
      const response = await fetch('http://localhost:8000/api/token/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: this.tokens.refresh }),
      });

      if (!response.ok) {
        throw new Error('Ошибка обновления токена');
      }

      const data = await response.json();
      this.setTokens({
        ...this.tokens,
        access: data.access,
      });
      
      return true;
    } catch (error) {
      this.logout();
      return false;
    }
  }
}

export const authStore = new AuthStore();