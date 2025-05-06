import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

interface User {
  email: string;
  nome: string;
  foto?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, nome: string, password: string, foto?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Set default authorization header
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // Fetch user data
      fetchUserData();
    }
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/user');
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Error fetching user data:', error);
      logout();
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post('http://localhost:8000/auth/token', {
        username: email,
        password: password,
      });
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      await fetchUserData();
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (email: string, nome: string, password: string, foto?: string) => {
    try {
      const response = await axios.post('http://localhost:8000/auth/register', {
        email,
        nome,
        senha: password,
        foto,
      });
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      await fetchUserData();
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}; 