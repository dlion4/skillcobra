self.addEventListener("install", (event)=>{
    console.log("service worker installing ...")
})

self.addEventListener("activate", (event)=>{
    console.log("service worker activating ...")
})

self.addEventListener("message", (even)=>{
    console.log("message received from main thread: ", event.data)
    self.clients.matchAll().then((clients)=>{
        clients.forEach((client)=>{
            client.postMessage("message received from service worker: " + event.data)
        })
    })
})

self.addEventListener("push", (event)=>{
    const data = event.data.json();
    const options = {
        body: data.body,
        icon: "/icon.png",
        badge: "/badge.png"
    };

    event.waitUntil(self.registration.showNotification(data.title, options));
})

self.addEventListener("notificationclick", (event)=>{
    event.notification.close();
    event.waitUntil(clients.openWindow("/"));
})