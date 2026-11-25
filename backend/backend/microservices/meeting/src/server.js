const app = require('./app');
const createEurekaClient = require('./config/eureka');

// Port read from the PORT environment variable to allow several instances
const PORT = Number(process.env.PORT) || 8083;

const eurekaClient = createEurekaClient(PORT);

app.listen(PORT, () => {
  console.log(`meeting microservice running on http://localhost:${PORT}`);
  console.log(`Swagger UI: http://localhost:${PORT}/swagger-ui`);

  // Register in Eureka once the HTTP server is up
  eurekaClient.start((error) => {
    console.log(error ? `Eureka registration failed: ${error}` : 'Registered in Eureka as MEETING');
  });
});

// Unregister from Eureka when the app is stopped (Ctrl+C)
const shutdown = () => {
  eurekaClient.stop(() => process.exit(0));
};
process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
