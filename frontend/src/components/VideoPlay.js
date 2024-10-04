import React, { useEffect, useRef } from 'react';
import Hls from 'hls.js'; 

const VideoPlay = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    if (Hls.isSupported()) {
      const hls = new Hls();
      const video = videoRef.current;
      hls.loadSource('https://cctvjss.jogjakota.go.id/atcs/ATCS_Simpang_Amongrogo_View_Timur.stream/chunklist_w14842540.m3u8');
      hls.attachMedia(video);
    }
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '20px' }}>
        <video ref={videoRef} controls style={{ width: '50%', height: 'auto' }} />
      </div>
    </div>
  );
};

export default VideoPlay;
