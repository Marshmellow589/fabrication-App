import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table } from 'react-bootstrap';
import { useAuth } from '../../context/AuthContext';
import api from '../../config/api';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    projects: 0,
    materialInspections: 0,
    fitupInspections: 0,
    finalInspections: 0,
    ndtRequests: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [projects, materials, fitups, finals, ndts] = await Promise.all([
          api.get('/projects'),
          api.get('/material'),
          api.get('/fitup'),
          api.get('/final'),
          api.get('/ndt')
        ]);
        
        setStats({
          projects: projects.data.length,
          materialInspections: materials.data.length,
          fitupInspections: fitups.data.length,
          finalInspections: finals.data.length,
          ndtRequests: ndts.data.length
        });
      } catch (error) {
        console.error('获取统计数据失败:', error);
      }
    };

    fetchStats();
  }, []);

  return (
    <Container className="mt-4">
      <h2>仪表盘</h2>
      <p>欢迎回来, {user?.username}!</p>
      
      <Row className="mb-4">
        <Col md={6} lg={3}>
          <Card bg="primary" text="white" className="mb-3">
            <Card.Body>
              <Card.Title>项目总数</Card.Title>
              <Card.Text className="display-4">{stats.projects}</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6} lg={3}>
          <Card bg="success" text="white" className="mb-3">
            <Card.Body>
              <Card.Title>材料检验</Card.Title>
              <Card.Text className="display-4">{stats.materialInspections}</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6} lg={3}>
          <Card bg="info" text="white" className="mb-3">
            <Card.Body>
              <Card.Title>组对检验</Card.Title>
              <Card.Text className="display-4">{stats.fitupInspections}</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6} lg={3}>
          <Card bg="warning" text="white" className="mb-3">
            <Card.Body>
              <Card.Title>最终检验</Card.Title>
              <Card.Text className="display-4">{stats.finalInspections}</Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        <Col>
          <Card>
            <Card.Header>最近的NDT请求</Card.Header>
            <Card.Body>
              <Table striped bordered hover>
                <thead>
                  <tr>
                    <th>项目</th>
                    <th>部门</th>
                    <th>负责人</th>
                    <th>状态</th>
                    <th>创建时间</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td colSpan="5" className="text-center">暂无数据</td>
                  </tr>
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;