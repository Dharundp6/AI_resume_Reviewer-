import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Paper,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DescriptionIcon from '@mui/icons-material/Description';
import { resumeService } from '../services/api';

function UploadResume({ onNext, setResumeData, resumeData }) {
  const [file, setFile] = useState(resumeData?.file || null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setError(null);
      setLoading(true);

      try {
        const result = await resumeService.uploadResume(uploadedFile);
        setResumeData({
          file: uploadedFile,
          text: result.resume_text,
          filename: result.filename,
        });
        setLoading(false);
      } catch (err) {
        setError('Failed to upload resume. Please try again.');
        setLoading(false);
      }
    }
  }, [setResumeData]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    multiple: false,
  });

  const handleNext = () => {
    if (resumeData) {
      onNext();
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Upload Your Resume
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Upload your resume in PDF format to get started with AI-powered analysis
      </Typography>

      <Paper
        {...getRootProps()}
        sx={{
          p: 4,
          textAlign: 'center',
          cursor: 'pointer',
          border: '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.400',
          backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
          transition: 'all 0.3s ease',
          '&:hover': {
            borderColor: 'primary.main',
            backgroundColor: 'action.hover',
          },
        }}
      >
        <input {...getInputProps()} />
        <CloudUploadIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />

        {loading ? (
          <Box>
            <CircularProgress sx={{ mb: 2 }} />
            <Typography>Processing your resume...</Typography>
          </Box>
        ) : file ? (
          <Box>
            <DescriptionIcon sx={{ fontSize: 48, color: 'success.main', mb: 1 }} />
            <Typography variant="h6" color="success.main">
              {file.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Resume uploaded successfully!
            </Typography>
          </Box>
        ) : (
          <Box>
            <Typography variant="h6" gutterBottom>
              {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume here'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              or click to browse (PDF only)
            </Typography>
          </Box>
        )}
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          onClick={handleNext}
          disabled={!resumeData || loading}
          size="large"
        >
          Next
        </Button>
      </Box>
    </Box>
  );
}

export default UploadResume;
