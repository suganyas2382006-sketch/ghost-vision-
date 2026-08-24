'use client';
import { useEffect, useRef, useState } from 'react';

export default function GhostVisionPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const outputRef = useRef<HTMLImageElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const [mode, setMode] = useState<string>('visible');
  const [hasBackground, setHasBackground] = useState<boolean>(false);
  const [isConnected, setIsConnected] = useState<boolean>(false);

  useEffect(() => {
    // 1. Initialize Camera Stream
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => console.error("Camera access denied:", err));

    // 2. Establish WebSocket Connection
    // Ensure this matches the port your FastAPI server is running on
    const ws = new WebSocket('ws://localhost:8000/ws');
    wsRef.current = ws;

    ws.onopen = () => setIsConnected(true);
    ws.onclose = () => setIsConnected(false);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (outputRef.current) {
        outputRef.current.src = data.image;
      }
      setMode(data.mode);
      setHasBackground(data.has_background);
    };

    return () => ws.close();
  }, []);

  // 3. Real-time Frame Extraction Loop
  useEffect(() => {
    let animationId: number;

    const sendFrame = () => {
      if (
        wsRef.current?.readyState === WebSocket.OPEN &&
        videoRef.current &&
        canvasRef.current &&
        videoRef.current.readyState === videoRef.current.HAVE_ENOUGH_DATA
      ) {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        if (ctx) {
          // Flip horizontally for a natural mirror effect
          ctx.translate(canvas.width, 0);
          ctx.scale(-1, 1);
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          
          // Compress heavily (0.4) to maintain high framerate over WebSockets
          const imageData = canvas.toDataURL('image/jpeg', 0.4); 
          
          wsRef.current.send(JSON.stringify({ 
            image: imageData,
            command: 'process'
          }));
        }
      }
      animationId = requestAnimationFrame(sendFrame);
    };

    animationId = requestAnimationFrame(sendFrame);
    return () => cancelAnimationFrame(animationId);
  }, [isConnected]);

  const captureBackground = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ command: 'capture_background', image: '' }));
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-4xl mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-light tracking-tight">
          <span className="font-bold text-amber-500">Ghost</span>Vision
        </h1>
        <div className="flex items-center gap-3">
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-500' : 'bg-red-500'}`} />
          <span className="text-xs tracking-wider uppercase text-gray-400">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>
      
      <div className="relative w-full max-w-4xl aspect-video bg-gray-900 rounded-xl overflow-hidden shadow-2xl border border-gray-800">
        <video ref={videoRef} autoPlay playsInline muted className="hidden" />
        <canvas ref={canvasRef} className="hidden" />
        
        <img ref={outputRef} className="w-full h-full object-cover" alt="Processed Feed" />
        
        {hasBackground && (
          <div className="absolute top-4 left-4 flex flex-col gap-2">
            <div className={`px-3 py-1 rounded text-xs tracking-wider uppercase backdrop-blur-md ${mode === 'visible' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'}`}>
              Mode: {mode}
            </div>
          </div>
        )}
      </div>

      <div className="mt-8 flex flex-col items-center gap-4 text-center min-h-[6rem]">
        {!hasBackground ? (
          <div className="space-y-4">
            <p className="text-gray-400 text-sm">Step out of frame and capture the background environment.</p>
            <button 
              onClick={captureBackground}
              className="px-6 py-2 bg-white text-black hover:bg-gray-200 rounded font-medium transition-colors text-sm shadow-lg shadow-white/10"
            >
              Capture Background
            </button>
          </div>
        ) : (
          <p className="text-gray-400 text-sm">
            <strong className="text-gray-200">Controls:</strong> Raise <span className="text-amber-400">two closed fists</span> to become invisible, or <span className="text-emerald-400">two open palms</span> to return.
          </p>
        )}
      </div>
    </div>
  );
}
