const app = require('./app');
const { Eureka } = require('eureka-js-client');

const port = Number(process.env.PORT || 8083);
const baseUrl = `http://localhost:${port}`;

const client = new Eureka({
    instance: {
        app: 'MEETING',
        instanceId: `localhost:meeting:${port}`,
        hostName: 'localhost',
        ipAddr: '127.0.0.1',
        port: { $: port, '@enabled': true },
        vipAddress: 'meeting',
        healthCheckUrl: `${baseUrl}/health`,
        statusPageUrl: `${baseUrl}/info`,
        dataCenterInfo: {
            '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
            name: 'MyOwn',
        },
    },
    eureka: {
        host: 'localhost',
        port: 8761,
        servicePath: '/eureka/apps/',
        fetchRegistry: false,
    },
});

const server = app.listen(port, () => {
    console.log(`Meeting disponible sur ${baseUrl}/api/meetings/hello`);

    client.start((error) => {
        if (error) {
            console.error('Inscription Eureka échouée', error);
            return;
        }

        console.log(`MEETING inscrit dans Eureka sur le port ${port}`);
    });
});

process.once('SIGINT', () => {
    client.stop(() => server.close());
});