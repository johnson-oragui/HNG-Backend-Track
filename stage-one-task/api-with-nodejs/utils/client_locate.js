const geoip = require('geoip-lite2');

const IpLookUp = (client_ip) => {
    try {
        const geo = geoip.lookup(client_ip);
        console.log('client_ip: ', client_ip);
        if (!geo) {
            console.error(`Could not get geo from client_i ${client_ip}`);
            return { latitude: false, longitude: false };
        }
        const { ll } = geo;  // ll contains [longitude, and latitude]

        const [latitude, longitude] = ll;

        return { latitude, longitude };
    } catch (err) {
        console.error(err.message);
        return { latitude: false, longitude: false };
    }
};

module.exports = IpLookUp;
