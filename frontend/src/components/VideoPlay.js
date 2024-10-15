import React, { useEffect, useRef } from 'react';
import Hls from 'hls.js'; 

const VideoPlay = () => {
  const videoRef = useRef(null);
  
  useEffect(() => {
    if (Hls.isSupported()) {
      const hls = new Hls();
      const video = videoRef.current;
      hls.loadSource('http://localhost:5000/playlist/simpang_demangan_view_utara/simpang_demangan_view_utara.m3u8');
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

// import React, { useEffect, useRef } from 'react';

// const VideoPlay = () => {
//   const videoRef = useRef(null);

//   useEffect(() => {
//     if (videoRef.current) {
//       videoRef.current.src = 'http://localhost:5000/start_stream';
//     }
//   }, []);

//   return (
//     <div style={{ padding: '20px' }}>
//       <div style={{ marginBottom: '20px' }}>
//         <img ref={videoRef} alt="Video stream" style={{ width: '50%', height: 'auto' }} />
//       </div>
//     </div>
//   );
// };

// export default VideoPlay;