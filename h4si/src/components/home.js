import React from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import LegalAid from './legalAid'; // Import the LegalAid component
import Testimonials from './testimonials'; // Import the Testimonials component

const HomePage = () => {
  const [showAnalyzer, setShowAnalyzer] = React.useState(false); // State to toggle the LegalAid component

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      
      {/* Hero Section */}
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Empower Your Tenant Rights
        </Typography>
        
        <Typography variant="h5" sx={{ mx: 6, mt: 4 }} component="p" gutterBottom>
          Get data-driven insights and legal support to challenge landlords who fail to meet their obligations.
        </Typography>

        {/* Button to trigger the LegalAid component */}
        {!showAnalyzer && (
          <Button 
            variant="contained" 
            color="primary" 
            size="large" 
            onClick={() => setShowAnalyzer(true)} // Show LegalAid when clicked
            sx={{ mx: 6, mt: 4 }}
          >
            Analyze My Petition
          </Button>
        )}
        
      </Box>

      {/* Render LegalAid Component */}
      {showAnalyzer && (
        <Box mt={4}>
          <LegalAid />
          {/* Button to hide the analyzer */}
          <Button 
            variant="outlined" 
            color="secondary" 
            size="large" 
            onClick={() => setShowAnalyzer(false)} // Hide LegalAid when clicked
            sx={{ mt: 2 }}
          >
            Hide Analyzer
          </Button>
        </Box>
      )}

      {/* Testimonials Section */}
      {!showAnalyzer && (
        <Testimonials />
      )}

     
            {/* Educational Resources Section */}
            <Box id="know-your-rights" sx={{ mt: 8 }}>
                <Typography variant="h3">Know Your Rights</Typography>

                {/* Habitability Standards */}
                <Box sx={{ mt: 4 }}>
                    <Typography variant="h5">Habitability Standards</Typography>
                    <Typography variant="body1">
                        Under California Civil Code Section 1941.1, landlords are required to maintain rental units in a habitable condition.
                    </Typography>
                    <ul>
                        <li>Effective waterproofing and weather protection of roof and exterior walls.</li>
                        <li>Plumbing facilities maintained in good working order.</li>
                        <li>A water supply capable of providing hot and cold running water.</li>
                        {/* Add more points as needed */}
                    </ul>
                    <Button variant="outlined" color="primary" href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1941.1&lawCode=CIV">
                        Learn More
                    </Button>
                </Box>

                {/* Rent Control Laws */}
                <Box sx={{ mt: 6 }}>
                    <Typography variant="h5">Rent Control Laws</Typography>
                    <Typography variant="body1">
                        Rent control laws limit how much your landlord can increase your rent each year. Learn more about rent control in your area.
                    </Typography>
                    <Button variant="outlined" color="primary" href="https://hcidla.lacity.org/rent-control">
                        Learn More About Rent Control
                    </Button>
                </Box>

                {/* Eviction Protections */}
                <Box sx={{ mt: 6 }}>
                    <Typography variant="h5">Eviction Protections</Typography>
                    <Typography variant="body1">
                        If your landlord is attempting to evict you without just cause, you may be protected under local eviction laws.
                    </Typography>
                    <Button variant="outlined" color="primary" href="https://evictiondefense.org/">
                        Learn More About Eviction Protections
                    </Button>
                </Box>

            </Box>

            {/* Footer */}
            <footer style={{ marginTop: '50px', textAlign: 'center', paddingTop: '20px', paddingBottom: '20px', backgroundColor: '#f5f5f5' }}>
                © {new Date().getFullYear()} Tenant Empowerment App | All Rights Reserved
            </footer> 

    </Container>
  );
};

export default HomePage;

// import React from 'react';
// import { Container, Typography, Button, Box, Grid } from '@mui/material';

// const HomePage = () => {
//     return (
//         <Container maxWidth="lg" sx={{ py: 4 }}>
//             {/* Hero Section */}
//             <Box sx={{ textAlign: 'center', mb: 4 }}>
//                 <Typography variant="h2" component="h1" gutterBottom>
//                     Empower Your Tenant Rights
//                 </Typography>
//                 <Typography variant="h5" component="p" gutterBottom>
//                     Get data-driven insights and legal support to challenge landlords who fail to meet their obligations.
//                 </Typography>
//                 <Button variant="contained" color="primary" size="large" href="/analyze-petition" sx={{ mx: 2 }}>
//                     Analyze My Petition
//                 </Button>
//                 <Button variant="outlined" color="secondary" size="large" href="#know-your-rights" sx={{ mx: 2 }}>
//                     Know Your Rights
//                 </Button>
//             </Box>


//             {/* Success Stories Section */}
//             <Box sx={{ mt: 8, textAlign: 'center' }}>
//                 <Typography variant="h3">Success Stories from Tenants Like You</Typography>
//                 <Box sx={{ mt: 4 }}>
//                     <blockquote>"Thanks to this app, I was able to successfully reduce my rent after my landlord failed to fix unsafe conditions."</blockquote>
//                     <cite>- Anonymous Tenant</cite>
//                 </Box>
//                 <Box sx={{ mt: 4 }}>
//                     <blockquote>"The legal argument suggestions helped me win my case against an unreasonable rent increase."</blockquote>
//                     <cite>- Anonymous Tenant</cite>
//                 </Box>
//                 <Button variant="outlined" color="secondary" href="/success-stories" sx={{ mt: 4 }}>
//                     Read More Success Stories
//                 </Button>
//             </Box>

//             {/* Educational Resources Section */}
//             <Box id="know-your-rights" sx={{ mt: 8 }}>
//                 <Typography variant="h3">Know Your Rights</Typography>

//                 {/* Habitability Standards */}
//                 <Box sx={{ mt: 4 }}>
//                     <Typography variant="h5">Habitability Standards</Typography>
//                     <Typography variant="body1">
//                         Under California Civil Code Section 1941.1, landlords are required to maintain rental units in a habitable condition.
//                     </Typography>
//                     <ul>
//                         <li>Effective waterproofing and weather protection of roof and exterior walls.</li>
//                         <li>Plumbing facilities maintained in good working order.</li>
//                         <li>A water supply capable of providing hot and cold running water.</li>
//                         {/* Add more points as needed */}
//                     </ul>
//                     <Button variant="outlined" color="primary" href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1941.1&lawCode=CIV">
//                         Learn More
//                     </Button>
//                 </Box>

//                 {/* Rent Control Laws */}
//                 <Box sx={{ mt: 6 }}>
//                     <Typography variant="h5">Rent Control Laws</Typography>
//                     <Typography variant="body1">
//                         Rent control laws limit how much your landlord can increase your rent each year. Learn more about rent control in your area.
//                     </Typography>
//                     <Button variant="outlined" color="primary" href="https://hcidla.lacity.org/rent-control">
//                         Learn More About Rent Control
//                     </Button>
//                 </Box>

//                 {/* Eviction Protections */}
//                 <Box sx={{ mt: 6 }}>
//                     <Typography variant="h5">Eviction Protections</Typography>
//                     <Typography variant="body1">
//                         If your landlord is attempting to evict you without just cause, you may be protected under local eviction laws.
//                     </Typography>
//                     <Button variant="outlined" color="primary" href="https://evictiondefense.org/">
//                         Learn More About Eviction Protections
//                     </Button>
//                 </Box>

//             </Box>

//             {/* Footer */}
//             <footer style={{ marginTop: '50px', textAlign: 'center', paddingTop: '20px', paddingBottom: '20px', backgroundColor: '#f5f5f5' }}>
//                 © {new Date().getFullYear()} Tenant Empowerment App | All Rights Reserved
//             </footer>

//         </Container >
//     );
// };

// export default HomePage;