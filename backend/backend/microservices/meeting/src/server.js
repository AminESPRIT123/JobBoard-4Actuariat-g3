
const app = require('./app');
const Eureka = require('eureka-js-client').Eureka;

const PORT = Number(process.env.PORT) || 8083;

// Configuration du client Eureka
const client = new Eureka({
  instance: {
    app: 'MEETING',
    instanceId: `MEETING-${PORT}`,
    hostName: 'localhost',
    ipAddr: '127.0.0.1',

    port: {
      '$': PORT,
      '@enabled': 'true'
    },

    statusPageUrl: `http://localhost:${PORT}/swagger-ui`,
    vipAddress: 'MEETING',

    dataCenterInfo: {
      '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
      name: 'MyOwn'
    }
  },

  eureka: {
    host: 'localhost',
    port: 8761,
    servicePath: '/eureka/apps/'
  }
});

// Démarrage du serveur Express
const server = app.listen(PORT, () => {
  console.log(`Meeting running on http://localhost:${PORT}`);
  console.log(`Swagger UI: http://localhost:${PORT}/swagger-ui`);

  // Enregistrement auprès de Eureka
  client.start();
});

// Arrêt propre du service
function shutdown() {
  console.log('Stopping Meeting service...');

  client.stop();

  server.close(() => {
    process.exit(0);
  });
}

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
