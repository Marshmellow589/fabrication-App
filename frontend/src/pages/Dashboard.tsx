import React, { useEffect, useState } from 'react';
import { Table, Button, Space, Tag, Modal, Form, Input, Select } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { fetchMaterials, createMaterial } from '../store/materialSlice';
import type { MaterialInspection } from '../types';

const { Option } = Select;

const Dashboard: React.FC = () => {
  const dispatch = useAppDispatch();
  const materials = useAppSelector(state => state.material.items);
  const loading = useAppSelector(state => state.material.loading);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    dispatch(fetchMaterials());
  }, [dispatch]);

  const handleCreate = async (values: any) => {
    await dispatch(createMaterial(values));
    setIsModalOpen(false);
    form.resetFields();
  };

  const columns = [
    { title: 'Material Type', dataIndex: 'material_type', key: 'material_type' },
    { title: 'Grade', dataIndex: 'grade', key: 'grade' },
    { title: 'Thickness', dataIndex: 'thickness', key: 'thickness' },
    { title: 'MVR Report No', dataIndex: 'mvr_report_no', key: 'mvr_report_no' },
    { title: 'Result', dataIndex: 'inspection_result', key: 'inspection_result',
      render: (result: string) => (
        <Tag color={result === 'Pass' ? 'green' : result === 'Fail' ? 'red' : 'orange'}>
          {result}
        </Tag>
      )
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <Button type="link">Edit</Button>
          <Button type="link" danger>Delete</Button>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <h2>Material Inspection Records</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>
          Add New Record
        </Button>
      </div>
      <Table
        columns={columns}
        dataSource={materials}
        rowKey="id"
        loading={loading}
        pagination={{ pageSize: 10 }}
      />

      <Modal
        title="Add Material Inspection"
        open={isModalOpen}
        onOk={() => form.submit()}
        onCancel={() => setIsModalOpen(false)}
      >
        <Form form={form} layout="vertical" onFinish={handleCreate}>
          <Form.Item name="material_type" label="Material Type" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="grade" label="Grade" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="thickness" label="Thickness (mm)" rules={[{ required: true }]}>
            <Input type="number" />
          </Form.Item>
          <Form.Item name="mvr_report_no" label="MVR Report No" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="inspection_result" label="Result" rules={[{ required: true }]}>
            <Select>
              <Option value="Pass">Pass</Option>
              <Option value="Fail">Fail</Option>
              <Option value="Conditional">Conditional</Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Dashboard;