import React from 'react';
import { Box, Typography } from '@mui/material';
import TestimonialCard from './testimonialCard';

const testimonialsData = [
  {
    message: "Thanks to this app, I was able to successfully reduce my rent after my landlord failed to fix unsafe conditions.",
    name: "Anonymous Tenant",
  },
  {
    message: "The legal argument suggestions helped me win my case against an unreasonable rent increase.",
    name: "Anonymous Tenant",
  },
];

const Testimonials = () => {
  return (
    <Box sx={{ mt: 8 }}>
      <Typography variant="h3" gutterBottom textAlign="center">
        Success Stories from Tenants Like You
      </Typography>
      
      {testimonialsData.map((testimonial, index) => (
        <TestimonialCard key={index} testimonial={testimonial} />
      ))}
    </Box>
  );
};

export default Testimonials