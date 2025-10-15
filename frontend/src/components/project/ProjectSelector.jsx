import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { getProjects } from '../../utils/api';
import './ProjectSelector.css';

const ProjectSelector = ({ onProjectSelect }) => {
  const { token } = useAuth();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        const projectsData = await getProjects(token);
        setProjects(projectsData);
      } catch (err) {
        setError('Failed to load projects');
        console.error('Error fetching projects:', err);
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchProjects();
    }
  }, [token]);

  const handleProjectSelect = (project) => {
    onProjectSelect(project);
  };

  if (loading) {
    return (
      <div className="project-selector-container">
        <div className="loading-spinner">Loading projects...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="project-selector-container">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="project-selector-container">
      <div className="project-selector-header">
        <h2>Select a Project</h2>
        <p>Choose which project you want to work on</p>
      </div>
      
      <div className="projects-grid">
        {projects.map((project) => (
          <div
            key={project.id}
            className="project-card"
            onClick={() => handleProjectSelect(project)}
          >
            <div className="project-info">
              <h3 className="project-name">{project.project_name}</h3>
              <p className="project-number">{project.project_number}</p>
              <p className="project-client">Client: {project.client}</p>
              <p className="project-status">
                Status: <span className={`status-${project.status}`}>{project.status}</span>
              </p>
              {project.project_manager && (
                <p className="project-manager">Manager: {project.project_manager}</p>
              )}
            </div>
            <div className="project-select-button">
              Select Project
            </div>
          </div>
        ))}
      </div>

      {projects.length === 0 && (
        <div className="no-projects">
          <h3>No Projects Available</h3>
          <p>There are no projects in the system yet.</p>
          <p>Please contact an administrator to create projects.</p>
        </div>
      )}
    </div>
  );
};

export default ProjectSelector;
