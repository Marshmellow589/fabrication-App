import React, { createContext, useContext, useState, useEffect } from 'react';

export interface User {
  id: number;
  username: string;
  email: string;
  role: 'Inspector' | 'QA Manager' | 'Admin';
  permissions: string[];
  token: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (userData: User) => void;
  logout: () => void;
  hasPermission: (permission: string) => boolean;
  isAdmin: () => boolean;
  isQAManager: () => boolean;
  isInspector: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem('user');
    if (saved) setUser(JSON.parse(saved));
  }, []);

  const login = (userData: User) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', userData.token);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  };

  const hasPermission = (permission: string) => {
    return user?.permissions.includes(permission) || false;
  };

  const isAdmin = () => user?.role === 'Admin';
  const isQAManager = () => user?.role === 'QA Manager';
  const isInspector = () => user?.role === 'Inspector';

  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated: !!user, login, logout, hasPermission, isAdmin, isQAManager, isInspector }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};