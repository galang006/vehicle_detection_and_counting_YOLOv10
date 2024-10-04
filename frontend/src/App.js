import './App.css';
import VehicleLineChart from './components/VehicleLineChart';
import VehicleDataTable from './components/VehicleTableChart';
import VideoPlay from './components/VideoPlay';

function App() {
  return (
    <div className="App">
      <h1>Vehicle Dashboard</h1>

      <div style={{ marginBottom: '50px' }}>
        <VideoPlay />
      </div>
      <div style={{ marginBottom: '50px' }}>
        <VehicleLineChart />
      </div>
      <div >
        <VehicleDataTable />
      </div>
    </div>
  );
}

export default App;
