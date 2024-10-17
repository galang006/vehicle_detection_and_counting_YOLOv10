import './App.css';
import SimpangDemanganDashboard from './components/SimpangDemanganDashboard';
import SimpangAmongrogoDashboard from './components/SimpangAmongrogoDashboard';
import VehicleDetail from './components/VehicleDetail';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { Navbar, Nav, Card, Container, Row, Col, Dropdown, Button } from 'react-bootstrap';
import logo from './assets/Logo_Stempel_HD.png';
import { useState } from 'react';

function HomePage() {
  const [selectedLocation, setSelectedLocation] = useState('');
  const navigate = useNavigate();

  const handleSelect = (loc) => {
    setSelectedLocation(loc);
  };

  const handleGoClick = () => {
    if (selectedLocation) {
      navigate(selectedLocation);
    }
  };

  return (
    <div className="animated-background">
      <Container className="text-center mt-5" style={{ paddingTop: '50px' }}>
        <Row className="justify-content-center">
          <Col md={10}>
            <Card className="custom-card" style={{ paddingTop: '5px', paddingBottom: '20px' }}>
              <Card.Body>
                <h1>Selamat Datang di Dashboard Vehicle Detection</h1>
                <p>Pilih lokasi di bawah ini untuk melihat dashboard kendaraan pada lokasi yang Anda pilih.</p>

                <Row className="justify-content-center mt-4">
                  <Col md={6}>
                    <Dropdown onSelect={handleSelect}>
                      <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                        {selectedLocation
                          ? selectedLocation === '/dashboard/demangan?loc=simpang_demangan_view_utara'
                            ? 'Simpang Demangan'
                            : 'Simpang Amongrogo'
                          : 'Select Location'}
                      </Dropdown.Toggle>

                      <Dropdown.Menu>
                        <Dropdown.Item eventKey="/dashboard/demangan?loc=simpang_demangan_view_utara">
                          Simpang Demangan
                        </Dropdown.Item>
                        <Dropdown.Item eventKey="/dashboard/amongrogo?loc=simpang_amongrogo_view_timur">
                          Simpang Amongrogo
                        </Dropdown.Item>
                      </Dropdown.Menu>
                    </Dropdown>
                  </Col>
                </Row>

                <Row className="justify-content-center mt-3">
                  <Col md={6}>
                    <Button
                      variant="success"
                      onClick={handleGoClick}
                      disabled={!selectedLocation}
                      className="w-100">
                      Go to Dashboard
                    </Button>
                  </Col>
                </Row>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div >
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navbar */}
        <Navbar className="navbar" expand="lg">
          <Navbar.Brand style={{ marginLeft: '20px' }} as={Link} to="/" className="text-dark fw-bold">
            <img
              src={logo}
              alt="Logo"
              height="30px"
              className="d-inline-block align-top"
              style={{ marginRight: '10px' }}
            />
            Vehicle Dashboard
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              {/* Menu 1: Simpang Demangan */}
              <Nav.Link
                as={Link}
                to="/dashboard/demangan?loc=simpang_demangan_view_utara"
                className="text-dark"
              >
                Simpang Demangan
              </Nav.Link>
              {/* Menu 2: Simpang Amongrogo */}
              <Nav.Link
                as={Link}
                to="/dashboard/amongrogo?loc=simpang_amongrogo_view_timur"
                className="text-dark"
              >
                Simpang Amongrogo
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>

        {/* Routes */}
        <div className="container">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/dashboard/demangan" element={<SimpangDemanganDashboard />} />
            <Route path="/dashboard/amongrogo" element={<SimpangAmongrogoDashboard />} />
            <Route path="/vehicle/:loc/:trackId/:className" element={<><Card className="mb-3 mt-3 custom-card">
              <Card.Body>
                <VehicleDetail />
              </Card.Body>
            </Card></>} />
          </Routes>
        </div>

        {/* Footer */}
        <footer className="footer mt-auto py-2">
          <div className="container text-center">
            <span className="text-muted">© 2024 Vehicle Dashboard. All Rights Reserved.</span>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
















// import './App.css';
// import VehicleLineChart from './components/VehicleLineChart';
// import VehicleDataTable from './components/VehicleTableChart';
// import VideoPlay from './components/VideoPlay';
// import VehicleSpeedBarChart from './components/VehicleSpeedBarChart';
// import VehicleDirectionBarChart from './components/VehicleDirectionBarChart';
// import VehicleDetail from './components/VehicleDetail';
// import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
// import { Navbar, Nav, Card } from 'react-bootstrap';
// import logo from './assets/Logo_Stempel_HD.png';

// function App() {
//   return (
//     <Router>
//       <div className="App">
//         {/* Navbar */}
//         <Navbar className="navbar" expand="lg">
//           <Navbar.Brand as={Link} to="/" className="navbar-brand">
//             <img
//               src={logo}
//               alt="Logo"
//               height="30px"
//               className="navbar-img"
//             />
//             Vehicle Dashboard
//           </Navbar.Brand>
//           <Navbar.Toggle aria-controls="basic-navbar-nav" />
//           <Navbar.Collapse id="basic-navbar-nav">
//             <Nav className="me-auto">
//               <Nav.Link as={Link} to="/" className="nav-link, nav-link:hover">
//                 Home
//               </Nav.Link>
//               {/* Tambahkan link lainnya di sini jika diperlukan */}
//             </Nav>
//           </Navbar.Collapse>
//         </Navbar>

//         {/* Content di bawah navbar */}
//         <div className="container mt-3">
//           <Routes>
//             {/* Route for the dashboard */}
//             <Route
//               path="/"
//               element={
//                 <>
//                   {/* Video player card */}
//                   <Card className="mb-3 custom-card">
//                     <Card.Body>
//                       <VideoPlay />
//                     </Card.Body>
//                   </Card>

//                   {/* Line chart card */}
//                   <Card className="mb-3 custom-card">
//                     <Card.Body>
//                       <VehicleLineChart />
//                     </Card.Body>
//                   </Card>

//                   {/* Bar charts row */}
//                   <div className="chart-row" style={{ display: 'flex', justifyContent: 'space-between', gap: '10px', marginBottom: '5px', marginTop: '10px' }}>
//                     <Card className="mb-3 custom-card" style={{ flex: 1, marginRight: '5px' }}>
//                       <Card.Body>
//                         <VehicleSpeedBarChart />
//                       </Card.Body>
//                     </Card>

//                     <Card className="mb-3 custom-card" style={{ flex: 1, marginLeft: '5px' }}>
//                       <Card.Body>
//                         <VehicleDirectionBarChart />
//                       </Card.Body>
//                     </Card>
//                   </div>

//                   {/* Table data card */}
//                   <Card className="mb-5 custom-card">
//                     <Card.Body>
//                       <VehicleDataTable />
//                     </Card.Body>
//                   </Card>
//                 </>
//               }
//             />
//             {/* Route for vehicle detail page */}
//             <Route path="/vehicle/:trackId/:className" element={<><Card className="mb-3 custom-card">
//               <Card.Body>
//                 <VehicleDetail />
//               </Card.Body>
//             </Card></>} />
//           </Routes>
//         </div>
//         {/* Footer */}
//         <footer className="footer mt-auto py-3">
//           <div className="container text-center">
//             <span className="text-muted">© 2024 Vehicle Dashboard. All Rights Reserved.</span>
//           </div>
//         </footer>
//       </div>
//     </Router>
//   );
// }

// export default App;
