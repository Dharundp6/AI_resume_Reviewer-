import axios from 'axios';

// Use relative URL for production (Vercel), absolute URL for local development
const API_BASE_URL = process.env.REACT_APP_API_URL ||
  (process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000/api');

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
    const formData = new FormData();
    formData.append('resume_text', resumeText);
    formData.append('job_role', jobRole);
    if (jobDescription) {
      formData.append('job_description', jobDescription);
    }

    const response = await api.post('/resume/analyze', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  checkATS: async (resumeText, jobDescription) => {
    const formData = new FormData();
    formData.append('resume_text', resumeText);
    if (jobDescription) {
      formData.append('job_description', jobDescription);
    }

    const response = await api.post('/resume/ats-check', formData, {
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
    const formData = new FormData();
    formData.append('company_name', companyName);

    const response = await api.post('/company/research', formData, {
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
