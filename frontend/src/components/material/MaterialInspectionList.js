import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Row, Col, Alert } from 'react-bootstrap';
import { useAuth } from '../../context/AuthContext';
import api from '../../config/api';

const MaterialInspectionList = () => {
  const { hasAnyRole } = useAuth();
  const [inspections, setInspections] = useState([]);
  const [projects, setProjects] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingInspection, setEditingInspection] = useState(null);
  const [formData, setFormData] = useState({
    project_id: '',
    material_type: '',
    grade: '',
    thickness: '',
    size: '',
    spec: '',
    material_category: '',
    inspection_date: '',
    inspection_result: 'Pass',
    mvr_report_no: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [inspectionsRes, projectsRes] = await Promise.all([
        api.get('/material'),
        api.get('/projects')
      ]);
      setInspections(inspectionsRes.data);
      setProjects(projectsRes.data);
      setLoading(false);
    } catch (error) {
      setError('获取数据失败');
      setLoading(false);
    }
  };

  const handleShowModal = (inspection = null) => {
    if (inspection) {
      setEditingInspection(inspection);
      setFormData({
        project_id: inspection.project_id,
        material_type: inspection.material_type,
        grade: inspection.grade,
        thickness: inspection.thickness,
        size: inspection.size || '',
        spec: inspection.spec || '',
        material_category: inspection.material_category || '',
        inspection_date: inspection.inspection_date.split('T')[0],
        inspection_result: inspection.inspection_result,
        mvr_report_no: inspection.mvr_report_no
      });
    } else {
      setEditingInspection(null);
      setFormData({
        project_id: '',
        material_type: '',
        grade: '',
        thickness: '',
        size: '',
        spec: '',
        material_category: '',
        inspection_date: '',
        inspection_result: 'Pass',
        mvr_report_no: ''
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingInspection(null);
    setError('');
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      if (editingInspection) {
        await api.put(`/material/${editingInspection.id}`, formData);
      } else {
        await api.post('/material', formData);
      }
      handleCloseModal();
      fetchData();
    } catch (error) {
      setError(error.response?.data?.detail || '保存失败');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('确定要删除这条记录吗？')) {
      try {
        await api.delete(`/material/${id}`);
        fetchData();
      } catch (error) {
        setError('删除失败');
      }
    }
  };

  if (loading) {
    return <div className="text-center mt-5">加载中...</div>;
  }

  return (
    <div className="p-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>材料检验记录</h2>
        {hasAnyRole('admin', 'member') && (
          <Button variant="primary" onClick={() => handleShowModal()}>
            新增记录
          </Button>
        )}
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>项目</th>
            <th>材料类型</th>
            <th>等级</th>
            <th>厚度</th>
            <th>检验日期</th>
            <th>结果</th>
            <th>MVR报告号</th>
            {hasAnyRole('admin', 'member') && <th>操作</th>}
          </tr>
        </thead>
        <tbody>
          {inspections.length === 0 ? (
            <tr>
              <td colSpan={hasAnyRole('admin', 'member') ? 8 : 7} className="text-center">
                暂无数据
              </td>
            </tr>
          ) : (
            inspections.map(inspection => (
              <tr key={inspection.id}>
                <td>{projects.find(p => p.id === inspection.project_id)?.name || inspection.project_id}</td>
                <td>{inspection.material_type}</td>
                <td>{inspection.grade}</td>
                <td>{inspection.thickness}</td>
                <td>{inspection.inspection_date.split('T')[0]}</td>
                <td>
                  <span className={`badge bg-${
                    inspection.inspection_result === 'Pass' ? 'success' :
                    inspection.inspection_result === 'Fail' ? 'danger' : 'warning'
                  }`}>
                    {inspection.inspection_result}
                  </span>
                </td>
                <td>{inspection.mvr_report_no}</td>
                {hasAnyRole('admin', 'member') && (
                  <td>
                    <Button 
                      variant="outline-primary" 
                      size="sm" 
                      className="me-2"
                      onClick={() => handleShowModal(inspection)}
                    >
                      编辑
                    </Button>
                    <Button 
                      variant="outline-danger" 
                      size="sm"
                      onClick={() => handleDelete(inspection.id)}
                    >
                      删除
                    </Button>
                  </td>
                )}
              </tr>
            ))
          )}
        </tbody>
      </Table>

      {/* Modal for Create/Edit */}
      <Modal show={showModal} onHide={handleCloseModal} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            {editingInspection ? '编辑材料检验记录' : '新增材料检验记录'}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {error && <Alert variant="danger">{error}</Alert>}
          <Form onSubmit={handleSubmit}>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3" controlId="project_id">
                  <Form.Label>项目 *</Form.Label>
                  <Form.Select
                    name="project_id"
                    value={formData.project_id}
                    onChange={handleChange}
                    required
                  >
                    <option value="">请选择项目</option>
                    {projects.map(project => (
                      <option key={project.id} value={project.id}>
                        {project.name} ({project.code})
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3" controlId="material_type">
                  <Form.Label>材料类型 *</Form.Label>
                  <Form.Control
                    type="text"
                    name="material_type"
                    value={formData.material_type}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3" controlId="grade">
                  <Form.Label>等级 *</Form.Label>
                  <Form.Control
                    type="text"
                    name="grade"
                    value={formData.grade}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3" controlId="thickness">
                  <Form.Label>厚度 *</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.01"
                    name="thickness"
                    value={formData.thickness}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3" controlId="size">
                  <Form.Label>尺寸</Form.Label>
                  <Form.Control
                    type="text"
                    name="size"
                    value={formData.size}
                    onChange={handleChange}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3" controlId="spec">
                  <Form.Label>规格</Form.Label>
                  <Form.Control
                    type="text"
                    name="spec"
                    value={formData.spec}
                    onChange={handleChange}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3" controlId="material_category">
                  <Form.Label>材料类别</Form.Label>
                  <Form.Control
                    type="text"
                    name="material_category"
                    value={formData.material_category}
                    onChange={handleChange}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3" controlId="inspection_date">
                  <Form.Label>检验日期 *</Form.Label>
                  <Form.Control
                    type="date"
                    name="inspection_date"
                    value={formData.inspection_date}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3" controlId="inspection_result">
                  <Form.Label>检验结果 *</Form.Label>
                  <Form.Select
                    name="inspection_result"
                    value={formData.inspection_result}
                    onChange={handleChange}
                    required
                  >
                    <option value="Pass">通过</option>
                    <option value="Fail">失败</option>
                    <option value="Conditional">有条件通过</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3" controlId="mvr_report_no">
                  <Form.Label>MVR报告号 *</Form.Label>
                  <Form.Control
                    type="text"
                    name="mvr_report_no"
                    value={formData.mvr_report_no}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <div className="d-flex justify-content-end">
              <Button variant="secondary" onClick={handleCloseModal} className="me-2">
                取消
              </Button>
              <Button variant="primary" type="submit">
                保存
              </Button>
            </div>
          </Form>
        </Modal.Body>
      </Modal>
    </div>
  );
};

export default MaterialInspectionList;