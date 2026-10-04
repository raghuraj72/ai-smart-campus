import { useEffect, useRef, useState, useCallback } from 'react';

export const useWebSocket = (token) => {
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  const socketRef = useRef(null);
  const reconnectTimerRef = useRef(null);
  const isMountedRef = useRef(false);

  const connect = useCallback(() => {
    if (!token || !isMountedRef.current) {
      return;
    }

    // Prevent duplicate connections
    if (
      socketRef.current &&
      (socketRef.current.readyState === WebSocket.OPEN ||
        socketRef.current.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    const protocol =
      window.location.protocol === 'https:' ? 'wss:' : 'ws:';

    const wsUrl = `${protocol}//${window.location.host}/ws?token=${encodeURIComponent(token)}`;

    console.log('[WS] Connecting:', `${protocol}//${window.location.host}/ws`);

    const socket = new WebSocket(wsUrl);

    socketRef.current = socket;

    socket.onopen = () => {
      if (!isMountedRef.current) {
        socket.close();
        return;
      }

      console.log('[WS] Connected');
      setIsConnected(true);
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setMessages((prev) => [data, ...prev]);
      } catch (err) {
        console.error('[WS] Failed to parse message:', err);
      }
    };

    socket.onerror = (error) => {
      console.error('[WS] Error:', error);
    };

    socket.onclose = (event) => {
      console.log(
        '[WS] Disconnected. Code:',
        event.code,
        'Reason:',
        event.reason || 'none'
      );

      setIsConnected(false);

      if (!isMountedRef.current) {
        return;
      }

      if (reconnectTimerRef.current) {
        clearTimeout(reconnectTimerRef.current);
      }

      reconnectTimerRef.current = setTimeout(() => {
        reconnectTimerRef.current = null;
        connect();
      }, 3000);
    };
  }, [token]);

  useEffect(() => {
    isMountedRef.current = true;

    connect();

    return () => {
      isMountedRef.current = false;

      if (reconnectTimerRef.current) {
        clearTimeout(reconnectTimerRef.current);
        reconnectTimerRef.current = null;
      }

      if (socketRef.current) {
        socketRef.current.onclose = null;
        socketRef.current.close();
        socketRef.current = null;
      }

      setIsConnected(false);
    };
  }, [connect]);

  return {
    messages,
    isConnected,
  };
};