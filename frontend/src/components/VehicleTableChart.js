import React, { useEffect, useState } from 'react';
import Table from 'react-bootstrap/Table';
import { useNavigate } from 'react-router-dom';

const VehicleDataTable = () => {
  const [vehicleData, setVehicleData] = useState([]);
  // const [selectedData, setSelectedData] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 100;
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
  };

  // Get current data to display based on pagination
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentData = vehicleData.slice(indexOfFirstItem, indexOfLastItem);

  // Handle next and previous page buttons
  const handleNextPage = () => {
    if (indexOfLastItem < vehicleData.length) {
      setCurrentPage(prevPage => prevPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(prevPage => prevPage - 1);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Vehicle Track Table</h2>
      <table className="table table-bordered table-hover">
        <thead className="table-primary">
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
          {currentData.map((vehicle, index) => (
            <tr key={index} onClick={() => handleRowClick(vehicle['Track ID'], vehicle['Class Name'])}>
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
      </table>

      {/* Pagination controls */}
      <div className="pagination-controls">
        <button className="btn btn-primary" onClick={handlePrevPage} disabled={currentPage === 1}>
          Prev
        </button>
        <span className="mx-3">Page {currentPage}</span>
        <button className="btn btn-primary" onClick={handleNextPage} disabled={indexOfLastItem >= vehicleData.length}>
          Next
        </button>
      </div>
    </div>
  );
};

export default VehicleDataTable;
