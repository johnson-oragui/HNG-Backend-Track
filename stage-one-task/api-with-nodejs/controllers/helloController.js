const IpLookUp = require('../utils/client_locate');
const fetchClientWeather = require('../utils/fetchClientWeather');

class HelloController {
    static async hello(req, res, next) {
        try {
            const { visitor_name } = req.query;
            const hardcodedIp = '172.29.148.228';
            // req.ip will consider X-Forwarded-For if behind a proxy
            const client_ip = req.ip  !== '::1' ? req.ip : hardcodedIp;

            if (!client_ip) {
                console.error(`Could not retrieve Ip Address: ${ip}`);
                return res.status(401).json({ error: "ip not found" });
            }

            const { latitude, longitude } = IpLookUp(client_ip);

            console.log('latitude, longitude: ', latitude, longitude);

            if (!latitude || !longitude ) {
                console.error(`Could not locate client  latitude or longitude : ${client_ip}`);
                return res.status(404).json({ error: 'Location not found' });
            }

            const { cityName, temperature } = await fetchClientWeather(latitude, longitude);

            if (!cityName || !temperature) {
                console.error(`Could not locate client  cityName and temperature : ${cityName, temperature}`);
                return res.status(404).json({ error: 'cityName and temperature not found' });
            }

            const message = {
                client_ip,
                location: cityName || 'Lagos',
                greeting: `Hello, ${visitor_name}!, the temperature is ${temperature} degrees Celcius in ${cityName}`
            }
            return res.status(200).json(message);
        } catch (err) {
            console.error('Error in hello controller: ', err.message);
            return next(err);
        }
    }
}

module.exports = HelloController;
