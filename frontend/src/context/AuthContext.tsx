import React, { createContext, useContext, useState, useEffect } from 'react';

export interface User {
  id: number;
  username: string;
  email: string;
  role: 'Inspector' | 'QA Manager' | 'Admin';
  permissions: string[];
  token: string;
}

export interface Project {
  id: number;
  project_number: string;
  project_name: string;
  client: string;
  status: string;
  project_manager?: string;
}

interface AuthContextType {
  user: User | null;
  selectedProject: Project | null;
  isAuthenticated: boolean;
  login: (userData: User) => void;
  logout: () => void;
  selectProject: (project: Project) => void;
  clearProject: () => void;
  hasPermission: (permission: string) => boolean;
  isAdmin: () => boolean;
  isQAManager: () => boolean;
  isInspector: () => boolean;
  token: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem('user');
    const savedProject = localStorage.getItem('selectedProject');
    if (saved) setUser(JSON.parse(saved));
    if (savedProject) setSelectedProject(JSON.parse(savedProject));
  }, []);

  const login = (userData: User) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', userData.token);
  };

  const logout = () => {
    setUser(null);
    setSelectedProject(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    localStorage.removeItem('selectedProject');
  };

  const selectProject = (project: Project) => {
    setSelectedProject(project);
    localStorage.setItem('selectedProject', JSON.stringify(project));
  };

  const clearProject = () => {
    setSelectedProject(null);
    localStorage.removeItem('selectedProject');
  };

  const hasPermission = (permission: string) => {
    return user?.permissions.includes(permission) || false;
  };

  const isAdmin = () => user?.role === 'Admin';
  const isQAManager = () => user?.role === 'QA Manager';
  const isInspector = () => user?.role === 'Inspector';

  const token = user?.token || null;

  return (
    <AuthContext.Provider
      value={{
        user,
        selectedProject,
        isAuthenticated: !!user,
        login,
        logout,
        selectProject,
        clearProject,
        hasPermission,
        isAdmin,
        isQAManager,
        isInspector,
        token
      }}
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
