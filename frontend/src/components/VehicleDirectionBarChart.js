// src/components/VehicleDirectionBarChart.js
import React, { useState, useEffect } from 'react';
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

const VehicleDirectionBarChart = () => {
    const [directionData, setDirectionData] = useState([]);

    useEffect(() => {
        // Ambil data dari API
        axios.get('http://127.0.0.1:5000/vehicle_track?loc=simpang_demangan_view_utara')
            .then(response => {
                console.log(response.data); // Debug data
                const formattedData = response.data.reduce((acc, item) => {
                    const direction = item.Direction;

                    // Buat objek jika belum ada untuk direction ini
                    if (!acc[direction]) {
                        acc[direction] = {
                            name: direction,
                            bus: 0,
                            car: 0,
                            motorcycle: 0,
                            truck: 0,
                        };
                    }

                    // Tambah jumlah kendaraan per kelas
                    if (item['Class Name'] === 'bus') {
                        acc[direction].bus += 1;
                    } else if (item['Class Name'] === 'car') {
                        acc[direction].car += 1;
                    } else if (item['Class Name'] === 'motorcycle') {
                        acc[direction].motorcycle += 1;
                    } else if (item['Class Name'] === 'truck') {
                        acc[direction].truck += 1;
                    }

                    return acc;
                }, {});

                // Ubah objek menjadi array
                const dataArray = Object.values(formattedData);
                setDirectionData(dataArray);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, []);

    return (
        <div style={{ width: '100%', height: 400 }}>
            <h2>Vehicle Count by Direction</h2>
            <ResponsiveContainer width="90%" height="100%">
                <BarChart data={directionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="bus" fill="#8884d8" name="Bus" />
                    <Bar dataKey="car" fill="#82ca9d" name="Car" />
                    <Bar dataKey="motorcycle" fill="#ffc658" name="Motorcycle" />
                    <Bar dataKey="truck" fill="#ff7300" name="Truck" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default VehicleDirectionBarChart;
