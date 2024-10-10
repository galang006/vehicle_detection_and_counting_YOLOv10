import './App.css';
import VehicleLineChart from './components/VehicleLineChart';
import VehicleDataTable from './components/VehicleTableChart';
import VideoPlay from './components/VideoPlay';
import VehicleSpeedBarChart from './components/VehicleSpeedBarChart';
import VehicleDirectionBarChart from './components/VehicleDirectionBarChart';
import VehicleDetail from './components/VehicleDetail';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';
import logo from './assets/Logo_Stempel_HD.png';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navbar */}
        <Navbar bg="info" variant="dark" expand="lg">
          <Navbar.Brand style={{ marginLeft: '20px' }} as={Link} to="#" className="text-dark fw-bold">
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
              <Nav.Link as={Link} to="/" className="text-dark">
                Home
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>

        <Routes>
          {/* Route for the dashboard */}
          <Route
            path="/"
            element={
              <>
                <div style={{ marginBottom: '25px' }}>
                  <VideoPlay />
                </div>
                <div style={{ marginBottom: '50px' }}>
                  <VehicleLineChart />
                </div>
                <div className="chart-row">
                  <div style={{ flex: 1, padding: '0 20px' }}>
                    <VehicleSpeedBarChart />
                  </div>
                  <div style={{ flex: 1, padding: '0 20px' }}>
                    <VehicleDirectionBarChart />
                  </div>
                </div>
                <div>
                  <VehicleDataTable />
                </div>
              </>
            }
          />
          {/* Route for vehicle detail page */}
          <Route path="/vehicle/:trackId/:className" element={<VehicleDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
