import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Col, Row } from 'react-bootstrap';

const VehicleDetail = () => {
  const { loc, trackId, className } = useParams();  // Get trackId and className from the URL
  const [vehicleDetail, setVehicleDetail] = useState(null);

  useEffect(() => {
    // Fetch data from the backend using the trackId and className from the URL
    console.log(`Fetching details for Track ID: ${trackId}, Class Name: ${className}`);
    fetch(`http://127.0.0.1:5000/vehicle_track?loc=${loc}&track_id=${trackId}&class_name=${className}`)
      .then(response => response.json())
      .then(data => setVehicleDetail(data))
      .catch(error => console.error('Error fetching vehicle detail:', error));
  }, [loc, trackId, className]);

  if (!vehicleDetail) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2 className="text-center mb-4">Vehicle Detail - Track ID: {trackId}</h2>
      <Row xs={1} md={2} lg={3} className="g-4">
        {vehicleDetail.map((vehicle, index) => (
          <Col key={index}>
            <Card className="h-100">
              <Card.Body>
                <Card.Title className="text-center">{vehicle['Class Name']}</Card.Title>
                <Card.Text>
                  <div className="details-row">
                    <strong>Direction:</strong>
                    <span>{vehicle['Direction']}</span>
                  </div>
                  <div className="details-row">
                    <strong>Speed:</strong>
                    <span>{vehicle['Speed']} km/h</span>
                  </div>
                  <div className="details-row">
                    <strong>Timestamp:</strong>
                    <span>{vehicle['Timestamp']}</span>
                  </div>
                  <div className="details-row">
                    <strong>Coordinates:</strong>
                    <span>({vehicle['x1']}, {vehicle['y1']}) ({vehicle['x2']}, {vehicle['y2']})</span>
                  </div>
                </Card.Text>
                <img
                  src={vehicle['Image URL']}
                  alt="Vehicle"
                  className="img-fluid rounded"
                  style={{ height: '200px', objectFit: 'cover' }} // menggunakan object-fit untuk menjaga proporsi gambar
                />
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default VehicleDetail;
