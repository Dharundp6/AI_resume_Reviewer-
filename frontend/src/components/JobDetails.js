import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Grid,
} from '@mui/material';

function JobDetails({ onNext, onBack, setJobData, jobData }) {
  const [formData, setFormData] = useState({
    jobRole: jobData?.jobRole || '',
    companyName: jobData?.companyName || '',
    jobDescription: jobData?.jobDescription || '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleNext = () => {
    if (formData.jobRole && formData.companyName) {
      setJobData(formData);
      onNext();
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Job Details
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Provide information about the job you're applying for
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            required
            label="Job Role"
            name="jobRole"
            value={formData.jobRole}
            onChange={handleChange}
            placeholder="e.g., Senior Software Engineer"
            helperText="The position you're applying for"
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            required
            label="Company Name"
            name="companyName"
            value={formData.companyName}
            onChange={handleChange}
            placeholder="e.g., Google, Microsoft"
            helperText="Company you're applying to"
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            multiline
            rows={8}
            label="Job Description"
            name="jobDescription"
            value={formData.jobDescription}
            onChange={handleChange}
            placeholder="Paste the full job description here..."
            helperText="Optional but recommended for better analysis"
          />
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={onBack} size="large">
          Back
        </Button>
        <Button
          variant="contained"
          onClick={handleNext}
          disabled={!formData.jobRole || !formData.companyName}
          size="large"
        >
          Next
        </Button>
      </Box>
    </Box>
  );
}

export default JobDetails;
