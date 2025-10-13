import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from './Login';
import { AuthProvider } from '../../context/AuthContext';
import api from '../../config/api';

// Mock API
jest.mock('../../config/api');

describe('Login Component', () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
  });

  test('renders login form', () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    );

    expect(screen.getByText('登录')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('请输入用户名')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('请输入密码')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /登录/i })).toBeInTheDocument();
  });

  test('displays error message on failed login', async () => {
    api.post.mockRejectedValueOnce({
      response: { data: { detail: 'Invalid credentials' } }
    });

    render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    );

    fireEvent.change(screen.getByPlaceholderText('请输入用户名'), {
      target: { value: 'testuser' }
    });
    fireEvent.change(screen.getByPlaceholderText('请输入密码'), {
      target: { value: 'wrongpassword' }
    });
    fireEvent.click(screen.getByRole('button', { name: /登录/i }));

    await waitFor(() => {
      expect(screen.getByText('Invalid credentials')).toBeInTheDocument();
    });
  });

  test('redirects to dashboard on successful login', async () => {
    const mockNavigate = jest.fn();
    jest.mock('react-router-dom', () => ({
      ...jest.requireActual('react-router-dom'),
      useNavigate: () => mockNavigate,
    }));

    api.post.mockResolvedValueOnce({
      data: { access_token: 'mock-token' }
    });
    api.get.mockResolvedValueOnce({
      data: { username: 'testuser', role: 'member' }
    });

    render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    );

    fireEvent.change(screen.getByPlaceholderText('请输入用户名'), {
      target: { value: 'testuser' }
    });
    fireEvent.change(screen.getByPlaceholderText('请输入密码'), {
      target: { value: 'correctpassword' }
    });
    fireEvent.click(screen.getByRole('button', { name: /登录/i }));

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });
});