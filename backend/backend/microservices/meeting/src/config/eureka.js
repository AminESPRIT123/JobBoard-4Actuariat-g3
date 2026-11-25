/**
 * Eureka client configuration: registers this service as MEETING
 * on the Eureka server (http://localhost:8761/eureka).
 */
const { Eureka } = require('eureka-js-client');

const createEurekaClient = (port) =>
  new Eureka({
    instance: {
      app: 'MEETING',
      instanceId: `localhost:meeting:${port}`, // unique per instance (port differs)
      hostName: 'localhost',
      ipAddr: '127.0.0.1',
      port: { $: port, '@enabled': true },
      vipAddress: 'meeting',
      statusPageUrl: `http://localhost:${port}/info`, // link in the Eureka dashboard
      healthCheckUrl: `http://localhost:${port}/health`,
      homePageUrl: `http://localhost:${port}/`,
      dataCenterInfo: {
        '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
        name: 'MyOwn',
      },
    },
    eureka: {
      host: process.env.EUREKA_HOST || 'localhost',
      port: Number(process.env.EUREKA_PORT) || 8761,
      servicePath: '/eureka/apps/',
      maxRetries: 10,
      requestRetryDelay: 2000,
    },
  });

module.exports = createEurekaClient;
