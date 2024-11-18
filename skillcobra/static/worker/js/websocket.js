class WebSocketManager {
    constructor(path) {
        this.socket = null;
        this.path = path;
        this.websocketPath = `wss://${window.location.host}/ws`;
    }

    init() {
        const url = `${this.websocketPath}/${this.path}`;
        this.socket = new WebSocket(url);

        this.socket.onopen = (event) => {
            console.log(`WebSocket connected: ${event}`);
            this.onConnectionEstablished();
        };

        this.socket.onmessage = (event) => {
            this.handleMessage(event);
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        this.socket.onclose = () => {
            console.log('WebSocket closed');
        };
    }

    handleMessage(event) {
        let data;
        try {
            data = JSON.parse(event.data);
            console.log(`Message received:`, data);
            this.updateMessageCount(data);
        } catch (error) {
            console.error("Failed to parse JSON:", error);
        }
    }

    sendMessage(message) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(message));
        } else {
            console.error('WebSocket is not open. Message not sent:', message);
        }
    }

    onConnectionEstablished() {
        console.log("WebSocket connection is established.");
    }

    // Example method to update message count
    updateMessageCount(data) {
    }

}