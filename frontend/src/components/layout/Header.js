import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';

const Header = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">工业检验平台</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            {user && (
              <>
                <Nav.Link as={Link} to="/">仪表盘</Nav.Link>
                <Nav.Link as={Link} to="/material">材料检验</Nav.Link>
                <Nav.Link as={Link} to="/fitup">组对检验</Nav.Link>
                <Nav.Link as={Link} to="/final">最终检验</Nav.Link>
                <Nav.Link as={Link} to="/ndt">NDT请求</Nav.Link>
                {user.role === 'admin' && (
                  <>
                    <Nav.Link as={Link} to="/users">用户管理</Nav.Link>
                    <Nav.Link as={Link} to="/projects">项目管理</Nav.Link>
                  </>
                )}
              </>
            )}
          </Nav>
          {user && (
            <Nav>
              <Nav.Item className="d-flex align-items-center me-3">
                <span className="text-white">欢迎, {user.username}</span>
              </Nav.Item>
              <Button variant="outline-light" onClick={handleLogout}>
                退出登录
              </Button>
            </Nav>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;