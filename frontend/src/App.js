import './App.css';
import VehicleLineChart from './components/VehicleLineChart';
import VehicleDataTable from './components/VehicleTableChart';
import VideoPlay from './components/VideoPlay';
import VehicleDetail from './components/VehicleDetail';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>Vehicle Dashboard</h1>

        <Routes>
          {/* Route for the dashboard */}
          <Route
            path="/"
            element={
              <>
                <div style={{ marginBottom: '50px' }}>
                  <VideoPlay />
                </div>
                <div style={{ marginBottom: '50px' }}>
                  <VehicleLineChart />
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
