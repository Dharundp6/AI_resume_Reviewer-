import React, { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
  Alert,
  CircularProgress,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DownloadIcon from '@mui/icons-material/Download';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import { documentService } from '../services/api';

function Results({ onBack, onReset, analysisResults, resumeData, jobData }) {
  const [generatingDocs, setGeneratingDocs] = useState(false);
  const [documents, setDocuments] = useState(null);
  const [docError, setDocError] = useState(null);

  console.log('Results component - analysisResults:', analysisResults);
  console.log('Results component - resumeData:', resumeData);
  console.log('Results component - jobData:', jobData);

  if (!analysisResults) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          No analysis results found. Please go back and run the analysis again.
        </Alert>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Debug Info: analysisResults is {String(analysisResults)}
        </Typography>
        <Button variant="contained" onClick={onBack}>Go Back</Button>
      </Box>
    );
  }

  const { resumeAnalysis, atsScore, companyResearch, recommendations } = analysisResults;

  const getScoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'error';
  };

  const handleGenerateDocuments = async () => {
    setGeneratingDocs(true);
    setDocError(null);

    try {
      const result = await documentService.generateDocuments({
        resume_text: resumeData.text,
        job_role: jobData.jobRole,
        company_name: jobData.companyName,
        analysis: resumeAnalysis,
        ats_score: atsScore,
        company_research: companyResearch,
        recommendations: recommendations,
      });
      setDocuments(result);
    } catch (err) {
      setDocError('Failed to generate documents. Please try again.');
    } finally {
      setGeneratingDocs(false);
    }
  };

  const handleDownload = async (filename) => {
    try {
      const blob = await documentService.downloadDocument(filename);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download failed:', err);
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Analysis Results
      </Typography>

      {/* Overall Scores */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Resume Score
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Typography variant="h3" color={getScoreColor(resumeAnalysis.overall_score * 10)}>
                  {resumeAnalysis.overall_score.toFixed(1)}/10
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={resumeAnalysis.overall_score * 10}
                color={getScoreColor(resumeAnalysis.overall_score * 10)}
                sx={{ height: 10, borderRadius: 5 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                ATS Compatibility
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Typography variant="h3" color={getScoreColor(atsScore.ats_score)}>
                  {atsScore.ats_score}%
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={atsScore.ats_score}
                color={getScoreColor(atsScore.ats_score)}
                sx={{ height: 10, borderRadius: 5 }}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Resume Analysis */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Resume Analysis</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" color="success.main" gutterBottom>
                <CheckCircleIcon sx={{ fontSize: 16, mr: 1, verticalAlign: 'middle' }} />
                Strengths
              </Typography>
              {resumeAnalysis.strengths.map((item, idx) => (
                <Chip key={idx} label={item} size="small" sx={{ m: 0.5 }} />
              ))}
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" color="warning.main" gutterBottom>
                <WarningIcon sx={{ fontSize: 16, mr: 1, verticalAlign: 'middle' }} />
                Areas to Improve
              </Typography>
              {resumeAnalysis.improvement_areas.map((item, idx) => (
                <Typography key={idx} variant="body2" sx={{ mb: 1 }}>
                  • {item}
                </Typography>
              ))}
            </Grid>

            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                Keywords to Add
              </Typography>
              {resumeAnalysis.keywords_to_add.map((item, idx) => (
                <Chip key={idx} label={item} size="small" color="primary" sx={{ m: 0.5 }} />
              ))}
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* ATS Analysis */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">ATS Compatibility Details</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                Keyword Match: {atsScore.keyword_match}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={atsScore.keyword_match}
                sx={{ mb: 2 }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                Missing Keywords
              </Typography>
              {atsScore.missing_keywords.map((item, idx) => (
                <Chip key={idx} label={item} size="small" variant="outlined" sx={{ m: 0.5 }} />
              ))}
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                Recommendations
              </Typography>
              {atsScore.recommendations.map((item, idx) => (
                <Typography key={idx} variant="body2" sx={{ mb: 1 }}>
                  • {item}
                </Typography>
              ))}
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Company Research */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Company Insights: {jobData.companyName}</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="body2" paragraph>
            {companyResearch.company_overview}
          </Typography>
          <Typography variant="subtitle2" gutterBottom>
            Mission & Values
          </Typography>
          {companyResearch.mission_and_values.map((item, idx) => (
            <Typography key={idx} variant="body2" sx={{ mb: 0.5 }}>
              • {item}
            </Typography>
          ))}
          <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
            Company Culture
          </Typography>
          <Typography variant="body2">{companyResearch.culture}</Typography>
        </AccordionDetails>
      </Accordion>

      {/* Recommendations */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Personalized Recommendations</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                Resume Alignment Actions
              </Typography>
              {recommendations.resume_alignment.map((item, idx) => (
                <Typography key={idx} variant="body2" sx={{ mb: 1 }}>
                  {idx + 1}. {item}
                </Typography>
              ))}
            </Grid>

            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                Cover Letter Talking Points
              </Typography>
              {recommendations.cover_letter_talking_points.map((item, idx) => (
                <Typography key={idx} variant="body2" sx={{ mb: 1 }}>
                  • {item}
                </Typography>
              ))}
            </Grid>

            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                Interview Preparation
              </Typography>
              {recommendations.interview_questions.map((item, idx) => (
                <Typography key={idx} variant="body2" sx={{ mb: 1 }}>
                  Q{idx + 1}: {item}
                </Typography>
              ))}
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Document Generation */}
      <Card sx={{ mt: 3, p: 2, bgcolor: 'primary.50' }}>
        <Typography variant="h6" gutterBottom>
          Generate Optimized Documents
        </Typography>
        <Typography variant="body2" sx={{ mb: 2 }}>
          Create professionally optimized resume and cover letter based on the analysis
        </Typography>

        {docError && <Alert severity="error" sx={{ mb: 2 }}>{docError}</Alert>}

        {documents ? (
          <Box>
            <Alert severity="success" sx={{ mb: 2 }}>
              Documents generated successfully!
            </Alert>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<DownloadIcon />}
                  onClick={() => handleDownload(documents.resume_file_path.split('/').pop())}
                >
                  Download Resume
                </Button>
              </Grid>
              <Grid item xs={12} md={6}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<DownloadIcon />}
                  onClick={() => handleDownload(documents.cover_letter_file_path.split('/').pop())}
                >
                  Download Cover Letter
                </Button>
              </Grid>
            </Grid>
          </Box>
        ) : (
          <Button
            fullWidth
            variant="contained"
            onClick={handleGenerateDocuments}
            disabled={generatingDocs}
            startIcon={generatingDocs ? <CircularProgress size={20} /> : <DownloadIcon />}
          >
            {generatingDocs ? 'Generating Documents...' : 'Generate Documents'}
          </Button>
        )}
      </Card>

      {/* Action Buttons */}
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={onBack}>Back</Button>
        <Button
          variant="outlined"
          startIcon={<RestartAltIcon />}
          onClick={onReset}
        >
          Start New Analysis
        </Button>
      </Box>
    </Box>
  );
}

export default Results;
