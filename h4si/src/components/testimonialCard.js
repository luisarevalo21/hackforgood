import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

const TestimonialCard = ({ testimonial }) => {
  return (
    <Card sx={{ maxWidth: 345, marginBottom: '20px' }}>
      <CardContent>
        <Typography variant="body1" color="textSecondary">
          "{testimonial.message}"
        </Typography>
        <Typography variant="subtitle2" color="textSecondary" sx={{ marginTop: '10px' }}>
          - {testimonial.name}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default TestimonialCard;