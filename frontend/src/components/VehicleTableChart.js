import React, { useEffect, useState } from 'react';
import Table from 'react-bootstrap/Table';
import { useNavigate } from 'react-router-dom';

const VehicleDataTable = () => {
  const [vehicleData, setVehicleData] = useState([]);
  // const [selectedData, setSelectedData] = useState(null);
  const navigate = useNavigate(); 

  useEffect(() => {
    fetch('http://127.0.0.1:5000/vehicle_track') 
      .then(response => response.json())
      .then(data => setVehicleData(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  // Function to handle row click
  const handleRowClick = (trackId, className) => {
    navigate(`/vehicle/${trackId}/${className}`);
    // console.log('Clicked Track ID:', trackId);
    // console.log('Clicked Class Name:', className);

    // fetch(`http://127.0.0.1:5000/vehicle_track?track_id=${trackId}&class_name=${className}`)
    //   .then(response => response.json())
    //   .then(data => {
    //     console.log('Fetched data:', data);  // Log the data returned from the API
    //     setSelectedData(data);  // You can set this to state or process it further
    //   })
    //   .catch(error => console.error('Error fetching specific data:', error));
  };

  return (
    <div style={{ width: '100%', height: 400 }}>
        <h2>Vehicle Track Table</h2>
        <Table striped bordered hover variant="dark" style={{ border: '1px solid white' }}>
        <thead>
            <tr>
            <th>Class Name</th>
            <th>Track ID</th>
            <th>Direction</th>
            <th>x1</th>
            <th>y1</th>
            <th>x2</th>
            <th>y2</th>
            <th>Speed</th>
            <th>Timestamp</th>
            </tr>
        </thead>
        <tbody>
            {vehicleData.map((vehicle, index) => (
            <tr key={index} onClick={() =>  handleRowClick(vehicle['Track ID'], vehicle['Class Name'])}>
                <td>{vehicle['Class Name']}</td>
                <td>{vehicle['Track ID']}</td>
                <td>{vehicle['Direction']}</td>
                <td>{vehicle['x1']}</td>
                <td>{vehicle['y1']}</td>
                <td>{vehicle['x2']}</td>
                <td>{vehicle['y2']}</td>
                <td>{vehicle['Speed']}</td>
                <td>{vehicle['Timestamp']}</td>
            </tr>
            ))}
        </tbody>
        </Table>
    </div>
  );
};

export default VehicleDataTable;