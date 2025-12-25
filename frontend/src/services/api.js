import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Resume Services
export const resumeService = {
  uploadResume: async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/resume/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  analyzeResume: async (resumeText, jobRole, jobDescription) => {
    const params = new URLSearchParams();
    params.append('resume_text', resumeText);
    params.append('job_role', jobRole);
    if (jobDescription) {
      params.append('job_description', jobDescription);
    }

    const response = await api.post('/resume/analyze', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  checkATS: async (resumeText, jobDescription) => {
    const params = new URLSearchParams();
    params.append('resume_text', resumeText);
    if (jobDescription) {
      params.append('job_description', jobDescription);
    }

    const response = await api.post('/resume/ats-check', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },
};

// Company Services
export const companyService = {
  researchCompany: async (companyName) => {
    const params = new URLSearchParams();
    params.append('company_name', companyName);

    const response = await api.post('/company/research', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },
};

// Analysis Services
export const analysisService = {
  generateRecommendations: async (data) => {
    const response = await api.post('/analysis/recommendations', data);
    return response.data;
  },
};

// Document Services
export const documentService = {
  generateDocuments: async (data) => {
    const response = await api.post('/documents/generate', data);
    return response.data;
  },

  downloadDocument: async (filename) => {
    const response = await api.get(`/documents/download/${filename}`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export default api;
