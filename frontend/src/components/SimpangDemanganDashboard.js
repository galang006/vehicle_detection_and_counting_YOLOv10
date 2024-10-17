import React from 'react';
import { useLocation } from 'react-router-dom';
import VehicleLineChart from './VehicleLineChart';
import VehicleDataTable from './VehicleTableChart';
import VideoPlay from './VideoPlay';
import VehicleSpeedBarChart from './VehicleSpeedBarChart';
import VehicleDirectionBarChart from './VehicleDirectionBarChart';
import { Card } from 'react-bootstrap';

const SimpangDemanganDashboard = () => {
    const search = useLocation().search;
    const loc = new URLSearchParams(search).get('loc');

    return (
        <div className="dashboard">
            {/* Video player card */}
            <Card className="mb-3 mt-3 custom-card">
                <Card.Body>
                    <VideoPlay />
                </Card.Body>
            </Card>

            {/* Line chart card */}
            <Card className="mb-3 custom-card">
                <Card.Body>
                    <VehicleLineChart loc={loc} />
                </Card.Body>
            </Card>

            {/* Bar charts row */}
            <div className="chart-row" style={{ display: 'flex', justifyContent: 'space-between', gap: '10px', marginBottom: '5px', marginTop: '10px' }}>
                <Card className="mb-3 custom-card" style={{ flex: 1, marginRight: '5px' }}>
                    <Card.Body>
                        <VehicleSpeedBarChart loc={loc} />
                    </Card.Body>
                </Card>

                <Card className="mb-3 custom-card" style={{ flex: 1, marginLeft: '5px' }}>
                    <Card.Body>
                        <VehicleDirectionBarChart loc={loc} />
                    </Card.Body>
                </Card>
            </div>

            {/* Table data card */}
            <Card className="mb-5 custom-card">
                <Card.Body>
                    <VehicleDataTable loc={loc} />
                </Card.Body>
            </Card>
        </div>
    );
};

export default SimpangDemanganDashboard;
