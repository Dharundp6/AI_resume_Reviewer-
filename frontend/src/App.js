import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import {
  Container,
  Box,
  Stepper,
  Step,
  StepLabel,
  Paper,
  Typography,
} from '@mui/material';
import UploadResume from './components/UploadResume';
import JobDetails from './components/JobDetails';
import Analysis from './components/Analysis';
import Results from './components/Results';
import './App.css';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#667eea',
    },
    secondary: {
      main: '#764ba2',
    },
  },
});

const steps = ['Upload Resume', 'Job Details', 'Analysis', 'Results'];

function App() {
  const [activeStep, setActiveStep] = useState(0);
  const [resumeData, setResumeData] = useState(null);
  const [jobData, setJobData] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
    setResumeData(null);
    setJobData(null);
    setAnalysisResults(null);
  };

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <UploadResume
            onNext={handleNext}
            setResumeData={setResumeData}
            resumeData={resumeData}
          />
        );
      case 1:
        return (
          <JobDetails
            onNext={handleNext}
            onBack={handleBack}
            setJobData={setJobData}
            jobData={jobData}
          />
        );
      case 2:
        return (
          <Analysis
            onNext={handleNext}
            onBack={handleBack}
            resumeData={resumeData}
            jobData={jobData}
            setAnalysisResults={setAnalysisResults}
          />
        );
      case 3:
        return (
          <Results
            onBack={handleBack}
            onReset={handleReset}
            analysisResults={analysisResults}
            resumeData={resumeData}
            jobData={jobData}
          />
        );
      default:
        return 'Unknown step';
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box className="app-background">
        <Container maxWidth="lg" sx={{ py: 4 }}>
          <Paper elevation={3} sx={{ p: 4, borderRadius: 2 }}>
            <Typography
              variant="h3"
              component="h1"
              gutterBottom
              align="center"
              sx={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontWeight: 'bold',
                mb: 4,
              }}
            >
              Job Application Optimizer
            </Typography>

            <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
              {steps.map((label) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>

            <Box sx={{ minHeight: 400 }}>
              {getStepContent(activeStep)}
            </Box>
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
