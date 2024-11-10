// src/components/LegalAidInterface.js

import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Alert,
  CircularProgress,
  Card,
  CardContent,
} from '@mui/material';
import {
  Description,
  CheckCircle,
  Warning,
  ArrowForward,
} from '@mui/icons-material';

const LegalAid = () => {
  const [caseText, setCaseText] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);


  const analyzePetition = async () => {
    setLoading(true);
  
    try {
      const response = await fetch('http://localhost:5000/analyze_petition', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ petition_text: caseText }),
      });
  
      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error("Error analyzing petition:", error);
    } finally {
      setLoading(false);
    }
  };

//   const analyzePetition = async () => {
//     setLoading(true);
  
//     try {
//       const response = await fetch('/analyze_petition', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ petition_text: caseText }),
//       });
  
//       const data = await response.json();
//       setAnalysis(data);
//     } catch (error) {
//       console.error("Error analyzing petition:", error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const analyzePetition = async () => {
//     setLoading(true);
//     // Simulated API call
//     setTimeout(() => {
//       setAnalysis({
//         success_probability: 0.75,
//         key_arguments: [
//           "Persistent maintenance issues reported multiple times",
//           "Violations of local housing codes",
//           "Documented communication attempts with landlord"
//         ],
//         suggested_precedents: [
//           "Case #2021-15: Similar maintenance issues, favorable outcome",
//           "Case #2022-08: Successful petition based on code violations"
//         ],
//         improvement_areas: [
//           "Include more photographic evidence",
//           "Add specific dates of maintenance requests",
//           "Reference relevant local ordinances"
//         ]
//       });
//       setLoading(false);
//     }, 1500);
//   };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Box display="flex" alignItems="center" gap={1} mb={2}>
          <Description color="primary" />
          <Typography variant="h5" component="h1">
            Legal Petition Analyzer
          </Typography>
        </Box>

        <TextField
          fullWidth
          multiline
          rows={6}
          variant="outlined"
          placeholder="Enter your petition details here..."
          value={caseText}
          onChange={(e) => setCaseText(e.target.value)}
          sx={{ mb: 2 }}
        />

        <Button
          variant="contained"
          fullWidth
          disabled={loading || !caseText}
          onClick={analyzePetition}
          startIcon={loading ? <CircularProgress size={20} color="inherit" /> : null}
        >
          {loading ? 'Analyzing...' : 'Analyze Petition'}
        </Button>
      </Paper>

      {analysis && (
        <Box sx={{ mt: 4, gap: 3, display: 'flex', flexDirection: 'column' }}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <CheckCircle color="success" />
                <Typography variant="h6">
                  Success Probability: {(analysis.success_probability * 100).toFixed(1)}%
                </Typography>
              </Box>

              <Typography variant="h6" gutterBottom>
                Key Arguments Identified:
              </Typography>
              <List>
                {analysis.key_arguments.map((arg, i) => (
                  <ListItem key={i}>
                    <ListItemIcon>
                      <ArrowForward color="primary" />
                    </ListItemIcon>
                    <ListItemText primary={arg} />
                  </ListItem>
                ))}
              </List>

              <Typography variant="h6" gutterBottom>
                Similar Successful Cases:
              </Typography>
              <List>
                {analysis.suggested_precedents.map((precedent, i) => (
                  <ListItem key={i}>
                    <ListItemIcon>
                      <CheckCircle color="success" />
                    </ListItemIcon>
                    <ListItemText primary={precedent} />
                  </ListItem>
                ))}
              </List>

              <Alert 
                severity="warning"
                icon={<Warning />}
                sx={{ mt: 2 }}
              >
                <Typography variant="h6" gutterBottom>
                  Suggested Improvements:
                </Typography>
                <List>
                  {analysis.improvement_areas.map((area, i) => (
                    <ListItem key={i}>
                      <ListItemText primary={area} />
                    </ListItem>
                  ))}
                </List>
              </Alert>
            </CardContent>
          </Card>
        </Box>
      )}
    </Container>
  );
};

export default LegalAid;