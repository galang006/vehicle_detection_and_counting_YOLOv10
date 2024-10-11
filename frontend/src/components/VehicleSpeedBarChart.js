<<<<<<< HEAD
// src/components/VehicleSpeedBarChart.js
import React, { useState, useEffect } from 'react';
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';

const VehicleSpeedBarChart = () => {
    const [speedData, setSpeedData] = useState([]);

    useEffect(() => {
        // Ambil data dari API atau JSON statis
        axios.get('http://127.0.0.1:5000/vehicle_track') // Ganti dengan endpoint API jika diperlukan
            .then(response => {
                const data = response.data;

                // Mengelompokkan data berdasarkan Class Name dan menghitung rata-rata kecepatan
                const speedSums = {};
                const classCounts = {};

                data.forEach(item => {
                    const className = item['Class Name'];
                    const speed = item['Speed'];

                    if (!speedSums[className]) {
                        speedSums[className] = 0;
                        classCounts[className] = 0;
                    }

                    speedSums[className] += speed;
                    classCounts[className] += 1;
                });

                // Mengubah data menjadi array untuk digunakan di BarChart
                const formattedData = Object.keys(speedSums).map(className => ({
                    name: className,
                    averageSpeed: speedSums[className] / classCounts[className],
                }));

                setSpeedData(formattedData);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, []);

    return (
        <div style={{ width: '100%', height: 400 }}>
            <h2>Average Vehicle Speed by Class</h2>
            <ResponsiveContainer width="90%" height="100%">
                <BarChart data={speedData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="averageSpeed" fill="#82ca9d" name="Average Speed" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default VehicleSpeedBarChart;
=======
// src/components/VehicleSpeedBarChart.js
import React, { useState, useEffect } from 'react';
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';

const VehicleSpeedBarChart = () => {
    const [speedData, setSpeedData] = useState([]);

    useEffect(() => {
        // Ambil data dari API atau JSON statis
        axios.get('http://127.0.0.1:5000/vehicle_track') // Ganti dengan endpoint API jika diperlukan
            .then(response => {
                const data = response.data;

                // Mengelompokkan data berdasarkan Class Name dan menghitung rata-rata kecepatan
                const speedSums = {};
                const classCounts = {};

                data.forEach(item => {
                    const className = item['Class Name'];
                    const speed = item['Speed'];

                    if (!speedSums[className]) {
                        speedSums[className] = 0;
                        classCounts[className] = 0;
                    }

                    speedSums[className] += speed;
                    classCounts[className] += 1;
                });

                // Mengubah data menjadi array untuk digunakan di BarChart
                const formattedData = Object.keys(speedSums).map(className => ({
                    name: className,
                    averageSpeed: speedSums[className] / classCounts[className],
                }));

                setSpeedData(formattedData);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, []);

    return (
        <div style={{ width: '100%', height: 400 }}>
            <h2>Average Vehicle Speed by Class</h2>
            <ResponsiveContainer width="90%" height="100%">
                <BarChart data={speedData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="averageSpeed" fill="#82ca9d" name="Average Speed" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default VehicleSpeedBarChart;
>>>>>>> ce38f0ac1bbae3a1826030c653329f6d2588848a
