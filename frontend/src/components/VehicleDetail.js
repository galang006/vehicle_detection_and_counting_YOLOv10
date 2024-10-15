import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const VehicleDetail = () => {
  const { trackId, className } = useParams();  // Get trackId and className from the URL
  const [vehicleDetail, setVehicleDetail] = useState(null);

  useEffect(() => {
    // Fetch data from the backend using the trackId and className from the URL
    fetch(`http://127.0.0.1:5000/vehicle_track?loc=${"simpang_demangan_view_utara"}&track_id=${trackId}&class_name=${className}`)
      .then(response => response.json())
      .then(data => setVehicleDetail(data))
      .catch(error => console.error('Error fetching vehicle detail:', error));
  }, [trackId, className]);

  if (!vehicleDetail) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Vehicle Detail - Track ID: {trackId}</h2>
      {vehicleDetail.map((vehicle, index) => (
        <div key={index} style={{ border: '1px solid black', margin: '10px', padding: '10px' }}>
          <h3>{vehicle['Class Name']}</h3>
          <p>Direction: {vehicle['Direction']}</p>
          <p>Speed: {vehicle['Speed']} km/h</p>
          <p>Timestamp: {vehicle['Timestamp']}</p>
          <p>Coordinates: ({vehicle['x1']}, {vehicle['y1']}) ({vehicle['x2']}, {vehicle['y2']})</p>
          <img src={vehicle['Image URL']} alt="Vehicle" style={{ width: 'auto', height: '300px' }} />
        </div>
      ))}
    </div>
  );
};

export default VehicleDetail;