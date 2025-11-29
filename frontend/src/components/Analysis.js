import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Typography,
  CircularProgress,
  Alert,
  LinearProgress,
} from '@mui/material';
import { resumeService, companyService, analysisService } from '../services/api';

function Analysis({ onNext, onBack, resumeData, jobData, setAnalysisResults }) {
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');

  useEffect(() => {
    performAnalysis();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const performAnalysis = async () => {
    setError(null);

    try {
      // Step 1: Analyze Resume
      setCurrentStep('Analyzing your resume...');
      setProgress(25);
      const resumeAnalysis = await resumeService.analyzeResume(
        resumeData.text,
        jobData.jobRole,
        jobData.jobDescription
      );

      // Step 2: Check ATS Compatibility
      setCurrentStep('Checking ATS compatibility...');
      setProgress(50);
      const atsScore = await resumeService.checkATS(
        resumeData.text,
        jobData.jobDescription
      );

      // Step 3: Research Company
      setCurrentStep('Researching company information...');
      setProgress(75);
      const companyResearch = await companyService.researchCompany(
        jobData.companyName
      );

      // Step 4: Generate Recommendations
      setCurrentStep('Generating personalized recommendations...');
      setProgress(90);
      const recommendations = await analysisService.generateRecommendations({
        job_role: jobData.jobRole,
        company_name: jobData.companyName,
        analysis: resumeAnalysis,
        ats_score: atsScore,
        company_research: companyResearch,
      });

      setProgress(100);
      setCurrentStep('Analysis complete!');

      const results = {
        resumeAnalysis,
        atsScore,
        companyResearch,
        recommendations,
      };

      console.log('Analysis complete - Setting results:', results);
      setAnalysisResults(results);

      setTimeout(() => {
        console.log('Moving to next step...');
        onNext();
      }, 1000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
    }
  };

  return (
    <Box sx={{ textAlign: 'center', py: 4 }}>
      <Typography variant="h5" gutterBottom>
        Analyzing Your Application
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
        Our AI is working hard to optimize your job application
      </Typography>

      {error ? (
        <Box>
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <Button onClick={onBack}>Back</Button>
            <Button variant="contained" onClick={performAnalysis}>
              Retry
            </Button>
          </Box>
        </Box>
      ) : (
        <Box sx={{ maxWidth: 600, mx: 'auto' }}>
          <CircularProgress size={80} sx={{ mb: 3 }} />

          <Typography variant="h6" sx={{ mb: 2 }}>
            {currentStep}
          </Typography>

          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{ mb: 2, height: 8, borderRadius: 4 }}
          />

          <Typography variant="body2" color="text.secondary">
            {progress}% Complete
          </Typography>

          <Box sx={{ mt: 4 }}>
            <Typography variant="body2" color="text.secondary">
              This process includes:
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Resume Analysis • ATS Check • Company Research • AI Recommendations
            </Typography>
          </Box>
        </Box>
      )}
    </Box>
  );
}

export default Analysis;
